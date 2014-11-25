import pickle as pkl
from HeyLetsDataScience import heylets_datascience

secret = pkl.load(open('secret.pkl','r')) # credentials
ds = heylets_datascience(**secret)
print "Training..."
ds.train()
print "Dumping..."
ds.dump_sql()