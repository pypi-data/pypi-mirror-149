import copy
import time
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from .feature_analysis import cross_woe_iv
from .feature_analysis import FeatureAnalysis
from .function import divide, keep_drop_judge

# 字段衍生舍弃iv阈值
low_iv = 0.02
# 字段衍生舍弃相关程度阈值
high_corr = 0.9


def is_opt_derive(data, label, col1, col2, judge):
    operators = ['+', '-', '*', '/']
    opt_col = {}
    derive_df = None
    derive_name = None
    derive_list = []  # 保存衍生的原字段和运算符
    for operator in operators:
        if operator == '/':
            col1_d_col2 = col1 + '/' + col2
            col2_d_col1 = col2 + '/' + col1
            derive_df = pd.DataFrame(data={
                col1_d_col2: divide(data[col1], data[col2], -1),
                col2_d_col1: divide(data[col2], data[col1], -1),
                col1: data[col1],
                col2: data[col2],
                label: data[label]})
            cross_df_1_2 = pd.crosstab(derive_df[col1_d_col2], data[label], margins=True)
            cross_df_2_1 = pd.crosstab(derive_df[col2_d_col1], data[label], margins=True)
            _, iv_1_2 = cross_woe_iv(cross_df_1_2)
            _, iv_2_1 = cross_woe_iv(cross_df_2_1)
            if iv_1_2 > low_iv or iv_2_1 > low_iv:
                corr_pd = derive_df.corr()
                if iv_1_2 > low_iv:
                    if (abs(corr_pd[col1_d_col2][col1]) < high_corr) and (abs(corr_pd[col1_d_col2][col2]) < high_corr)\
                        and (abs(corr_pd[col1_d_col2][label]) > judge):
                        opt_col[col1_d_col2] = derive_df[col1_d_col2]
                        derive_list.append([col1, operator, col2])
                if iv_2_1 > low_iv:
                    if (abs(corr_pd[col2_d_col1][col1]) < high_corr) and (abs(corr_pd[col2_d_col1][col2]) < high_corr)\
                        and (abs(corr_pd[col2_d_col1][label]) > judge):
                        opt_col[col2_d_col1] = derive_df[col2_d_col1]
                        derive_list.append([col2, operator, col1])
        else:
            if operator == '+':
                derive_name = col1 + '+' + col2
                derive_df = pd.DataFrame(data={
                    derive_name: data[col1] + data[col2],
                    col1: data[col1],
                    col2: data[col2],
                    label: data[label]})
            elif operator == '-':
                derive_name = col1 + '-' + col2
                derive_df = pd.DataFrame(data={
                    derive_name: data[col1] - data[col2],
                    col1: data[col1],
                    col2: data[col2],
                    label: data[label]})
            elif operator == '*':
                derive_name = col1 + '*' + col2
                derive_df = pd.DataFrame(data={
                    derive_name: data[col1] * data[col2],
                    col1: data[col1],
                    col2: data[col2],
                    label: data[label]})
            cross_df = pd.crosstab(derive_df[derive_name], data[label], margins=True)
            _, iv = cross_woe_iv(cross_df)
            if iv <= low_iv:
                continue
            corr_pd = derive_df.corr()
            if (abs(corr_pd[derive_name][col1]) < high_corr) and (abs(corr_pd[derive_name][col2]) < high_corr)\
                    and (abs(corr_pd[derive_name][label]) > judge):
                opt_col[derive_name] = derive_df[derive_name]
                derive_list.append([col1, operator, col2])
    return opt_col, derive_list


