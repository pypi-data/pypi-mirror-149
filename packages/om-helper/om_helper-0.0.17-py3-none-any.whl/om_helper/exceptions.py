class ExceptionBase(Exception):
    err_code = 10000
    err_msg = 'base_error_msg'


class TimeoutException(TimeoutError):
    err_code = 10001
    err_msg = 'code_timeout'
