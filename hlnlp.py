'''
HeyLets NLP classes for delivery

Written by 205 Consulting for HeyLets

ankit@205consulting.com
ankitk@stanford.edu
'''
import numpy as np
import gensim
import nltk
import string
import pickle as pkl

# LSI class
class HeyLetsLSI_205(gensim.models.lsimodel.LsiModel):

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
        Note that this *DOES* normalize the array (to have unit length!!)
        '''
        # preprocess and turn the query into a gensim bag
        gensim_bag = self.id2word.doc2bow(self.preprocess(query))
        # query the lda model
        distribution = self.__getitem__(gensim_bag)
        # turn into a numpy array
        array = np.zeros(self.num_topics)
        for index,score in distribution:
            array[index] = score
        
        return array / np.linalg.norm(array)






# LDA class
class HeyLetsLDA_205(gensim.models.ldamodel.LdaModel):

	def __init__(self, corpus=None, num_topics=100, id2word=None, distributed=False, chunksize=2000, passes=1, update_every=1, alpha='symmetric', eta=None, decay=0.5, eval_every=10, iterations=50, gamma_threshold=0.001):
		# if corpus is given, it's assumed to be an iterable of strings. so we turn it into a gensim bag. 
		self.stop_words = pkl.load(open('stop_words.pkl','r'))
		if corpus is not None:
			corpus, id2word = self.generate_gensim_corpus_from_strings(corpus, id2word)
		gensim.models.ldamodel.LdaModel.__init__(self, corpus=corpus, num_topics=num_topics, id2word=id2word, distributed=distributed, chunksize=chunksize, passes=passes, update_every=update_every, alpha=alpha, eta=eta, decay=decay, eval_every=eval_every, iterations=iterations, gamma_threshold=gamma_threshold)



	

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

	def add_documents(self, corpus):
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
		self.update(corpus)
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
		gamma, sstats = self.inference([gensim_bag])
		# normalize the gamma (gamma here is theta)
		normalized_gamma = gamma[0] / gamma[0].sum()
		return normalized_gamma