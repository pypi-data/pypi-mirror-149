
import time
import numpy as np
from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix, f1_score
import lightgbm as lgb
import xgboost as xgb
try:
    from sklearn.externals import joblib
except ImportError:
    import joblib
# from .function import rfc_2d_section


version = lgb.__version__
model_name = {'RF': {'RFC', 'RF', 'rf', 'rfc', 'RandomForestClassifier'},
              'LGB': {'LGB', 'lgb', 'Lgb', 'lightgbm'},
              'XGB': {'XGB', 'xgb', 'xgboost'}}
train_test_split_params = {'test_size', 'train_size', 'random_state', 'shuffle', 'stratify'}


def adjust_num_leaves(fitting, num_leaves):
    if fitting <= 0.005:
        num_leaves += 4
    elif 0.005 < fitting <= 0.01:
        num_leaves += 3
    elif 0.01 < fitting <= 0.015:
        num_leaves += 2
    elif 0.015 < fitting <= 0.02:
        num_leaves += 1
    elif fitting > 0.02:
        if num_leaves < 3:
            return 2
        else:
            num_leaves -= 1
    return num_leaves


def function():
    pass


def rfc_model_importance(x_train, x_val, y_train, y_val, max_depth, weight):
    model = RandomForestClassifier(n_jobs=-1, class_weight={0: 1, 1: weight},
                                   n_estimators=100, max_depth=max_depth, random_state=1)
    model.fit(x_train, y_train)
    pre_train = model.predict(x_train)
    pre_val = model.predict(x_val)
    feature_importance = pd.DataFrame(data={
        'feature_names': x_train.columns, 'importance': model.feature_importances_.round(4)})
    feature_importance = feature_importance.sort_values('importance', ascending=False)
    print(confusion_matrix(y_train, pre_train))
    print(classification_report(y_train, pre_train, digits=4))
    print('在训练集下的精度为：', accuracy_score(y_train, pre_train))
    print('=' * 55)
    print(confusion_matrix(y_val, pre_val))
    print(classification_report(y_val, pre_val, digits=4))
    print('在验证集下的精度为：', accuracy_score(y_val, pre_val))
    return model, feature_importance


def lgb_init(x_train, x_val, y_train, y_val, num_leaves, weight, epoch,
             early_stopping, is_evaluate, evaluate_func):
    train_data = lgb.Dataset(x_train, y_train)
    val_data = lgb.Dataset(x_val, y_val)
    metric = 'auc' if not is_evaluate else 'None'
    lgb_params = {
        'num_leaves': num_leaves,
        'min_data_in_leaf': 23,
        'objective': 'binary',
        'learning_rate': 0.01,
        "feature_fraction": 0.9,
        "bagging_freq": 1,
        "bagging_fraction": 0.9,
        "bagging_seed": 11,
        "metric": metric,
        "lambda_l1": 0.1,
        "verbosity": -1,
        "num_threads": 8,
        "scale_pos_weight": weight,
        "random_state": 1}
    if is_evaluate:
        if evaluate_func is None:
            def lgb_evaluate_func(pre, train):
                labels = train.get_label()
                pre = np.where(pre >= 0.5, 1, 0)
                return 'f1_score', f1_score(pre, labels), True
        else:
            lgb_evaluate_func = evaluate_func
        if version >= '3.3.0':
            callbacks = [lgb.early_stopping(early_stopping)]
            model = lgb.train(lgb_params, train_data, epoch, valid_sets=[train_data, val_data],
                              feval=lgb_evaluate_func, callbacks=callbacks)
        else:
            model = lgb.train(lgb_params, train_data, epoch, valid_sets=[train_data, val_data],
                              feval=lgb_evaluate_func, early_stopping_rounds=early_stopping, verbose_eval=False)
    else:
        if version >= '3.3.0':
            callbacks = [lgb.early_stopping(early_stopping)]
            model = lgb.train(lgb_params, train_data, epoch, valid_sets=[train_data, val_data],
                              callbacks=callbacks)
        else:
            model = lgb.train(lgb_params, train_data, epoch, valid_sets=[train_data, val_data],
                              early_stopping_rounds=early_stopping, verbose_eval=False)
    return model


