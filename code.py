import numpy as np

mode = input("""Выберите режим: 
diff1 - поиск общих строк в файлах и их места в исходном,
diff2 - посимвольное сравнение,
reset1 - восстановление нового файла, при подача файла с разницей, полученного после diff1,
reset2 - восстановление после посимвольного сравнения\n
""")

old_file_name = input("Введите название старого файла: ")
new_file_name = input("Введите название нового файла: ")
diff_file_name = input("Введите название файла для записи изменений: ")
old_file = open(old_file_name, 'r')

old_file_string = np.array([0])
for line in old_file:
    old_file_string = np.append(old_file_string, line)


if mode == 'diff2':
    new_file = open(new_file_name, 'r')
    diff_file = open(diff_file_name, 'w')
    diff_file.write("Differences:\n")
    new_file_string = np.array([0])
    for line in new_file:
        new_file_string = np.append(new_file_string, line)
    for i in range(1, len(new_file_string)):
        diff_file.write(new_file_string[i])
        tmp_str = ""

        if (len(new_file_string[i]) > len(old_file_string[i])):
            for j in range(len(old_file_string[i]) - 1):
                if(old_file_string[i][j] == new_file_string[i][j]):
                    tmp_str += '+'
                else:
                    tmp_str += '-'
            for j in range(len(new_file_string[i]) - len(old_file_string[i])):
                tmp_str += '-'

        if (len(new_file_string[i]) < len(old_file_string[i])):
            for j in range(len(new_file_string[i]) - 1):
                if (old_file_string[i][j] == new_file_string[i][j]):
                    tmp_str += '+'
                else:
                    tmp_str += '-'
            for j in range(-len(new_file_string[i]) + len(old_file_string[i])):
                tmp_str += '_'

        if (len(new_file_string[i]) == len(old_file_string[i])):
            for j in range(len(new_file_string[i]) - 1 ):
                if (old_file_string[i][j] == new_file_string[i][j]):
                    tmp_str += '+'
                else:
                    tmp_str += '-'

        tmp_str += '\n'
        diff_file.write(tmp_str)


if mode == 'reset2':
    new_file = open(new_file_name, 'w')
    diff_file = open(diff_file_name, 'r')
    diff_file_string = np.array([])
    for line in diff_file:
        diff_file_string = np.append(diff_file_string, line)
    for i in range(int(len(diff_file_string) / 2)):
        new_file.write(diff_file_string[2 * i + 1])



if mode == 'diff1':
    old_file_string_hashes = np.array([0])
    new_file = open(new_file_name, 'r')
    diff_file = open(diff_file_name, 'w')

    new_file_string_hashes = np.array([0])

    new_file_string = np.array([0])
    for line in old_file:
        old_file_string_hashes = np.append(old_file_string_hashes, hash(line))

    for line in new_file:
        new_file_string = np.append(new_file_string, line)
        new_file_string_hashes = np.append(new_file_string_hashes, hash(line))

    hash_diff = np.array([np.zeros(len(new_file_string_hashes)), np.zeros(len(new_file_string_hashes))])
    for i in range(len(new_file_string_hashes)):
        d, = np.where(new_file_string_hashes[i] == old_file_string_hashes)
        if (len(d) > 0):
            hash_diff[1][d[0]] += 1
            if len(d) >= hash_diff[1][d[0]]:
                hash_diff[0][i] = d[0]

    diff_file.write("Differences:\n")
    for i in range(1, len(new_file_string_hashes)):
        if (hash_diff[0][i] > 0):
            diff_file.write(f"% {int(hash_diff[0][i])} th_str % " + new_file_string[i])
        else:
            diff_file.write("% new_str % " + new_file_string[i])
    print("Разница успешна найдена!")


if mode == 'reset1':
    new_file = open(new_file_name, 'w')
    diff_file = open(diff_file_name, 'r')
    diff_file_string = np.array([])
    for line in diff_file:
        diff_file_string = np.append(diff_file_string, line)
    for i in range(1, len(diff_file_string)):
        number = diff_file_string[i].split()[0]
        if number.isnumeric():
            new_file.write(old_file_string[int(number)])
        else:
            (new_file.write(diff_file_string[i][12:]))
    print("Восстановлено!")
