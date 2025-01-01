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
t = 5
M = dict() # ma trận người dùng - bài toán thể hiện người dùng đã giải được bài toán hoặc không
F = dict() # ma trận người dùng - bài toán thể hiện số lần người dùng thử giải bài toán
Fs = dict() # ma trận người dùng - bài toán được cải tiến dùng logic mờ
problem_failed_set = dict() # danh sách bài toán người dùng đã thử nhưng chưa giải được
x_uf = dict() # lần thử trung bình của người dùng với bài toán p trong trường hợp chưa giải được
dev_uf = dict() # độ lệch số lần thử trung bình của người dùng với bài toán p trong trường hợp chưa giải được
C_uv = dict() # tập bài toán cả hai người dùng u, v cùng tương tác
SimProb_p = dict() # độ tương đồng giữa hai người dùng được xác định theo một bài toán cụ thể p 
Sim = dict() # độ tương đồng tổng quát của hai người dùng 
users = set([x['code'] for x in users_data])
problems = set([x['code'] for x in problems_data])
t = 5
user_problem_dict_test = {}

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
    for u in users:
        M[u] = dict()
        F[u] = dict()
        Fs[u] = dict()
        x_uf[u] = dict()
        dev_uf[u] = dict()
        problem_failed_set[u] = set()
        for p in problems:
            M[u][p] = 0
            F[u][p] = 0
            Fs[u][p] = 0
            SimProb_p[p] = dict()

    for p in problems:
        for u in users:
            SimProb_p[p][u] = dict()
            C_uv[u] = dict()
            Sim[u] = dict()
            for v in users:
                C_uv[u][v] = set()
                SimProb_p[p][u][v] = 0
                Sim[u][v] = 0

    for d in data:
        u = d['user']
        p = d['problem']
        r = d['result']
        if r == 'AC':
            M[u][p] = 1
        F[u][p] = F[u][p] + 1
    
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
        
def pre_process_data():
    # tiền xử lý dữ liệu
    for u in users:
        for p in problems:
            if M[u][p] == 0 and F[u][p] > 0:
                problem_failed_set[u].add(p)

    for u in users:
        failed_problems = problem_failed_set[u]

        if len(failed_problems) > 0:
            x_uf[u] = sum(F[u][p] for p in failed_problems) / len(failed_problems)
            dev_uf[u] = sum(abs(F[u][p] - x_uf[u]) for p in failed_problems) / len(failed_problems)
        else:
            x_uf[u] = 0
            dev_uf[u] = 0
        
    for u in users:
        failed_problems = problem_failed_set[u]

        lower_bound = x_uf[u] - dev_uf[u]
        upper_bound = x_uf[u] + dev_uf[u]

        for p in failed_problems:
            if F[u][p] < lower_bound or F[u][p] > upper_bound:
                F[u][p] = x_uf[u] 
                
def apply_fuzzy_logic():
    for u in users:
        for p in problems:
            if F[u][p] <= t:
                Fs[u][p] = F[u][p] / t
            else:
                Fs[u][p] = 1

def calc_similar():
    for u in Fs.keys():
        for v in Fs.keys():
            if u == v:
                continue  # Bỏ qua trường hợp u == v
            
            # Tập hợp các bài toán mà cả hai người dùng u và v đều có F* > 0
            common_problems = {p for p in problems if Fs[u][p] > 0 and Fs[v][p] > 0}
            C_uv[u][v] = common_problems

    for u in users:
        for v in users:
            common_p = C_uv[u][v]
            for problem in common_p:
                if M[u][problem] == M[v][problem]:
                    SimProb_p[problem][u][v] = 1 - abs(Fs[u][problem] - Fs[v][problem])   

    # Duyệt qua từng cặp người dùng u và v
    for u in Fs.keys():
        for v in Fs.keys():
            if u == v:
                continue  # Bỏ qua trường hợp u == v
            
            # Lấy tập hợp các bài toán chung trong C_{u, v}
            common_problems = C_uv[u][v]
            
            # Tính tổng SimProb cho các bài toán chung và độ lớn của C_{u, v}
            simprob_sum = 0
            for p in common_problems:
                simprob_sum += SimProb_p[p][u][v]
            
            # Tính độ tương đồng Sim(u, v)
            if len(common_problems) > 0:
                Sim[u][v] = simprob_sum / len(common_problems)

def get_k_near_user(user, k):
    sorted_sUX = dict(sorted(Sim[user].items(), key=lambda item: item[1], reverse=True))
    kUserNear = dict(list(sorted_sUX.items())[:k])
    return kUserNear

def get_n_recommend_problem(user, n):
    no_xp = problems.difference(set([p for p in problems if F[user][p] > 0]))
    recProblem = {}
    kUserNear = get_k_near_user(user=user, k=K)
    for p in no_xp:
        wp = 0
        # Duyệt qua từng người dùng trong danh sách hàng xóm
        for u, sim_value in kUserNear.items():
            # Kiểm tra nếu người dùng u đã giải quyết thành công bài toán p
            if M[u].get(p, 0) == 1:  # M[u][p] == 1, sử dụng get để tránh KeyError
                wp += sim_value  # Cộng dồn điểm tương đồng nếu u đã giải quyết bài toán p
        # Lưu điểm số cho bài toán p
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
    pre_process_data()
    apply_fuzzy_logic()
    calc_similar()
    not_solved, solved, recommended, not_recommened = get_info_user('B23DCCN863')
    print("not_solved", not_solved)
    print("solved", solved)
    print("recommended", recommended)
    print("not_recommened", not_recommened)

    precision, recall, f1 = get_score('B23DCCN863')
    print("precision", precision)
    print("recall", recall)
    print("f1", f1)