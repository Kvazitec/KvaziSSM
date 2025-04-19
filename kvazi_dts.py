def datasearch(file_name, objectl, parameter):
    file = open(file_name, 'r')
    info = file.read()
    i = info.index(objectl) + len(objectl)
    while info[i+1: i+len(parameter)+2] != parameter+' ':
        i = i+1
        if info[i: i+len('object_end')] == 'object_end':
            print(f'Параметр {parameter} объекта {objectl} не найден в файле {file_name}. Продолжение работы программы невозможно')
            exit(1)
    j = i+len(parameter)+2
    while info[j] == ' ' or  info[j] == '=':
        j = j + 1
    k = j
    while info[k] != '\n':
        k = k + 1
    return info[j:k]