class RV64Exception(Exception):
    '''rv64 base exception'''

def error(message):
    raise RV64Exception(message)
