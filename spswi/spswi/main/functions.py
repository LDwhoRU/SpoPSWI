import os, sys

def replace_line(file_name, line_num, text):
    lines = open(file_name, 'r').readlines()
    lines[line_num] = text
    out = open(file_name, 'w')
    out.writelines(lines)
    out.close()

def read_file(file_name, line_num):
    file_path = os.path.join(sys.path[0]) + file_name
    lines = open(file_path, 'r').readlines()
    return lines[line_num]

