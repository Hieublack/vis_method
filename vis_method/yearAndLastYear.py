import pandas as pd
import math
import numpy as np
import os
from scipy.stats.mstats import gmean, hmean


# # data = pd.read_csv('./DataYearHOSE_update03042022.csv')
# path = ''

class YearAndLastYear:
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
        self.name = 'YearAndLastYear'
        self._alpha = ''
        self.data_full = pd.DataFrame()
        self.data_test = pd.DataFrame()
        self.description = ''
        self.module = []
        self.method_create_exp = ['create_exp_all', 'sinhmoi']
        self._result = []
        self._element = ""
        self._index = 0
        self._index_vetcan = []
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
        self._type_data = 'YEAR'
        self._g = 1
        self._g0 = 1
        self._method = 1
        self._ct1 = 0
        self._ct2 = 0
        self._list_lai_g = [] 
        self._list_lo_g = [] 
        self._pf_lai = [] 
        self._pf_lo = [] 
        self._profit_group = 1
        self._list_lai_pre = []
        self._list_lo_pre = []
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
        self._update_last_time()
        if module == 'basic':
            self.get_profit = self.get_profit_basic
            self.data_full = self.data_full.sort_values(by=['TIME', 'SYMBOL'], ascending=[False, True], ignore_index=True)
        else:
            self.data_full = self.data_full.sort_values(by=['TIME', 'PROFIT'], ascending=[False, False], ignore_index=True)
            self.get_profit = self.get_profit_harmean_rank
        self._time_moment = time_moment
        self._number_ct = number_ct
        self._profit_condition = profit_condition
        self._type_data = type_data

        self._index_T = self._get_index_T()
        self.data_test = self.data_full.loc()[self._index_T[-self._time_moment]:self._index_T[-1]].reset_index(drop=True)
        self._index_test = self._get_index_T(for_data= 'test')

        self._run(method)
        self._save_process()

        file_fomula = pd.DataFrame({'fomula': self._exp_high_profit, 'profit': self._high_profit})

        return file_fomula


    def auto_sinh_rieng_T_1(self):
        toantu = '+-*/'
        toanhang = self._alpha
        list_ct = []
        
        for tt in toantu[:2]:
            for th1 in toanhang:
                list_ct.append('(' + tt + th1 + ')')
                for tt2 in toantu:
                    for th2 in toanhang:
                        if th1 == th2:
                            continue
                        ct = '('+tt+th1+tt2+th2+')'
                        list_ct.append(ct)
        list_ct = self._cleanData(list_ct)
        
        list_lai_0 = []
        list_lo_0 = []
        for ct in list_ct:
            profit = self.get_profit(ct)
            if profit > 1+self._profit_group:
                list_lai_0.append(ct)
                if profit >= self._profit_condition:
                    self._high_profit.append(profit)
                    self._exp_high_profit.append(ct)
                    if len(self._high_profit) >= self._number_ct:
                        raise Exception('Target Complete')

            elif profit< 1-self._profit_group:
                list_lo_0.append(ct)
            
        try:
            index_history = pd.read_csv(f'{self.path}/index.csv')
            self._g0 = index_history['generation'][0]
        except:
            self._g0 = 1
        for g in range(self._g0,5):
            self._g = g

            pd.DataFrame({'congthuc':[], 'profit':[]}).to_csv(f'{self.path}/data/Time{self._time_moment}/high_profit_{self._g}.csv', index= False)
            pd.DataFrame({'congthuc':[], 'profit':[]}).to_csv(f'{self.path}/data/Time{self._time_moment}/low_profit_{self._g}.csv', index= False)
            
        
            
            try:
                self._list_lai_pre = list(pd.read_csv(f'{self.path}/data/Time{self._time_moment}/high_profit_{g-1}.csv')['congthuc'])
                self._list_lo_pre = list(pd.read_csv(f'{self.path}/data/Time{self._time_moment}/low_profit_{g-1}.csv')['congthuc'])
                self._list_lai_g = list(pd.read_csv(f'{self.path}/data/Time{self._time_moment}/high_profit_{g}.csv')['congthuc'])
                self._pf_lai = list(pd.read_csv(f'{self.path}/data/Time{self._time_moment}/high_profit_{g}.csv')['profit'])
                self._list_lo_g = list(pd.read_csv(f'{self.path}/data/Time{self._time_moment}/low_profit_{g}.csv')['congthuc'])
                self._pf_lo = list(pd.read_csv(f'{self.path}/data/Time{self._time_moment}/low_profit_{g}.csv')['profit'])
                index_history = pd.read_csv(f'{self.path}/index.csv')
                m0 = index_history['method'][0]
                m1 = index_history['ct1'][0] 
                m2 = index_history['ct2'][0]
            except:
                list_lai_pre, list_lo_pre, list_lai_g, list_lo_g, pf_lai, pf_lo = [], [], [], [], [], []
                m0, m1, m2 = 1, 0, 0
                pass

            print(self._time_moment, self._g, m0, m1, m2)
            print(len(list_lai_pre), len(list_lo_pre), len(list_lai_g), len(list_lo_g), len(pf_lai), len(pf_lo))

            if self._g == 1:
                for method in range(m0,4):
                    if method == 1:
                        for ct1 in range(m1, len(list_lai_0)):
                            for ct2 in range(m2, len(list_lai_0)):
                                if ct1 == ct2:
                                    continue
                                else:
                                    list_merge = self._merge_ct(list_lai_0[ct1], list_lai_0[ct2], 1)
                                    for ct in list_merge:
                                        if self.check(ct) == False:
                                            continue
                                        profit = self.get_profit(ct)
                                        if profit > 1 + self._profit_group*(self._g+1):
                                            self._list_lai_g.append(ct)
                                            self._pf_lai.append(profit)
                                            if profit >= self._profit_condition:
                                                self._high_profit.append(profit)
                                                self._exp_high_profit.append(ct)
                                                if len(self._high_profit)  >= self._number_ct:
                                                    raise Exception('Target Complete')
                                        elif profit < 1-self._profit_group*self._g:
                                            self._list_lo_g.append(ct)
                                            self._pf_lo.append(profit)
                    elif method == 2:
                        for self._ct1 in range(m1, len(list_lo_0)):
                            for self._ct2 in range(m2, len(list_lo_0)):
                                if self._ct1 == self._ct2:
                                    continue
                                else:
                                    list_merge = self._merge_ct(list_lo_0[self._ct1], list_lo_0[self._ct2], 1)
                                    for ct in list_merge:
                                        if self._check(ct) == False:
                                            continue
                                        profit = self.get_profit(ct)
                                        if profit > 1+self._profit_group*(self._g+1):
                                            self._list_lai_g.append(ct)
                                            self._pf_lai.append(profit)
                                            if profit >= self._profit_condition:
                                                self._high_profit.append(profit)
                                                self._exp_high_profit.append(ct)
                                                if len(self._high_profit) >= self._number_ct:
                                                    raise Exception('Target Complete')
                                        elif profit < 1-self._profit_group*self._g:
                                            self._list_lo_g.append(ct)
                                            self._pf_lo.append(profit)
                    else:
                        for self._ct1 in range(m1, len(list_lai_0)):
                            for self._ct2 in range(m2, len(list_lo_0)):
                                list_merge = self._merge_ct(list_lai_0[self._ct1], list_lo_0[self._ct2], 0)
                                for ct in list_merge:
                                    if self._check(ct) == False:
                                        continue
                                    profit = self.get_profit(ct)
                                    if profit > 1+self._profit_group*(self._g+1):
                                        self._list_lai_g.append(ct)
                                        self._pf_lai.append(profit)
                                        if profit >= self._profit_condition:
                                            self._high_profit.append(profit)
                                            self._exp_high_profit.append(ct)
                                            if len(self._high_profit) >= self._number_ct:
                                                raise Exception('Target Complete')
                                    elif profit < 1-self._profit_group*self._g:
                                        self._list_lo_g.append(ct)
                                        self._pf_lo.append(profit)

            else:
                for method in range(m0,4):
                    if method == 1:
                        all_lai = list_lai_0+self._list_lai_pre
                        for self._ct1 in range(m1, len(all_lai)):
                            for self._ct2 in range(m2, len(self._list_lai_pre)):
                                if all_lai[ct1] == self._list_lai_pre[self._ct2]:
                                    continue
                                else:
                                    list_merge = self._merge_ct(all_lai[self._ct1], self._list_lai_pre[self._ct2], 1)
                                    for ct in list_merge:
                                        if self._check(ct) == False:
                                            continue
                                        profit = self.get_profit(ct)
                                        if profit > 1+self._profit_group*(self._g+1):
                                            self._list_lai_g.append(ct)
                                            self._pf_lai.append(profit)
                                            if profit >= self._profit_condition:
                                                self._high_profit.append(profit)
                                                self._exp_high_profit.append(ct)
                                                if len(self._high_profit) >= self._number_ct:
                                                    raise Exception('Target Complete')
                                        elif profit < 1-self._profit_group*self._g:
                                            self._list_lo_g.append(ct)
                                            self._pf_lo.append(profit)
                    elif method == 2:
                        all_lo = list_lo_0+self._list_lo_pre
                        for self._ct1 in range(m1, len(all_lo)):
                            for self._ct2 in range(m2, len(self._list_lo_pre)):
                                if all_lo[self._ct1] == self._list_lo_pre[self._ct2]:
                                    continue
                                else:
                                    list_merge = self._merge_ct(all_lo[self._ct1], self._list_lo_pre[self._ct2], 1)
                                    for ct in list_merge:
                                        if self._check(ct) == False:
                                            continue
                                        profit = self.get_profit(ct)
                            
                                        if profit > 1+self._profit_group*(self._g+1):
                                            self._list_lai_g.append(ct)
                                            self._pf_lai.append(profit)
                                            if profit >= self._number_ct:
                                                self._high_profit.append(profit)
                                                self._exp_high_profit.append(ct)
                                                if len(self._high_profit) >= self._number_ct:
                                                    raise Exception('Target Complete')
                                        elif profit < 1-self._profit_group*self._g:
                                            self._list_lo_g.append(ct)
                                            self._pf_lo.append(profit)
                    else:
                        for self._ct1 in range(m1,len(self._list_lai_pre)):
                            for self._ct2 in range(m2,len(self._list_lo_pre)):
                                list_merge = self._merge_ct(self._list_lai_pre[self._ct1], self._list_lo_pre[self._ct2], 0)
                                for ct in list_merge:
                                    if self._check(ct) == False:
                                        continue
                                    profit = self.get_profit(ct)
                                    if profit > 1+self._profit_group*(self._g+1):
                                        self._list_lai_g.append(ct)
                                        self._pf_lai.append(profit)
                                        if profit >= self._profit_condition:
                                            self._high_profit.append(profit)
                                            self._exp_high_profit.append(ct)
                                            if len(self._high_profit)  >= self._number_ct:
                                                raise Exception('Target Complete')
                                    elif profit < 1-self._profit_group*self._g:
                                        self._list_lo_g.append(ct) 
                                        self._pf_lo.append(profit)
            
            index_history = pd.DataFrame({'quater':[self._time_moment],'generation':[g+1], 'method':[1], 'ct1':[0], 'ct2':[0]})
            index_history.to_csv(f'{self.path}/index.csv', index= False)

            file_ct_cao = pd.DataFrame({'congthuc':self._list_lai_g, 'profit':self._pf_lai})
            file_ct_thap = pd.DataFrame({'congthuc':self._list_lo_g, 'profit':self._pf_lo})
            file_ct_cao.to_csv(f'{self.path}/data/Year{self._time_moment}/high_profit_{self._g}.csv', index= False)
            file_ct_thap.to_csv(f'{self.path}/data/Year{self._time_moment}/low_profit_{self._g}.csv', index= False)

    def get_profit_basic(self, fomula):
        '''
            fomula:             Công thức cần kiểm tra lợi nhuận
        '''
        result_ =  np.nan_to_num(eval(fomula), nan=-1000000000000000000, posinf=-1000000000000000000, neginf=-1000000000000000000)
        loinhuan = 1
        for j in range(len(self._index_test)-2, 0, -1):
            index_max = np.argmax(result_[self._index_test[j-1]:self._index_test[j]])+self._index_test[j-1]
            loinhuan*= Z[index_max]
        return loinhuan**(1.0/(self._time_moment-2))

    def get_profit_harmean_rank(self, fomula):
        '''
            fomula:             Công thức cần kiểm tra lợi nhuận
        '''
        result_ =  np.nan_to_num(eval(fomula), nan=-1000000000000000000, posinf=-1000000000000000000, neginf=-1000000000000000000)
        rank = []
        for j in range(len(self._index_test)-2, 0, -1):
            rank_i = np.argmax(result_[self._index_test[j-1]:self._index_test[j]]) + 1
            rank.append(1/rank_i)
        hmean_rank = hmean(rank)
        if hmean_rank > self.min_rank_val:
            index_replace = np.argmin(self.high_rank_val)
            self.high_rank_val[index_replace] = hmean_rank
            self.high_rank_fomula[index_replace] = fomula
            self.min_rank_val = np.min(self.high_rank_val)
        return hmean_rank

    def get_value_profit_company(self, fomula):
        '''
            fomula:             Công thức cần kiểm tra lợi nhuận
        '''
        result_ =  np.nan_to_num(eval(fomula), nan=-1000000000000000000, posinf=-1000000000000000000, neginf=-1000000000000000000)
        loinhuan = []
        company = []
        value = []
        year = []
        for j in range(len(self._index_test)-2, 0, -1):
            index_max = np.argmax(result_[self._index_test[j-1]:self._index_test[j]])+self._index_test[j-1]
            loinhuan.append(Z[index_max])
            company.append(COMPANY[index_max])
            value.append(result_[index_max])
            year.append(self.data_test['TIME'][index_max])
        return value, loinhuan, company, year


    def get_barier(self, file_ct):
        '''
            file_ct:            dataframe có 2 cột là fomula và profit tương ứng
        '''
        file_barier = pd.DataFrame({'fomula': [], 'profit': [], 'profit_barier': [], 'barier': [], 'value/barier': []})

        return file_barier

    def get_variable(self):
        list_variable = [[]]*26
        list_last_variable = [[]]*26
        list_column = list(self.data_test.columns)
        for i in range(4, len(list_column)-18):
            list_variable[i-4] = np.array(self.data_test[list_column[i]])
            list_last_variable[[i-4]] = self._set_value(np.array(self.data_test[list_column[i]]))
        return list_variable, list_last_variable

    def _run(self, method):

        global A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z, PROFIT, COMPANY
        global a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z
        [A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z] = [[]]*26
        [a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z] = [[]]*26
        [A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z],[a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z]  = self.get_variable()
        PROFIT = np.array(self.data_test["PROFIT"])
        COMPANY = np.array(self.data_test["SYMBOL"])
        var_char = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        count = 0
        var_last_year = 'abcdefghijklmnopqrstuvwxyz'
        for var in [A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z]:
            if len(var) > 0:
                self._alpha = self._alpha + var_char[count] + var_last_year[count]
            count += 1
        PROFIT = np.array(self.data_test["PROFIT"])
        COMPANY = np.array(self.data_test["SYMBOL"])

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
        # else:
            # try:
            #     os.mkdir(f'{self.path}/data')
            # except:
            #     pass
            # try:
            #     os.mkdir(f'{self.path}/data/Timme{self._time_moment}')
            # except:
            #     pass
            # while True:
            #     try:
            #         self.auto_sinh_rieng_T_1
            #     except:
            #         break

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

    def _merge_ct(SELF,ct1,ct2,choose):
        if choose == 1:
            ctn1 = '(' + ct1 + '+' + ct2 + ')'
            ctn2 = '(' + ct1 + '*' + ct2 + ')'
            return [ctn1, ctn2]
        else:
            ctn1 = '(' + ct1 + '-' + ct2 + ')'
            ctn2 = '(' + ct1 + '/' + ct2 + ')'
            ctn3 = '(' + ct2 + '-' + ct1 + ')'
            ctn4 = '(' + ct2 + '/' + ct1 + ')'
            return ctn1, ctn2, ctn3, ctn4

    def _set_value(self, arr, type = 'test'):
            
        index = self._get_index(type)
        result = []

        for i in range(len(index)):
            if index[i] == -100000000:
                result.append(0)
            else:
                result.append(arr[index[i]])
        
        return np.array(result)

    def _get_index(self, type = 'test'):
        if type == 'full':
            data_ = self.data_full
        else:
            data_ = self.data_test
        year = data_["TIME"]
        company = data_["SYMBOL"]
        dict = {}
        for i in range(len(year)):
            try:
                dict[company[i]].append([year[i], i])
            except:
                dict[company[i]] = [[year[i], i]]

        result_index = len(year) * [-100000000]
        for company, value in dict.items():
            for i in range(len(value)-1):
                if value[i][0] == value[i+1][0]+1:
                    result_index[value[i][1]] = value[i+1][1]

        return result_index

    def _check(self,ct):
        val_T = 'ABCDEFGHI'
        val_T_1 = 'JKMLPVTYU'
        if set(val_T) & set(ct) != set() and set(val_T_1) & set(ct) != set():
            return True
        else:
            return False

    def _cleanData(self, list_ct):
        result = []
        dicter = {}
        '''
        ex_data_df : một mảng các biểu thức được đọc từ file
        dicter : dùng để loại bỏ các biểu thức trùng lặp
        Sử dụng try, except : xảy ra lỗi khi biểu thức không trùng lặp( chưa được xuất hiện trong các biểu thức
        trước đó) 
        result : Lưu các biểu thức không trùng lặp
        '''
        for i in range(len(list_ct)):
            try:
                k = dicter[self._convert(list_ct[i])]
            except:
                dicter[self._convert(list_ct[i])] = 1
                result.append(list_ct[i])
        return result

    def _convert(self, exp):
        data = self._split_exp(exp)
        data_process_ct = []
        dicter = {}
        result = []
        '''
        data : mảng trả về sau khi cắt biểu thức thành các elements con
        data_process : mỗi phần tử của mảng data sau khi được xử lí thông qua hàm process sẽ được
        thêm vào mảng data_process
        dicter: đếm các lần xuất hiện của các phần tử trong data_process(nếu op là - : value--
        op là + : value++
        result : Mỗi phần tử trong result được ghép lại bởi 2 thành phần là key và value(dicter[key] = value)
        Bước cuối : sắp xếp mảng result, chèn \ vào mỗi phần tử
        Mục đích(sắp xếp và chèn) : 2 exp giống nhau sẽ trả về cùng một kết quả
        '''
        for i in range(len(data)):
            data_process_ct.append(self._process_ct(data[i]))

        for i in range(len(data_process_ct)):
            if data_process_ct[i][0] == "+":
                try:
                    dicter[data_process_ct[i][1:]] += 1
                except:
                    dicter[data_process_ct[i][1:]] = 1
            else:
                try:
                    dicter[data_process_ct[i][1:]] -= 1
                except:
                    dicter[data_process_ct[i][1:]] = -1

        for key, value in dicter.items():
            if value == 0:
                pass
            else:
                result.append(str(value)+key)

        return "\\".join(sorted(result))

    def _split_exp(self, exp):
        if exp[0] in ["-", "+"]:
            pass
        else:
            exp = "+" + exp
        ''' dataA : mảng trả về sau khi cắt chuỗi ban đầu theo dấu +
            dataB : mảng trả về sau khi cắt từng phần tử của dataA theo dấu - 
            index : chỉ số sẽ tăng lên mỗi khi tìm thấy dấu + hoặc - ở chuỗi ban đầu(mục đích 
            để trước mỗi element sẽ có dấu + hoặc - thể hiện cho dấu của element đó trong chuỗi ban đầu)
            '''
        dataA = exp[1:].split("+")
        result = []
        index = 0
        for i in range(len(dataA)):
            dataB = dataA[i].split("-")
            for j in range(len(dataB)):
                result.append(dataB[j])
        for i in range(len(exp)):
            if exp[i] in ["+", "-"]:
                result[index] = exp[i] + result[index]
                index += 1
        return result

    #process : hàm xử lí chuỗi(+a*e/e ==> +a)
    def _process_ct(self, element):
        if len(element) == 2:
            return element
        else:
            '''
            dicter : dùng để lưu số lần xuất hiện của một chữ cái bất kì trong element truyền vào với key là chữ cái, 
            value là số lần xuất hiện 
            op : lưu dấu của element truyền vào(operator)
            the_dividend : chuỗi kí tự để lưu các kí tự có value trong dicter > 0(số bị chia)
            divisor : chuỗi kì tự để lưu các kí tự có value trong dicter < 0(số chia)
            '''
            dicter = {}
            dicter[element[1]] = 1
            op = element[0]
            the_dividend = ""
            divisor = ""
            for i in range(2, len(element)):
                if element[i] == "*":
                    try:
                        dicter[element[i+1]] += 1
                    except:
                        dicter[element[i+1]] = 1
                elif element[i] == "/":
                    try:
                        dicter[element[i+1]] -= 1
                    except:
                        dicter[element[i+1]] = -1

            for key, value in dicter.items():
                if value < 0:
                    for i in range(-value):
                        divisor += key
                elif value > 0:
                    for i in range(value):
                        the_dividend += key

            if len(divisor) == len(the_dividend) == 0:
                return op+"1"
            elif len(divisor) == 0:
                return op + "".join(sorted(list(the_dividend)))
            elif len(the_dividend) == 0:
                return op+"1"+"/"+divisor
            return op+"".join(sorted(list(the_dividend)))+"/" + "".join(sorted(list(divisor)))




# a = Value()
# a.path = './test'
# # data = pd.read_csv('DataYearHOSE_update03042022.csv')
# a.data_read = data

# check = a.create_exp_option(13,3000, 1.2, 'YEAR')

# print(check)
