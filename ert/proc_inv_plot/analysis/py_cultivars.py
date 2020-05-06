import pandas as pd
import numpy as np

# cultivars names
cf = 1
cn = 10
cn_range = range(cf, cf + cn)
cn_names = ['C{:02d}'.format(i) for i in cn_range]

# cultivars names
sf = 1
sn = 11
sn_range = range(sf, sf + sn)
sn_names = ['S{:02d}'.format(i) for i in sn_range]

# coordinates

## size
c_l = 1.4
s_l = 1.5
t_l = c_l + s_l
## start
c_1s = 1.5
## end 
c_ls = c_1s + ((cn - 1) * t_l)
## numpy
c_1s = np.around(c_1s, 2)
c_ls = np.around(c_ls, 2)
c_s = np.arange(c_1s, c_ls + t_l, t_l)
c_c = c_s + (c_l / 2)
c_e = c_s + c_l
print(c_s)
print(c_c)
print(c_e)
## spaces
s_1s = c_1s - s_l  # one space before first plot of plants 
s_ls = c_ls + c_l # one space after last plot of plants
s_s = np.arange(s_1s, s_ls + t_l, t_l)
s_c = s_s + (s_l / 2)
s_e = s_s + s_l
print(s_s)
print(s_c)
print(s_e)

## pandas
cnp = {'name': cn_names, 'type': 'crop', 'xmin': c_s, 'xmax': c_e}
cdf = pd.DataFrame(cnp)
snp = {'name': sn_names, 'type': 'space', 'xmin': s_s, 'xmax': s_e}
sdf = pd.DataFrame(snp)
df = pd.concat([cdf, sdf])
df = df.set_index('name')
df['ymin'] = -0.80
df['ymax'] = 0
df['zmin'] = np.nan
df['zmax'] = np.nan
df = df.round(2)
print(df)
df.to_csv('plant_plots.csv')

