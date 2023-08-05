# Machine Learning Evx

This is a simplified version of [alphaneural](https://towardsdatascience.com/a-financial-neural-network-for-quants-45ec0aaef73c) package used to generate buy and sell signals for crypto and conventional stock markets based on the above article on medium.

# Installation
Install alphaneural with `python3 -m pip install alphaneural`  
# Usage

In your python script simply import the module and use as follows:

```  
from alphaneural.alphaneural import alpha_param
print(apha_param(df,'mem'))
```
The above methods take OHCLV data and the option to specifiy the file path as 'file' or in memory saved variable 'mem'. This will result in a single parameter  
named alpha.   

# Testing an entire dataframe
Testing of a dataframe for correct buy, sell signals is as simple as applying the lambda function as follows:  

```
import pandas as pd
from alphaneural import alpha_param

df = pd.read_csv('../../../path/to_your.csv')

def getEnterSignal(data,src):
    alpha = alpha_param(data,f'{src}')
    return alpha

mainsig = getEnterSignal(df,'mem')

df['sig'] = df['alpha'].apply(lambda x: 1 if x < mainsig else 0)

```
Alphaneural can be applied to a file as follows:
```
from alphaneural import alpha_param  
alpha = alpha_param('../../../path/to_your.csv','file')
```

# Warning
This is not financial advise. Alphaneural is entirely on its preliminary stages. Use it at your own risk.