import pickle

with open("data", "rb") as fp:
    games_data = pickle.load(fp)
temp = []
for i in games_data:
    temp.append(i[0])
if 'SLPM-65763' in temp:
    print('ouyé')
