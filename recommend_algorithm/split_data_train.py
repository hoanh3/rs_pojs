import random
from collections import defaultdict
import json
import math

with open('data_history_submission.json', 'r') as file:
    SUBMISSIONS = json.load(file)

print(len(SUBMISSIONS))

train_data = []
test_data = []

user_problem_submissions = defaultdict(lambda: defaultdict(list))

for sub in SUBMISSIONS:
    user = sub['user']
    problem = sub['problem']
    user_problem_submissions[user][problem].append(sub)

for user, problems in user_problem_submissions.items():
    problem_set = list(problems.keys())
    random.shuffle(problem_set)
    k = math.floor(0.8 * len(problem_set))
    train_p = problem_set[:k]
    test_p = problem_set[k:]
    for problem in train_p:
        train_data.extend(problems[problem])
    for problem in test_p:
        test_data.extend(problems[problem])

with open("data_train.json", 'w') as file:
    json.dump(train_data, file)
    
with open("data_test.json", 'w') as file:
    json.dump(test_data, file)    

print(len(train_data))
print(len(test_data))

print(f"Tập huấn luyện có {len(train_data)} lần nộp bài.")
print(f"Tập kiểm tra có {len(test_data)} lần nộp bài.")