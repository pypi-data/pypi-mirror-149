
import re
import copy
import math
import pandas as pd
import time
from.function import is_number, col_is_number, keep_drop_judge

# 最高10类数量占比
top10_rate = 0.9
# 最少类别个数
min_type_number = 1
# 最小类别占比
min_type_rate = 0.6
# 最大类别个数
max_type_num = 30
# 最小判断是否为资产型数据所需行数
min_is_structure_nums = 10


def is_meaningless(
    col: str,
    meaningless_field: list = None,
) -> bool:
    """
    判断字段是否有意义
    """
    if meaningless_field is None:
        meaningless_field = ['id', 'nbr', 'date']
    for field in meaningless_field:
        if re.match('.*?'+field, col, re.I):
            return True
        return False


def is_assets(data: pd.Series) -> bool:
    """
    大致判断字段是否为资产型字段
    """
    indexes = data.value_counts().index[:min_is_structure_nums]
    for index in indexes:
        nums = re.findall(r'\d+', str(index))
        types = re.findall(r'[^\d]+', str(index))
        if len(types) < 2 or (len(nums) != len(types)):
            return False
    return True


def is_fill_with_others(data: pd.Series) -> bool:
    """
    如果数据本身不含0，不适合以0填充
    """
    return (data == 0).any()


def convert_sta(x):
    res = ''
    nums = re.findall(r'\d+', str(x))
    for num in nums:
        res += '无' if int(num) == 0 else '有'
    return res


def separate_convert(x, n):
    try:
        return float(re.findall(r'\d+', str(x))[n])
    except IndexError:
        return 0


def deal_with_structure(
    data: pd.DataFrame,
    col: str,
    convert_dict: dict,
    structure_copy: list,
    form: str = 'sum'
    ):
    """
    处理类似资产数据
    :param:
        form: str, default sum
            sum:求和
            separate: 划分成多个字段
            have: 换成有无再分类
    :return: pd.DataFrame or pd.Series
    """

    if form == 'sum':
        data[col] = data[col].map(lambda x: sum(list(map(int, re.findall(r'\d+', str(x))))))
        return
    s = str(data[col][data[col].first_valid_index()]).replace('+', '')
    types = re.findall(r'[^\d]+', s)
    if form == 'separate':
        structure_copy.append(col)
        for i in range(len(types)):
            if types[i] in set(data.columns):
                continue
            data[types[i]] = data[col].map(lambda x: separate_convert(x, i))
        return
    if form == 'have':
        data[col] = data[col].map(lambda x: convert_sta(x))
        all_types = pd.value_counts(data[col])
        type_dict = {}
        for i, kind in enumerate(all_types.index):
            type_dict[kind] = i
        data[col] = data[col].map(lambda x: type_dict[x] if x in type_dict else -1)
        convert_dict[col]['convert'] = type_dict


def text_deal_with_nan(
        data: pd.DataFrame,
        col_dict: dict,
):
    """
    如果训练集某字段不含有缺失值而测试集含有，则在测试集上对此字段单独填充
    """
    nan_col = data.isnull().any()
    col_index = nan_col[nan_col].index
    for col in col_index:
        if col in col_dict['num_col']:
            if is_fill_with_others(data[col]):
                data[col].fillna(0, inplace=True)
            else:
                data[col].fillna(data[col].median(), inplace=True)
        if (col in col_dict['to_cla_col']) or (col in col_dict['num_cla_col']):
            data[col].fillna(-1, inplace=True)
    return data


