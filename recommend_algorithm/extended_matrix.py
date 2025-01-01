import json

with open('data_train.json', 'r') as file:
    data = json.load(file)

with open('data_user.json', 'r') as file:
    users_data = json.load(file)

with open('data_problem.json', 'r') as file:
    problems_data = json.load(file)

with open('data_test.json', 'r') as file:
    test_data = json.load(file)
    
# Khởi tạo biến
N = 3
K = 10
p1 = 2 # giới hạn giữa các trường hợp ít và nhiều lần thử với kết quả không giải được
p2 = 3 # giới hạn giữa các trường hợp ít và nhiều lần thử với kết quả giải được
user_problem_dict_test = {}
user_problem_dict = {} # ma trận người dùng - bài toán: dữ liệu được sử dụng để đề xuất
C1u = dict() # tập các bài toán mà người dùng cần nhiều lần thử để giải
C2u = dict() # tập các bài toán mà người dùng cần ít lần thử để giải
C1p = dict() # tập người dùng đã giải bài toán p sau nhiều lần thử
C2p = dict() # tập người dùng đã giải bài toàn p sau ít lần thử
M = dict() # ma trận người dùng - bài toán: biểu diễn các giá trị tương tác khác nhau
Ms = dict() # ma trận được làm giàu
S = dict() # ma trận biểu diễn độ tương đồng của người dùng
users = set([x['code'] for x in users_data])
problems = set([x['code'] for x in problems_data])

# Biểu diễn quan hệ người dùng - bài toán: số lần thử và kết quả cuối cùng
class SubmissionData:
    def __init__(self, user, problem, sub_count, solved):
        self.user = user
        self.problem = problem
        self.sub_count = sub_count
        self.solved = solved
    
    def update_count(self):
        self.sub_count = self.sub_count + 1
    
    def is_solved(self, result):
        self.solved = True if result == 'AC' else self.solved
        
    def __str__(self):
        return "{user} - {problem} - {cnt} - {solved}".format(user = self.user, problem = self.problem, cnt = self.sub_count, solved = self.solved)
def init_data():
    for d in data:
        user = d['user']
        problem = d['problem']
        if user not in user_problem_dict:
            user_problem_dict[user] = {}
        if problem not in user_problem_dict[user]:
            user_problem_dict[user][problem] = SubmissionData(user, problem, 0, False)
        submision_data = user_problem_dict[user][problem]
        submision_data.update_count()
        submision_data.is_solved(d['result'])

    #khởi tạo ma trận
    for u in users:
        M[u] = {}
        Ms[u] = {}
        C1u[u] = set()
        C2u[u] = set()
        S[u] = dict()
        for p in problems:
            C1p[p] = set()
            C2p[p] = set()
            M[u][p] = 0
            Ms[u][p] = 0
    for u in users:
        for v in users:
            S[u][v] = 0
    
    for d in test_data:
        user = d['user']
        problem = d['problem']
        if user not in user_problem_dict_test:
            user_problem_dict_test[user] = {}
        if problem not in user_problem_dict_test[user]:
            user_problem_dict_test[user][problem] = SubmissionData(user, problem, 0, False)
        submision_data = user_problem_dict_test[user][problem]
        submision_data.update_count()
        submision_data.is_solved(d['result'])
    
def get_matrix_up():
    # tạo ma trận u-p
    for user, user_data in user_problem_dict.items():
        for problem, problem_data in user_data.items():
            if problem_data.solved:
                M[user][problem] = 3 if problem_data.sub_count >= p2 else 4
                Ms[user][problem] = 3 if problem_data.sub_count >= p2 else 4
            else:
                if problem_data.sub_count == 0:
                    M[user][problem] = 0
                    Ms[user][problem] = 0
                else:
                    M[user][problem] = 1 if problem_data.sub_count >= p1 else 2
                    Ms[user][problem] = 1 if problem_data.sub_count >= p1 else 2

def extend_matrix_up():
    # làm giàu ma trận
    for user, user_data in M.items():
        for problem, problem_data in user_data.items():
            if M[user][problem] == 3:
                C1u[user].add(problem)
                C1p[problem].add(user)
            else:
                C2u[user].add(problem)
                C2p[problem].add(user)
                
def preprocess_natural_noise():
    for user, user_data in M.items():
        for problem, problem_data in user_data.items():
            if M[user][problem] == 3:
                Ms[user][problem] = 4 if len(C2u[user]) >= 2*len(C1u[user]) and len(C2p[problem]) >= 2*len(C1p[problem]) else 3
            else:
                Ms[user][problem] = 3 if len(C1u[user]) >= 2*len(C2u[user]) and len(C1p[problem]) >= 2*len(C2p[problem]) else 3

def get_similar_of_user():
    # tính toán độ tương đồng người dùng
    for x in users:
        for u in users:
            try:
                if u == x:
                    continue
                x_problems = set(user_problem_dict[x].keys())
                u_problems = set(user_problem_dict[u].keys())
                
                intersection_size = len(x_problems.intersection(u_problems))
                union_size = len(x_problems.union(u_problems))
                if union_size > 0:
                    S[x][u] = intersection_size / union_size
            except:
                S[x][u] = 0

def get_k_near_user(user, k):
    sorted_sUX = dict(sorted(S[user].items(), key=lambda item: item[1], reverse=True))
    kUserNear = dict(list(sorted_sUX.items())[:k])
    return kUserNear

def get_n_recommend_problem(user, n):
    no_xp = problems.difference(set(user_problem_dict[user].keys()))
    recProblem = {}
    kUserNear = get_k_near_user(user=user, k=K)
    for p in no_xp:
        wp = 0
        for u in kUserNear:
            try:
                wp = wp + kUserNear[u] * Ms[u][p]
            except:
                wp = wp
        recProblem[p] = wp
        
    sortedRecProblem = dict(sorted(recProblem.items(), key= lambda x:x[1], reverse=True))
    return list(sortedRecProblem.keys())[:n]

def get_info_user(user):
    not_solved = set(p for p, data in user_problem_dict_test[user].items() if not data.solved)
    solved = set(p for p, data in user_problem_dict_test[user].items() if data.solved)
    recommended = set(get_n_recommend_problem(user=user, n=N))
    not_recommened = problems.difference(recommended)
    return not_solved, solved, recommended, not_recommened

def get_score(user):
    not_solved, solved, recommended, not_recommened = get_info_user('B23DCCN863')
    tp = len(solved.intersection(recommended))
    fp = len(solved.intersection(not_recommened))
    tn = len(not_solved.intersection(recommended))
    fn = len(not_solved.intersection(not_recommened))
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    f1 = (2 * precision * recall) / (precision + recall)
    return precision, recall, f1

if __name__ == '__main__':
    init_data()
    get_matrix_up()
    extend_matrix_up()
    preprocess_natural_noise()
    get_similar_of_user()
    not_solved, solved, recommended, not_recommened = get_info_user('B23DCCN863')
    print("not_solved", not_solved)
    print("solved", solved)
    print("recommended", recommended)
    print("not_recommened", not_recommened)

    precision, recall, f1 = get_score('B23DCCN863')
    print("precision", precision)
    print("recall", recall)
    print("f1", f1)