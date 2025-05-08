import random
import pickle
import os

# if os.path.exists(".\\temp\\test.tmp"):
with open(".\\temp\\student.tmp", "rb") as f:
    data = pickle.load(f)["students"]
# else:
#     with open(".\\student.pkl", "rb") as f:
#         data = pickle.load(f)["students"]

names = tuple(data.keys())
returnBack = []
times = 1
if os.path.exists(".\\temp\\cdraw.tmp"):
    with open(".\\temp\\cdraw.tmp", "rb") as f:
        times = pickle.load(f)

for i in range(times):
    returnBack.append(names[random.randint(0, len(data) - 1)])

with open(".\\temp\\now.tmp", "wb") as f:
    pickle.dump(returnBack, f)
