def l(message, level=None):
    s = '{}: {}'.format(level, message) if level else message
    print s
