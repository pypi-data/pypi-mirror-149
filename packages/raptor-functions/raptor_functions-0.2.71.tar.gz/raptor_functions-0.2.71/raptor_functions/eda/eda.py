# !pip install raptor_functions pandas_profiling
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from raptor_functions.datasets import get_data




# import ssl
# ssl._create_default_https_context = ssl._create_unverified_context
#
df = get_data()
#
from pandas_profiling import ProfileReport
profile = ProfileReport(df, title="Pandas Profiling Report", explorative=True)
profile.to_file("pandas_profiling_report.html")



import sweetviz as sv
my_report = sv.analyze(df)
my_report.show_html() # Default arguments will generate to "SWEETVIZ_REPORT.html"



from autoviz.AutoViz_Class import AutoViz_Class
AV = AutoViz_Class()

import nltk
nltk.download('wordnet')

_ = AV.AutoViz('df.csv')




import dtale
import dtale.app as dtale_app
# dtale_app.USE_COLAB = True
dtale_app.USE_NGROK = True
dtale.show(df)