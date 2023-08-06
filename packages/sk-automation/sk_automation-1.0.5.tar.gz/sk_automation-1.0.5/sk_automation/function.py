
import numpy as np
import pandas as pd


# 字段衍生舍弃iv阈值
low_iv = 0.02
# 字段衍生舍弃相关程度阈值
high_corr = 0.9


def is_number(s: str) -> bool:
    """
    判断字符是否为数字
    """
    try:
        float(s)
        return True
    except ValueError:
        return False


def col_is_number(data, col):
    try:
        data[col].astype(float)
        return True
    except ValueError:
        unique_kind = data[col].unique()
        for kind in unique_kind:
            if pd.isnull(kind):
                continue
            if not is_number(str(kind)):
                return False
        return True


def keep_drop_judge(white_set, field_dict, drop, drop_name, keep, keep_name, col):
    field_name = col if col not in field_dict else field_dict[col]
    if col in white_set:
        keep.append(col)
        keep_name.append(field_name)
        return False
    else:
        drop.append(col)
        drop_name.append(field_name)
        return True


def divide(df1, df2, inf_value):
    divide_df = pd.Series(map(lambda a, b: a/b if b != 0 else inf_value,
                          df1, df2))
    divide_df.index = df1.index
    return divide_df


def rfc_section(data, label, weight_range, max_depth, delta, function):
    iter_num = 0
    score_dict = {}
    diff = 1e9
    opt_score = None
    opt_weight = None
    left = weight_range[0]
    right = weight_range[1]
    left_mid = left + delta * np.abs(right - left)
    right_mid = right - delta * np.abs(right - left)
    while np.abs(diff) > 1e-5 and iter_num < 200:
        iter_num += 1
        left_mid = np.round(left_mid, 2)
        right_mid = np.round(right_mid, 2)
        if left_mid in score_dict:
            score_left_mid = score_dict[left_mid]
        else:
            score_left_mid = function(data, label, max_depth, left_mid)
            score_dict[left_mid] = score_left_mid

        if right_mid in score_dict:
            score_right_mid = score_dict[right_mid]
        else:
            score_right_mid = function(data, label, max_depth, right_mid)
            score_dict[right_mid] = score_right_mid
        if score_left_mid >= score_right_mid:
            opt_score = score_left_mid
            opt_weight = left_mid
            right = right_mid
            right_mid = left_mid
            left_mid = left + delta * np.abs(right - left)
        else:
            opt_score = score_right_mid
            opt_weight = right_mid
            left = left_mid
            left_mid = right_mid
            right_mid = right - delta * np.abs(right - left)
        diff = score_right_mid - score_left_mid
    return opt_weight, opt_score


def rfc_2d_section(data, label, depth_range, weight_range, delta, function):
    iter_num = 0
    score_dict = {}
    diff = 1e9
    opt_depth = None
    opt_weight = None
    opt_score = None
    left = depth_range[0]
    right = depth_range[1]
    left_mid = left + delta * np.abs(right - left)
    right_mid = right - delta * np.abs(right - left)
    while np.abs(diff) > 1e-5 and iter_num < 200:
        iter_num += 1
        left_mid = np.round(left_mid, 0).astype(int)
        right_mid = np.round(right_mid, 0).astype(int)
        if left_mid in score_dict:
            weight_l, score_left_mid = score_dict[left_mid]
        else:
            weight_l, score_left_mid = rfc_section(data, label, weight_range, left_mid, delta, function)
            score_dict[left_mid] = [weight_l, score_left_mid]
        if right_mid in score_dict:
            weight_r, score_right_mid = score_dict[right_mid]
        else:
            weight_r, score_right_mid = rfc_section(data, label, weight_range, right_mid, delta, function)
            score_dict[right_mid] = [weight_r, score_right_mid]
        if score_left_mid >= score_right_mid:
            opt_score = score_left_mid
            opt_weight = weight_l
            opt_depth = left_mid
            right = right_mid
            right_mid = left_mid
            left_mid = left + delta * np.abs(right - left)
        else:
            opt_score = score_right_mid
            opt_weight = weight_r
            opt_depth = right_mid
            left = left_mid
            left_mid = right_mid
            right_mid = right - delta * np.abs(right - left)
        diff = score_right_mid - score_left_mid
        print('depth, weight, f1_score:', opt_depth, opt_weight, opt_score)
    return opt_depth, opt_weight, opt_score
