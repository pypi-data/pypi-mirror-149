import copy
import time
import pandas as pd
import numpy as np
import scipy.stats as st
from sklearn.ensemble import RandomForestClassifier
from .data_pretreatment import col_is_number
from .function import divide


# 最高10类数量占比
top10_rate = 0.9
# 最大类别个数
max_type_num = 30


def identify_col(data, col):
    n = data[col].count()
    judge = pd.value_counts(data[col]).iloc[:10].sum() / n
    if col_is_number(data, col):
        if judge < top10_rate:
            return 'num_col'
        judge2 = len(pd.value_counts(data[col]))
        if judge2 > max_type_num:
            return 'to_cla_col'
        return 'num_cla_col'
    return 'to_cla_col'


def cross_woe_iv(cross_df):
    """
    基于cross_df
    """
    pos = cross_df[1]['All']
    neg = cross_df[0]['All']
    cross_df['rate'] = (cross_df[1] / cross_df['All']).round(4)
    bad_rat = cross_df[0] / neg
    good_rat = cross_df[1] / pos
    woe = pd.DataFrame(np.log(divide(good_rat, bad_rat, 1).map(lambda a: 1 if a == 0 else a)) * 100, columns=['woe'])
    woe.index = cross_df.index
    cross_df['woe'] = woe
    bad_dev = good_rat - bad_rat
    iv = sum(bad_dev * cross_df['woe']) / 100
    return cross_df, iv


def num_bins_woe_iv(num_bins, data, after_pretreatment):
    """
    基于num_bins
    """
    columns = ["min", "max", "0", "1"]
    df = pd.DataFrame(num_bins, columns=columns)
    range_pd = pd.DataFrame(map(lambda a, b: '(%s,%s]' % (round(a, 3), round(b, 3)),
                                df['min'], df['max']), columns=['range'])
    range_pd.iloc[0] = range_pd['range'].iloc[0].replace('(', '[')
    df.drop(['min', 'max'], axis=1, inplace=True)
    range_pd.index = df.index
    df = pd.concat([range_pd, df], axis=1)
    df["All"] = df['0'] + df['1']
    if not after_pretreatment:
        nan_0 = data[data.iloc[:, 1] == 0].isnull().sum().iloc[0]
        nan_1 = data[data.iloc[:, 1] == 1].isnull().sum().iloc[0]
        all_0 = data[data.iloc[:, 1] == 0].count().iloc[1]
        all_1 = data[data.iloc[:, 1] == 1].count().iloc[1]
        all_n = all_0 + all_1
        if nan_0 > 0 or nan_1 > 0:
            nan_row = pd.DataFrame([['nan', nan_0, nan_1, nan_0 + nan_1]],
                                   columns=['range', '0', '1', 'All'])
            df = pd.concat([df, nan_row], axis=0)
    else:
        all_0 = df['0'].sum()
        all_1 = df['1'].sum()
        all_n = all_0 + all_1
    df["rate"] = (df['1'] / df.All).round(4)
    df["woe"] = np.log(divide(df['1'] / all_1, df['0'] / all_0, 1).map(lambda a: 1 if a == 0 else a) * 100)
    all_row = pd.DataFrame([['All', all_0, all_1, all_n, round(all_1 / all_n, 4), 0]],
                           columns=['range', '0', '1', 'All', 'rate', 'woe'])
    df = pd.concat([df, all_row], axis=0)
    rate = (df['1'] / all_1) - (df['0'] / all_0)
    iv = np.sum(rate * df.woe)
    return df, iv


