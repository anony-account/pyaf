import pyaf.Bench.TS_datasets as tsds
import tests.artificial.process_artificial_dataset as art




art.process_dataset(N = 128 , FREQ = 'D', seed = 0, trendtype = "MovingAverage", cycle_length = 0, transform = "RelativeDifference", sigma = 0.0, exog_count = 20, ar_order = 0);