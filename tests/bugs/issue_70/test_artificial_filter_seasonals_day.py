
import pyaf.ForecastEngine as autof
import pyaf.Bench.TS_datasets as tsds




b1 = tsds.generate_random_TS(N = 4000 , FREQ = 'D', seed = 0, trendtype = "constant", cycle_length = 24, transform = "None", sigma = 0.1, exog_count = 0);

df = b1.mPastData

lEngine = autof.cForecastEngine()
lEngine

H = 12;
lEngine.mOptions.mFilterSeasonals = True;
lEngine.mOptions.mParallelMode = False;
lEngine.mOptions.mDebugPerformance = True;
lEngine.train(df , b1.mTimeVar , b1.mSignalVar, H);
lEngine.getModelInfo();
print(lEngine.mSignalDecomposition.mTrPerfDetails.head());

