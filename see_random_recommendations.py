import pickle as pkl
from HeyLetsDataScience import heylets_datascience
from queries import *
import random

secret = pkl.load(open('secret.pkl','r')) # credentials
ds = heylets_datascience(**secret)
print "Training..."
ds.train()

eq = ExperienceQuery(**secret)
all_experiences = eq.get_next_chunk(100000)

user_mapping = {}
for user in ds.male_users + ds.female_users:
	user_mapping[user.MB_Id] = user

while True:
	x = raw_input("Hit Enter to continue looking at users; 'exit' to stop")
	if x == 'exit':
		break
	# pick a random user from ds.train
	user = random.choice(ds.male_users + ds.female_users)
	# profile the user's interests
	print "The user's interests are: "
	nonzero = [i for i in range(len(user.MB_InterestsRaw)) if user.MB_InterestsRaw[i] == 1]
	for i in nonzero:
		print ds.interests_mapping[i]
	y = raw_input("Do you want to see this user's recommendations (using ONLY the interest model, nothing else)? Enter to see recommendations, 'no' to go to pick another random user")
	if y == 'no':
		continue
	all_exp_scored = [(exp, ds.interest_similarity(user.MB_InterestsRaw, user_mapping[exp.EX_MB_Id].MB_InterestsRaw)) if exp.EX_MB_Id in user_mapping else (exp, 0) for exp in all_experiences]
	all_exp_sorted = sorted(all_exp_scored, key=lambda x:x[1])[::-1]
	for exp in all_exp_sorted[:20]:
		try:
			expvec = ast.literal_eval(exp[0].EX_Interests)
		except:
			expvec = [-1 for i in range(47)]
		listed_interests = [i for i in range(len(expvec)) if expvec[i] == 1]
		print "score: %s; description of experience: %s; listed_interests: %s" % (exp[1], exp[0].EX_Description, ', '.join([ds.interests_mapping[i] for i in listed_interests]))





