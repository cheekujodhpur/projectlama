import pickle

d={}
f1=open("reward_table1.pickle","wb")
f2=open("poss_moves_table1.pickle","wb")
f3=open("q_table1.pickle","wb")
pickle.dump(d,f1)
pickle.dump(d,f2)
pickle.dump(d,f3)
f1.close()
f2.close()
f3.close()