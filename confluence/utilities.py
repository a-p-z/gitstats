def buildTable(header, data):
    header = map(str, header)
    header = ["||%s||" % "||".join(header)]
    data = map(lambda x: map(str, x) if isinstance(x, list) or isinstance(x, tuple) else [str(x)], data)
    data = map(lambda x: "|%s|" % "|".join(x), data)
    
    return "\n".join(header + data)


def limit(data, limit):
    if len(data) <= limit:
        return data
    result = data[:limit-1]
    others = ["others"] + data[limit][1:] if len(data) > limit else []
    data = data[limit+1:]
    
    for value in data:
        for i in range(1, len(others)):
            others[i] += value[i]
    
    return result + [others]


def splitHeaderAndData(data):
    return (data[0], data[1:])


def cumulate(data):
    for i in range(1, len(data)):
        for j in range(1, len(data[i])):
            data[i][j] += data[i-1][j]
    
    return data


def getTotal(data):
    total = map(lambda x: 0, data[0]) if len(data) > 0 else ["total", 0]
    total[0] = "total"
    
    for value in data:
        for i in range(1, len(value)):
            total[i] += value[i]
    
    return map(lambda x: "*%s*" % x, total)

def getUsername(email):
    return email.partition("@")[0]
