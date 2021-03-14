def merge_files(file_list):
    # This methods opens all the files with names specified in a list of strings,
    # and combines them in a single file, intercalating a line of every file, as
    # long as there are more lines in the file.
    list_of_lines = []
    lines = []
    flag = True
    for file_name in file_list:
        reader = open(file_name,'r')
        list_of_lines.append(reader.readlines())
    while flag:
        counter = 0
        for lines_file in list_of_lines:
            k = len(lines_file)
            if k > 0:
                lines.append(lines_file.pop(0))
                counter += k
        if counter == 0:
            flag = False
    out = open('out.txt','w')
    for line in lines:
        out.write(line)
    out.close()