class FeatureProject(FeatureAnalysis):
    """
    特征工程，包括：
    计算字段iv值或字段重要性
    给定iv阈值或重要性阈值剔除字段
    字段衍生
    """

    def __init__(
        self,
        is_drop_corr: bool = True,
        white_set: set = None,
        field_dict: dict = None,
        label_first: bool = False,
        info_first: bool = False,
        corr: float = 0.9,
        is_drop_iv: bool = True,
        iv_threshold: float = 0.02,
        is_drop_importance: bool = True,
        importance_threshold: float = 0.95,
        is_feature_derive: bool = True,
        derive_n: int = 10,
        time_cost: bool = True
    ):
        """
        Parameters
        ----------
        is_drop_iv: bool
            是否删除低iv字段
        iv_threshold: float
            删除低iv字段阈值
        is_drop_importance: bool
            是否删除低重要性字段
        importance_threshold: float
            保留重要性超过importance_threshold的前k个字段
        is_feature_derive: bool
            是否进行字段衍生
        derive_n: int
            被衍生的字段个数
        """
        super().__init__(field_dict=field_dict, is_drop_corr=is_drop_corr, white_set=white_set,
                         label_first=label_first, info_first=info_first, corr=corr, time_cost=time_cost)
        self.is_drop_iv = is_drop_iv
        self.iv_threshold = iv_threshold
        self.is_drop_importance = is_drop_importance
        self.importance_threshold = importance_threshold
        self.is_feature_derive = is_feature_derive
        self.derive_n = derive_n
        self.col_iv_dict = None
        self.col_importance_dict = None
        self.drop_corr_list = []
        self.drop_iv_list = []
        self.drop_importance_list = []
        self.all_drop_col = []
        self.derive_list = []

    def fit(
            self,
            data: pd.DataFrame,
            label,
            is_drop_corr: bool = None,
            white_set: set = None,
            field_dict: dict = None,
            label_first: bool = None,
            info_first: bool = None,
            corr: float = None,
            is_drop_iv: bool = None,
            iv_threshold: float = None,
            is_drop_importance: bool = None,
            importance_threshold: float = None,
            is_feature_derive: bool = None,
            derive_n: int = None,
    ):
        self.reset_atr()
        self.is_drop_corr = self.is_drop_corr if is_drop_corr is None else is_drop_corr
        self.white_set = self.white_set if white_set is None else white_set
        self.field_dict = self.field_dict if field_dict is None else field_dict
        self.label_first = self.label_first if label_first is None else label_first
        self.info_first = self.info_first if info_first is None else info_first
        if self.label_first:
            self.info_first = False
        self.corr = self.corr if corr is None else corr
        self.is_drop_iv = self.is_drop_iv if is_drop_iv is None else is_drop_iv
        self.iv_threshold = self.iv_threshold if iv_threshold is None else iv_threshold
        self.is_drop_importance = self.is_drop_importance if is_drop_importance is None else is_drop_importance
        self.importance_threshold = self.importance_threshold if importance_threshold is None else importance_threshold
        self.is_feature_derive = self.is_feature_derive if is_feature_derive is None else is_feature_derive
        self.derive_n = self.derive_n if derive_n is None else derive_n
        data = copy.deepcopy(data)
        if self.is_drop_corr:
            print('----------\n 删除高度相关字段')
            self.drop_corr_list = self.drop_corr_col(data, label)
            data.drop(self.drop_corr_list, axis=1, inplace=True)
            self.all_drop_col.extend(self.drop_corr_list)
        if self.is_drop_iv:
            print('----------\n 删除低iv字段')
            self.drop_iv_list = self.drop_iv_col(data, label)
            data.drop(self.drop_iv_list, axis=1, inplace=True)
            self.all_drop_col.extend(self.drop_iv_list)
        if self.is_drop_importance:
            print('----------\n 删除低重要性字段')
            self.drop_importance_list = self.drop_importance_col(data, label)
            data.drop(self.drop_importance_list, axis=1, inplace=True)
            self.all_drop_col.extend(self.drop_importance_list)
        if self.is_feature_derive:
            print('----------\n 字段衍生')
            data, self.derive_list = self.feature_derive(data, label)
        return data

    def fit_transform(
        self,
        data: pd.DataFrame
    ):
        data = copy.deepcopy(data)
        data.drop(self.all_drop_col, axis=1, inplace=True)
        derive_dict = {}
        for derive in self.derive_list:
            col1, operator, col2 = derive
            if operator == '+':
                derive_dict[col1 + operator + col2] = data[col1] + data[col2]
            elif operator == '-':
                derive_dict[col1 + operator + col2] = data[col1] - data[col2]
            elif operator == '*':
                derive_dict[col1 + operator + col2] = data[col1] * data[col2]
            elif operator == '/':
                derive_dict[col1 + operator + col2] = divide(data[col1], data[col2], 0)
        derive_df = pd.DataFrame(derive_dict)
        derive_df.index = data.index
        data = pd.concat([data, derive_df], axis=1)
        return data

    def cal_iv_importance(
            self,
            data: pd.DataFrame,
            label: str,
            base: str = 'iv',
    ):
        if base == 'iv':
            col_iv_dict = {}
            for col in data.columns.drop(label):
                cross_df = pd.crosstab(data[col], data[label], margins=True)
                _, iv = cross_woe_iv(cross_df)
                col_iv_dict[col] = iv
            self.col_iv_dict = col_iv_dict
            return col_iv_dict
        if base == 'importance':
            x = data.drop(label, axis=1)
            weight = round(data[data[label] == 0][label].count() / data[data[label] == 1][label].count(), 3)
            forest = RandomForestClassifier(n_estimators=100, max_depth=8, n_jobs=-1,
                                            class_weight={0: 1, 1: weight}, random_state=1)
            forest.fit(x, data[label])
            fields = x.columns
            col_importance_dict = {}
            importance = forest.feature_importances_
            for i, field in enumerate(fields):
                col_importance_dict[field] = importance[i]
            self.col_importance_dict = col_importance_dict
            return col_importance_dict

    def drop_iv_col(
        self,
        data: pd.DataFrame,
        label: str,
    ):
        start = time.time()
        iv_keep = []
        iv_keep_name = []
        iv_drop = []
        iv_drop_name = []
        col_iv_dict = self.cal_iv_importance(data, label, base='iv')
        for k, v in col_iv_dict.items():
            if v < self.iv_threshold:
                _ = keep_drop_judge(self.white_set, self.field_dict, iv_drop, iv_drop_name, iv_keep, iv_keep_name, k)
        if iv_keep:
            if self.field_dict:
                df = pd.DataFrame(data={'field': iv_keep, 'name': iv_keep_name})
            else:
                df = pd.DataFrame(data={'field': iv_keep})
            print('iv小于给定的阈值但因在白名单内而被保留的字段:\n', df)
        if iv_drop:
            if self.field_dict:
                df = pd.DataFrame(data={'field': iv_drop, 'name': iv_drop_name})
            else:
                df = pd.DataFrame(data={'field': iv_drop})
            print('因iv小于给定的阈值而被舍弃的字段:\n', df)
        end = time.time()
        if self.time_cost:
            print('耗时:', round(end - start, 4))
        return iv_drop

    def drop_importance_col(
        self,
        data: pd.DataFrame,
        label: str
    ):
        start = time.time()
        importance_keep = []
        importance_keep_name = []
        col_importance_dict = self.cal_iv_importance(data, label, base='importance')
        sort_col_importance = sorted(col_importance_dict.items(), key=lambda x: x[1], reverse=True)
        importance_list = list(col_importance_dict.keys())  # 需要剔除的字段
        importance_threshold = self.importance_threshold
        for col in self.white_set:
            field_name = col if col not in self.field_dict else self.field_dict[col]
            importance_threshold -= col_importance_dict[col]
            importance_list.remove(col)
            importance_keep.append(col)
            importance_keep_name.append(field_name)
            if importance_threshold < 0:
                if importance_list:
                    df = pd.DataFrame(data={'field': importance_list})
                    if self.field_dict:
                        df['name'] = df['field'].map(lambda x: self.field_dict[x] if x in self.field_dict else x)
                    print('因重要性小于给定的阈值而被剔除的字段:\n', df)
                return importance_list
        for col, importance in sort_col_importance:
            if col in importance_keep:
                continue
            importance_threshold -= importance
            importance_list.remove(col)
            if importance_threshold < 0:
                break
        if importance_list:
            df = pd.DataFrame(data={'field': importance_list})
            if self.field_dict:
                df['name'] = df['field'].map(lambda x: self.field_dict[x] if x in self.field_dict else x)
            print('因重要性小于给定的阈值而被剔除的字段:\n', df)
        end = time.time()
        if self.time_cost:
            print('耗时:', round(end - start, 4))
        return importance_list

    def feature_derive(
            self,
            data: pd.DataFrame,
            label: str,
    ):
        n = data.shape[0]
        start = time.time()
        if self.corr_with_label is None:
            self.corr_with_label = self.col_label_corr(data, label)
        if self.col_importance_dict is None:
            self.col_importance_dict = self.cal_iv_importance(data, label, base='importance')
        sort_col_importance = sorted(self.col_importance_dict.items(), key=lambda x: x[1], reverse=True)
        derive_columns = []
        for filed in sort_col_importance:
            if filed[0] in self.drop_importance_list:
                continue
            judge = pd.value_counts(data[filed[0]]).iloc[:10].sum() / n
            if judge < 0.9:
                derive_columns.append(filed[0])
            if len(derive_columns) == self.derive_n:
                break
        derive_dict = {}
        derive_list = []
        for i in range(len(derive_columns)):
            for j in range(i+1, len(derive_columns)):
                # 衍生准则:
                # 1. 衍生字段iv值大于iv_阈值;
                # 2. 衍生字段与被衍生字段不高度相关;
                # 3. 衍生字段与label的相关性更高.
                judge = max(abs(self.corr_with_label[derive_columns[i]]), abs(self.corr_with_label[derive_columns[j]]))
                opt_col_i_j, derive_i_j = is_opt_derive(data, label, derive_columns[i], derive_columns[j], judge)
                derive_dict.update(opt_col_i_j)
                derive_list.extend(derive_i_j)
        derive_df = pd.DataFrame(derive_dict)
        derive_df.index = data.index
        data = pd.concat([data, derive_df], axis=1)
        end = time.time()
        if derive_dict:
            field = []
            name = []
            for col in derive_list:
                name0 = col[0] if col[0] not in self.field_dict else self.field_dict[col[0]]
                name1 = col[2] if col[2] not in self.field_dict else self.field_dict[col[2]]
                field.append(col[0]+col[1]+col[2])
                name.append(name0+col[1]+name1)
            if self.field_dict:
                df = pd.DataFrame(data={'field': field, 'name': name})
            else:
                df = pd.DataFrame(data={'field': field})
            print('衍生的字段:\n', df)
        if self.time_cost:
            print('耗时:', round(end - start, 4))
        return data, derive_list

    def reset_atr(self):
        self.col_iv_dict = None
        self.col_importance_dict = None
        self.drop_corr_list = []
        self.drop_iv_list = []
        self.drop_importance_list = []
        self.all_drop_col = []
        self.derive_list = []
