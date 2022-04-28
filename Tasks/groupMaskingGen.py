
import random
import ipdb

g0 = ["L12", "K45", "E33"]
g1 = ["G56", "T21", "W90"]
g2 = ["Y87", "V27", "S20"]

participants = []

for i in range(35):
    participants.append(random.sample(g0, 1)[0])
    participants.append(random.sample(g1, 1)[0])
    participants.append(random.sample(g2, 1)[0])

random.shuffle(participants)

with open("groups.txt", "w") as f:
     for p_group in participants:
        f.write("%s\n" % p_group)
