import logging, sys

'''
DEBUG = Detailed debugging during normal execution
INFO = Less detailed debugging
WARNING = For things that shouldnt happen but are outside the users control (warning.warn()) if its the users fault
ERROR = error that dont prevent the program from running
CRITICAL = Error that prevents the program from running
'''



def init_logger():
    global logger
    formatter = logging.Formatter(
        '[(%(asctime)s) (%(module)s:%(lineno)s) : %(levelname)s] "%(message)s"'
    )


    logger = logging.getLogger(name = "mylogger")
    logger.setLevel(logging.DEBUG)
    

    streamhandler = logging.StreamHandler(sys.stdout)
    '''###'''
    streamhandler.setLevel(logging.DEBUG)
    '''###'''
    streamhandler.setFormatter(formatter)
    logger.addHandler(streamhandler)

    filehandler = logging.FileHandler(r"logs\1DEBUG.log")
    
    filehandler.setLevel(logging.DEBUG)
    filehandler.setFormatter(formatter)
    logger.addHandler(filehandler)

    filehandler = logging.FileHandler(r"logs\2INFO.log")
    filehandler.setLevel(logging.INFO)
    filehandler.setFormatter(formatter)
    logger.addHandler(filehandler)

    filehandler = logging.FileHandler(r"logs\3WARNING.log")
    filehandler.setLevel(logging.WARNING)
    filehandler.setFormatter(formatter)
    logger.addHandler(filehandler)

    filehandler = logging.FileHandler(r"logs\4ERROR.log")
    filehandler.setLevel(logging.ERROR)
    filehandler.setFormatter(formatter)
    logger.addHandler(filehandler)

    filehandler = logging.FileHandler(r"logs\5CRITICAL.log")
    filehandler.setLevel(logging.CRITICAL)
    filehandler.setFormatter(formatter)
    logger.addHandler(filehandler)

def getLogger():
    try:
        return logger
    except:
        init_logger()
        return logger
