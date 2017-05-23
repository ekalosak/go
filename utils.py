import logging

def make_logger(name, verbose = True):
    # https://docs.python.org/2/howto/logging-cookbook.html
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fh = logging.FileHandler('{}.log'.format(name))
    fh.setLevel(logging.INFO)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # create formatter and add it to the handlers
    fmt ='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(fmt)
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    if verbose:
        logger.addHandler(ch)
    return logger

def _writetolog(what, log, debuglevel):

    if debuglevel == "debug":
        log.debug("function <{}> returned <{}>".format(
            function, result))
    elif debuglevel == "info":
        log.info("function <{}> returned <{}>".format(
            function, result))
    else:
        raise Exception('Unsupported debugging level <{}>'.format(
            debugging))

def loggable(log, debuglevel="debug"):
    # decorator that logs returned object of function
    def wrap(function):
        def inner(*args):
            result = function(args)
            _writetolog(what, log, debuglevel)
            return result
        return inner
    return wrap
