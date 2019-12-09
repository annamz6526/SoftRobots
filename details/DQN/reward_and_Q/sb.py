import pickle

with open('reward.txt', 'rb') as f:
	mylist = pickle.load(f)

print("reward")
print(mylist)

with open('qvalue.txt', 'rb') as f:
	mylist = pickle.load(f)

print("qvalue")
print(mylist)