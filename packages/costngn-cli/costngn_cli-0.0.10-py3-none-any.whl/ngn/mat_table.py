import numpy as np
#import pandas as pd
from matplotlib import pyplot as plt
plt.rcParams["figure.figsize"] = [5.00, 3.50]
plt.rcParams["figure.autolayout"] = False
#pd.set_option('display.max_columns', None);pd.set_option('display.max_colwidth', None)
#fig, axs = plt.subplots(1, 1)
fig, axs = plt.subplots(figsize=(5, 4))



#fig.tight_layout() #
#fig.patch.set_visible(False) #
data = np.random.random((10, 3))
columns = ("Column I", "Column II", "Column III")
#axs.axis('tight')
axs.axis('off')
the_table = axs.table(cellText=data, colLabels=columns, loc='center')
plt.autoscale(enable=False, axis='both', tight=True)
plt.show()
#plt.plot()