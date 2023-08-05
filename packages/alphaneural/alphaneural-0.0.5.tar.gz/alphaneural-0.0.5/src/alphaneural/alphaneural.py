import pandas as pd
import numpy as np
import time
from termcolor import colored
import fire
pd.options.mode.chained_assignment = None  # default='warn'
# Read in the data from the csv file

class seekAlpha:
    def __init__(self,ohlcvdata):
        self.ohlcvdata = ohlcvdata
        self.data = self.ohlcvdata
    def preprocess(self):
        # Reduce the column names to lower case
        df = self.ohlcvdata
        df.columns = map(str.lower, df.columns)
        # compute the change to use as a guide in backtesting
        df['change'] = df['close'] - df['open']
        # populate the classifier
        df['ind'] = (df['high']/df['open']) -1
        # Initialize the weights
        param = np.linspace(-6,6,len(self.data))
        df['param'] = param
        #print(df.head())
        return df

    # Fire the neural network
    def train(self):
        eta = 0
        dub = []
        try:
            while eta < 100:
                for i in self.preprocess().param:
                    alpha = 1/(1+np.exp(-i))
                    test = self.data[self.data['ind'] >= alpha]
                    if len(test) > 0:
                        pos = test[test['change'] > 0]
                        eta = len(pos)*100/len(test)
                        if eta >= 100:
                            opt = (i,alpha,len(test),eta)
                            dub.append(opt)
                    else:
                        pass
            else:
                pass
        except Exception as e:
            print(e)

        return dub


def alpha_param(ohlcvdata,source):
    try:
        if source == 'file':
            df = pd.read_csv(f'{ohlcvdata}')
            return seekAlpha(df).train()[0][1]
        elif source == 'mem':
            df = ohlcvdata
            return seekAlpha(df).train()[0][1]
        else:
            print('invalid datatype and/or source')
    except Exception as e:
        print(e)

if __name__ == '__main__':
    fire.Fire(alpha_param)
