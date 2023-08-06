
import pandas as pd
from .data_pretreatment import DataPretreatment
from .feature_analysis import FeatureAnalysis
from .feature_project import FeatureProject
from .model_build import ModelBuild, function

train_test_split_params = {'test_size', 'train_size', 'random_state', 'shuffle', 'stratify'}


class AutoModel(DataPretreatment, FeatureProject, FeatureAnalysis, ModelBuild):

    def __init__(
            self,
            is_analysis: bool = True,
            white_set: set = None,
            field_dict: dict = None,
            drop_col: list = None,
            start_num: int = 1,
            nan_rate: float = 0.3,
            meaningless_field: list = None,
            is_structure: bool = False,
            structure_list: list = None,
            form: str = 'sum',
            is_extreme: bool = True,
            lower: float = 0.01,
            upper: float = 0.99,
            is_drop_corr: bool = True,
            label_first: bool = False,
            info_first: bool = False,
            corr: float = 0.9,
            after_pretreatment: bool = True,
            init_box: int = 30,
            final_box: int = 7,
            importance_rate: float = None,
            top_importance_k: int = 20,
            is_drop_iv: bool = True,
            iv_threshold: float = 0.02,
            is_drop_importance: bool = True,
            importance_threshold: float = 0.95,
            is_feature_derive: bool = True,
            derive_n: int = 10,
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
            # is_search: bool = False,
            # max_depth_range: list = None,
            # num_leaves_range: list = None,
            # weight_range: list = None,
            time_cost: bool = True,
            **kwargs
    ):
        """
        Parameters
        ----------
        is_analysis: bool
            是否进行特征分析
        See Also
        ----------
        automation.data_pretreatment.DataPretreatment,
        automation.feature_analysis.FeatureAnalysis,
        automation.feature_project.FeatureProject,
        automation.model_build.ModelBuild
        """
        DataPretreatment.__init__(
            self, white_set=white_set, drop_col=drop_col, start_num=start_num, nan_rate=nan_rate,
            meaningless_field=meaningless_field, is_structure=is_structure, structure_list=structure_list,
            form=form, is_extreme=is_extreme, lower=lower, upper=upper, time_cost=time_cost
        )
        FeatureProject.__init__(
            self, is_drop_corr=is_drop_corr, white_set=white_set, label_first=label_first,
            info_first=info_first, corr=corr, is_drop_iv=is_drop_iv, iv_threshold=iv_threshold,
            is_drop_importance=is_drop_importance, importance_threshold=importance_threshold,
            is_feature_derive=is_feature_derive, derive_n=derive_n, time_cost=time_cost
        )
        FeatureAnalysis.__init__(
            self, white_set=white_set, is_drop_corr=is_drop_corr, label_first=label_first,
            info_first=info_first, corr=corr, after_pretreatment=after_pretreatment, init_box=init_box,
            final_box=final_box, importance_rate=importance_rate, top_importance_k=top_importance_k,
            time_cost=time_cost
        )
        ModelBuild.__init__(
            self, baseline=baseline, max_depth=max_depth, weight=weight, lgb_params=lgb_params,
            xgb_params=xgb_params, early_stopping=early_stopping, verbose=verbose, epoch=epoch,
            is_evaluate=is_evaluate, evaluate_func=evaluate_func, is_adjust_parameter=is_adjust_parameter,
            time_cost=time_cost
        )
        self.is_analysis = is_analysis
        self.field_dict = field_dict
        self.kwargs = kwargs
        if 'random_state' not in kwargs:
            kwargs['random_state'] = 1
        for k, v in kwargs.items():
            if k not in train_test_split_params:
                raise ValueError('未知参数:%s' % k)
        self.pretreatment = None
        self.train_pretreatment_df = None
        self.test_pretreatment_df = None
        self.project = None
        self.train_project_df = None
        self.test_project_df = None
        self.model_build = None
        self.pre_df = None

    def fit(
            self,
            data: pd.DataFrame,
            label: str,
            is_analysis: bool = None,
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
            is_drop_corr: bool = None,
            label_first: bool = None,
            info_first: bool = None,
            corr: float = None,
            after_pretreatment: bool = None,
            init_box: int = None,
            final_box: int = None,
            importance_rate: float = None,
            top_importance_k: int = None,
            is_drop_iv: bool = None,
            iv_threshold: float = None,
            is_drop_importance: bool = None,
            importance_threshold: float = None,
            is_feature_derive: bool = None,
            derive_n: int = None,
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
        self.is_analysis = self.is_analysis if is_analysis is None else is_analysis
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
        self.is_drop_corr = self.is_drop_corr if is_drop_corr is None else is_drop_corr
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
        self.is_drop_iv = self.is_drop_iv if is_drop_iv is None else is_drop_iv
        self.iv_threshold = self.iv_threshold if iv_threshold is None else iv_threshold
        self.is_drop_importance = self.is_drop_importance if is_drop_importance is None else is_drop_importance
        self.importance_threshold = self.importance_threshold if importance_threshold is None else importance_threshold
        self.is_feature_derive = self.is_feature_derive if is_feature_derive is None else is_feature_derive
        self.derive_n = self.derive_n if derive_n is None else derive_n
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
        if kwargs is not None:
            for k, v in kwargs.items():
                if k not in train_test_split_params:
                    raise ValueError('未知参数:%s' % k)
            self.kwargs = kwargs
        print('==========\n 数据预处理')
        pretreatment = DataPretreatment(
            white_set=self.white_set, field_dict=self.field_dict, drop_col=self.drop_col, start_num=self.start_num,
            nan_rate=self.nan_rate, meaningless_field=self.meaningless_field, is_structure=self.is_structure,
            structure_list=self.structure_list, form=self.form, is_extreme=self.is_extreme, lower=self.lower,
            upper=self.upper, time_cost=self.time_cost)
        pretreatment_df = pretreatment.fit(data, label)
        col_dict = pretreatment.col_dict
        convert_dict = pretreatment.convert_dict
        self.pretreatment = pretreatment
        self.train_pretreatment_df = pretreatment_df
        if self.is_analysis:
            print('==========\n 特征分析')
            analysis = FeatureAnalysis(
                col_dict=col_dict, convert_dict=convert_dict, field_dict=self.field_dict, white_set=self.white_set,
                is_drop_corr=self.is_drop_corr, label_first=self.label_first, info_first=self.info_first,
                corr=self.corr, after_pretreatment=self.after_pretreatment, init_box=self.init_box,
                final_box=self.final_box, importance_rate=self.importance_rate,
                top_importance_k=self.top_importance_k, time_cost=self.time_cost
            )
            analysis.fit(pretreatment_df, label, original_data=data)
        print('==========\n 特征工程')
        project = FeatureProject(
            is_drop_corr=self.is_drop_corr, field_dict=self.field_dict, white_set=self.white_set,
            label_first=self.label_first, info_first=self.info_first, corr=self.corr, is_drop_iv=self.is_drop_iv,
            iv_threshold=self.iv_threshold, is_drop_importance=self.is_drop_importance,
            importance_threshold=self.importance_threshold, is_feature_derive=self.is_feature_derive,
            derive_n=self.derive_n, time_cost=self.time_cost
        )
        project_df = project.fit(pretreatment_df, label)
        self.train_project_df = project_df
        self.project = project
        print('==========\n 模型构建')
        model_build = ModelBuild(
            baseline=self.baseline, max_depth=self.max_depth, weight=self.weight, lgb_params=self.lgb_params,
            xgb_params=self.xgb_params, early_stopping=self.early_stopping, verbose=self.verbose, epoch=self.epoch,
            is_evaluate=self.is_evaluate, evaluate_func=self.evaluate_func,
            is_adjust_parameter=self.is_adjust_parameter, time_cost=self.time_cost
        )
        model, importance = model_build.fit(project_df, label)
        self.model_build = model_build
        return model, importance

    def fit_transform(
            self,
            data: pd.DataFrame
    ):
        print('==========\n 数据预处理')
        test_project_df = self.pretreatment.fit_transform(data)
        self.test_project_df = test_project_df
        print('==========\n 特征工程')
        test_project_df = self.project.fit_transform(test_project_df)
        self.test_project_df = test_project_df
        print('==========\n 模型预测')
        pre_df = self.model_build.fit_transform(test_project_df)
        return pre_df
