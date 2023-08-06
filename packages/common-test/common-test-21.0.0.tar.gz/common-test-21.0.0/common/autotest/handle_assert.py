from loguru import logger
from common.autotest.handle_allure import allure_step
from common.data.data_process import DataProcess
from common.data.handle_common import req_expr, convert_json, extractor, is_not_bank, get_jpath


def assert_result(res: dict, expect_str: str):
    """ 预期结果实际结果断言方法
    :param res: 实际响应结果
    :param expect_str: 预期响应内容，从excel中读取
    return None
    """
    # 后置sql变量转换
    expect_str = req_expr(expect_str, DataProcess.response_dict)
    expect_dict = convert_json(expect_str)
    index = 0
    for k, v in expect_dict.items():
        # 获取需要断言的实际结果部分
        actual = get_jpath(res, k)
        index += 1
        assert_equals(actual, v, f'第{index}个断言检查')

def assert_excel_contain(res: dict, expect_str: str):
    """ 预期结果实际结果断言方法
    :param res: 实际响应结果
    :param expect_str: 预期响应内容，从excel中读取
    return None
    """
    # 后置sql变量转换
    expect_str = req_expr(expect_str, DataProcess.response_dict)
    expect_dict = convert_json(expect_str)
    index = 0
    for k, v in expect_dict.items():
        # 获取需要断言的实际结果部分
        actual = get_jpath(res, k)
        index += 1
        assert_contains(actual, v, f'第{index}个断言检查')


def assert_equals(actual, expect, desc :str='断言检查'):
    allure_step(f'{desc}', f'实际结果:{actual} = 预期结果:{expect}')
    try:
        if isinstance(expect, dict):
            for k, v in expect.items():
                if isinstance(actual, dict):
                    assert str(actual[k]).strip() == str(expect[k]).strip()
                else:
                    assert str(expect[k]).strip() == str(actual).strip()
        if isinstance(expect, list):
            for _index in range(len(expect)):
                if isinstance(actual, list):
                    assert str(expect[_index]).strip() == str(actual[_index]).strip()
                else:
                    assert str(expect[_index]).strip() == str(actual).strip()
        if isinstance(expect, str):
            if isinstance(actual, list):
                for _index in range(len(actual)):
                    assert str(actual[_index]).strip() == str(expect).strip()
            else:
                assert str(actual).strip() == str(expect).strip()
    except AssertionError:
        raise AssertionError(f'{desc} |- 实际结果:{actual} != 预期结果: {expect}')


def assert_contains(actual, expect, desc:str='断言检查'):
    allure_step(f'{desc}', f'实际结果:{actual} 包含 预期结果:{expect}')
    try:
        if isinstance(expect, dict):
            for k, v in expect.items():
                if isinstance(actual, dict):
                    assert str(expect[k]).strip() in str(actual[k]).strip()
                else:
                    assert str(expect[k]).strip() in str(actual).strip()
        elif isinstance(expect, list):
            for _index in range(len(expect)):
                if isinstance(actual, list):
                    assert str(expect[_index]).strip() in str(actual[_index]).strip()
                else:
                    assert str(expect[_index]).strip() in str(actual).strip()
        elif isinstance(expect, str):
            assert str(expect).strip() in str(actual).strip()
        else:
            assert expect in actual
    except AssertionError:
        raise AssertionError(f'{desc} |- 实际结果:{actual} 不包含 预期结果: {expect}')

def assert_Nobank(res, desc:str='断言检查'):
    allure_step(f'{desc}', f'实际结果:{res} 不为空')
    try:
        assert is_not_bank(res)
    except AssertionError:
        raise AssertionError(f'{desc} |- 实际结果:{res} 为空')


def assert_not_contains(res, expect_str,desc:str='断言检查'):
    allure_step(f'{desc}', f'实际结果:{res} 不包含 预期结果:{expect_str}')
    try:
        assert expect_str not in res
    except AssertionError:
        raise AssertionError(f'{desc} |- 实际结果:{res} 包含 预期结果: {expect_str}')

def assert_scene_result(res, expect_dict):
    global actual

    index = 0
    for k, v in expect_dict.items():
        # 获取需要断言的实际结果部分
        try:
            actual = extractor(res, k)
            index += 1
            logger.info(f'第{index}个断言,实际结果:{actual} | 预期结果:{v} | 断言结果 {actual == v}')
            allure_step(f'第{index}个断言', f'实际结果:{actual} = 预期结果:{v}')

            assert actual == v
        except AssertionError:
            raise AssertionError(f'第{index}个断言失败 -|- 实际结果:{actual} || 预期结果: {v}')

# 比对数据
def compare_data(set_key, src_data, dst_data, noise_data, num):
    if isinstance(src_data, dict) and isinstance(dst_data, dict):
        """若为dict格式"""
        for key in dst_data:
            if key not in src_data:
                print("src不存在这个key")
                noise_data[key] = "src不存在这个key"
        for key in src_data:
            if key in dst_data:
                if src_data[key] != dst_data[key] and num == 1:
                    noise_data[key] = "容忍不等"
                if src_data[key] != dst_data[key] and num == 2:
                    noise_data[key] = {}
                    noise_data[key]["primary"] = src_data[key]
                    noise_data[key]["candidate"] = dst_data[key]
                """递归"""
                compare_data(key, src_data[key], dst_data[key], noise_data, num)
            else:
                noise_data[key] = ["dst不存在这个key"]
    elif isinstance(src_data, list) and isinstance(dst_data, list):
        """若为list格式"""
        if len(src_data) != len(dst_data) and len(set_key) != 0:
            print("list len: '{}' != '{}'".format(len(src_data), len(dst_data)))
            noise_data[set_key]["primary"] = str(src_data)
            noise_data[set_key]["candidate"] = str(dst_data)
            return
        if len(src_data) == len(dst_data) and len(src_data) > 1:
            for index in range(len(src_data)):
                for src_list, dst_list in zip(sorted(src_data[index]), sorted(dst_data[index])):
                    """递归"""
                    compare_data("", src_list, dst_list, noise_data, num)
        else:
            for src_list, dst_list in zip(sorted(src_data), sorted(dst_data)):
                """递归"""
                compare_data("", src_list, dst_list, noise_data, num)
    else:
        if str(src_data) != str(dst_data):
            print("src_data", src_data, "dst_data", dst_data)
    return noise_data



if __name__ == '__main__':
    # res = "/883343Test8838"
    # res2 = "88"
    # print(assert_contains(res,res2))
    # res={'a':2,'b':3,'c':4}
    # res2={'a':2}
    # print(assert_contains(res, res2))
    res = ['a','b','c']
    res2 ={'a':'1'}
    print(assert_contains(res, res2))



    # except_dict = '{"$.a":2,"$.b":3,"$.c":3}'
    # assert_result(res,except_dict)