def xgb_init(x_train, x_val, y_train, y_val, max_depth, weight, epoch,
             early_stopping, is_evaluate, evaluate_func):
    train_data = xgb.DMatrix(x_train, y_train)
    val_data = xgb.DMatrix(x_val, y_val)
    watchlist = [(train_data, 'train'), (val_data, 'valid_data')]
    xgb_params = {'eta': 0.02,
                  'max_depth': max_depth,
                  'subsample': 0.8,
                  'colsample_bytree': 0.8,
                  'nthread': 8,
                  'objective': 'reg:logistic',
                  'eval_metric': 'auc',
                  'scale_pos_weight': weight
                  }
    if is_evaluate:
        if evaluate_func is None:
            def xgb_evaluate_func(pre, train):
                labels = train.get_label()
                pre = np.where(pre >= 0.5, 1, 0)
                score = f1_score(pre, labels)
                return '1-f1_score', 1 - score  # xgb目标是将目标指标降
        else:
            xgb_evaluate_func = evaluate_func
        model = xgb.train(dtrain=train_data, num_boost_round=epoch, evals=watchlist, verbose_eval=False,
                          early_stopping_rounds=early_stopping, params=xgb_params, feval=xgb_evaluate_func)
    else:
        model = xgb.train(dtrain=train_data, num_boost_round=epoch, evals=watchlist, verbose_eval=False,
                          early_stopping_rounds=early_stopping, params=xgb_params)
    return model, train_data, val_data


def rfc_cal_fitting(x_train, x_val, y_train, y_val, max_depth, weight):
    model = RandomForestClassifier(n_jobs=-1, class_weight={0: 1, 1: weight}, n_estimators=100,
                                   max_depth=max_depth, random_state=1)
    model.fit(x_train, y_train)
    pre_train = model.predict(x_train)
    pre_val = model.predict(x_val)
    matrix = confusion_matrix(y_train, pre_train)
    if matrix[1, 1] == 0:
        recall = 0
        precision = 1
    else:
        precision = matrix[1, 1] / (matrix[1, 1] + matrix[0, 1])
        recall = matrix[1, 1] / (matrix[1, 1] + matrix[1, 0])
    train_f1 = f1_score(y_train, pre_train)
    val_f1 = f1_score(y_val, pre_val)
    return recall - precision, train_f1 - val_f1


def rfc_adjust_parameter(x_train, x_val, y_train, y_val, max_depth, weight, balance, fitting, parameter_dict=None):
    # 如果下一组参数已计算过，则返回这组参数
    if parameter_dict is None:
        parameter_dict = {}
    if (max_depth, weight) in parameter_dict:
        print('因重复参数而停止调参')
        opt_num_leaves = max_depth
        opt_weight = weight
        opt_fitting = 0
        for k, v in parameter_dict.items():
            if abs(v[0]) <= 0.1 and v[1] < 0.03:
                if v[1] > opt_fitting:
                    opt_fitting = v[1]
                    opt_num_leaves = k[0]
                    opt_weight = k[1]
        return opt_num_leaves, opt_weight
    parameter_dict[(max_depth, weight)] = (balance, fitting)
    if (abs(balance) <= 0.1) and (fitting >= 0.02) and (fitting <= 0.03):
        return max_depth, weight
    if fitting < 0.02 or fitting > 0.03:
        if balance != -1:
            if fitting < 0.02:
                max_depth += 1
            if fitting > 0.03:
                if max_depth == 1:
                    return max_depth, weight
                max_depth -= 1
        if balance < -0.1:
            weight += 0.5
        if balance > 0.1:
            weight -= 0.5
        balance, fitting = rfc_cal_fitting(x_train, x_val, y_train, y_val, max_depth, weight)
        print('----------\n max_depth: %d, weight: %s, 召回-精度: %s, 验证f1-训练f1: %s' %
              (max_depth, round(weight, 1), round(balance, 4), round(fitting, 4)))
        return rfc_adjust_parameter(x_train, x_val, y_train, y_val, max_depth, weight,
                                    balance, fitting, parameter_dict)
    if balance < -0.1 or balance > 0.1:
        if balance < -0.1:
            weight += 0.5
        if balance > 0.1:
            weight -= 0.5
        if balance != -1:
            if fitting < 0.02:
                max_depth += 1
            if fitting > 0.03:
                if max_depth == 1:
                    return max_depth, weight
                max_depth -= 1
        balance, fitting = rfc_cal_fitting(x_train, x_val, y_train, y_val, max_depth, weight)
        print('----------\n max_depth: %d, weight: %s, balance: %s, fitting: %s' %
              (max_depth, round(weight, 1), round(balance, 4), round(fitting, 4)))
        return rfc_adjust_parameter(x_train, x_val, y_train, y_val, max_depth, weight,
                                    balance, fitting, parameter_dict)


