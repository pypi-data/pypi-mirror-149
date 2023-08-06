class ExceptionBase(Exception):
    err_code = 10000
    err_msg = 'Base Error Msg'


class TimeoutException(ExceptionBase):
    err_code = 10001
    err_msg = 'code timeout'
