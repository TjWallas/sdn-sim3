import csv
import re

import wekatools


class AttributeImpactRecallValue:
    def __init__(self, train_arff, test_arff):
        self.train_arff = train_arff
        self.test_arff = test_arff
        self.attributes_full = ['1minDNSDownCount','2minDNSDownCount','4minDNSDownCount','8minDNSDownCount','16minDNSDownCount','32minDNSDownCount','64minDNSDownCount','1minDNSUpCount','2minDNSUpCount','4minDNSUpCount','8minDNSUpCount','16minDNSUpCount','32minDNSUpCount','64minDNSUpCount','1minNTPDownCount','2minNTPDownCount','4minNTPDownCount','8minNTPDownCount','16minNTPDownCount','32minNTPDownCount','64minNTPDownCount','1minNTPUpCount','2minNTPUpCount','4minNTPUpCount','8minNTPUpCount','16minNTPUpCount','32minNTPUpCount','64minNTPUpCount','1minDNSDownRate','2minDNSDownRate','4minDNSDownRate','8minDNSDownRate','16minDNSDownRate','32minDNSDownRate','64minDNSDownRate','1minDNSUpRate','2minDNSUpRate','4minDNSUpRate','8minDNSUpRate','16minDNSUpRate','32minDNSUpRate','64minDNSUpRate','1minNTPDownRate','2minNTPDownRate','4minNTPDownRate','8minNTPDownRate','16minNTPDownRate','32minNTPDownRate','64minNTPDownRate','1minNTPUpRate','2minNTPUpRate','4minNTPUpRate','8minNTPUpRate','16minNTPUpRate','32minNTPUpRate','64minNTPUpRate','1minLANDownCount','2minLANDownCount','4minLANDownCount','8minLANDownCount','16minLANDownCount','32minLANDownCount','64minLANDownCount','1minLANDownRate','2minLANDownRate','4minLANDownRate','8minLANDownRate','16minLANDownRate','32minLANDownRate','64minLANDownRate','1minANYWANDownCount','2minANYWANDownCount','4minANYWANDownCount','8minANYWANDownCount','16minANYWANDownCount','32minANYWANDownCount','64minANYWANDownCount','1minANYWANDownRate','2minANYWANDownRate','4minANYWANDownRate','8minANYWANDownRate','16minANYWANDownRate','32minANYWANDownRate','64minANYWANDownRate','1minANYWANUpCount','2minANYWANUpCount','4minANYWANUpCount','8minANYWANUpCount','16minANYWANUpCount','32minANYWANUpCount','64minANYWANUpCount','1minANYWANUpRate','2minANYWANUpRate','4minANYWANUpRate','8minANYWANUpRate','16minANYWANUpRate','32minANYWANUpRate','64minANYWANUpRate','1minSSDPUpCount','2minSSDPUpCount','4minSSDPUpCount','8minSSDPUpCount','16minSSDPUpCount','32minSSDPUpCount','64minSSDPUpCount','1minSSDPUpRate','2minSSDPUpRate','4minSSDPUpRate','8minSSDPUpRate','16minSSDPUpRate','32minSSDPUpRate','64minSSDPUpRate',]
        self.attributes_subset = ['32minDNSDownCount', '64minDNSDownCount', '16minDNSDownRate', '64minDNSDownRate', '8minDNSUpRate', '16minDNSUpRate', '32minDNSUpRate', '64minDNSUpRate', '64minNTPDownRate', '32minNTPUpRate', '64minNTPUpRate', '4minLANDownRate', '4minANYWANDownCount', '8minANYWANDownCount', '16minANYWANDownCount', '32minANYWANDownCount', '64minANYWANDownCount', '1minANYWANDownRate', '64minANYWANDownRate', '1minANYWANUPCount', '2minANYWANUPCount', '4minANYWANUPCount', '32minANYWANUPCount', '1minANYWANUPRate', '2minANYWANUPRate', '8minANYWANUPRate', '64minANYWANUPRate', '64minSSDPUpCount', '4minSSDPUpRate', '8minSSDPUpRate', '64minSSDPUpRate']

        self.full_attribute_lower = [x.lower() for x in self.attributes_full]


    def get_instance_id(self, attribute_list):
        indexlist = []

        attribute_list_lower = [x.lower() for x in attribute_list]

        for e_attribute in attribute_list_lower:
            indexlist.append(self.full_attribute_lower.index(e_attribute)+1)
        return indexlist

    def read_confusion_matrix(self,evauation_file):

        confusion_matrix = []

        with open(evauation_file, 'r') as fid:
            on_test = 0;
            for line in fid:

                if on_test == 0:
                    m = re.search("=== Error on test data ===", line)
                    if m is not None:
                        on_test = 1
                elif on_test == 1:
                    m = re.search("^ *(\d+) +(\d+) +(\d+) +(\d+) +(\d+) +(\d+) +(\d+) +(\d+) +(\d+) +(\d+) +(\d+) +(\d+) +(\d+) +(\d+) +(\d+) +(\d+) +(\d+) \| +[a-z] = \d+$", line)
                    if m is not None:
                        conf_mapline = m.groups()
                        confusion_matrix.append([int(x) for x in conf_mapline])


        return confusion_matrix

    def get_precision_recall(self,confusion_matrix):
        import numpy as np
        cm = np.array(confusion_matrix)
        true_pos = np.diag(cm)
        false_pos = np.sum(cm, axis=0) - true_pos
        false_neg = np.sum(cm, axis=1) - true_pos


        device_precisions= true_pos/(true_pos + false_pos)
        device_precisions[np.isnan(device_precisions)] = 0
        precision = np.average(device_precisions)

        device_recalls=true_pos / (true_pos + false_neg)
        device_recalls[np.isnan(device_recalls)] = 0

        recall = np.average(device_recalls)
        return precision,recall

    def evaluate_attributes(self, selected_attributes_ids):
        attribute_full_index = range(1, len(self.full_attribute_lower) + 1)
        removed_attribute = [a_id for a_id in attribute_full_index if a_id not in selected_attributes_ids]

        removed_attribute_str = [str(x) for x in removed_attribute]

        print("removed_attributes: %s" % ','.join(removed_attribute_str))
        print("No of removed_attributes: %d" % len(removed_attribute_str))

        removed_attribute_str = ','.join(removed_attribute_str)
        weka_out = wekatools.classify_Randomforest_evaluation(self.train_arff, self.test_arff, './wekaout.tmp.txt',
                                                              removed_attribute_str)

        confusion_matrix = self.read_confusion_matrix('./wekaout.tmp.txt')
        precision,recall = self.get_precision_recall(confusion_matrix)
        accuracy,rrse = wekatools.findAccuracyRRSE('./wekaout.tmp.txt')
        return precision,recall,accuracy,rrse


if __name__ == "__main__":

    ai = AttributeImpactRecallValue('../weka_processing/arff_files/training-3month-include-feb.arff', '../weka_processing/arff_files/testing-3month-include-feb.arff')

    selected_attributes = ai.get_instance_id(ai.attributes_subset)
    print(selected_attributes)

    # exit()

    fid = open('./accuracyrrse.txt', 'w')
    spam_writer = csv.writer(fid, delimiter=' ')

    for i in range(1, len(selected_attributes) + 1):
        c_attributs = selected_attributes[0:i]
        precision, recall, accuracy, rrse = ai.evaluate_attributes(c_attributs)


        spam_writer.writerow([i, precision,recall,accuracy,rrse])

    fid.close()