def cla_bin(data, col, label, convert_dict, n, after_pretreatment):
    n = len(pd.value_counts(data[col])) if len(pd.value_counts(data[col])) <= n else n
    cross_df = pd.crosstab(data[col], data[label], margins=True, dropna=False)
    cross_df.iloc[:-1] = cross_df.iloc[:-1].sort_values('All', ascending=False)
    all_df = cross_df.iloc[-1:]
    cross_df = cross_df.iloc[:-1]
    if after_pretreatment:
        if convert_dict is None:
            raise ValueError('对预处理后的数据做分析请输入convert_dict')
        if 'is_assets' not in convert_dict[col]:
            v_k_dict = dict(zip(convert_dict[col].values(), convert_dict[col].keys()))
        else:
            v_k_dict = dict(zip(convert_dict[col]['convert'].values(), convert_dict[col]['convert'].keys()))
        cross_df.index = cross_df.index.map(v_k_dict)
    if cross_df.shape[0] > n+1:
        other_df = pd.DataFrame([[sum(cross_df[0].iloc[n:]), sum(cross_df[1].iloc[n:]),
                                  sum(cross_df['All'].iloc[n:])]], columns=[0, 1, 'All'])
        other_df.index = ['其他']
        cross_df = pd.concat([cross_df.iloc[:n], other_df], axis=0)
    if not after_pretreatment:
        nan_all = all_df.All.iloc[-1] - cross_df.All.sum()
        if nan_all > 0:
            nan_0 = all_df[0].iloc[-1] - cross_df[0].sum()
            nan_1 = all_df[1].iloc[-1] - cross_df[1].sum()
            nan_df = pd.DataFrame([[nan_0, nan_1, nan_all]], columns=[0, 1, 'All'])
            nan_df.index = ['nan']
            cross_df = cross_df.append(nan_df)
    cross_df = pd.concat([cross_df, all_df], axis=0)
    cross_df, iv = cross_woe_iv(cross_df)
    return cross_df, iv


def num_bin(data, col, label, n, after_pretreatment):
    n = len(pd.value_counts(data[col])) if len(pd.value_counts(data[col])) <= n else n
    cross_df = pd.crosstab(data[col], data[label], margins=True, dropna=False)
    cross_df.iloc[:-1] = cross_df.iloc[:-1].sort_values('All', ascending=False)
    all_df = cross_df.iloc[-1:]
    cross_df = cross_df.iloc[:-1]
    if cross_df.shape[0] > n+1:
        other_df = pd.DataFrame([[sum(cross_df[0].iloc[n:-1]), sum(cross_df[1].iloc[n:-1]),
                                  sum(cross_df['All'].iloc[n:-1])]], columns=[0, 1, 'All'])
        other_df.index = ['其他']
        cross_df = pd.concat([cross_df.iloc[:n], other_df], axis=0)
    if not after_pretreatment:
        nan_all = all_df.All.iloc[-1] - cross_df.All.sum()
        if nan_all > 0:
            nan_0 = all_df[0].iloc[-1] - cross_df[0].sum()
            nan_1 = all_df[1].iloc[-1] - cross_df[1].sum()
            nan_df = pd.DataFrame([[nan_0, nan_1, nan_all]], columns=[0, 1, 'All'])
            nan_df.index = ['nan']
            cross_df = cross_df.append(nan_df)
    cross_df = pd.concat([cross_df, all_df], axis=0)
    cross_df, iv = cross_woe_iv(cross_df)
    return cross_df, iv


def bin_base_chi2(num_bins, n, data, after_pretreatment):
    pvs = []
    for i in range(len(num_bins) - 1):
        x1 = num_bins[i][2:]
        x2 = num_bins[i + 1][2:]
        # 0 返回 chi2 值，1 返回 p 值。
        pv = st.chi2_contingency([x1, x2])[1]
        pvs.append(pv)
    while len(pvs) > n:
        i = pvs.index(max(pvs))
        if i == len(pvs)-1:
            num_bins[i - 1:i + 1] = [(
                num_bins[i - 1][0],
                num_bins[i][1],
                num_bins[i - 1][2] + num_bins[i][2],
                num_bins[i - 1][3] + num_bins[i][3])]
            x1 = num_bins[i-1][2:]
            x2 = num_bins[i][2:]
            pv = st.chi2_contingency([x1, x2])[1]
            pvs[i-1] = pv
            pvs.pop(i)
        else:
            num_bins[i:i + 2] = [(
                num_bins[i][0],
                num_bins[i + 1][1],
                num_bins[i][2] + num_bins[i + 1][2],
                num_bins[i][3] + num_bins[i + 1][3])]
            x1 = num_bins[i][2:]
            x2 = num_bins[i + 1][2:]
            pv = st.chi2_contingency([x1, x2])[1]
            pvs[i] = pv
            pvs.pop(i+1)
    bins_df, iv = num_bins_woe_iv(num_bins, data, after_pretreatment)
    return bins_df, iv


