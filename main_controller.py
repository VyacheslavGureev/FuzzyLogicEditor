from main_model import MainModel
from main_view import MainView
from lin_var import *


class MainController():

    def __init__(self, main_view: MainView, plot_views, create_plot_view, main_model: MainModel):
        super().__init__()
        self.model = main_model
        self.view = main_view
        self.plot_views = plot_views
        self.create_plot_view = create_plot_view
        self.connects()

    def connects(self):
        self.view.signal_view_init.connect(self.fill_view)
        self.view.ui.pushButtonDraw.released.connect(self.draw_lin_var)
        self.view.ui.pushButtonAddNewLinVar.released.connect(self.add_new_lin_var)
        self.view.ui.pushButtonRuleAdd.released.connect(self.add_new_rule)
        self.view.ui.pushButtonRuleDel.released.connect(self.del_rule)
        self.view.ui.pushButtonCalculate.released.connect(self.calculate)
        self.view.ui.comboBoxLv0.currentTextChanged.connect(
            lambda: self.fill_cb_terms_lv0(self.view.get_cb_lv0_curr_txt()))
        self.view.ui.comboBoxLv1.currentTextChanged.connect(
            lambda: self.fill_cb_terms_lv1(self.view.get_cb_lv1_curr_txt()))
        self.view.ui.comboBoxLv2.currentTextChanged.connect(
            lambda: self.fill_cb_terms_lv2(self.view.get_cb_lv2_curr_txt()))

        self.view.ui.lineEditVar0.textChanged.connect(self.lv0_var_changed)
        self.view.ui.lineEditVar1.textChanged.connect(self.lv1_var_changed)
        self.view.ui.lineEditVar2.textChanged.connect(self.lv2_var_changed)

        self.view.ui.lineEditValueVar0.textChanged.connect(self.lv0_var_val_changed)
        self.view.ui.lineEditValueVar1.textChanged.connect(self.lv1_var_val_changed)

        self.view.ui.tabWidget.currentChanged.connect(self.tab_change)

    def draw_lin_var(self):
        self.assemble_lin_var()
        lin_var = self.model.get_lin_var()
        state = self.plot_views['lin_var'].draw_lin_var(lin_var)
        if state == "Ok":
            self.plot_views['lin_var'].show()

    def assemble_lin_var(self):
        lin_var_name, table_data = self.view.get_table_data()
        table_data = self.model.convert_data(table_data)
        if table_data == "Not correct!":
            self.view.send_err_msg("Данные не корректны!")
            self.model.set_lin_var(None)
        else:
            self.view.send_err_msg("Данные корректны!")
            lin_var = self.model.create_lin_var(lin_var_name, table_data)
            msg = lin_var.check_requirements()
            self.view.send_err_msg(msg)
            self.model.set_lin_var(lin_var)

    def add_new_lin_var(self):
        self.assemble_lin_var()
        state = self.model.save_lin_variable()
        if state == "Ok":
            self.view.send_err_msg("Лин. переменная сохранена")

    def add_new_rule(self):
        data_for_rule = self.view.get_rule_data()
        self.model.save_rule(data_for_rule)
        self.upd_rules()

    def del_rule(self):
        rule_name = self.view.get_curr_rule()
        self.model.del_rule(rule_name)
        self.upd_rules()

    def calculate(self):
        rules_names = self.model.get_names_rules()
        rules = []
        for rn in rules_names:
            rule = self.model.load_rule(rn)
            rules.append(rule)
        solver = Solver(self.model.get_dir_lin_vars())
        rules_groups = solver.group(rules)
        for g in range(len(rules_groups)):
            rule_res = solver.get_agregation(rules_groups[g][0])
            x, y_buff = solver.get_activization(rules_groups[g][0], rule_res)
            for i in range(1, len(rules_groups[g])):
                rule_res = solver.get_agregation(rules_groups[g][i])
                x, y = solver.get_activization(rules_groups[g][i], rule_res)
                y_buff = solver.concat_set(y_buff, y)
            defuzz_res = solver.get_defuzz(x, y_buff)
            res_var_name = rules_groups[g][0].get_res_var_name()
            res_lv_name = rules_groups[g][0].get_res_lv_name()
            plot_view = self.create_plot_view()
            self.plot_views[g] = plot_view
            self.plot_views[g].draw_result(x, y_buff, defuzz_res, res_lv_name, res_var_name + " = " + str(round(defuzz_res, 3)))
            self.plot_views[g].show()

    def fill_view(self):
        opers = self.model.get_operators()
        self.view.set_operators(opers)
        lin_vars = self.model.get_names_lin_vars()
        self.view.set_lin_vars(lin_vars)
        self.upd_rules()

    def upd_rules(self):
        rules = self.model.get_names_rules()
        self.view.set_rules(rules)

    def fill_cb_terms_lv0(self, curr_txt):
        if curr_txt != "":
            terms_names = self.model.load_lv0_terms(curr_txt)
            self.view.set_terms_names_cb_lv0(terms_names)

    def fill_cb_terms_lv1(self, curr_txt):
        if curr_txt != "":
            terms_names = self.model.load_lv1_terms(curr_txt)
            self.view.set_terms_names_cb_lv1(terms_names)

    def fill_cb_terms_lv2(self, curr_txt):
        if curr_txt != "":
            terms_names = self.model.load_lv2_terms(curr_txt)
            self.view.set_terms_names_cb_lv2(terms_names)

    def lv0_var_changed(self, txt):
        self.model.set_state_for_lv0_var(txt)
        state = self.model.get_button_state()
        self.view.set_button_state(state)

    def lv1_var_changed(self, txt):
        self.model.set_state_for_lv1_var(txt)
        state = self.model.get_button_state()
        self.view.set_button_state(state)

    def lv2_var_changed(self, txt):
        self.model.set_state_for_lv2_var(txt)
        state = self.model.get_button_state()
        self.view.set_button_state(state)

    def lv0_var_val_changed(self, txt):
        self.model.set_state_for_lv0_var_value(txt)
        state = self.model.get_button_state()
        self.view.set_button_state(state)

    def lv1_var_val_changed(self, txt):
        self.model.set_state_for_lv1_var_value(txt)
        state = self.model.get_button_state()
        self.view.set_button_state(state)

    def tab_change(self, i):
        if i == 1:
            self.fill_view()
