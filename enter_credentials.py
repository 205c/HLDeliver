import pickle
secret = {}
db = raw_input("Enter the database name: ")
host = raw_input ("Enter the host: ")
pwd = raw_input ("Enter the pwd: ")
user = raw_input ("Enter the user: ")
print "Your entries: db: %s; host: %s; pwd: %s; user: %s. If this is not correct, re-run the script." % (db, host, pwd, user)
pickle.dump(secret, open('secret.pkl','w'))