from os import listdir
from os.path import isfile, join
import pandas as pd

IS_TEST = True
TEST_NUM = 100

class Utilities:
    def __init__(self, is_test, test_num):
        self.is_test = is_test
        self.num_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
        self.test_num = test_num

    def get_all_files_in_dir(self, dir_name):
        fnames = [join(dir_name, f) for f in listdir(dir_name) if isfile(join(dir_name, f))]
        return fnames[:self.test_num if self.is_test else len(fnames)]
    
    def get_dataframes(self, dir_name):
        dfs = []
        for fname in self.get_all_files_in_dir(dir_name):
            try:
                df = pd.read_csv(fname)
                if len(df) < 300: continue
                df['Date'] = pd.to_datetime(df['Date'])
                for nc in self.num_cols:
                    if (df[nc] == 0).any():
                        raise Exception("zero price")
                    df[nc] = pd.to_numeric(df[nc])
                df.drop(columns='OpenInt', inplace=True)
                df['Date'] = pd.to_datetime(df['Date'])
                df.set_index('Date', inplace=True)
                df.name = fname.split('/')[-1].split('.')[0].upper()
                dfs.append(df)
            except Exception as e:
                pass # ignore invalid/empty files
                # print(e)
        return dfs