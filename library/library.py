import datetime


def log_printer(*args, sep=" ", end="", **kwargs):
    joined_string = sep.join([str(arg) for arg in args])
    print(str(datetime.datetime.now()) + ' : ' + joined_string + "\n", sep=sep, end=end, **kwargs)