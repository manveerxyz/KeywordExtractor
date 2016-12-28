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

    def run(self):
        # Get command line arguments and initialize test_dir with directory
        self.init_arguments()
        self.test_dir = self.args.directory

        # Get test_set by calling read_data from test_data.py
        test_set = test_data.read_data(self.test_dir)

        for test_doc in test_set.values():
            # Initially creates a .key file from default rake and adds default keywords to the file
            self.get_keywords_for_key_file(test_doc)
            # Gets optimum parameters by using .key file created in previous step, and creates
            # a rake object using these parameters
            self.get_final_keywords(test_doc, test_set)

        print('Keywords will be stored in a .key file with the same name as the input file.')

    def get_keywords_for_key_file(self, test_doc):
        """
        In order to get optimum parameters,
        there needs to be a .key file to compare results to.
        This function accomplishes that.
        :param test_doc: document to extract keywords from
        """

        # Create a default rake for getting initial keywords
        rake_test = rake.Rake('SmartStoplist.txt')

        # Get keywords and open .key file
        keywords = rake_test.run(test_doc.text)
        key_file = open(os.path.join(self.test_dir, test_doc.name + '.key'), 'w')

        # Add significant keywords to .key file
        for keyword in keywords:
            if keyword[1] > 1.0:
                key_file.write(keyword[0] + '\n')
        key_file.close()

    def get_final_keywords(self, test_doc, test_set):
        """
        Gets optimum parameters and initializes a rake object using them.
        Gets keywords and add them to the .key file under the same name as test_doc
        :param test_doc: document to extract keywords from
        :param test_set: set of documents
        """

        # Gets optimum parameters for document
        best_params = optimize_rake.get_best_params(test_doc, test_set)
        # Initializes rake object using optimized parameters
        rake_object_final = rake.Rake('SmartStoplist.txt',
                                      best_params[0],
                                      best_params[1],
                                      best_params[2])

        # Get keywords and opens .key file
        keywords = rake_object_final.run(test_doc.text)
        key_file = open(os.path.join(self.test_dir, test_doc.name + '.key'), 'w')

        # Add keywords to .key file along with scores
        for keyword in keywords:
            key = keyword[0]
            score = str(round(keyword[1], 1))
            key_file.write(key + '.'*(30-len(key)) + score + '\n')

    def init_arguments(self):
        """
        Get command line arguments
        """
        parser = argparse.ArgumentParser(description='Extract keywords from subtitle files.')
        parser.add_argument('directory',
                            help='Directory containing subtitle files to extract keywords from')

        # Assign passed arguments to class variable
        self.args = parser.parse_args()

if __name__ == "__main__":
    extractor = KeywordExtractor()
    extractor.run()