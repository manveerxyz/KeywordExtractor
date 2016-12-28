from __future__ import absolute_import
from pysubs2 import *
import os
import io


# class to hold our test instance (document plus its correct manual keywords)
class TestDoc:
    def __init__(self, name):
        self.name = name
        self.text = ''
        self.keywords = []


# reading documents and their keywords from a directory
def read_data(input_dir):

    test_set = {}

    for doc in os.listdir(input_dir):
        if not (doc.endswith('.srt') or doc.endswith('.ass') or doc.endswith('.ssa') or doc.endswith('.sub')):
            continue
        sub_file = load(os.path.join(input_dir,doc))
        file_name = doc[:-4]
        if file_name not in test_set:
            d = TestDoc(file_name)
        else:
            d = test_set[file_name]

        # get document text
        text = ''
        for line in sub_file:
            line.text = line.text.replace('\\N', '\n')
            for split_line in line.text.split('\n'):
                split_line = split_line.strip().lower()
                if '\t' in split_line:
                    text += split_line[0:split_line.find('\t')] + ' '
                else:
                    text += split_line + ' '
        d.text = text

        # get document keywords
        try:
            file_reader = open(os.path.join(input_dir, file_name + '.key'), 'r+')
        except FileNotFoundError:
            open(os.path.join(input_dir, file_name + '.key'), 'a+')
            file_reader = open(os.path.join(input_dir, file_name + '.key'), 'r+')
        manual_keywords = file_reader.read()
        for line in manual_keywords.split('\n'):
            line = line.strip().lower()
            if len(line) > 0:
                if '\t' in line:
                    d.keywords.append(line[0:line.find('\t')])
                else:
                    d.keywords.append(line)

        # add document to test set
        test_set[file_name] = d

    return test_set
