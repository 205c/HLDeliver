from queries import *
from interests import interest_smoother
from hlnlp import HeyLetsLDA_205
import pickle as pkl
import ast
import numpy as np

class heylets_datascience(object):
    def __init__(self, host, user, pwd, db):
        # load stored values
        self.ignore_members = pkl.load(open('fake_members.pkl','r'))
        self.interests_mapping = pkl.load(open('interests_mapping.pkl','r'))

        # instantiate the user query and the experience query
        self.male_uq = UserQuery(host, user, pwd, db)
        self.male_uq.ignore_members(self.ignore_members)
        self.male_uq.filter_by_gender(1)
        self.female_uq = UserQuery(host, user, pwd, db)
        self.female_uq.ignore_members(self.ignore_members)
        self.female_uq.filter_by_gender(2)
       
        self.eq = ExperienceQuery(host, user, pwd, db)
        self.eq.ignore_members(self.ignore_members)

        # create the interest smoother and the nlp module
        self.male_interest_model = interest_smoother()
        self.female_interest_model = interest_smoother()
        self.interest_model = interest_smoother()

        # create the queries that will dump into the SQL tablea
        self.interest_creator = CreateInterests(host, user, pwd, db)
        self.interest_loader = InterestLoader(host, user, pwd, db)
        self.interest_loader_2 = InterestLoader(host,user,pwd,db)

        self.trained = False

    def dump_sql(self):
        '''
        Dumps the trained vectors into SQL for querying. Note that this assumes that the class has been trained (a check is there)
        '''
        # check that the model was trained
        if not self.trained:
            raise Exception("You haven't yet trained the model. You must call .train() before .dump_sql().")
        # create the SQL table
        self.interest_creator.createTable(25)
        self.interest_creator.createInterestsTable(25)

        # we can only dump 1000 at a time, so let's chunk our data
        chunks = [self.female_users[x:x+999] for x in xrange(0, len(self.female_users), 999)]
        total_dumped = 0
        for chunk in chunks:
            # fill a dict mapping mbId -> interest vector
            curr_chunk_dict = {}
            for user in chunk:
                smoothed_vec = self.interest_model.smooth(user.MB_InterestsRaw)
                if np.isnan(smoothed_vec[0]):
                    # this user had no interests; simply ignore
                    continue
                else:
                    curr_chunk_dict[user.MB_Id] = smoothed_vec
            # dump into sql
            self.interest_loader.load_interests(curr_chunk_dict)
            total_dumped += len(curr_chunk_dict)


        # now the males
        chunks = [self.male_users[x:x+999] for x in xrange(0, len(self.male_users), 999)]
      
        for chunk in chunks:
            # fill a dict mapping mbId -> interest vector
            curr_chunk_dict = {}
            for user in chunk:
                smoothed_vec = self.interest_model.smooth(user.MB_InterestsRaw)
                if np.isnan(smoothed_vec[0]):
                    # this user had no interests; simply ignore
                    continue
                else:
                    curr_chunk_dict[user.MB_Id] = smoothed_vec
            # dump into sql
            self.interest_loader.load_interests(curr_chunk_dict)
            total_dumped += len(curr_chunk_dict)
        print "total dumped: %s" % total_dumped


        # dump experiences into SQL
        exp_dict = {}
        chunks = [self.all_experiences[x:x+999] for x in xrange(0, len(self.all_experiences),999)]

        count_no_exp = 0
        numdumped = 0
        for chunk in chunks:
            curr_chunk_dict = {}
            for exp in chunk:
                try:
                    smoothed_vec = self.interest_model.smooth(ast.literal_eval(exp.EX_Interests))
                except:
                    count_no_exp += 1
                    continue
                if np.isnan(smoothed_vec[0]):
                    continue # no interests;ignore
                else:
                    curr_chunk_dict[exp.EX_Id] = smoothed_vec
            self.interest_loader.load_experiences(curr_chunk_dict)
            numdumped += len(curr_chunk_dict)
        print "num experiences with no interests: %s" % count_no_exp
        print "num dumped: %s" % numdumped

        # for exp in self.all_experiences:
        #     try: #try except loop to check malformed exp.EX_Interests
        #         smoothed_vec = self.interest_model.smooth(ast.literal_eval(exp.EX_Interests))
        #     except:
        #         count_no_exp += 1
        #         continue
        #     if np.isnan(smoothed_vec[0]):
        #         continue
        #     else:
        #         exp_dict[exp.EX_Id] = smoothed_vec
        # print "here"
        # self.interest_loader_2.load_experiences(exp_dict)



    def train(self):
        '''
        trains both the models and prepares the datascience model for queries
        '''
        # get male users
        male_users = self.male_uq.get_next_chunk(1000000) 
       
        # get female users
        female_users = self.female_uq.get_next_chunk(1000000)

        # train models
        self.male_interest_model.train(male_users, num_topics=25)
        self.female_interest_model.train(female_users, num_topics=25)
        ######## ------------------- ########
        # add male, female flags
        for male in male_users:
            male.MB_InterestsRaw += [1,-1]
        for female in female_users:
            female.MB_InterestsRaw += [-1,1]
        ######### --------------------- ########
        self.female_users = female_users
        self.male_users = male_users

        self.interest_model.train(male_users + female_users, num_topics=25)
        # to train the nlp model, we need to turn the users into a corpus
        corpus = self.get_experience_corpus()
        # now we can train the model
        self.nlp_model = HeyLetsLDA_205(corpus, num_topics=25)
        self.trained = True

    def get_experience_corpus(self):
        self.all_experiences = self.eq.get_experiences()
        all_strings_trunc = [x.EX_Description for x in self.all_experiences if len(x.EX_Description.split()) > 5]
        return all_strings_trunc

    def interest_vec_to_query(self, vec):
        '''
        turns the interest vector ([1,1,1...,-1,-1,1,,,]) into a query
        '''
        nonzero = [i for i in range(len(vec)) if vec[i] == 1]
        return ' '.join([str(x) for x in nonzero])

    def interest_similarity(self, one, two):
        '''
        computes the similarity between the two interest vectors, one and two, using the interests model
        '''
        vec_one = self.interest_model.lsi.query(self.interest_vec_to_query(one))
        vec_two = self.interest_model.lsi.query(self.interest_vec_to_query(two))

        # compute cosine similarity
        numerator = np.dot(vec_one, vec_two)
        denominator = np.linalg.norm(vec_one) * np.linalg.norm(vec_two) # if normalized, this shouldn't be necessary

        return numerator/denominator

    def f_interest_similarity(self, one, two):
        '''
        computes the similarity between the two interest vectors, one and two, using the interests model
        '''
        vec_one = self.female_interest_model.lsi.query(self.interest_vec_to_query(one))
        vec_two = self.female_interest_model.lsi.query(self.interest_vec_to_query(two))

        # compute cosine similarity
        numerator = np.dot(vec_one, vec_two)
        denominator = np.linalg.norm(vec_one) * np.linalg.norm(vec_two) # if normalized, this shouldn't be necessary

        return numerator/denominator

    def users_to_corpus(self, users):
        '''
        turns a list of users into a corpus for nlp training
        '''
        corpus = []
        ctr = 0
        for user in users:
            print "on user: " + str(ctr)
            all_experiences = user.get_experiences_created() + user.get_experiences_wishlisted()
            strings = [exp.EX_Description for exp in all_experiences if len(exp.EX_Description.split()) > 5]
            corpus.append(' '.join(strings))
            ctr += 1
        
        return corpus

    def to_V_matr_dump(self):
        # find the permutation of the matrix
        permute = []
        for i in range(47): # these are the interests
            permute.append(self.interest_model.lsi.id2word.token2id[str(i)])
        
        mat = self.interest_model.lsi.projection.u[:,:25].T
        mat = mat[:,permute] # permutes correctly
        list_of_tuples = []
        for row in range(mat.shape[0]):
            tup = tuple([row] + list(mat[row]))
            list_of_tuples.append(tup)
        return list_of_tuples


if __name__ == '__main__':
    secret = pkl.load(open('secret.pkl','r')) # credentials
    ds = heylets_datascience(**secret)
    print "Training..."
    ds.train()
    # print "Dumping..."
    # ds.dump_sql()

    import numpy as np
    interest_similarity_matrix = np.zeros((47,47)) # make a 45x45 matrix to store similarities
    for i in range(47):
        for j in range(47):
        # find the similarity in the model's vector space between interest i and j
            vector_i = [-1 if k != i else 1 for k in range(47)] # makes a vector of all -1s, except for the ith spot
            vector_j = [-1 if k != j else 1 for k in range(47)]
            interest_similarity_matrix[i,j] = ds.interest_similarity(vector_i,vector_j)
    similarity_matrix = interest_similarity_matrix - np.eye(47)
    most_similar = np.argmax(similarity_matrix, axis=1) # axis can be 1 or 0, since we have transpose symmetry in the similarity matrix
    for i in range(47):
        print "the most similar interest to %s is %s" % (ds.interests_mapping[i], ds.interests_mapping[most_similar[i]])



