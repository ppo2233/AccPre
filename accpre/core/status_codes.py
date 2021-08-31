"""
'0000': 成功
'0001' ~ '0099': 通用错误
'0100' ~ '0199': 用户管理错误
'0200' ~ '0299': 标签管理错误
'0300' ~ '0399': 分类管理错误
'0400' ~ '0499': 文章管理错误
'0500' ~ '0599': 链接管理错误
'9999: 其他异常
"""


SUCCESS_CODE = '0000'

PARAM_IS_NULL_CODE = '0001'  # 参数为空
PARAM_IS_DUPLICATED = '0002'  # 参数重复
PARAM_LENGTH_ERR_CODE = '0003'  # 参数字符长度错误

USER_OR_PASSWORD_ERROR_CODE = '0100'  # 用户名或密码有误
USER_ROLE_ERROR_CODE = '0101'  # 用户角色错误

UNKNOWN_ERROR = '9999'  # 其他未捕获到的异常


CODE_MSG = {
    SUCCESS_CODE: '',  # 成功

    PARAM_IS_NULL_CODE: '[{param}] is null',
    PARAM_IS_DUPLICATED: '[{param}] is duplicate',
    PARAM_LENGTH_ERR_CODE: '[{param}] incorrect character length',

    USER_OR_PASSWORD_ERROR_CODE: 'username or password is error',
    USER_ROLE_ERROR_CODE: 'user role error',

    UNKNOWN_ERROR: 'other error',
}
