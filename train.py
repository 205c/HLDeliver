import pickle as pkl
from VTable import VTable
from HeyLetsDataScience import heylets_datascience

secret = pkl.load(open('secret.pkl','r')) # credentials
ds = heylets_datascience(**secret)
print "Training..."
ds.train()
print "Dumping..."
ds.dump_sql()
VTable.createTable()
VTable.loadTable(ds.to_V_matr_dump())
