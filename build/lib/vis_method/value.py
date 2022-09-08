import pandas as pd
import math
import numpy as np
from scipy.stats.mstats import gmean, hmean

# # data = pd.read_csv('./DataYearHOSE_update03042022.csv')
# path = ''
class Value:
    def __init__(self) -> None:
        '''
        path:   địa chỉ lưu file
        data:   file dữ liệu dùng để test
        result, element, index, last_op,
            index_ht, index_file_kq,
            n, count, high_profit, 
            exp_high_profit, index_file :   các biến số trong quá trình xử lí
        '''
        self.path = ''
        self._name = 'Value'
        self._alpha = ''
        self.data_full = pd.DataFrame()
        self.data_test = pd.DataFrame()
        self._description = 'với công thức được chọn, mỗi năm, tính giá trị công thức với các biến số tương ứng của cty, cty nào có giá tị lớn nhất thì chọn'
        self._module = []
        self._method_create_exp = ['create_exp_all', 'sinhF']
        self._result = []
        self._element = ""
        self._index_vetcan = []
        self._index = 0
        self._index_F = 0   
        self._last_op = ""
        self._index_ht = 0
        self._index_qk = 0
        self._index_file_qk = 0
        self._n = 1
        self._count = 0
        self._high_profit = []
        self._exp_high_profit = []
        self._index_file = 0
        self._number_ct = math.inf
        self._profit_condition = 0
        self._index_T = []  
        self._index_test = []
        self._time_moment = 0
        self._Fn = None
        self._expFn = []
        self._pfFn = []
        self._maxpf = 0
        self._F0 = None
        self._type_data = 'YEAR'
        self._flag = True
        self._dtFn = pd.DataFrame()
        self.high_rank_fomula = ['test']*100
        self.high_rank_val = np.zeros(100)
        self.min_rank_val = np.min(self.high_rank_val)
    
    def _update_last_time(self):
        try:
            self._index_qk = int(pd.read_csv(f'{self.path}/index.csv')['index'][0])
            self._index_file_qk = int(pd.read_csv(f'{self.path}/index.csv')['index_file'][0])
            self._count =  int(pd.read_csv(f'{self.path}/index.csv')['count'][0])
            self._n =  int(pd.read_csv(f'{self.path}/index.csv')['n'][0])
        except:
            pass

    def create_exp_option(self, time_moment, number_ct=5000, profit_condition=1.4, type_data = 'YEAR', method = 'vetcan', module = 'basic'):
        '''
            data:               file dữ liệu
            time_moment:        số năm muốn test
            number_ct:          số công thức muốn lấy
            profit_condition:   lợi nhuận tối thiểu công thức muốn lấy
        '''
        if module == 'basic':
            self.get_profit = self.get_profit_basic
            self.data_full = self.data_full.sort_values(by=['TIME', 'SYMBOL'], ascending=[False, True], ignore_index=True)
        else:
            self.data_full = self.data_full.sort_values(by=['TIME', 'PROFIT'], ascending=[False, False], ignore_index=True)
            self.get_profit = self.get_profit_harmean_rank
        self._update_last_time()
        self._time_moment = time_moment
        self._number_ct = number_ct
        self._profit_condition = profit_condition
        self._type_data = type_data
        
        self._index_T = self._get_index_T()
        self.data_test = self.data_full.loc()[self._index_T[-self._time_moment]:self._index_T[-1]].reset_index(drop=True)
        self._index_test = self._get_index_T(for_data= 'test')
        self._run(method)
        if method == 'sinhF':
            self._save_file()
        self._save_process()

        file_fomula = pd.DataFrame({'fomula': self._exp_high_profit, 'profit': self._high_profit})

        return file_fomula

    def get_profit_basic(self, fomula):
        '''
            fomula:             Công thức cần kiểm tra lợi nhuận
        '''
        result_ =  np.nan_to_num(eval(fomula), nan=-math.inf, posinf=-math.inf, neginf=-math.inf)
        loinhuan = 1
        for j in range(len(self._index_test)-1, 0, -1):
            index_max = np.argmax(result_[self._index_test[j-1]:self._index_test[j]])+self._index_test[j-1]
            loinhuan*= PROFIT[index_max]
        return loinhuan**(1.0/(self._time_moment-1))

    def get_value_profit_company(self, fomula):
        '''
            fomula:             Công thức cần kiểm tra lợi nhuận
        '''
        result_ =  np.nan_to_num(eval(fomula), nan=-math.inf, posinf=-math.inf, neginf=-math.inf)
        loinhuan = []
        company = []
        value = []
        year = []
        for j in range(len(self._index_test)-1, 0, -1):
            index_max = np.argmax(result_[self._index_test[j-1]:self._index_test[j]])+self._index_test[j-1]
            loinhuan.append(PROFIT[index_max])
            company.append(COMPANY[index_max])
            value.append(result_[index_max])
            year.append(self.data_test['TIME'][index_max])
        return value, loinhuan, company, year

    def get_variable(self):
        list_variable = [[]]*26
        list_column = list(self.data_test.columns)
        for i in range(4, len(list_column)):
            list_variable[i-4] = np.array(self.data_test[list_column[i]])
        return list_variable
    
    def _run(self, method):
        global A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z, PROFIT, COMPANY

        [A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z] = [[]]*26
        [A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z] = self.get_variable()
        PROFIT = np.array(self.data_test["PROFIT"])
        COMPANY = np.array(self.data_test["SYMBOL"])
        var_char = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        count = 0
        for var in [A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z]:
            if len(var) > 0:
                self._alpha = self._alpha + var_char[count]
            count += 1

        if method == 'vetcan':
            while True:
                try:
                    self._index_file = self._index_file_qk
                    self._crExp()
                    self._index_file = 0
                    self._index_file_qk = 0
                    self._n += 1
                except:
                    break
        elif method == 'sinhbac':
            print('chạy sinh bậc')
            while True:
                try:
                    self._crExp_sinh_bac()
                    self._index_file = 0
                    self._index_file_qk = 0
                    self._n += 1
                except:
                    break
        elif method == 'sinhF':
            print('chạy sinh F')
            self._save_F0()
            self._read_file()
            while True:
                try:
                    self._auto_code_F()
                except:
                    break

    def _processListSize(self, listSizeEle):
        result = []
        for i in range(len(listSizeEle)):
            listSizeEle[i] = [(listSizeEle[i][j], listSizeEle[i][j+1])
                            for j in range(0, len(listSizeEle[i]), 2)]
            listSizeEle[i].sort(key=lambda x: x[0])
            listSizeEle[i].sort(key=lambda x: x[0]+x[1])
        dict_list = {}
        for i in range(len(listSizeEle)):
            try:
                k = dict_list[str(listSizeEle[i])]
            except:
                dict_list[str(listSizeEle[i])] = 1
                result.append(listSizeEle[i])
        for i in range(len(result)):
            dict_ele_size = {}
            for j in range(len(result[i])):
                try:
                    dict_ele_size[f"{result[i][j][0]}_{result[i][j][1]}"] += 1
                except:
                    dict_ele_size[f"{result[i][j][0]}_{result[i][j][1]}"] = 1
            result[i] = dict_ele_size
        return result

    def _sizeElement(self, listSizeEle, sizeEle, total_size):
        if sum(sizeEle) == total_size:
            if len(sizeEle) % 2 == 1:
                sizeEle.append(0)
                listSizeEle.append(sizeEle.copy())
                sizeEle.pop()
            else:
                listSizeEle.append(sizeEle.copy())
        else:
            if len(sizeEle) == 0:
                for i in range(1, total_size - sum(sizeEle)+1):
                    sizeEle.append(i)
                    self._sizeElement(listSizeEle, sizeEle, total_size)
                    sizeEle.pop()
            else:
                if len(sizeEle) % 2 == 1:
                    for i in range(total_size - sum(sizeEle)+1):
                        sizeEle.append(i)
                        self._sizeElement(listSizeEle, sizeEle, total_size)
                        sizeEle.pop()
                else:
                    for i in range(1, total_size - sum(sizeEle)+1):
                        sizeEle.append(i)
                        self._sizeElement(listSizeEle, sizeEle, total_size)
                        sizeEle.pop()
        return listSizeEle

    def _expInvalid(self, exp1, exp2):
        key = dict()
        for i in range(0, len(exp1), 2):
            key[exp1[i]] = 1
        for i in range(0, len(exp2), 2):
            try:
                key[exp2[i]] += 1
                return False
            except:
                pass
        return True

    def _creatElement(self, multi, divide):
        key = {}
        for i in range(len(self._alpha)):
            key[self._alpha[i]] = i+1
        exp_multi = [list(self._alpha)]
        n = max(multi, divide)
        while len(exp_multi) < n:
            exp_multi.append([])
            for i in range(len(exp_multi[-2])):
                for j in range(key[exp_multi[-2][i][-1]] - 1, len(self._alpha)):
                    exp_multi[-1].append(exp_multi[-2][i]+"*"+self._alpha[j])
        if divide == 0:
            return exp_multi[multi-1]
        exp_divide = list(map(lambda x: x.replace("*", "/"), exp_multi[divide-1]))
        exp_multi = exp_multi[multi-1]
        result = []
        
      
        for i in range(len(exp_multi)):
            for j in range(len(exp_divide)):
                if self._expInvalid(exp_multi[i], exp_divide[j]):
                    result.append(exp_multi[i] + "/" + exp_divide[j])
        return result

    def _auto_code(self, elements, exp):
        if len(exp) == len(elements):
            self._index_ht += 1
            if self._index_ht >= self._index_qk:
                ct = "".join(exp)
                p = self.get_profit(ct)
                if p > self._profit_condition:
                    self._high_profit.append(p)
                    self._exp_high_profit.append(ct)
                    if len(self._exp_high_profit) > self._number_ct:
                        raise Exception('Target Complete')

        else:
            n = len(exp)
            for i in range(len(elements[n])):
                exp.append(elements[n][i])
                self._auto_code(elements, exp)
                exp.pop()

    def _crElement(self, elements, times):
        if len(self._index_vetcan) == times:
            self._result.append(self._element)
        else:
            if len(self._index_vetcan) == 0:
                start = 0
            else:
                start = self._index_vetcan[-1]
            last_op_psedou = self._last_op
            for i in range(start, len(elements)):
                for op in ['+', '-']:
                    if i == start and op != self._last_op and self._last_op != "":
                        continue
                    else:
                        self._element += op + elements[i]
                        self._index_vetcan.append(i)
                        self._last_op = op
                        self._crElement(elements, times)
                        self._element = self._element[:len(self._element)-len(elements[0])-1]
                        self._index_vetcan.pop()
                        self._last_op = last_op_psedou
        
    def _crExp(self):
        list_size = self._processListSize(self._sizeElement([], [], self._n))
        list_exp_child = []
        for i in range(self._index_file_qk, len(list_size)):
            for key, value in list_size[i].items():
                key = key.split('_')
                self._crElement(self._creatElement(int(key[0]), int(key[1])), value)
                list_exp_child.append(self._result.copy())
                self._result = []
                self._element = ""
                self._index_vetcan = []
                self._last_op = ""
            self._result = []
            try:
                self._auto_code(list_exp_child, [])
            except:
                raise Exception('Đã sinh đủ công thức theo yêu cầu')
            list_exp_child = []
            self._index_file += 1
            self._index_ht = 0
            self._index_qk = 0
        
        return "DONE"

    def _save_process(self):
        if self._index_ht > 0:
            self._index_ht -= 1

        size = min(len(self._high_profit), len(self._exp_high_profit))
        self._high_profit = self._high_profit[:size]
        self._exp_high_profit = self._exp_high_profit[:size]
        if len(self._high_profit) != 0:
            self._count += 1
            df = pd.DataFrame({'profit':self._high_profit, 'congthuc':self._exp_high_profit})
            df.to_csv(f"{self.path}/high_profit{self._count}.csv", index=False)
        df = pd.DataFrame({'index':[self._index_ht], 'index_file':[self._index_file], 'n': [self._n], 'count':[self._count]}) 
        df.to_csv(f"{self.path}/index.csv")

    def _get_index_T(self, for_data = 'full'):
        if for_data == 'full':
            list_T = self.data_full['TIME']
            index_T = [0]
            for i in range(len(list_T)-1):
                if list_T[i] != list_T[i+1]:
                    index_T.append(i+1)
            index_T.append(len(list_T))
            return index_T
        else:
            list_T = self.data_test['TIME']
            index_T = [0]
            for i in range(len(list_T)-1):
                if list_T[i] != list_T[i+1]:
                    index_T.append(i+1)
            index_T.append(len(list_T))
            return index_T

    def _getIndex(self):
        arr = np.array(self.data_full['TIME'])
        if self._type_data == 'YEAR':
            for s in arr:
                yield (int(s)-np.min(arr))+1
        else:
            for s in arr:
                yield (int(s)-np.min(arr))+1

    def _crElement_create_F(self):
        dict_key = {}
        for i in range(len(self._alpha)):
            dict_key[self._alpha[i]] = i+1
        res_exp = [list(self._alpha)]
        while len(res_exp) < self._n:
            res_exp.append([])
            for i in range(len(res_exp[-2])):
                if len(res_exp) == 2:
                    last_op = '+'
                else:
                    last_op = res_exp[-2][i][-2]
                for j in range(dict_key[res_exp[-2][i][-1]]-1, len(dict_key)):
                    for op in ['+', '-']:
                        if j == dict_key[res_exp[-2][i][-1]]-1 and op != last_op:
                            # print(j, dict_key[res_exp[-2][i][-1]]-1)
                            pass
                        else:
                            res_exp[-1].append(res_exp[-2][i]+op+res_exp[0][j])
        return res_exp[-1]

    def _F(self):
        res_exp = self._crElement_create_F()
        s_pf = []
        s_exp = []
        for i in range(len(res_exp)):
            for j in range(len(res_exp)):
                if i != j:
                    if self._n == 1:
                        exp = res_exp[i] + '/' + res_exp[j]
                        s_exp.append(exp)
                        s_pf.append(self.get_profit(exp))
                
                    else:
                        exp = f"({res_exp[i]})/({res_exp[j]})"
                        s_exp.append(exp)
                        s_pf.append(self.get_profit(exp))
        
        df = pd.DataFrame({'congthuc' : s_exp, 'profit': s_pf})
        df.to_csv(f'{self.path}/f0.csv', index=False)

        df = pd.DataFrame({'n': [0], 'mpf': [max(s_pf)]})
        df.to_csv(f'{self.path}/fn.csv', index=False)

        df = pd.DataFrame({'index' : [0]})
        df.to_csv(f'{self.path}/indexF.csv', index=False)

        df = pd.DataFrame({'index_file': [0]})
        df.to_csv(f'{self.path}/index_file.csv', index=False)
        return "DONE F0"

    def _save_F0(self):
        try:
            self._dtFn = pd.read_csv(f'{self.path}/f0.csv')
        except:
            self._n = 2
            self._F()

    def _read_file(self):
        try:
            self._index_F = int(pd.read_csv(f'{self.path}/indexF.csv')['index'][0])
            self._maxpf = float(pd.read_csv(f'{self.path}/fn.csv')['mpf'][0])
            self._n = int(pd.read_csv(f'{self.path}/fn.csv')['n'][0])
            self._F0 = list(pd.read_csv(f'{self.path}/f0.csv')['congthuc'])
            self._Fn = list(pd.read_csv(f'{self.path}/f{self._n}.csv')['congthuc'])
        except:
            raise Exception("Kết thúc vì quy trình xảy ra gián đoạn!")

    def _save_file(self):
        self._expFn = self._expFn[:min(len(self._expFn), len(self._pfFn))]
        self._pfFn = self._pfFn[:min(len(self._expFn), len(self._pfFn))]

        if len(self._expFn) != 0:
            df = pd.DataFrame({'index': [self._index_ht]})
            df.to_csv(f'{self.path}/indexF.csv', index=False)

            try:
                self._dtFn = pd.read_csv(f'{self.path}/f{self._n+1}.csv')
                self._expFn = list(self._dtFn['congthuc']) + self._expFn
                self._pfFn = list(self._dtFn['profit']) + self._pfFn
            except:
                pass
            finally:
                self._dtFn = pd.DataFrame({'congthuc': self._expFn, 'profit': self._pfFn})
                self._dtFn.to_csv(f'{self.path}/f{self._n+1}.csv', index=False)

            if self._flag:
                df = pd.DataFrame({'n': [self._n+1], 'mpf': [max(self._pfFn)]})
                df.to_csv(f'{self.path}/fn.csv', index=False)
                self._flag = False
            df = 0
        
        else:
            return "........"
        return "DONE SAVE FILE"
    
    def _auto_code_F(self):
        while True:
            for i in range(self._index, len(self._Fn)): 
                for j in range(self._index_F, len(self._F0)):
                    for op in ['+', '-', '*', '/']:
                        if self._index_ht >= self._index_F:
                            exp = self._Fn[i] + op + self._F0[j]
                            p = self.get_profit(exp)
                            #cao hơn max_pf thì lưu để tạo F(n+1)
                            if p > self._maxpf:
                                self._expFn.append(exp)
                                self._pfFn.append(p)
                            if p > self._profit_condition:
                                self._high_profit.append(p)
                                self._exp_high_profit.append(exp)
                                if len(self._exp_high_profit) > self._number_ct:
                                    raise Exception('Target Complete')
                self._index_ht += 1
                self._index_F = 0
            self._flag = True
            if self._save_file() != "DONE SAVE FILE":
                break
            self._expFn = []
            self._pfFn = []
            self._index_ht = 0
            self._index_F = 0
            self._index = 0
            try:
                self._read_file()
            except:
                break

    def _get_same(self, list_size_element):
        new_size_element = []
        for item in list_size_element:
            mod_arr = np.mod(np.array(item), 2)
            # print('nhìn', mod_arr)
            if np.sum(mod_arr) == 0:
                # print('check', item)
                new_size_element.append(item)
            elif np.sum(mod_arr) == len(mod_arr)/2:
                # print('check', item)
                new_size_element.append(item)
        return new_size_element

    def _get_bac(self, item_full):
        item = [item_full[i] for i in range(0, len(item_full), 2)]
        bac = np.min(item)
        list_bac = []
        list_bac_possible = [bac-2*x for x in range(round(bac/2)+1)]
        for bac in list_bac_possible:
            if bac > 0:
                list_bac.append(bac)
        return list_bac

    def _preProcessListSize(self, new_size_element):
        list_all_bac = []
        for item in new_size_element:
            list_all_bac.append(self._get_bac(item))
        list_all_size_element = []
        for id in range(len(list_all_bac)):
            size_element = new_size_element[id]
            list_bac = list_all_bac[id]
            for bac in list_bac:
                temp_size_element = size_element.copy()
                check = True
                for i in range(0, len(size_element), 2):
                    if temp_size_element[i] > bac:
                        temp_size_element[i+1] = int((temp_size_element[i] - bac)/2)
                        # if temp_size_element[i+1] % 1 != 0:
                        #     check = False
                        temp_size_element[i] = int((temp_size_element[i] + bac)/2)
                # if check == True:
                list_all_size_element.append(temp_size_element)
                temp_size_element = []
        return list_all_size_element
  
    def _crExp_sinh_bac(self):
        print(self._n)
        list_size = self._processListSize(self._preProcessListSize(self._get_same(self._process_list_size_element(self._sizeElement([], [], self._n)))))
        list_exp_child = []
        for i in range(self._index_file_qk, len(list_size)):
            list_power = []
            for key, value in list_size[i].items():
                key = key.split('_')
                self._crElement(self._creatElement(int(key[0]), int(key[1])), value)
                power = int(key[0])- int(key[1])
                list_power.append(power)
                list_exp_child.append(self._result.copy())
                self._result = []
                self._element = ""
                self._index = []
                self._last_op = ""
            self._result = []
            try:
                self._auto_code_power(list_exp_child, [], 0, list_power)
            except:
                raise Exception('Đã sinh đủ công thức theo yêu cầu')
            list_exp_child = []
            self._index_file += 1
            self._index_ht = 0
            self._index_qk = 0
        
        return "DONE"
 
    def _process_list_size_element(self, list_size_element):
        list_new_size_element = []
        for item in list_size_element:
            check = True
            for i in range(1, len(item), 2):
                if item[i] > 0:
                    check = False
            if check == True:
                list_new_size_element.append(item)
        return list_new_size_element
    
    def _auto_code_power(self, elements, exp, power, list_power):
        if len(exp) == len(elements):
            self._index_ht += 1
            if self._index_ht >= self._index_qk:
                ct = f'({"".join(exp)}){"/A" * power}'
                p = self.get_profit(ct)
                if p > self._profit_condition:
                    self._high_profit.append(p)
                    self._exp_high_profit.append(ct)
                    if len(self._exp_high_profit) > self._number_ct:
                        raise Exception('Target Complete')

        else:
            n = len(exp)
            for i in range(len(elements[n])):
                exp.append(elements[n][i])
                power = list_power[n]
                self._auto_code_power(elements, exp, power, list_power)
                exp.pop()
                
    def get_barier(self, file_ct, time_moment):
        '''
            file_ct:            dataframe có 2 cột là fomula và profit tương ứng
        '''
        self._time_moment = time_moment
        self.data_full = self.data_full.sort_values(by=['TIME', 'SYMBOL'], ascending=[False, True], ignore_index=True)
        self._index_T = self._get_index_T()
        self.data_test = self.data_full.loc()[self._index_T[-self._time_moment-1]:self._index_T[-1]].reset_index(drop=True)
        self._index_test = self._get_index_T(for_data= 'test')
        file_barier = pd.DataFrame({'fomula': [], 'profit': [], 'profit_barier': [], 'barier': [], 'value/barier': []})
        global A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z, PROFIT, COMPANY
        [A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z] = [[]]*26
        [A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z] = self.get_variable()
        PROFIT = np.array(self.data_test["PROFIT"])
        COMPANY = np.array(self.data_test["SYMBOL"])
        var_char = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        count = 0
        for var in [A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z]:
            if len(var) > 0:
                self._alpha = self._alpha + var_char[count]
            count += 1
        df_pf = pd.DataFrame({'congthuc':list(file_ct['congthuc'])})
        df_val = pd.DataFrame({'congthuc':list(file_ct['congthuc'])})
        all_pf = []
        all_val = []
        current_company = []
        list_ct = list(file_ct['congthuc'])
        for ct in list_ct:
            test = self.get_value_profit_company(ct)
            all_val.append(test[0])
            all_pf.append(test[1])
            current_company.append(test[2][-1])
        for i in range(self._time_moment):
            df_pf[i+1] = [item[i] for item in all_pf]
            df_val[i+1] = [item[i] for item in all_val]
        df_pf['company'] = current_company
        df_val['company'] = current_company
        file_barier = pd.DataFrame(index=np.arange(0, len(list_ct)),columns=('Year', 'Company_fake', 'profit_ct', 'if_barrier', 'current_val/barrier','barrier', 'con_lai', 'quater_val', 'Profit', 'COMPANY'))
        for i in range(len(df_pf)):
            cthuc = list_ct[i]
            company = current_company[i]
            list_val_ct= all_val[i][:-1]
            list_pf_ct = all_pf[i][:-1]
            profit_ct = gmean(list_pf_ct)
            val_per_quater = [-math.inf]
            profit_barrier = []
            for j in range(1,len(list_pf_ct)):
                if list_pf_ct[j-1] < 1:
                    val_per_quater.append(list_val_ct[j-1]/list_pf_ct[j-1]**2)
                else:
                    val_per_quater.append(list_val_ct[j]/list_pf_ct[j])
                if list_val_ct[j] >= val_per_quater[j]:
                    profit_barrier.append(list_pf_ct[j])
            con_lai_Hieu = len(profit_barrier)
            result_if_barrier = gmean(np.array(profit_barrier))
            current_val = all_val[i][-1]
            current_pf = all_pf[i][-1]
            file_barier.loc[i] = [self._time_moment, cthuc, profit_ct, result_if_barrier, current_val/val_per_quater[-1], val_per_quater[-1], con_lai_Hieu, current_val, current_pf, company]
       
        return file_barier, df_pf, df_val

    def get_profit_harmean_rank(self, fomula):
        result_ =  np.nan_to_num(eval(fomula), nan=-math.inf, posinf=-math.inf, neginf=-math.inf)
        rank = []
        # loinhuan = 1
        for j in range(len(self._index_test)-1, 0, -1):
            if np.max(result_[self._index_test[j-1]:self._index_test[j]]) == 0:
                return 0
            rank_i = np.argmax(result_[self._index_test[j-1]:self._index_test[j]]) + 1
            rank.append(1/rank_i)

            # loinhuan*= PROFIT[index_max]
        hmean_rank = hmean(rank)
        if hmean_rank > self.min_rank_val:
            index_replace = np.argmin(self.high_rank_val)
            self.high_rank_val[index_replace] = hmean_rank
            self.high_rank_fomula[index_replace] = fomula
            self.min_rank_val = np.min(self.high_rank_val)
        return hmean_rank

    # def get_profit_harmean_rank_print(self, fomula):
    #     result_ =  np.nan_to_num(eval(fomula), nan=-math.inf, posinf=-math.inf, neginf=-math.inf)
    #     rank = []
    #     loinhuan = 1
    #     for j in range(len(self._index_test)-1, 0, -1):
    #         index_max = np.argmax(result_[self._index_test[j-1]:self._index_test[j]])+self._index_test[j-1]
    #         rank_i = index_max - self._index_test[j-1] + 1
    #         print(rank_i, self.data_test['TIME'][index_max], self._index_test[j-1])
    #         print(result_[self._index_test[j-1]:self._index_test[j]])
    #         rank.append(1/rank_i)
    #         loinhuan*= PROFIT[index_max]
    #     print(rank, fomula)
    #     return hmean(rank)



        