class FeatureAnalysis:
    """
    特征分析，功能：
    计算字段之间相关性
    计算字段与标签相关性
    剔除高度相关字段
    自动分箱
    计算特征重要性
    """

    def __init__(
            self,
            col_dict: dict = None,
            convert_dict: dict = None,
            field_dict: dict = None,
            is_drop_corr: bool = True,
            white_set: set = None,
            label_first: bool = False,
            info_first: bool = False,
            corr: float = 0.9,
            after_pretreatment: bool = True,
            init_box: int = 30,
            final_box: int = 7,
            importance_rate: float = None,
            top_importance_k: int = 20,
            time_cost: bool = True
    ):
        """
        Parameters
        ----------
        convert_dict: dict
            字段转数值映射关系
        is_drop_corr: bool
            是否删除高度相关字段
        white_set: set
            白名单
        label_first: bool
            尽可能地保留与label更相关的字段
        info_first: bool
            尽可能地保留更多字段
        corr: float
            相关性
        after_pretreatment: bool
            是否分析预处理之后的数据
        init_box: int
            初始分箱个数
        final_box: int
            最终分箱个数
        importance_rate: float
            取重要性总占比超过importance_rate的字段
        top_importance_k: int
            取重要性前k个字段
        time_cost: bool
            是否显示耗时
        """
        self.col_dict = col_dict
        if col_dict is not None:
            self.col_dict_copy = {}
            for k, vs in col_dict.items():
                for v in vs:
                    self.col_dict_copy[v] = k
        self.convert_dict = convert_dict
        self.field_dict = {} if field_dict is None else field_dict
        self.is_drop_corr = is_drop_corr
        self.white_set = {} if white_set is None else white_set
        if label_first and info_first:
            raise ValueError('label_first与info_first不可同时为True')
        self.label_first = label_first
        self.info_first = info_first
        if not self.label_first and not self.info_first:
            self.info_first = True
        self.corr = corr
        self.after_pretreatment = after_pretreatment
        self.init_box = init_box
        self.final_box = final_box
        self.importance_rate = importance_rate
        self.top_importance_k = top_importance_k
        self.corr_pd = None  # corr dataframe
        self.corr_dict = None
        self.corr_with_label = None
        self.top_k_dict = {}
        self.time_cost = time_cost

    def fit(
            self,
            pre_data: pd.DataFrame,
            label: str,
            original_data: pd.DataFrame = None,
            is_drop_corr: bool = None,
            white_set: set = None,
            field_dict: dict = None,
            label_first: bool = None,
            info_first: bool = None,
            corr: float = None,
            after_pretreatment: bool = None,
            init_box: int = None,
            final_box: int = None,
            importance_rate: float = None,
            top_importance_k: int = None,
    ):
        self.is_drop_corr = self.is_drop_corr if is_drop_corr is None else is_drop_corr
        self.white_set = self.white_set if white_set is None else white_set
        self.field_dict = self.field_dict if field_dict is None else field_dict
        self.label_first = self.label_first if label_first is None else label_first
        self.info_first = self.info_first if info_first is None else info_first
        if self.label_first:
            self.info_first = False
        self.corr = self.corr if corr is None else corr
        self.after_pretreatment = self.after_pretreatment if after_pretreatment is None else after_pretreatment
        self.init_box = self.init_box if init_box is None else init_box
        self.final_box = self.final_box if final_box is None else final_box
        self.importance_rate = self.importance_rate if importance_rate is None else importance_rate
        self.top_importance_k = self.top_importance_k if top_importance_k is None else top_importance_k
        pre_data = copy.deepcopy(pre_data)
        if self.is_drop_corr:
            print('----------\n 删除高度相关字段')
            drop_corr_list = self.drop_corr_col(pre_data, label)
            pre_data.drop(drop_corr_list, axis=1, inplace=True)
        print('----------\n 提取前k个特征')
        top_k_list = list(self.feature_importance(pre_data, label).keys())
        print('----------\n 特征分析')
        if self.after_pretreatment:
            self.auto_bin(pre_data, label, top_k_list)
        if not self.after_pretreatment:
            if original_data is None:
                raise ValueError('对源数据进行分析请输入源数据')
            self.auto_bin(original_data, label, top_k_list)

    def col_corr(
            self,
            data: pd.DataFrame,
            label: str,
    ):
        start = time.time()
        self.corr_pd = data.drop(label, axis=1).corr()
        corr_dict = {}
        for i, col in enumerate(data.columns.drop(label)):
            for j in range(i + 1, len(data.columns.drop(label))):
                if abs(self.corr_pd[col][j]) >= self.corr:
                    if col in corr_dict:
                        corr_dict[col].append(data.columns[j])
                    else:
                        corr_dict[col] = [data.columns[j]]
        self.corr_dict = corr_dict
        end = time.time()
        if self.time_cost:
            print('耗时:', round(end - start, 4))
        return self.corr_pd, self.corr_dict

    def col_label_corr(
            self,
            data: pd.DataFrame,
            label: str
    ):
        self.corr_with_label = data.corrwith(data[label])
        return self.corr_with_label

    def drop_corr_col(
            self,
            data: pd.DataFrame,
            label: str
    ):
        if self.corr_dict is None:
            self.col_corr(data, label)
        if self.corr_with_label is None:
            self.col_label_corr(data, label)
        corr_drop = []
        corr_drop_name = []
        if self.label_first:
            for k, v in self.corr_dict.items():
                k_name = k if k not in self.field_dict else self.field_dict[k]
                if k in self.white_set:
                    for col in v:
                        if col in self.white_set:
                            if self.field_dict:
                                if k in self.field_dict and col in self.field_dict:
                                    print('%s:%s与%s:%s\n高度相关但因白名单而保留' %
                                          (k, self.field_dict[k], col, self.field_dict[col]))
                            else:
                                print('%s与%s高度相关但因白名单而保留' % (k, col))
                        else:
                            corr_drop.append(col)
                            field_name = col if col not in self.field_dict else self.field_dict[col]
                            corr_drop_name.append(field_name)
                    continue
                field_name_list = []
                for col in v:
                    field_name = col if col not in self.field_dict else self.field_dict[col]
                    field_name_list.append(field_name)
                    if col in self.white_set:
                        corr_drop.append(k)
                        corr_drop_name.append(k_name)
                        continue
                k_label = abs(self.corr_with_label[k])
                v_label = [abs(self.corr_with_label[i]) for i in v]
                max_value = max(v_label)
                if k_label > max_value:
                    corr_drop.extend(v)
                    corr_drop_name.append(field_name_list)
                else:
                    corr_drop.append(k)
                    corr_drop_name.append(k_name)
        if self.info_first:
            for k, v in self.corr_dict.items():
                k_name = k if k not in self.field_dict else self.field_dict[k]
                if k in self.white_set:
                    for col in v:
                        if col in self.white_set:
                            if self.field_dict:
                                if k in self.field_dict and col in self.field_dict:
                                    print('%s:%s与%s:%s\n高度相关但因白名单而保留' %
                                          (k, self.field_dict[k], col, self.field_dict[col]))
                            else:
                                print('%s与%s高度相关但因白名单而保留' % (k, col))
                        else:
                            corr_drop.append(col)
                            field_name = col if col not in self.field_dict else self.field_dict[col]
                            corr_drop_name.append(field_name)
                    continue
                for col in v:
                    if col in self.white_set:
                        corr_drop.append(k)
                        corr_drop_name.append(k_name)
                        continue
                if len(v) >= 2:
                    corr_drop.append(k)
                    corr_drop_name.append(k_name)
                else:
                    if self.corr_with_label[k] <= self.corr_with_label[v[0]]:
                        corr_drop.append(k)
                        corr_drop_name.append(k_name)
                    else:
                        col_name = v[0] if v[0] not in self.field_dict else self.field_dict[v[0]]
                        corr_drop.append(v[0])
                        corr_drop_name.append(col_name)
        if corr_drop:
            if self.field_dict:
                df = pd.DataFrame(data={'field': corr_drop, 'name': corr_drop_name})
            else:
                df = pd.DataFrame(data={'field': corr_drop})
            print('因相关性而被舍弃的字段:\n', df)
        return corr_drop

    def auto_bin_col(
            self,
            data: pd.DataFrame,
            label: str,
            col: str,
    ):
        bins_df = None,
        iv = None
        if self.after_pretreatment:
            if self.col_dict is None:
                raise ValueError('对预处理之后的数据做数据分析请输入col_dict')
            try:
                type_ = self.col_dict_copy[col]
            except KeyError:
                type_ = identify_col(data, col)
        else:
            type_ = identify_col(data, col)
        if type_ == 'to_cla_col':
            bins_df, iv = cla_bin(data, col, label, self.convert_dict, self.final_box, self.after_pretreatment)
        if type_ == 'num_cla_col':
            bins_df, iv = num_bin(data, col, label, self.final_box, self.after_pretreatment)
        if type_ == 'num_col':
            data = data[[col, label]].copy()
            data["q_cut"], bins = pd.qcut(data[col], retbins=True, q=self.init_box, duplicates="drop")
            count_y0 = data.loc[data[label] == 0].groupby(by="q_cut")[label].count()
            count_y1 = data.loc[data[label] == 1].groupby(by="q_cut")[label].count()
            num_bins = [*zip(bins, bins[1:], count_y0, count_y1)]  # 左开右闭
            # 确保每个分组的数据都包含有 0 和 1
            i = 0
            while i < len(num_bins):
                if i == 0:
                    if 0 in num_bins[i][2:]:
                        num_bins[i:2] = [(
                            num_bins[i][0],
                            num_bins[i + 1][1],
                            num_bins[i][2] + num_bins[i + 1][2],
                            num_bins[i][3] + num_bins[i + 1][3])]
                        continue
                    else:
                        i += 1
                if (len(num_bins) > 1) and (0 in num_bins[i][2:]):
                    num_bins[i - 1:i + 1] = [(
                        num_bins[i - 1][0],
                        num_bins[i][1],
                        num_bins[i - 1][2] + num_bins[i][2],
                        num_bins[i - 1][3] + num_bins[i][3])]
                    i -= 1
                else:
                    i += 1
            bins_df, iv = bin_base_chi2(num_bins, self.final_box, data, self.after_pretreatment)
        if self.field_dict:
            if col in self.field_dict:
                print('字段:%s, 字段名:%s' % (col, self.field_dict[col]))
        else:
            print('字段:', col)
        print(bins_df)
        print('iv值:', iv)
        return bins_df, iv

    def feature_importance(
            self,
            data: pd.DataFrame,
            label: str
    ):
        start = time.time()
        x = data.drop(label, axis=1)
        weight = round(data[data[label] == 0][label].count() / data[data[label] == 1][label].count(), 3)
        forest = RandomForestClassifier(n_estimators=100, max_depth=8, n_jobs=-1,
                                        class_weight={0: 1, 1: weight}, random_state=1)
        forest.fit(x, data[label])
        field = x.columns
        importance = forest.feature_importances_
        indices = np.argsort(importance)[::-1]
        top_k_dict = {}
        if self.importance_rate is not None:
            total_rate = 0
            for index in indices:
                top_k_dict[field[index]] = importance[index]
                total_rate += importance[index]
                if total_rate >= self.importance_rate:
                    break
        else:
            for index in indices[:self.top_importance_k]:
                top_k_dict[field[index]] = importance[index]
        end = time.time()
        if self.time_cost:
            print('耗时:', round(end - start, 4))
        return top_k_dict

    def auto_bin(
            self,
            data: pd.DataFrame,
            label: str,
            col_list: list
    ):
        columns = data.columns
        for col in col_list:
            if not self.after_pretreatment:
                if col not in columns:
                    continue
            _ = self.auto_bin_col(data, label, col)
