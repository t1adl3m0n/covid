import datetime
import matplotlib as mpl
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
mpl.colors.Colormap('rainbow')
df = pd.read_csv('D:/data/covid/CO_20200522/patternCount.csv')
df.DATE=pd.to_datetime(df.DATE, errors='raise', dayfirst=False, yearfirst=True, utc=None, format=None, exact=True, unit=None, infer_datetime_format=False, origin='unix', cache=True)
    
fig, ax = plt.subplots()
locator = mdates.AutoDateLocator()
formatter = mdates.ConciseDateFormatter(locator)
ax.xaxis.set_major_locator(locator)
ax.xaxis.set_major_formatter(formatter)
    
ax.plot(df.DATE, df.COUNT)
ax.set_title('Concise Date Formatter')