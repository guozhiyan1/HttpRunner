import datetime


def getdate(number=0, add_date=None, delete_date=None):
    """
    "%Y-%m-%d %H:%M:%S"
    "%Y-%m-%d"
    "%Y-%m-%dT%H:%M:%S.000Z"
    """
    string_list = ["%Y-%m-%d", '%Y-%m-%d %H:%M:%S', "%Y-%m-%dT%H:%M:%S.000Z"]
    strings = string_list[number]
    now_time = datetime.datetime.now()
    if add_date:
        result = (now_time + datetime.timedelta(days=add_date)).strftime(strings)
    elif delete_date:
        result = (now_time - datetime.timedelta(days=delete_date)).strftime(strings)
    else:
        result = now_time.strftime(strings)
    return result


if __name__ == '__main__':

    print(getdate(number=1, add_date=1))


