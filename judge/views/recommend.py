from judge.models import RecommendationData, Problem, Profile, Survey
from datetime import datetime
from django.db.models import Prefetch
import cProfile
import pstats

class RecommendationList:
    def __init__(self, user, ltype):
        self.user = user
        self.ltype = ltype
        
    def get_db_data(self):
        self.data_survey = Survey.objects.all()
        self.users = Profile.objects.exclude(id=1).values_list('id', flat=True)
        self.problems = Problem.objects.all().values_list('id', flat=True)

    def setup_for_recommend(self):
        self.get_db_data()
        
        self.M = dict() # ma trận người dùng - bài toán thể hiện người dùng đã giải được bài toán hoặc không
        self.F = dict() # ma trận người dùng - bài toán thể hiện số lần người dùng thử giải bài toán
        self.Fs = dict() # ma trận người dùng - bài toán được cải tiến dùng logic mờ
        self.problem_failed_set = dict() # danh sách bài toán người dùng đã thử nhưng chưa giải được
        self.x_uf = dict() # lần thử trung bình của người dùng với bài toán p trong trường hợp chưa giải được
        self.dev_uf = dict() # độ lệch số lần thử trung bình của người dùng với bài toán p trong trường hợp chưa giải được
        self.C_uv = dict() # tập bài toán cả hai người dùng u, v cùng tương tác
        self.SimProb_p = dict() # độ tương đồng giữa hai người dùng được xác định theo một bài toán cụ thể p 
        self.Sim = dict() # độ tương đồng tổng quát của hai người dùng 
        self.Sims = dict() # độ tương đồng của hai người dùng dựa trên dữ liệu khảo sát
        self.t = 3 # số lần thử mà nếu vượt quá thì bài toán được coi là khó nhất
        
        # khởi tạo dữ liệu đề xuất
        for u_code in self.users:
            self.M[u_code] = dict()
            self.F[u_code] = dict()
            self.Fs[u_code] = dict()
            self.x_uf[u_code] = dict()
            self.dev_uf[u_code] = dict()
            self.problem_failed_set[u_code] = set()
            for p_code in self.problems:
                self.M[u_code][p_code] = 0
                self.F[u_code][p_code] = 0
                self.Fs[u_code][p_code] = 0
                self.SimProb_p[p_code] = dict()
                
        for p_code in self.problems:
            for u_code in self.users:
                self.SimProb_p[p_code][u_code] = dict()
                self.C_uv[u_code] = dict()
                self.Sim[u_code] = dict()
                for v_code in self.users:
                    self.C_uv[u_code][v_code] = set()
                    self.SimProb_p[p_code][u_code][v_code] = 0
                    self.Sim[u_code][v_code] = 0
        
    
    def get_default_data_survey(self):
        self.S = dict()
        for s in self.data_survey:
            u_code = s.user.id
            ans_set = set([s.language, s.experience, s.purpose , s.skill_level, s.algorithm, s.contest, s.hobby])
            self.S[u_code] = ans_set
        for u_code in self.users:
                self.Sims[u_code] = dict()
                for v_code in self.users:
                    try:
                        self.Sims[u_code][v_code] = len(self.S[u_code] & self.S[v_code]) / 7
                    except:
                        self.Sims[u_code][v_code] = 0
    
    def pre_process_data(self):
        for u_code in self.users:
            for p_code in self.problems:
                if self.F[u_code][p_code] > 0:
                    self.problem_failed_set[u_code].add(p_code)

        for u_code in self.users:
            failed_problems = self.problem_failed_set[u_code]

            if len(failed_problems) > 0:
                # Tính x_u_f
                self.x_uf[u_code] = sum(self.F[u_code][p] for p in failed_problems) / len(failed_problems)
                
                # Tính dev_u_f
                self.dev_uf[u_code] = sum(abs(self.F[u_code][p] - self.x_uf[u_code]) for p in failed_problems) / len(failed_problems)
            else:
                self.x_uf[u_code] = 0
                self.dev_uf[u_code] = 0
                
        for u_code in self.users:
            failed_problems = self.problem_failed_set[u_code]
            lower_bound = self.x_uf[u_code] - self.dev_uf[u_code]
            upper_bound = self.x_uf[u_code] + self.dev_uf[u_code]

            for p in failed_problems:
                if self.F[u_code][p] < lower_bound or self.F[u_code][p] > upper_bound:
                    self.F[u_code][p] = self.x_uf[u_code] 
    
    def apply_fuzzy(self):
        for u_code in self.users:
            for p_code in self.problems:
                if self.F[u_code][p_code] <= self.t:
                    self.Fs[u_code][p_code] = self.F[u_code][p_code] / self.t
                else:
                    self.Fs[u_code][p_code] = 1
    
    def calculate_similarity(self):
        # tính toán tập bài toán người dùng cùng có tương tác
        for u in self.Fs.keys():
            for v in self.Fs.keys():
                if u == v:
                    continue  # Bỏ qua trường hợp u == v
                
                # Tập hợp các bài toán mà cả hai người dùng u và v đều có F* > 0
                common_problems = {p for p in self.Fs[u].keys() if self.Fs[u][p] > 0 and self.Fs[v][p] > 0}
                
                # Lưu kết quả vào ma trận C_uv
                self.C_uv[u][v] = common_problems
                
        # tính toán độ tương đồng giữa hai người dùng trên 1 bài toán
        for u_code in self.users:
            for v_code in self.users:
                common_p = self.C_uv[u_code][v_code]
                for problem in common_p:
                    if self.M[u_code][problem] == self.M[v_code][problem]:
                        self.SimProb_p[problem][u_code][v_code] = 1 - abs(self.Fs[u_code][problem] - self.Fs[v_code][problem])   
    
        # Tính toán độ tương đồng tổng thể của hai người dùng
        for u in self.Fs.keys():
            for v in self.Fs.keys():
                if u == v:
                    continue  # Bỏ qua trường hợp u == v
                
                # Lấy tập hợp các bài toán chung trong C_{u, v}
                common_problems = self.C_uv[u][v]
                
                # Tính tổng SimProb cho các bài toán chung và độ lớn của C_{u, v}
                simprob_sum = 0
                for p in common_problems:
                    simprob_sum += self.SimProb_p[p][u][v]
                
                # Tính độ tương đồng Sim(u, v)
                if len(common_problems) > 0:
                    self.Sim[u][v] = simprob_sum / len(common_problems)

    def run_process(self):
        data_sub = RecommendationData.objects.select_related('problem', 'user').values(
            'problem_id', 'user_id', 'final_result', 'number_of_attempt'
        ).iterator(chunk_size=5000)
    

        for rec_data in data_sub:
            p_code = rec_data['problem_id']
            u_code = rec_data['user_id']
            final_result = rec_data['final_result']

            self.M.setdefault(u_code, {})[p_code] = 1 if final_result == "AC" else 0
            self.F.setdefault(u_code, {})[p_code] = rec_data['number_of_attempt']
    
        self.problem_map = {}

        for problem in Problem.objects.prefetch_related('types'):
            self.problem_map[problem.id] = [ptype.id for ptype in problem.types.all()]

    def calc_weight_point(self):
        n = len(self.ltype)
        start = 1.0
        step = 0.2
        decimal_values = [start - i * step for i in range(n)]
        self.type_values_dict = {self.ltype[i]: decimal_values[i] for i in range(n)}

    def get_max_decimal(self):
        self.problem_value = {}
        for problem, types in self.problem_map.items():
            values = [self.type_values_dict[t] for t in types if t in self.type_values_dict]
            self.problem_value[problem] = max(values, default=0.5)

    def get_recommendation_list(self):
        n = 15
        self.setup_for_recommend()
        self.run_process()
        self.calc_weight_point()
        self.get_max_decimal()
        
        self.pre_process_data()
        self.apply_fuzzy()
        self.calculate_similarity()
        self.get_default_data_survey()
        
        sUX = self.Sim[self.user]
        sUX.pop(self.user)
        sorted_sUX = dict(sorted(sUX.items(), key=lambda item: item[1], reverse=True))
        kUserNear = dict(list(sorted_sUX.items())[:n])

        if kUserNear[list(kUserNear.keys())[n-1]] == 0:
            sUX = self.Sims[self.user]
            sUX.pop(self.user)
            sorted_sUX = dict(sorted(sUX.items(), key=lambda item: item[1], reverse=True))
            kUserNear = dict(list(sorted_sUX.items())[:n])
        
        
        problemCode = set(k for k, v in self.M[self.user].items() if v == 1)
        p_code = set(self.problems)
        no_xp = p_code.difference(problemCode)
        recProblem = {}

        for p in no_xp:
            wp = 0
            for u, sim_value in kUserNear.items():
                if self.M[u].get(p, 0) == 1:
                    wp += sim_value
            recProblem[p] = wp * self.problem_value[p]

        sortedRecProblem = dict(sorted(recProblem.items(), key=lambda item: item[1], reverse=True))
        
        for i in list(sortedRecProblem.keys())[:15]:
            print(i, sortedRecProblem[i])

        return list(sortedRecProblem.keys())[:15]