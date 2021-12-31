def countMessages(fileName):
    totalCount = 0
    userCount = {}
    reader = open(fileName,'r')
    list_of_lines = reader.readlines()
    for line in list_of_lines:
        if line.find('/21,') != -1:
            aa = line.find(':')
            aa += 6
            nuLine = line[aa:]
            nn = nuLine.find(':')
            user = nuLine[:nn]
            if user.find('left') == -1 and user.find('joined') == -1:
                totalCount += 1
                if user in userCount:
                    userCount[user] += 1
                else:
                    userCount[user] = 1
    print(totalCount)
    return userCount
