import pickle as pkl
from HeyLetsDataScience import heylets_datascience

secret = pkl.load(open('secret.pkl','r')) # credentials
ds = heylets_datascience(**secret)
print "Training..."
ds.train()

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

