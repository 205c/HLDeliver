'''
LDA Wrapper on Gensim's LDA that allows it to be more easily trained by strings, etc

Ankit Kumar
ankit@205consulting.com
'''

import numpy as np
import gensim
import nltk
import string
import pickle as pkl

'''
USAGE: inherit this module and overwrite preprocess. Or, copy-paste this module and manually overwrite preprocess. 

you can use it like gensim's lda easily, i.e:

gw = GensimWrapper_205(corpus=['this is a sample corpus','here is more'], num_topics=10)
gw.add_documents(['another corpus','should be an iterable'])

the relevant apis are the __init__(), add_documents(), and query()

query() takes a string and returns a vector representation (in numpy)

this is not yet complete but has most of what you need for typical lda use (training and querying)
'''

class GensimWrapper_205(gensim.models.lsimodel.LsiModel):

    def __init__(self, corpus=None, num_topics=200, id2word=None, chunksize=20000, decay=1.0, distributed=False, onepass=True, power_iters=2, extra_samples=100):
        # if corpus is given, it's assumed to be an iterable of strings. so we turn it into a gensim bag. 
        self.stop_words = pkl.load(open('stop_words.pkl','r'))
        if corpus is not None:
            corpus, id2word = self.generate_gensim_corpus_from_strings(corpus, id2word)
        gensim.models.lsimodel.LsiModel.__init__(self, corpus=corpus, num_topics=num_topics, id2word=id2word, chunksize=chunksize, decay=decay, distributed=distributed, onepass=onepass, power_iters=power_iters, extra_samples=extra_samples)



    

    def preprocess(self, doc):
        '''
        baseline preprocessing function; just lowers and splits
        this function should be overwritten, but must always return a list of strings that represent the bag of words of the doc.
        '''
        # remove punctuations
        doc = doc.translate(string.maketrans("",""), string.punctuation)
        # lower and split into a bag of words
        split = [x for x in doc.lower().split() if x not in self.stop_words]
        return split

    def generate_gensim_corpus_from_strings(self, corpus, id2word):

        '''
        this function takes an iterable of strings and turns it into a gensim corpus. if id2word is none, it also creates a gensim dictionary.

        returns the gensim corpus and dictionary (just returns the original dictionary if one is given)
        '''
        # if id2word is none, create a dictionary
        if id2word is None:
            gensim_dict = gensim.corpora.dictionary.Dictionary()
            #update with documents
            gensim_dict.add_documents([self.preprocess(doc) for doc in corpus])
            #re-write over id2word
            id2word = gensim_dict



        

        # now we create the gensim corpus
        gensim_corpus = [id2word.doc2bow(self.preprocess(doc)) for doc in corpus]

        # and return both
        return gensim_corpus, id2word

    def update(self, corpus):
        '''
        params:
            - corpus: iterable of strings, each string considered to be a document

        returns:
            - none; trains the model

        notes:
        this is not called update simply so that it doesn't overwrite gensim's own update function
        '''
        # turn the corpus into a gensim corpus; this will also return an id2word dictionary if one isn't stored in the model yet
        corpus, self.id2word = self.generate_gensim_corpus_from_strings(corpus, self.id2word)
        # train lda model
        self.add_documents(corpus)
        return

    def query(self, query):
        '''
        params:
            - query: a string to query; or a document, for example
        returns:
            - num_topics dimensional vector representing the per-document topic distribution (theta)
        '''
        # preprocess and turn the query into a gensim bag
        gensim_bag = self.id2word.doc2bow(self.preprocess(query))
        # query the lda model
        distribution = self.__getitem__(gensim_bag)
        # turn into a numpy array
        array = np.zeros(self.num_topics)
        for index,score in distribution:
            array[index] = score
        return array

    def update_dictionary(self, chunk):
        raise NotImplementedError
        ''' to do: iterable online making of dictionary + training lda '''

    def update_model(self, chunk):
        raise NotImplementedError
        ''' to do ''' 

    '''to do: probability of generation stuff '''


if __name__ == "__main__":
    gw = GensimWrapper_205(['this is a sample corpus','just to see if it works','just three strings'], num_topics=10)
    gw.add_documents(['a sample corpus works','strings if it','break on new string?'])

