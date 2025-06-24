from PyQt5.QtCore import QObject
import random
from os import walk
import os
from lin_var import *


class MainModel(QObject):

    def __init__(self):
        super().__init__()

        self.current_lin_var = None
        self.current_lin_vars = [None, None, None]
        self.states_for_button_lv_vars = [False, False, False]
        self.states_for_button_lv_vars_values = [False, False]
        self.dir_lin_vars = 'lin_vars/'
        self.dir_rules = 'rules/'
        self.operators = ['И', 'ИЛИ']

    def convert_data(self, table_data):
        for r in table_data:
            try:
                r[0] = float(r[0])
                r[1] = float(r[1])
                r[2] = float(r[2])
                r[3] = float(r[3])
                r[4] = str(r[4])
            except:
                return "Not correct!"
        return table_data

    def create_lin_var(self, lin_var_name, table_data):
        terms = []
        for r in table_data:
            p0 = TermPoint(r[0], 0.0)
            p1 = TermPoint(r[1], 1.0)
            p2 = TermPoint(r[2], 1.0)
            p3 = TermPoint(r[3], 0.0)
            t = Term([p0, p1, p2, p3], r[4], [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)],
                     lin_var_name)
            terms.append(t)
        lin_var = LinguisticVariable(lin_var_name, terms)
        return lin_var

    def set_lin_var(self, lin_var):
        self.current_lin_var = lin_var

    def get_lin_var(self):
        return self.current_lin_var

    def save_lin_variable(self):
        if self.current_lin_var != None:
            name = self.current_lin_var.name
            with open(self.dir_lin_vars + name + ".pkl", "wb") as f:
                pickle.dump(self.current_lin_var, f)
            return "Ok"
        else:
            return None

    def save_rule(self, data):
        r = Rule(data)
        with open(self.dir_rules + r.name + ".pkl", "wb") as f:
            pickle.dump(r, f)

    def del_rule(self, rule_name):
        myfile = self.dir_rules + rule_name + ".pkl"
        if os.path.isfile(myfile):
            os.remove(myfile)

    def get_operators(self):
        return self.operators

    def get_names_lin_vars(self):
        return self.get_dir_all_filenames(self.dir_lin_vars)

    def get_names_rules(self):
        return self.get_dir_all_filenames(self.dir_rules)

    def get_dir_lin_vars(self):
        return self.dir_lin_vars

    def get_dir_all_filenames(self, dir):
        filenames = next(walk(dir), (None, None, []))[2]  # [] если файлов нет
        fs = []
        if len(filenames) != 0:
            for f in filenames:
                nf = f[:len(f) - 4]
                fs.append(nf)
        return fs

    def load_lv0_terms(self, lv_name):
        lin_var = self.load_lin_var(lv_name)
        self.current_lin_vars[0] = lin_var
        return lin_var.get_terms_names()

    def load_lv1_terms(self, lv_name):
        lin_var = self.load_lin_var(lv_name)
        self.current_lin_vars[1] = lin_var
        return lin_var.get_terms_names()

    def load_lv2_terms(self, lv_name):
        lin_var = self.load_lin_var(lv_name)
        self.current_lin_vars[2] = lin_var
        return lin_var.get_terms_names()

    def load_lin_var(self, lv_name):
        with open(self.dir_lin_vars + lv_name + ".pkl", "rb") as f:
            lin_var = pickle.load(f)
        return lin_var

    def load_rule(self, rule_name):
        with open(self.dir_rules + rule_name + ".pkl", "rb") as f:
            rule = pickle.load(f)
        return rule

    def set_state_for_lv0_var(self, txt):
        self.set_state_lv_vars(txt, 0)

    def set_state_for_lv1_var(self, txt):
        self.set_state_lv_vars(txt, 1)

    def set_state_for_lv2_var(self, txt):
        self.set_state_lv_vars(txt, 2)

    def set_state_lv_vars(self, txt, i):
        if txt == "" or txt.isspace():
            self.states_for_button_lv_vars[i] = False
        else:
            self.states_for_button_lv_vars[i] = True

    def set_state_for_lv0_var_value(self, txt):
        self.set_state_lv_vars_vals(txt, 0)

    def set_state_for_lv1_var_value(self, txt):
        self.set_state_lv_vars_vals(txt, 1)

    def set_state_lv_vars_vals(self, txt, i):
        try:
            value = float(txt)
            if self.current_lin_vars[i].terms[len(self.current_lin_vars[i].terms) - 1].points[3].x >= value:
                self.states_for_button_lv_vars_values[i] = True
            else:
                self.states_for_button_lv_vars_values[i] = False
        except:
            self.states_for_button_lv_vars_values[i] = False

    def get_button_state(self):
        state = self.states_for_button_lv_vars[0] and self.states_for_button_lv_vars[1] and \
                self.states_for_button_lv_vars[2]
        state = state and self.states_for_button_lv_vars_values[0] and self.states_for_button_lv_vars_values[1]
        return state