class DataPretreatment:
    """
    数据预处理，功能：
    缺失值统计
    字段类型识别
    字符转数字
    填补缺失值
    """

    def __init__(
            self,
            white_set: set = None,
            drop_col: list = None,
            field_dict: dict = None,
            start_num: int = 1,
            nan_rate: float = 0.3,
            meaningless_field: list = None,
            is_structure: bool = False,
            structure_list: list = None,
            form: str = 'sum',
            is_extreme: bool = True,
            lower: float = 0.01,
            upper: float = 0.99,
            time_cost: bool = True,
    ):
        """
        Parameters
        ----------
        white_set: set
            白名单
        drop_col: list
            黑名单
        field_dict: dict
            字段字典
        start_num: int
            类型变量编码以何值开始
        nan_rate: float
            舍弃缺失字段的阈值
        meaningless_field: list
            舍弃无意义字段所含有的字符(不区分大小写） example: id
        is_structure: bool
            是否处理资产结构数据
        structure_list: list
            资产结构字段
        form: str default sum
            处理资产结构数据形式
            sum:求和
            separate: 划分成多个字段
            have: 换成有无再分类
        is_extreme: bool
            是否处理极端值
        lower: float
            下限
        upper: float
            上限
        time_cost: bool
            是否显示耗时
        """
        if form not in {'sum', 'separate', 'have'}:
            raise ValueError('请在 sum, separate, have中选择一个')
        self.white_set = {} if white_set is None else white_set
        self.field_dict = {} if field_dict is None else field_dict
        self.start_num = start_num
        self.is_structure = is_structure
        self.structure_list = [] if structure_list is None else structure_list
        self.form = form
        self.is_extreme = is_extreme
        self.lower = lower
        self.upper = upper
        self.nan_rate = nan_rate
        self.meaningless_field = meaningless_field
        self.drop_col = [] if drop_col is None else drop_col
        self.col_dict = {
            'drop_col': copy.deepcopy(self.drop_col),
            'num_col': [],
            'num_cla_col': [],
            'to_cla_col': []
        }
        self.time_cost = time_cost
        self.structure_copy = copy.deepcopy(self.structure_list)
        self.nan_pd = None
        self.convert_dict = None
        self.fill_dict = None

    def fit(
            self,
            data: pd.DataFrame,
            label: str,
            white_set: set = None,
            field_dict: dict = None,
            drop_col: list = None,
            start_num: int = None,
            nan_rate: float = None,
            meaningless_field: list = None,
            is_structure: bool = None,
            structure_list: list = None,
            form: str = None,
            is_extreme: bool = None,
            lower: float = None,
            upper: float = None,
    ):
        """
        训练集上的预处理
        """
        self.white_set = self.white_set if white_set is None else white_set
        self.field_dict = self.field_dict if field_dict is None else field_dict
        self.drop_col = self.drop_col if drop_col is None else drop_col
        self.start_num = self.start_num if start_num is None else start_num
        self.nan_rate = self.nan_rate if nan_rate is None else nan_rate
        self.meaningless_field = self.meaningless_field if meaningless_field is None else meaningless_field
        self.is_structure = self.is_structure if is_structure is None else is_structure
        self.structure_list = self.structure_list if structure_list is None else structure_list
        self.form = self.form if form is None else form
        self.is_extreme = self.is_extreme if is_extreme is None else is_extreme
        self.lower = self.lower if lower is None else lower
        self.upper = self.upper if upper is None else upper
        self.reset_atr()
        data = copy.deepcopy(data)
        data.drop(self.drop_col, axis=1, inplace=True)
        print('统计缺失值')
        nan_pd, nan_drop_col = self.nan_statistic(data)
        self.nan_pd = nan_pd
        data.drop(nan_drop_col, axis=1, inplace=True)
        print('----------\n 字段类型识别')
        col_dict, identify_drop_col = self.identify_type(data, label)
        data.drop(identify_drop_col, axis=1, inplace=True)
        print('----------\n 类型字段转数值')
        convert_dict, data = self.str_to_number(data, label, col_dict=col_dict)
        data.drop(self.structure_copy, axis=1, inplace=True)
        print('----------\n 将obj字段转化为数值型')
        data = self.type_conversion(data)
        print('----------\n 填补缺失值')
        _, data = self.deal_with_nan(data, label, nan_pd=nan_pd, col_dict=col_dict)
        if self.is_extreme:
            print('----------\n 处理异常值')
            data = self.deal_with_extreme(data, label=label)
        return data

    def fit_transform(
            self,
            data: pd.DataFrame,
    ):
        """
        测试集上的预处理
        """
        data = copy.deepcopy(data)
        data.drop(self.col_dict['drop_col'], axis=1, inplace=True)
        print('类型字段转数值')
        data = self.str_to_number(data, '', convert_dict=self.convert_dict)
        data.drop(self.structure_copy, axis=1, inplace=True)
        print('填补缺失值')
        data = self.deal_with_nan(data, '', fill_dict=self.fill_dict)
        data = text_deal_with_nan(data, self.col_dict)
        if self.is_extreme:
            print('处理异常值')
            data = self.deal_with_extreme(data)
        return data

    def nan_statistic(
            self,
            data: pd.DataFrame,
    ) -> (pd.DataFrame, list):
        """
        统计缺失值总和及占比
        """
        start = time.time()
        n = data.shape[0]
        nan_pd = data.isnull().sum().to_frame().reset_index()
        nan_pd.columns = ['col', 'nan_count']
        nan_pd = nan_pd[nan_pd['nan_count'] != 0]
        nan_pd['nan_rate'] = (nan_pd.nan_count / n).map(lambda x: "%.2f%%" % (x * 100))
        min_nan_count = math.ceil(n * self.nan_rate)
        drop_col = (nan_pd[nan_pd['nan_count'] >= min_nan_count]['col']).to_list()
        keep = []
        drop = []
        keep_name = []
        drop_name = []
        for col in drop_col:
            _ = keep_drop_judge(self.white_set, self.field_dict, drop, drop_name, keep, keep_name, col)
        if keep:
            if self.field_dict:
                keep_df = pd.DataFrame(data={'field': keep, 'name': keep_name})
                print('含有过多的缺失值但因在白名单内而保留的字段:\n', keep_df)
            else:
                keep_df = pd.DataFrame(data={'field': keep})
                print('含有过多的缺失值但因在白名单内而保留的字段:\n', keep_df)
        if drop:
            if self.field_dict:
                drop_df = pd.DataFrame(data={'field': drop, 'name': drop_name})
                print('因过多的缺失值而被舍弃的字段:\n', drop_df)
            else:
                drop_df = pd.DataFrame(data={'field': drop})
                print('因过多的缺失值而被舍弃的字段:\n', drop_df)
        self.col_dict['drop_col'].extend(drop)
        end = time.time()
        if self.time_cost:
            print('耗时:', round(end - start, 4))
        return nan_pd, drop

    def identify_type(
            self,
            data: pd.DataFrame,
            label: str,
    ) -> (dict, list):
        """
        字段类型识别
        drop_col : 无用字段
        num_col : DataFrame中类别为数值类型的字段
        num_cla_col : 数值型类别字段
        to_cla_col : 类别字段，可做编码或one-hot
        """
        start = time.time()
        meaningless_drop = []
        meaningless_drop_name = []
        low_kind_drop = []
        low_kind_drop_name = []
        meaningless_keep = []
        meaningless_keep_name = []
        low_kind_keep = []
        low_kind_keep_name = []
        multi_kind_drop = []
        multi_kind_drop_name = []
        multi_kind_keep = []
        multi_kind_keep_name = []
        drop_col = []
        n = data.shape[0]
        for col in data.columns.drop(label):
            if col in self.col_dict['drop_col']:
                continue
            if is_meaningless(col, meaningless_field=self.meaningless_field):
                is_continue = keep_drop_judge(self.white_set, self.field_dict, meaningless_drop, meaningless_drop_name,
                                              meaningless_keep, meaningless_keep_name, col)
                if is_continue:
                    continue
            judge = pd.value_counts(data[col]).iloc[:10].sum() / n
            if col_is_number(data, col):
                if judge < top10_rate:
                    self.col_dict['num_col'].append(col)
                    continue
                judge2 = len(pd.value_counts(data[col]))
                if judge2 == min_type_number:
                    is_continue = keep_drop_judge(self.white_set, self.field_dict, low_kind_drop, low_kind_drop_name,
                                                  low_kind_keep, low_kind_keep_name, col)
                    if is_continue:
                        continue
                if judge2 > max_type_num:
                    self.col_dict['to_cla_col'].append(col)
                    continue
                self.col_dict['num_cla_col'].append(col)
                continue
            judge2 = len(pd.value_counts(data[col]))
            if judge2 == min_type_number:
                is_continue = keep_drop_judge(self.white_set, self.field_dict, low_kind_drop, low_kind_drop_name,
                                              low_kind_keep, low_kind_keep_name, col)
                if is_continue:
                    continue
            if judge < min_type_rate and judge2 > max_type_num:
                is_continue = keep_drop_judge(self.white_set, self.field_dict, multi_kind_drop, multi_kind_drop_name,
                                              multi_kind_keep, multi_kind_keep_name, col)
                if is_continue:
                    continue
            self.col_dict['to_cla_col'].append(col)
        if meaningless_keep:
            if self.field_dict:
                df = pd.DataFrame(data={'field': meaningless_keep, 'name': meaningless_keep_name})
            else:
                df = pd.DataFrame(data={'field': meaningless_keep})
            print('无意义但因白名单而保留的字段:\n', df)
        if low_kind_keep:
            if self.field_dict:
                df = pd.DataFrame(data={'field': low_kind_keep, 'name': low_kind_keep_name})
            else:
                df = pd.DataFrame(data={'field': low_kind_keep})
            print('过少种类但因白名单而保留的字段:\n', df)
        if multi_kind_keep:
            if self.field_dict:
                df = pd.DataFrame(data={'field': multi_kind_keep, 'name': multi_kind_keep_name})
            else:
                df = pd.DataFrame(data={'field': multi_kind_keep})
            print('过多种类且不集中但因白名单而保留的字段:\n', df)
        if meaningless_drop:
            if self.field_dict:
                df = pd.DataFrame(data={'field': meaningless_drop, 'name': meaningless_drop_name})
            else:
                df = pd.DataFrame(data={'field': meaningless_drop})
            print('因无意义而舍弃的字段:\n', df)
        if low_kind_drop:
            if self.field_dict:
                df = pd.DataFrame(data={'field': low_kind_drop, 'name': low_kind_drop_name})
            else:
                df = pd.DataFrame(data={'field': low_kind_drop})
            print('因过少的种类而舍弃的字段:\n', df)
        if multi_kind_drop:
            if self.field_dict:
                df = pd.DataFrame(data={'field': multi_kind_drop, 'name': multi_kind_drop_name})
            else:
                df = pd.DataFrame(data={'field': multi_kind_drop})
            print('因种类过多且不集中而被舍弃的字段:\n', df)
        drop_col.extend(meaningless_drop)
        drop_col.extend(low_kind_drop)
        drop_col.extend(multi_kind_drop)
        self.col_dict['drop_col'].extend(drop_col)
        end = time.time()
        if self.time_cost:
            print('耗时:', round(end - start, 4))
        return self.col_dict, drop_col

    def str_to_number(
            self,
            data: pd.DataFrame,
            label: str,
            col_dict: dict = None,
            convert_dict: dict = None,
    ) -> (dict, pd.DataFrame):
        """
        在调用identify_type方法后调用此方法将字符型变量转化为数值型变量
        :param:
        data: pd.DataFrame
            传入的data
        convert_dict: dict
            自定义映射关系，在测试集上使用
        """
        start = time.time()
        if col_dict is None and convert_dict is None:
            col_dict, _ = self.identify_type(data, label)
        data = copy.deepcopy(data)
        if convert_dict is not None:
            for k, v in convert_dict.items():
                if 'is_assets' in v:
                    form = v['is_assets']
                    if form == 'have':
                        data[k] = data[k].map(lambda x: convert_sta(x))
                        data[k] = data[k].map(v['convert'])
                        continue
                    deal_with_structure(data, k, {}, [], form)
                    continue
                data[k] = data[k].map(lambda x: v[x] if x in v else -1)
            return data
        convert_dict = {}
        for col in col_dict['to_cla_col']:
            if self.is_structure:
                if len(self.structure_list) == 0:
                    if is_assets(data[col]):
                        convert_dict[col] = {'is_assets': self.form}
                        deal_with_structure(data, col, convert_dict, self.structure_copy, self.form)
                        continue
                else:
                    if col in self.structure_list:
                        convert_dict[col] = {'is_assets': self.form}
                        deal_with_structure(data, col, convert_dict, self.structure_copy, self.form)
                        continue
            all_types = pd.value_counts(data[col]).iloc[:max_type_num]
            type_dict = {}
            for i, col_name in enumerate(all_types.index):
                type_dict[col_name] = self.start_num + i
                convert_dict[col] = type_dict
            data[col] = data[col].map(lambda x: type_dict[x] if x in type_dict else 31)
        self.convert_dict = convert_dict
        end = time.time()
        if self.time_cost:
            print('耗时:', round(end - start, 4))
        return convert_dict, data

    def deal_with_nan(
            self,
            data: pd.DataFrame,
            label: str,
            nan_pd: pd.DataFrame = None,
            col_dict: dict = None,
            fill_dict: dict = None,
    ) -> (dict, pd.DataFrame):
        """
        自动填补缺失值
        对于数值型变量以0填充
        对于类型变量以-1填充
        如果字段本身不含0，则以中位数填充
        """
        if fill_dict is None:
            if nan_pd is None:
                nan_pd, _ = self.nan_statistic(data)
            if col_dict is None:
                col_dict, _ = self.identify_type(data, label)
        start = time.time()
        if fill_dict is not None:
            for k, v in fill_dict.items():
                if k == 'others':
                    for col in v:
                        data[col].fillna(data[col].median(), inplace=True)
                else:
                    for col in v:
                        data[col].fillna(k, inplace=True)
            return data
        fill_dict = {0: [], -1: [], 'others': []}
        data = copy.deepcopy(data)
        fill_col = nan_pd['col']
        for col in fill_col:
            if col in col_dict['drop_col']:
                continue
            if col in col_dict['num_col']:
                if is_fill_with_others(data[col]):
                    fill_dict[0].append(col)
                    data[col].fillna(0, inplace=True)
                else:
                    fill_dict['others'].append(col)
                    data[col].fillna(data[col].median(), inplace=True)
            if (col in col_dict['to_cla_col']) or (col in col_dict['num_cla_col']):
                fill_dict[-1].append(col)
                data[col].fillna(-1, inplace=True)
        self.fill_dict = fill_dict
        end = time.time()
        if self.time_cost:
            print('耗时:', round(end - start, 4))
        return fill_dict, data

    def deal_with_extreme(
            self,
            data: pd.DataFrame,
            label: str = None
    ):
        start = time.time()
        data = copy.deepcopy(data)
        cols = data.columns
        if label is not None:
            cols = cols.drop(label)
        for col in cols:
            a = data[col].quantile(self.lower)
            b = data[col].quantile(self.upper)
            data[col] = data[col].map(lambda x: b if x > b else a if x < a else x)
        end = time.time()
        if self.time_cost:
            print('耗时:', round(end - start, 4))
        return data

    def type_conversion(
            self,
            data: pd.DataFrame,
    ):
        """
        将obj类型字段转化为数值
        """
        start = time.time()
        obj_col = data.select_dtypes(include=['object']).columns
        for col in obj_col:
            try:
                data[col] = data[col].astype(float)
            except ValueError:
                unique_kind = data[col].unique()
                type_dict = {}
                obj_list = []
                for kind in unique_kind:
                    if pd.isnull(kind):
                        continue
                    if is_number(str(kind)):
                        type_dict[kind] = float(kind)
                    else:
                        obj_list.append(kind)
                if type_dict:
                    max_num = max(type_dict.values()) + 1
                else:
                    max_num = 1
                for obj in obj_list:
                    type_dict[obj] = max_num
                    max_num += 1
                self.convert_dict[col] = type_dict
                data[col] = data[col].map(type_dict)
        end = time.time()
        if self.time_cost:
            print('耗时:', round(end - start, 4))
        return data

    def reset_atr(self):
        """
        重置对象属性
        """
        self.structure_copy = copy.deepcopy(self.structure_list)
        self.col_dict = {
            'drop_col': copy.deepcopy(self.drop_col),
            'num_col': [],
            'num_cla_col': [],
            'to_cla_col': []
        }
        self.nan_pd = None
        self.convert_dict = None
        self.fill_dict = None
