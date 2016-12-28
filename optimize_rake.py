from __future__ import absolute_import
from __future__ import print_function
import rake


def get_best_params(test_doc, test_set):
    best_fmeasure = 0
    best_vals = []

    for min_char_length in range(3, 8):
        for max_words_length in range(3, 6):
            for min_keyword_frequency in range(1, 7):

                rake_object = rake.Rake('SmartStoplist.txt', min_char_length, max_words_length, min_keyword_frequency)
                total_fmeasure = 0
                keywords = rake_object.run(test_doc.text)

                num_manual_keywords = len(test_doc.keywords)
                correct = 0
                try:
                    for i in range(0, min(3, len(keywords))):
                        if keywords[i][0] in set(test_doc.keywords):
                            correct += 1
                except IndexError:
                    print('Problem with evaluating ', keywords)

                precision = correct / float(3)
                recall = correct / float(num_manual_keywords)

                if precision > 0 and recall > 0:
                    total_fmeasure += 2 * precision * recall / (precision + recall)

                avg_fmeasure = round(total_fmeasure * 100 / float(len(test_set)), 2)

                if avg_fmeasure > best_fmeasure:
                    best_fmeasure = avg_fmeasure
                    best_vals = [min_char_length, max_words_length, min_keyword_frequency]

    return best_vals
