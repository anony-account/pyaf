import pandas as pd
import numpy as np
import pyaf.HierarchicalForecastEngine as hautof
import pyaf.Bench.TS_datasets as tsds

import datetime

#get_ipython().magic('matplotlib inline')

b1 = tsds.load_AU_infant_grouped_dataset();


def create_exog_data(b1):
    # fake exog data based on date variable
    lDate1 = b1.mPastData['Index']
    lDate2 = b1.mFutureData['Index'] # not needed. exogenous data are missing when not available.
    lDate = lDate1.append(lDate2)
    lExogenousDataFrame = pd.DataFrame()
    lExogenousDataFrame['Index'] = lDate
    lExogenousDataFrame['Index_ex1'] = lDate * lDate
    lExogenousDataFrame['Index_ex2'] = lDate.apply(str)
    lExogenousVariables = [col for col in lExogenousDataFrame.columns if col.startswith('Index_')]
    lExogenousData = (lExogenousDataFrame , lExogenousVariables) 
    return lExogenousData


df = b1.mPastData;

lEngine = hautof.cHierarchicalForecastEngine()
lEngine.mOptions.mHierarchicalCombinationMethod =  ["BU" , 'TD' , 'MO' , 'OC'];
lEngine.mOptions.mNbCores = 16
lEngine

H = b1.mHorizon;

# lEngine.mOptions.enable_slow_mode();
# lEngine.mOptions.mDebugPerformance = True;
lExogenousData = create_exog_data(b1)
lEngine.train(df , b1.mTimeVar , b1.mSignalVar, H, b1.mHierarchy, lExogenousData);

lEngine.getModelInfo();
#lEngine.standardPlots("outputs/AU_infant_");

dfapp_in = df.copy();
dfapp_in.tail()

dfapp_out = lEngine.forecast(dfapp_in, H);
#dfapp_out.to_csv("outputs/Grouped_AU_apply_out.csv")
