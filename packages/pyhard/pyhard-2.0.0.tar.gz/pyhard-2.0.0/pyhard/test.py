import time
from pathlib import Path

import pandas as pd

from pyhard.feature_selection import filtfeat


exp_path = Path(__file__).parent / "../experiments"
experiment = 'hospitalization'

df_meta = pd.read_csv(exp_path / f'{experiment}/metadata.csv', index_col='instances')
df_ih = pd.read_csv(exp_path / f'{experiment}/ih.csv', index_col='instances')

X = df_meta.filter(regex='^feature_').values
y_algo = df_meta.filter(regex='^algo_').values
y = df_ih.values

start = time.time()
s = filtfeat(X, y, method='IT', standardize=False, fit_method='average', n_splits=10, n_jobs=-1)
end = time.time()
delta = end - start
print(delta, 's')
