'''
CS375 Project 4
Aidan Tokarski, Cynthia Zafris,
Eda Wright, Xavier Markowitz

Utilities for creating a SCOWL-like dictionary from text files
'''

import os

def read_text_file(file, dir):
    with open("{}/{}".format(dir, file), 'r') as source_file:
        text = source_file.read()
    return text

def get_files(dir):
    return os.listdir(dir)

def add_to_dict(dict, text):
    words = text.split(" ")
    for word in words:
        word = word.lower()
        if word in dict.keys():
            dict[word] = dict[word] + 1
        else:
            dict[word] = 1

def create_common_dict(source, target):
    dict = {}
    for word in source:
        if word in target.keys():
            dict[word] = source[word]
    return dict

def read_dict_file(file, dir):
    with open("{}/{}".format(dir, file), 'r') as source_file:
        new_dict = {}
        text = source_file.read()
        words = text.split("\n")
        for word in words:
            new_dict[word] = 1
    return new_dict

def write_dict_file(file, dir, dict):
    with open("{}/{}".format(dir, file), 'w') as new_file:
        sorted_words = sorted(dict.keys())
        for word in sorted_words:
            new_file.write(word + "\n")

if __name__ == "__main__":
    cs_dict = {}
    files = get_files("CS375_extracted")
    for file in files:
        add_to_dict(cs_dict, read_text_file(file, "CS375_extracted"))
    scowl_dict = read_dict_file("en_US-large.txt", "dicts")
    common_dict = create_common_dict(cs_dict, scowl_dict)
    write_dict_file("CS375_dict.txt", "dicts", common_dict)
