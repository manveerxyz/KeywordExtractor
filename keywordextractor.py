#!/usr/bin/python3

import os
import argparse
import rake
import test_data
import optimize_rake


class KeywordExtractor:
    def __init__(self):
        self.test_dir = None
        self.args = None
        self.rake_test = None

    def run(self):
        self.init_arguments()
        self.test_dir = self.args.directory

        test_set = test_data.read_data(self.test_dir)
        self.rake_test = rake.Rake('SmartStoplist.txt')

        for test_doc in test_set.values():
            self.get_keywords_for_key_file(test_doc)
            self.get_final_keywords(test_doc)

        print('Keywords will be stored in a .key file with the same name as the input file.')

    def get_keywords_for_key_file(self, test_doc):
        keywords = self.rake_test.run(test_doc.text)
        key_file = open(os.path.join(self.test_dir, test_doc.name + '.key'), 'w')

        for keyword in keywords:
            if keyword[1] > 1.0:
                key_file.write(keyword[0] + '\n')
        key_file.close()

    def get_final_keywords(self, test_doc):
        best_params = optimize_rake.get_best_params(self.test_dir)
        rake_object_final = rake.Rake('SmartStoplist.txt',
                                      best_params[0],
                                      best_params[1],
                                      best_params[2])

        keywords = rake_object_final.run(test_doc.text)
        key_file = open(os.path.join(self.test_dir, test_doc.name + '.key'), 'w')

        for keyword in keywords:
            key = keyword[0]
            score = str(round(keyword[1], 1))
            key_file.write(key + '.'*(30-len(key)) + score + '\n')

    def init_arguments(self):
        parser = argparse.ArgumentParser(description='Extract keywords from subtitle files.')
        parser.add_argument('directory',
                            help='Directory containing subtitle files to extract keywords from')

        self.args = parser.parse_args()

if __name__ == "__main__":
    extractor = KeywordExtractor()
    extractor.run()