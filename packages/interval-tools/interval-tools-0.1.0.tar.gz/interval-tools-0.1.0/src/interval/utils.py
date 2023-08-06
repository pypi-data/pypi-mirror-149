"""
interval.utils
~~~~~~~~~~~~~~

This module provides utility functions.
"""

import random
import re
import string


def generate_nonce(length: int, chars: str='uld', population: str='',
                   *, prefix: str='', suffix: str='') -> str:
    """生成固定长度的随机字符串

    Args:
        length: 字符串总长度
        chars: 使用的字符种类：'u' - 大写字母，'l' - 小写字母，'d' - 数字
        population: 使用的字符集合；若指定了population则忽略chars
        prefix: 字符串前缀
        suffix: 字符串后缀

    Returns:
        随机字符串

    Raises:
        ValueError: 前缀和后缀的长度之和大于总长度；没有指定有效的字符种类或者字符集合
    """
    random_part_len = length - len(prefix + suffix)
    if random_part_len < 0:
        raise ValueError('Invalid length')
    if random_part_len == 0:
        return prefix + suffix
    if not population:
        if 'u' in chars:
            population += string.ascii_uppercase
        if 'l' in chars:
            population += string.ascii_lowercase
        if 'd' in chars:
            population += string.digits
        if not population:
            raise ValueError('Invalid chars')
    elements = random.choices(population, k=random_part_len)
    return prefix + ''.join(elements) + suffix


def check_email(email: str) -> bool:
    """检查电子邮箱格式是否正确

    Args:
        email: 电子邮箱

    Returns:
        格式正确返回True，否则返回False
    """
    pattern = r'\S+@\S+\.\S+'
    match_obj = re.fullmatch(pattern, email)
    return bool(match_obj)


def check_mobile(mobile: str) -> bool:
    """检查手机号码格式是否正确

    Args:
        mobile: 手机号码

    Returns:
        格式正确返回True，否则返回False
    """
    pattern = r'1[3-9]\d{9}'
    match_obj = re.fullmatch(pattern, mobile)
    return bool(match_obj)


def check_id_card(id_card: str) -> bool:
    """检查身份证号码格式是否正确

    Args:
        id_card: 身份证号码

    Returns:
        格式正确返回True，否则返回False
    """
    if len(id_card) == 18:
        pattern = r'[1-9]\d{5}[12]\d{3}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])\d{3}[\dxX]'
        match_obj = re.fullmatch(pattern, id_card)
        return bool(match_obj)
    if len(id_card) == 15:
        pattern = r'[1-9]\d{7}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])\d{3}'
        match_obj = re.fullmatch(pattern, id_card)
        return bool(match_obj)
    return False
