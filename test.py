name = 'hector gonzales martin debian'
names = name.split(' ')

def cleanNames(nameString):
    namesInput = nameString.split(' ')
    namesOut = []

    #First name
    namesOut.append(namesInput[0])

    #Middle name(s).. any extra names are assumed to be middle names
    if len(namesInput) > 2:
        namesOut.append(' '.join(namesInput[1:-1]))
    else:
        namesOut.append("NULL")

    #Last name(s)
    namesOut.append(namesInput[len(namesInput) - 1])
    return namesOut

print(cleanNames(name))