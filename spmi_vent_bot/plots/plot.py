import datetime
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

x=[]
y = []
for i in range(100):
    t = (datetime.datetime.now() + datetime.timedelta(hours=i)).strftime("%H:%M:%S")
    x.append(t)
    y.append(i*i)

xy = pd.DataFrame({"x":x, "y":y})
xy.plot(x="x", y="y", kind='line')
plt.show()