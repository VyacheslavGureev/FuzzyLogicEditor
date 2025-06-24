import pickle


class LinguisticVariable():
    def __init__(self, name, terms):
        self.name = name
        self.terms = terms

    def get_term_by_name(self, term_name):
        for t in self.terms:
            if t.name == term_name:
                return t

    def get_terms_names(self):
        t_names = []
        for t in self.terms:
            t_names.append(t.name)
        return t_names

    def check_requirements(self):
        n = len(self.terms)
        i_last_term = n - 1
        for t in self.terms:
            if not (t.points[0].x <= t.points[1].x and t.points[1].x <= t.points[2].x and t.points[2].x <= t.points[
                3].x):
                return "Ошибка формы терма (не правильная трапеция)"
        if not ((self.terms[0].points[0].x == self.terms[0].points[1].x) and (
                self.terms[i_last_term].points[2].x == self.terms[i_last_term].points[3].x)):
            return "Ошибка максимумов на краевых точках"
        x_max = self.terms[i_last_term].points[3].x
        x_min = self.terms[0].points[0].x
        p = x_min
        for i in range(len(self.terms)):
            if self.terms[i].points[3].x >= p and self.terms[i].points[0].x <= p:
                p = self.terms[i].points[3].x
        if p < x_max:
            return "Ошибка полноты покрытия"
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                if not (self.terms[i].points[1].x > self.terms[j].points[2].x or self.terms[i].points[2].x <
                        self.terms[j].points[1].x):
                    return "Ошибка несовместимости максимумов"
        return "Ошибок нет"


class Term():
    def __init__(self, points, name, color, name_lin_var):
        self.name = name
        self.color = color
        self.points = points
        self.name_lin_var = name_lin_var

    def function(self, x, a, b):
        return float((x - a) / (b - a))

    def get_fuzz(self, x):
        if self.points[0].x <= x and x <= self.points[1].x:
            if self.points[0].x == self.points[1].x:
                return 1.0
            else:
                return self.function(x, self.points[0].x, self.points[1].x)
        elif self.points[1].x <= x and x <= self.points[2].x:
            return 1.0
        elif self.points[2].x <= x and x <= self.points[3].x:
            if self.points[2].x == self.points[3].x:
                return 1.0
            else:
                return self.function(x, self.points[3].x, self.points[2].x)
        else:
            return 0.0


class TermPoint():
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Rule():
    def __init__(self, data):
        self.rule = {'Если': {'var0': data[2],
                              'val0': float(data[3]),
                              'lv0': data[0],
                              'term0': data[1],

                              'var1': data[7],
                              'val1': float(data[8]),
                              'lv1': data[5],
                              'term1': data[6]},
                     'Оператор': data[4],
                     'То': {'var': data[11],
                            'lv': data[9],
                            'term': data[10]}}
        self.name = "Если" + " " + "(" + self.rule["Если"]["var0"] + "=" + str(self.rule["Если"]["val0"]) + ")" \
                    + " есть " + self.rule["Если"]["term0"] + \
                    " " + self.rule["Оператор"] + " " \
                    + "(" + self.rule["Если"]["var1"] + "=" + str(self.rule["Если"]["val1"]) + ")" \
                    + " есть " + self.rule["Если"]["term1"] + " " + \
                    ", То" + " " + self.rule["То"]["var"] + " есть " + self.rule["То"]["term"] + \
                    " (" + self.rule["Если"]["lv0"] + " " + self.rule["Если"]["lv1"] + " " + self.rule["То"]["lv"] + ")"

    def get_res_var_name(self):
        return self.rule["То"]["var"]

    def get_res_lv_name(self):
        return self.rule["То"]["lv"]

    def __eq__(self, other):
        if isinstance(other, Rule):
            same = (self.rule["То"]["lv"] == other.rule["То"]["lv"]) and (
                    self.rule["То"]["var"] == other.rule["То"]["var"])
            return same
        return False

    def __hash__(self):
        return hash(self.rule["То"]["lv"] + self.rule["То"]["var"])


class Solver():
    def __init__(self, dir_lin_vars):
        self.dir_lin_vars = dir_lin_vars

    def group(self, rules):
        groups = []
        map_dict = {}
        for r in rules:
            if r in map_dict:
                pos = map_dict[r]
                groups[pos].append(r)
            else:
                pos = len(groups)
                map_dict[r] = pos
                groups.append([r])
        return groups

    def get_agregation(self, rule):
        lv0 = self.load_lin_var(rule.rule["Если"]["lv0"])
        lv1 = self.load_lin_var(rule.rule["Если"]["lv1"])
        t0 = lv0.get_term_by_name(rule.rule["Если"]["term0"])
        t1 = lv1.get_term_by_name(rule.rule["Если"]["term1"])
        val0 = rule.rule["Если"]["val0"]
        val1 = rule.rule["Если"]["val1"]
        a = t0.get_fuzz(val0)
        b = t1.get_fuzz(val1)
        res = 0.0
        if rule.rule["Оператор"] == 'И':
            res = min(a, b)
        elif rule.rule["Оператор"] == 'ИЛИ':
            res = max(a, b)
        return res

    def get_activization(self, rule, res):
        lv = self.load_lin_var(rule.rule["То"]["lv"])
        t = lv.get_term_by_name(rule.rule["То"]["term"])
        x, y = self.get_solve(lv, t, res)
        return x, y

    def get_solve(self, lv, t, res):
        i_last_term = len(lv.terms) - 1
        N = int((lv.terms[i_last_term].points[3].x - lv.terms[0].points[0].x) * 4)
        step = (lv.terms[i_last_term].points[3].x - lv.terms[0].points[0].x) / N
        x = []
        y = []
        for i in range(0, N + 1):
            x.append(lv.terms[0].points[0].x + step * i)
            perem = min(res, t.get_fuzz(lv.terms[0].points[0].x + step * i))
            if perem < 0.0:
                perem = 0.0
            y.append(perem)
        return x, y

    def concat_set(self, y1, y2):
        res_y = [0] * len(y1)
        for j in range(len(y1)):
            res_y[j] = max(y1[j], y2[j])
        return res_y

    def get_defuzz(self, x, y):
        sum1 = 0
        sum2 = 0
        for i in range(len(x)):
            sum1 += x[i] * y[i]
            sum2 += y[i]
        res = sum1 / sum2
        return res

    def load_lin_var(self, lv_name):
        with open(self.dir_lin_vars + lv_name + ".pkl", "rb") as f:
            lin_var = pickle.load(f)
        return lin_var
