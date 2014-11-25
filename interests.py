from queries import *
from hlnlp import HeyLetsLSI_205
import gensim
import numpy as np
import itertools
import pickle as pkl

class interest_smoother(object):
    def __init__(self):
        pass

    def smooth(self, vec):
        '''
        smooths vec using the different smoothing vectors stored in self.pagerank. note that self.M is assumed to be the smoothing vectors stored in a 45x45 matrix so that this function is simply the normalized version of self.smooth_vectors * vec
        '''
        return self.lsi.query(self.make_tex_from_vec(vec))

    def train(self, users, num_topics=25):
        '''
        trains the interest smoother on the users in "users"
        '''
        # get all the interests; split by women vs man
        all_interests = [user.MB_InterestsRaw for user in users]
        # create a tset for use in the model
        tset = self.create_tset_from_interests(all_interests)
        # pass into unsupervised learning LSI model
        self.lsi = HeyLetsLSI_205(tset, num_topics=num_topics)


    def create_tset_from_interests(self, all_interests):
        '''
        creates a training set from all the interests to pump into unsupervised learning
        '''
        # initialize at []
        tset = []
        for vec in all_interests:
            # add all interests of vec (vec is a user)
            tex = self.make_tex_from_vec(vec)
            tset.append(tex)
            #nonzero = [ind for ind in range(len(vec)) if vec[ind]==1]
            #tset.append(' '.join([str(x) for x in nonzero]))
        return tset

    def make_tex_from_vec(self, vec):
        '''
        makes a training example from a single vector
        '''
        nonzero = [ind for ind in range(len(vec)) if vec[ind]==1]
        
        return ' '.join([str(x) for x in nonzero])

    def create_interest_graph(self, users):
        '''
        creates a graph where nodes are interest indices and connections are when a person has both interests listed
        '''
        all_interests = [user.MB_InterestsRaw for user in users]
     
        G = self.fill_G_from_interests(all_interests)
        self.G = G
        return G


    def fill_G_from_interests(self, all_interests):
        '''
        creates a G from the list of all users interest vectors
        '''
        G = nx.MultiGraph()
        G.add_nodes_from(range(len(all_interests[0]))) #should be 45

        for vec in all_interests:
            # add the correct edges
            nonzero = [ind for ind in range(len(vec)) if vec[ind] == 1]
            G.add_edges_from(itertools.combinations(nonzero,2)) #all 2-len combs
            G.add_edges_from(zip(nonzero,nonzero)) #add self loops

        return G


    
    def run_pageranks(self, G, alpha=.5):
        '''
        runs 45 pageranks to see the personalized scores of each interest in relation to other interests
        '''
        pageranks = []
        for i in range(45):
            # make the personalization dict
            personalization_dict = dict.fromkeys(range(45),0)
            personalization_dict[i] = 1
            
            # run pagerank; should take ~1.5 min
            pr = nx.pagerank_numpy(G, alpha=alpha, personalization=personalization_dict)
            pageranks.append(pr)
            # print some info on where we are
            print "just finished pagerank " + str(i)
        return pageranks

    

if __name__ == '__main__':
    secret = pkl.load(open('secret.pkl','r'))
    uq = UserQuery(**secret)
    eq = ExperienceQuery(**secret)

    int_s = interest_smoother()
    all_users = uq.get_next_chunk(10000000)
    int_s.train(all_users)
