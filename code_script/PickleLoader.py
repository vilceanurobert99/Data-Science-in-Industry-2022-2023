'''
@author: solomon
@date: 28-01-2023
'''


import pickle

class PickleStore(object):
    def __int__(self):
        pass

    # write list to binary file
    def write_list(self, file_path, a_list):
        # store list in binary file so 'wb' mode
        with open(file_path, 'wb') as fp:
            pickle.dump(a_list, fp)
            print('Done writing list into a binary file')

    # Read list to memory
    def read_list(self, file_path):
        # for reading also binary mode is important
        with open(file_path, 'rb') as fp:
            n_list = pickle.load(fp)
            return n_list