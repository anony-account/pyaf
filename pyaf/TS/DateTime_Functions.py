# Copyright (C) 2016 Antoine Carme <Antoine.Carme@Laposte.net>
# All rights reserved.

# This file is part of the Python Automatic Forecasting (PyAF) library and is made available under
# the terms of the 3 Clause BSD license

import pandas as pd
import numpy as np
from enum import IntEnum

from . import Utils as tsutil

class eDatePart(IntEnum):
    Second = 1
    Minute = 2
    Hour = 3
    DayOfWeek = 4
    DayOfMonth = 5
    MonthOfYear = 6
    WeekOfYear = 7
    DayOfYear = 8

class eTimeResolution(IntEnum):
    NONE = 0
    SECOND = 1
    MINUTE = 2
    HOUR = 3
    DAY = 4
    MONTH = 5
    YEAR = 6
    
    
class cDateTime_Helper:

    def __init__(self):
        pass

    
    def apply_date_time_computer(self, iDatePart, series):
        lOut = None
        if(iDatePart == eDatePart.Second):
            lOut = series.dt.second
        elif(iDatePart == eDatePart.Minute):
            lOut = series.dt.minute
        elif(iDatePart == eDatePart.Hour):
            lOut = series.dt.hour
        elif(iDatePart == eDatePart.DayOfWeek):
            lOut = series.dt.dayofweek
        elif(iDatePart == eDatePart.DayOfMonth):
            lOut = series.dt.day
        elif(iDatePart == eDatePart.DayOfYear):
            lOut = series.dt.dayofyear
        elif(iDatePart == eDatePart.MonthOfYear):
            lOut = series.dt.month
        elif(iDatePart == eDatePart.WeekOfYear):
            lOut = series.dt.week
        if(lOut is None):
            print("apply_date_time_computer_failures" , iDatePart)
        assert(lOut is not None)
        return lOut

    def guess_time_resolution(self, iEstimTime):
        lEstimSecond = self.apply_date_time_computer(eDatePart.Second, iEstimTime)
        if(lEstimSecond.nunique() > 1.0):
            return eTimeResolution.SECOND;
        lEstimMinute = self.apply_date_time_computer(eDatePart.Minute, iEstimTime)
        if(lEstimMinute.nunique() > 1.0):
            return eTimeResolution.MINUTE;
        lEstimHour = self.apply_date_time_computer(eDatePart.Hour, iEstimTime)
        if(lEstimHour.nunique() > 1.0):
            return eTimeResolution.HOUR;
        lEstimDayOfMonth = self.apply_date_time_computer(eDatePart.DayOfMonth, iEstimTime)
        if(lEstimDayOfMonth.nunique() > 1.0):
            return eTimeResolution.DAY;
        lEstimMonth = self.apply_date_time_computer(eDatePart.MonthOfYear, iEstimTime)
        if(lEstimMonth.nunique() > 1.0):
            return eTimeResolution.MONTH;
        # fallback
        return eTimeResolution.YEAR;

    
    def get_lags_for_time_resolution(self):
        if(not self.isPhysicalTime()):
            return None;
        lARORder = {}
        lARORder[eTimeResolution.SECOND] = 60
        lARORder[eTimeResolution.MINUTE] = 60
        lARORder[eTimeResolution.HOUR] = 24
        lARORder[eTimeResolution.DAY] = 31
        lARORder[eTimeResolution.MONTH] = 12
        return lARORder.get(self.mResolution , None)


    def adaptTimeDeltaToTimeResolution(self, iResolution, iTimeDelta):
        if(eTimeResolution.SECOND == iResolution):
            lTimeDelta = pd.DateOffset(seconds=round(iTimeDelta / np.timedelta64(1,'s')))
            return lTimeDelta
        if(eTimeResolution.MINUTE == iResolution):
            lTimeDelta = pd.DateOffset(minutes=round(iTimeDelta / np.timedelta64(1,'m')))
            return lTimeDelta
        if(eTimeResolution.HOUR == iResolution):
            lTimeDelta = pd.DateOffset(hours=round(iTimeDelta / np.timedelta64(1,'h')))
            return lTimeDelta
        if(eTimeResolution.DAY == iResolution):
            lTimeDelta = pd.DateOffset(days=round(iTimeDelta / np.timedelta64(1,'D')))
            return lTimeDelta
        if(eTimeResolution.MONTH == iResolution):
            lTimeDelta = pd.DateOffset(months=round(iTimeDelta // np.timedelta64(30,'D')))
            return lTimeDelta
        if(eTimeResolution.YEAR == iResolution):
            lTimeDelta = pd.DateOffset(months=round(iTimeDelta // np.timedelta64(365,'D')))
            return lTimeDelta
        pass
    
    
    def get_beginning_of_period(self, iPeriod, x):
        # iPeriod can be "H" (hour), "D" (day), etc
        # https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#timeseries-offset-aliases
        return x.to_period(iPeriod).start_time

    
    def computeTimeFrequency_in_seconds(self, iTime):
        lTimeBefore = iTime.shift(1);
        lDiffs = iTime[1:] - lTimeBefore[1:]
        lDelta = np.min(lDiffs);
        return lDelta.total_seconds()