def get_rfc_score(
    x_train: pd.DataFrame,
    x_val: pd.DataFrame,
    y_train: pd.Series,
    y_val: pd.Series,
    max_depth: int,
    weight: float,
):
    model = RandomForestClassifier(n_jobs=-1, class_weight={0: 1, 1: weight},
                                   n_estimators=150, max_depth=max_depth, random_state=1)
    model.fit(x_train, y_train)
    pre_val = model.predict(x_val)
    score = f1_score(y_val, pre_val)
    return score


class ModelBuild:
    """
    划分数据集
    拟合rf、lgb、xgb模型
    自动调参
    测试集预测
    """

    def __init__(
            self,
            baseline: str = 'RF',
            max_depth: int = None,
            weight: float = None,
            lgb_params: dict = None,
            xgb_params: dict = None,
            early_stopping: int = 200,
            verbose: int = 100,
            epoch: int = 4000,
            is_evaluate: bool = False,
            evaluate_func: function = None,
            is_adjust_parameter: bool = False,
            # max_depth_range: list = None,
            # num_leaves_range: list = None,
            # weight_range: list = None,
            time_cost: bool = True,
            **kwargs
    ):
        """
        Parameters
        ----------
        baseline: str
            基模型类型
        max_depth: int
            最大树深
        weight: float
            权重
        lgb_params: dict
            lgb参数
        xgb_params: dict
            xgb参数
        early_stopping: int
            验证集early_stopping轮不提升则停止训练
        verbose: int
            lgb与xgb显示verbose轮训练结果
        epoch: int
            lgb与xgb训练的轮数
        is_evaluate: bool
            是否采用评价函数
        evaluate_func: function
            采用评价函数的具体函数
        is_adjust_parameter: bool
            是否自动调参
        time_cost:
            是否显示耗时
        kwargs:
            train_test_split内的参数
        """
        self.baseline = baseline
        self.max_depth = max_depth
        self.weight = weight
        self.lgb_params = lgb_params
        self.xgb_params = xgb_params
        self.early_stopping = early_stopping
        self.verbose = verbose
        self.epoch = epoch
        self.is_evaluate = is_evaluate
        self.evaluate_func = evaluate_func
        self.is_adjust_parameter = is_adjust_parameter
        self.time_cost = time_cost
        if 'random_state' not in kwargs:
            kwargs['random_state'] = 1
        for k, v in kwargs.items():
            if k not in train_test_split_params:
                raise ValueError('未知参数:%s' % k)
        self.kwargs = kwargs
        self.rfc_model = None
        self.lgb_model = None
        self.xgb_model = None

    def fit(
            self,
            data: pd.DataFrame,
            label: str,
            baseline: str = None,
            max_depth: int = None,
            weight: float = None,
            lgb_params: dict = None,
            xgb_params: dict = None,
            early_stopping: int = None,
            verbose: int = None,
            epoch: int = None,
            is_evaluate: bool = None,
            evaluate_func: function = None,
            is_adjust_parameter: bool = None,
            **kwargs
    ):
        self.baseline = self.baseline if baseline is None else baseline
        self.max_depth = self.max_depth if max_depth is None else max_depth
        self.weight = self.weight if weight is None else weight
        self.lgb_params = self.lgb_params if lgb_params is None else lgb_params
        self.xgb_params = self.xgb_params if xgb_params is None else xgb_params
        self.early_stopping = self.early_stopping if early_stopping is None else early_stopping
        self.verbose = self.verbose if verbose is None else verbose
        self.epoch = self.epoch if epoch is None else epoch
        self.is_evaluate = self.is_evaluate if is_evaluate is None else is_evaluate
        self.evaluate_func = self.evaluate_func if evaluate_func is None else evaluate_func
        self.is_adjust_parameter = self.is_adjust_parameter if is_adjust_parameter is None else is_adjust_parameter
        self.kwargs = self.kwargs if kwargs is None else kwargs
        if self.baseline in model_name['RF']:
            if not self.is_adjust_parameter:
                self.rfc_model, importance = self.rfc_fit(data, label)
            else:
                self.rfc_model, importance = self.rfc_auto_adjust_parameter(data, label)
            return self.rfc_model, importance
        if self.baseline in model_name['LGB']:
            if not self.is_adjust_parameter:
                self.lgb_model, importance = self.lgb_fit(data, label)
            else:
                self.lgb_model, importance = self.lgb_auto_adjust_parameter(data, label)
            return self.lgb_model, importance
        if self.baseline in model_name['XGB']:
            if not self.is_adjust_parameter:
                self.xgb_model, importance = self.xgb_fit(data, label)
            else:
                self.xgb_model, importance = self.xgb_auto_adjust_parameter(data, label)
            return self.xgb_model, importance

    def fit_transform(
        self,
        data: pd.DataFrame,
    ):
        pre = None
        if self.baseline in model_name['RF']:
            pre = self.rfc_model.predict(data)
        elif self.baseline in model_name['LGB']:
            pre = self.lgb_model.predict(data)
            pre = np.where(pre > 0.5, 1, 0)
        elif self.baseline in model_name['XGB']:
            pre = self.xgb_model.predict(data)
            pre = np.where(pre > 0.5, 1, 0)
        pre = pd.Series(pre)
        pre.index = data.index
        pre_df = pd.concat([data, pd.DataFrame(data={'pre': pre})], axis=1)
        return pre_df

    def train_test_split(
            self,
            data,
            label,
    ):
        x_train, x_val, y_train, y_val = train_test_split(
            data.drop(label, axis=1, inplace=False), data[label], **self.kwargs)
        return x_train, x_val, y_train, y_val

    def rfc_fit(
        self,
        data: pd.DataFrame,
        label: str
    ):
        x_train, x_val, y_train, y_val = self.train_test_split(data, label)
        max_depth = 8 if self.max_depth is None else self.max_depth
        if self.weight is None:
            weight = round(data[data[label] == 0][label].count() / data[data[label] == 1][label].count(), 3)
        else:
            weight = self.weight
        model, feature_importance = rfc_model_importance(x_train, x_val, y_train, y_val, max_depth, weight)
        return model, feature_importance

    def rfc_auto_adjust_parameter(
            self,
            data: pd.DataFrame,
            label: str
    ):
        start = time.time()
        x_train, x_val, y_train, y_val = self.train_test_split(data, label)
        balance, fitting = rfc_cal_fitting(x_train, x_val, y_train, y_val, 1, 1)
        print('----------\n max_depth: %d, weight: %s, 召回-精度: %s, 验证f1-训练f1: %s' %
              (1, 1, round(balance, 4), round(fitting, 4)))
        max_depth, weight = rfc_adjust_parameter(x_train, x_val, y_train, y_val, 1, 1, balance, fitting)
        print('最终max_depth: %s, 最终weight: %s' % (max_depth, weight))
        model, feature_importance = rfc_model_importance(x_train, x_val, y_train, y_val, max_depth, weight)
        end = time.time()
        if self.time_cost:
            print('耗时:', round(end - start, 4))
        return model, feature_importance

    # def rfc_param_search(
    #     self,
    #     data: pd.DataFrame,
    #     label: str
    # ):
    #     start = time.time()
    #     max_depth_range = [1, 10] if self.max_depth_range is None else self.max_depth_range
    #     weight_range = [0, 10] if self.weight_range is None else self.weight_range
    #     opt_depth, opt_weight, opt_score = rfc_2d_section(data, label, max_depth_range, weight_range, 0.38197,
    #                                                       self.get_rfc_score)
    #     end = time.time()
    #     if self.time_cost:
    #         print('耗时:', round(end - start, 4))
    #     return opt_depth, opt_weight

    def lgb_fit(
            self,
            data: pd.DataFrame,
            label: str,
    ):
        x_train, x_val, y_train, y_val = self.train_test_split(data, label)
        train_data = lgb.Dataset(x_train, y_train)
        val_data = lgb.Dataset(x_val, y_val)
        if self.lgb_params is None:
            scale_pos_weight = round(data[data[label] == 0][label].count() / data[data[label] == 1][label].count(), 3)
            metric = 'auc' if not self.is_evaluate else 'None'
            lgb_params = {
                'num_leaves': 31,
                'min_data_in_leaf': 23,
                'objective': 'binary',
                'learning_rate': 0.01,
                "feature_fraction": 0.9,
                "bagging_freq": 1,
                "bagging_fraction": 0.9,
                "bagging_seed": 11,
                "metric": metric,
                "lambda_l1": 0.1,
                "verbosity": -1,
                "num_threads": 8,
                "scale_pos_weight": scale_pos_weight,
                "random_state": 1}
        else:
            lgb_params = self.lgb_params
        if self.is_evaluate:
            if self.evaluate_func is None:
                def lgb_evaluate_func(pre, train):
                    labels = train.get_label()
                    pre = np.where(pre >= 0.5, 1, 0)
                    return 'f1_score', f1_score(pre, labels), True
            else:
                lgb_evaluate_func = self.evaluate_func
            if version >= '3.3.0':
                callbacks = [lgb.early_stopping(self.early_stopping), lgb.log_evaluation(self.verbose)]
                model = lgb.train(lgb_params, train_data, self.epoch, valid_sets=[train_data, val_data],
                                  feval=lgb_evaluate_func, callbacks=callbacks)
            else:
                model = lgb.train(lgb_params, train_data, self.epoch, valid_sets=[train_data, val_data],
                                  feval=lgb_evaluate_func, early_stopping_rounds=self.early_stopping,
                                  verbose_eval=self.verbose)
        else:
            if version >= '3.3.0':
                callbacks = [lgb.early_stopping(self.early_stopping), lgb.log_evaluation(self.verbose)]
                model = lgb.train(lgb_params, train_data, self.epoch, valid_sets=[train_data, val_data],
                                  callbacks=callbacks)
            else:
                model = lgb.train(lgb_params, train_data, self.epoch, valid_sets=[train_data, val_data],
                                  early_stopping_rounds=self.early_stopping, verbose_eval=self.verbose)
        importance = model.feature_importance() / (model.feature_importance().sum())
        importance = pd.DataFrame(data={'feature_names': x_train.columns, 'importance': importance.round(4)})
        importance = importance.sort_values('importance', ascending=False)
        pre_train = model.predict(x_train)
        pre_val = model.predict(x_val)
        pre_train = np.where(pre_train >= 0.5, 1, 0)
        pre_val = np.where(pre_val >= 0.5, 1, 0)
        print(confusion_matrix(y_train, pre_train))
        print(classification_report(y_train, pre_train, digits=4))
        print('在训练集下的精度为：', accuracy_score(y_train, pre_train))
        print('=' * 55)
        print(confusion_matrix(y_val, pre_val))
        print(classification_report(y_val, pre_val, digits=4))
        print('在验证集下的精度为：', accuracy_score(y_val, pre_val))
        return model, importance

    def lgb_cal_fitting(
            self,
            x_train,
            x_val,
            y_train,
            y_val,
            num_leaves,
            weight
    ):
        model = lgb_init(x_train, x_val, y_train, y_val, num_leaves, weight,
                         self.epoch, self.early_stopping, self.is_evaluate, self.evaluate_func)
        pre_train = model.predict(x_train)
        pre_val = model.predict(x_val)
        pre_train = np.where(pre_train >= 0.5, 1, 0)
        pre_val = np.where(pre_val >= 0.5, 1, 0)
        matrix = confusion_matrix(y_train, pre_train)
        if matrix[1, 1] == 0:
            recall = 0
            precision = 1
        else:
            precision = matrix[1, 1] / (matrix[1, 1] + matrix[0, 1])
            recall = matrix[1, 1] / (matrix[1, 1] + matrix[1, 0])
        train_f1 = f1_score(y_train, pre_train)
        val_f1 = f1_score(y_val, pre_val)
        return recall - precision, train_f1 - val_f1

    def lgb_adjust_parameter(self,
                             x_train, x_val, y_train, y_val, num_leaves, weight, balance, fitting, parameter_dict=None):
        # 如果下一组参数已计算过，则返回这组参数
        if parameter_dict is None:
            parameter_dict = {}
        if (num_leaves, weight) in parameter_dict:
            print('因重复参数而停止调参')
            opt_num_leaves = num_leaves
            opt_weight = weight
            opt_fitting = 0
            for k, v in parameter_dict.items():
                if abs(v[0]) <= 0.1 and v[1] < 0.03:
                    if v[1] > opt_fitting:
                        opt_fitting = v[1]
                        opt_num_leaves = k[0]
                        opt_weight = k[1]
            return opt_num_leaves, opt_weight
        parameter_dict[(num_leaves, weight)] = (balance, fitting)
        if (abs(balance) <= 0.1) and (fitting >= 0.02) and (fitting <= 0.03):
            return num_leaves, weight
        if fitting < 0.02 or fitting > 0.03:
            if balance != -1:
                num_leaves = adjust_num_leaves(fitting, num_leaves)
            if num_leaves == 1:
                return num_leaves, weight
            if balance < -0.1:
                weight += 0.5
            if balance > 0.1:
                weight -= 0.5
            balance, fitting = self.lgb_cal_fitting(x_train, x_val, y_train, y_val, num_leaves, weight)
            print('----------\n num_leaves: %d, weight: %s, 召回-精度: %s, 验证f1-训练f1: %s' %
                  (num_leaves, round(weight, 1), round(balance, 4), round(fitting, 4)))
            return self.lgb_adjust_parameter(x_train, x_val, y_train, y_val, num_leaves, weight, balance, fitting,
                                             parameter_dict)
        if balance < -0.1 or balance > 0.1:
            if balance < -0.1:
                weight += 0.5
            if balance > 0.1:
                weight -= 0.5
            if balance != -1:
                num_leaves = adjust_num_leaves(fitting, num_leaves)
            if num_leaves == 1:
                return num_leaves, weight
            balance, fitting = self.lgb_cal_fitting(x_train, x_val, y_train, y_val, num_leaves, weight)
            print('----------\n num_leaves: %d, weight: %s, 召回-精度: %s, 验证f1-训练f1: %s' %
                  (num_leaves, round(weight, 1), round(balance, 4), round(fitting, 4)))
            return self.lgb_adjust_parameter(x_train, x_val, y_train, y_val, num_leaves, weight, balance, fitting,
                                             parameter_dict)

    def lgb_auto_adjust_parameter(
            self,
            data: pd.DataFrame,
            label: str
    ):
        start = time.time()
        x_train, x_val, y_train, y_val = self.train_test_split(data, label)
        balance, fitting = self.lgb_cal_fitting(x_train, x_val, y_train, y_val, 10, 1)
        print('----------\n num_leaves: %d, weight: %s, 召回-精度: %s, 验证f1-训练f1: %s' %
              (10, 1, round(balance, 4), round(fitting, 4)))
        num_leaves, weight = self.lgb_adjust_parameter(x_train, x_val, y_train, y_val, 10, 1, balance, fitting)
        print('最终num_leaves: %s, 最终weight: %s' % (num_leaves, weight))
        model = lgb_init(x_train, x_val, y_train, y_val, num_leaves, weight,
                         self.epoch, self.early_stopping, self.is_evaluate, self.evaluate_func)
        importance = model.feature_importance() / (model.feature_importance().sum())
        importance = pd.DataFrame(data={'feature_names': x_train.columns, 'importance': importance.round(4)})
        importance = importance.sort_values('importance', ascending=False)
        pre_train = model.predict(x_train)
        pre_val = model.predict(x_val)
        pre_train = np.where(pre_train >= 0.5, 1, 0)
        pre_val = np.where(pre_val >= 0.5, 1, 0)
        print(confusion_matrix(y_train, pre_train))
        print(classification_report(y_train, pre_train, digits=4))
        print('在训练集下的精度为：', accuracy_score(y_train, pre_train))
        print('=' * 55)
        print(confusion_matrix(y_val, pre_val))
        print(classification_report(y_val, pre_val, digits=4))
        print('在验证集下的精度为：', accuracy_score(y_val, pre_val))
        end = time.time()
        if self.time_cost:
            print('耗时:', round(end - start, 4))
        return model, importance

    # def get_lgb_score(
    #     self,
    #     x_train: pd.DataFrame,
    #     x_val: pd.DataFrame,
    #     y_train: pd.Series,
    #     y_val: pd.Series,
    #     num_leaves: int,
    #     weight: float
    # ):
    #     model = lgb_init(x_train, x_val, y_train, y_val, num_leaves, weight,
    #                      self.epoch, self.early_stopping, self.is_evaluate, self.evaluate_func)
    #     pre_val = model.predict(x_val)
    #     pre_val = np.where(pre_val >= 0.5, 1, 0)
    #     score = f1_score(y_val, pre_val)
    #     return score

    # def lgb_param_search(
    #     self,
    #     data: pd.DataFrame,
    #     label: str
    # ):
    #     start = time.time()
    #     num_leaves_range = [25, 200] if self.num_leaves_range is None else self.num_leaves_range
    #     weight_range = [0, 10] if self.weight_range is None else self.weight_range
    #     opt_num_leaves, opt_weight, opt_score = rfc_2d_section(
    #         data, label, num_leaves_range, weight_range, 0.38197, self.get_lgb_score)
    #     end = time.time()
    #     if self.time_cost:
    #         print('耗时:', round(end - start, 4))
    #     return opt_num_leaves, opt_weight

    def xgb_fit(
        self,
        data: pd.DataFrame,
        label: str
    ):
        x_train, x_val, y_train, y_val = self.train_test_split(data, label)
        train_data = xgb.DMatrix(x_train, y_train)
        val_data = xgb.DMatrix(x_val, y_val)
        watchlist = [(train_data, 'train'), (val_data, 'valid_data')]
        if self.xgb_params is None:
            weight = round(data[data[label] == 0][label].count() / data[data[label] == 1][label].count(), 3)
            xgb_params = {'eta': 0.02,
                          'max_depth': 5,
                          'subsample': 0.8,
                          'colsample_bytree': 0.8,
                          'nthread': 8,
                          'objective': 'reg:logistic',
                          'eval_metric': 'auc',
                          'scale_pos_weight': weight
                          }
        else:
            xgb_params = self.xgb_params
        if self.is_evaluate:
            if self.evaluate_func is None:
                def xgb_evaluate_func(pre, train):
                    labels = train.get_label()
                    pre = np.where(pre >= 0.5, 1, 0)
                    score = f1_score(pre, labels)
                    return '1-f1_score', 1 - score  # xgb目标是将目标指标降
            else:
                xgb_evaluate_func = self.evaluate_func
            model = xgb.train(dtrain=train_data, num_boost_round=self.epoch, evals=watchlist,
                              early_stopping_rounds=self.early_stopping, verbose_eval=self.verbose, params=xgb_params,
                              feval=xgb_evaluate_func)
        else:
            model = xgb.train(dtrain=train_data, num_boost_round=self.epoch, evals=watchlist,
                              early_stopping_rounds=self.early_stopping, verbose_eval=self.verbose, params=xgb_params)
        importance = pd.DataFrame(list(model.get_score().items()), columns=['feature_names', 'importance'])
        importance = importance.sort_values('importance', ascending=False)
        importance['importance'] = importance['importance'] / importance['importance'].sum()
        pre_train = model.predict(train_data)
        pre_val = model.predict(val_data)
        pre_train = np.where(pre_train > 0.5, 1, 0)
        pre_val = np.where(pre_val > 0.5, 1, 0)
        print(confusion_matrix(y_train, pre_train))
        print(classification_report(y_train, pre_train, digits=4))
        print('在训练集下的精度为：', accuracy_score(y_train, pre_train))
        print('=' * 60)
        print(confusion_matrix(y_val, pre_val))
        print(classification_report(y_val, pre_val, digits=4))
        print('在验证集下的精度为：', accuracy_score(y_val, pre_val))
        return model, importance

    def xgb_cal_fitting(
            self,
            x_train,
            x_val,
            y_train,
            y_val,
            max_depth,
            weight
    ):
        model, train_data, val_data = xgb_init(
            x_train, x_val, y_train, y_val, max_depth, weight,
            self.epoch, self.early_stopping, self.is_evaluate, self.evaluate_func)
        pre_train = model.predict(train_data)
        pre_val = model.predict(val_data)
        pre_train = np.where(pre_train >= 0.5, 1, 0)
        pre_val = np.where(pre_val >= 0.5, 1, 0)
        matrix = confusion_matrix(y_train, pre_train)
        if matrix[1, 1] == 0:
            recall = 0
            precision = 1
        else:
            precision = matrix[1, 1] / (matrix[1, 1] + matrix[0, 1])
            recall = matrix[1, 1] / (matrix[1, 1] + matrix[1, 0])
        train_f1 = f1_score(y_train, pre_train)
        val_f1 = f1_score(y_val, pre_val)
        return recall - precision, train_f1 - val_f1

    def xgb_adjust_parameter(self,
                             x_train, x_val, y_train, y_val, max_depth, weight, balance, fitting, parameter_dict=None):
        # 如果下一组参数已计算过，则返回这组参数
        if parameter_dict is None:
            parameter_dict = {}
        if (max_depth, weight) in parameter_dict:
            print('因重复参数而停止调参')
            opt_num_leaves = max_depth
            opt_weight = weight
            opt_fitting = 0
            for k, v in parameter_dict.items():
                if abs(v[0]) <= 0.1 and v[1] < 0.03:
                    if v[1] > opt_fitting:
                        opt_fitting = v[1]
                        opt_num_leaves = k[0]
                        opt_weight = k[1]
            return opt_num_leaves, opt_weight
        parameter_dict[(max_depth, weight)] = (balance, fitting)
        if (abs(balance) <= 0.1) and (fitting >= 0.02) and (fitting <= 0.03):
            return max_depth, weight
        if fitting < 0.02 or fitting > 0.03:
            if balance != -1:
                if fitting < 0.02:
                    max_depth += 1
                if fitting > 0.03:
                    if max_depth < 2:
                        return max_depth, weight
                    max_depth -= 1
            if balance < -0.1:
                weight += 0.5
            if balance > 0.1:
                weight -= 0.5
            balance, fitting = self.xgb_cal_fitting(x_train, x_val, y_train, y_val, max_depth, weight)
            print('----------\n max_depth: %d, weight: %s, 召回-精度: %s, 验证f1-训练f1: %s' %
                  (max_depth, round(weight, 1), round(balance, 4), round(fitting, 4)))
            return self.xgb_adjust_parameter(x_train, x_val, y_train, y_val, max_depth, weight,
                                             balance, fitting, parameter_dict)
        if balance < -0.1 or balance > 0.1:
            if balance < -0.1:
                weight += 0.5
            if balance > 0.1:
                weight -= 0.5
            if balance != -1:
                if fitting < 0.02:
                    max_depth += 1
                if fitting > 0.03:
                    if max_depth < 2:
                        return max_depth, weight
                    max_depth -= 1
            balance, fitting = self.xgb_cal_fitting(x_train, x_val, y_train, y_val, max_depth, weight)
            print('----------\n num_leaves: %d, weight: %s, 召回-精度: %s, 验证f1-训练f1: %s' %
                  (max_depth, round(weight, 1), round(balance, 4), round(fitting, 4)))
            return self.xgb_adjust_parameter(x_train, x_val, y_train, y_val, max_depth, weight,
                                             balance, fitting, parameter_dict)

    def xgb_auto_adjust_parameter(
            self,
            data: pd.DataFrame,
            label: str
    ):
        start = time.time()
        x_train, x_val, y_train, y_val = self.train_test_split(data, label)
        balance, fitting = self.xgb_cal_fitting(x_train, x_val, y_train, y_val, 1, 1)
        print('----------\n max_depth: %d, weight: %s, 召回-精度: %s, 验证f1-训练f1: %s' %
              (1, 1, round(balance, 4), round(fitting, 4)))
        max_depth, weight = self.xgb_adjust_parameter(x_train, x_val, y_train, y_val, 1, 1, balance, fitting)
        print('最终max_depth: %s, 最终weight: %s' % (max_depth, weight))
        model, train_data, val_data = xgb_init(
            x_train, x_val, y_train, y_val, max_depth, weight,
            self.epoch, self.early_stopping, self.is_evaluate, self.evaluate_func)
        importance = pd.DataFrame(list(model.get_score().items()), columns=['feature_names', 'importance'])
        importance = importance.sort_values('importance', ascending=False)
        importance['importance'] = importance['importance'] / importance['importance'].sum()
        pre_train = model.predict(train_data)
        pre_val = model.predict(val_data)
        pre_train = np.where(pre_train >= 0.5, 1, 0)
        pre_val = np.where(pre_val >= 0.5, 1, 0)
        print(confusion_matrix(y_train, pre_train))
        print(classification_report(y_train, pre_train, digits=4))
        print('在训练集下的精度为：', accuracy_score(y_train, pre_train))
        print('=' * 55)
        print(confusion_matrix(y_val, pre_val))
        print(classification_report(y_val, pre_val, digits=4))
        print('在验证集下的精度为：', accuracy_score(y_val, pre_val))
        end = time.time()
        if self.time_cost:
            print('耗时:', round(end - start, 4))
        return model, importance

    # def get_xgb_score(
    #     self,
    #     x_train: pd.DataFrame,
    #     x_val: pd.DataFrame,
    #     y_train: pd.Series,
    #     y_val: pd.Series,
    #     max_depth: int,
    #     weight: float
    # ):
    #     model = xgb_init(x_train, x_val, y_train, y_val, max_depth, weight, self.epoch,
    #                      self.early_stopping, self.is_evaluate, self.evaluate_func)
    #     pre_val = model.predict(x_val)
    #     pre_val = np.where(pre_val >= 0.5, 1, 0)
    #     score = f1_score(y_val, pre_val)
    #     return score

    # def xgb_param_search(
    #     self,
    #     data: pd.DataFrame,
    #     label: str
    # ):
    #     start = time.time()
    #     max_depth_range = [2, 10] if self.max_depth_range is None else self.max_depth_range
    #     weight_range = [0, 10] if self.weight_range is None else self.weight_range
    #     opt_max_depth, opt_weight, opt_score = rfc_2d_section(
    #         data, label, max_depth_range, weight_range, 0.38197, self.get_xgb_score)
    #     end = time.time()
    #     if self.time_cost:
    #         print('耗时:', round(end - start, 4))
    #     return opt_max_depth, opt_weight

    def reset_atr(self):
        self.rfc_model = None
        self.lgb_model = None
        self.xgb_model = None
