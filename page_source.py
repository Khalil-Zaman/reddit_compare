from urllib import request


def get_page_source(redit):
    r = request.urlopen("http://redditmetrics.com/r/"+redit)
    bytecode = r.read()
    return str(bytecode)


def get_after(data, sub, max_after=0):
    a_index = str(data)
    a_index = a_index.index(sub) + len(sub)
    if max_after == 0:
        return data[a_index:]
    else:
        return data[a_index:(a_index + max_after)]


# Strip anything at the end that's not a number
def strip_ending(string):
    str_len = len(string) - 1
    counter = 0
    while string[str_len-counter] not in "0123456789":
        counter += 1
    return string[:-counter]


def number_of_subscribers(bytecode):
    data = bytecode.rsplit('\\n')
    start_collecting = False
    subscribers_data = []
    year_data = []
    for i in range(0, len(data)):
        if start_collecting is True:
            if "a" not in data[i]:
                return subscribers_data, year_data
            elif "data" not in data[i]:
                number = get_after(data[i], "a: ")
                number = strip_ending(number)
                year = get_after(data[i], "y: \\'", 12)
                year = strip_ending(year)
                year_data.append(year)
                subscribers_data.append(int(number))
        elif ("total-subscribers" in data[i]) and ("data" in data[i+1]):
            start_collecting = True
    return subscribers_data, year_data
