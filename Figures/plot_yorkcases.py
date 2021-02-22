import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime

#Medium-risk case (Thank you Arthur for tidying it up)
york_data= pd.read_csv('York_clean.csv')
york_data= york_data.dropna()

#Standard-risk case
york_s_raw= pd.read_csv('york_standard.csv')

#High-risk case
york_h= pd.read_csv('kpi-marac01-high-risk.csv')

#Reported domestic violence case to city of York police
york_reports= pd.read_csv('kpi-csp51-domestic-violence-reports.csv')

month_list = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

york_reports.drop(columns=['KpiName', 'KpiId', 'CollectionFrequency', 'DataType'],inplace=True)
york_reports['Value'] = york_reports['Value'].str.split(' ', expand=True)[0]
york_reports['Value'][york_reports['Value']=='NC']=np.nan
york_reports['Value'][york_reports['Value']=='nan']= np.nan
york_reports['Value'] = york_reports['Value'].astype(float)
york_reports= york_reports[np.array([york_reports['Period'].str.contains(monthString) for monthString in month_list]).T.sum(axis=1)==1]
york_reports['Period']= york_reports['Period'].str.split('_', expand=True)[1]
york_reports=york_reports.dropna()

incident_date_yr= york_reports.StartDate
incident_year_yr= pd.DatetimeIndex(incident_date_yr).year

#Calculate yearly mean
ymean_yr= york_reports.groupby(incident_year_yr)['Value'].transform('mean')
yealy_ave=ymean_yr.unique()
iyear= incident_year_yr.unique()

from datetime import date
dates_yr=[]
dates_yt=[]
for yd in york_reports.StartDate:
    dd=datetime.datetime.strptime(yd, '%Y-%m-%d')
    dtd= datetime.datetime.toordinal(dd)
    dates_yr.append( dd)
    dates_yt.append(dtd)

sm=[]
for y in range(len(iyear)):
    sm.append(date(iyear[y],6,1))

#Plot the figure
plt.figure()
plt.title('Number of Reported Domestic Violence case')
plt.plot(dates_yr, york_reports.Value)
plt.plot(sm, yealy_ave,'r*', linestyle='-', label='yearly average')
plt.legend(loc='best')

## Clean standard data
york_data['Period'] = york_data['Period'].str.split('_', expand=True)[1]#.astype(float)
york_s_raw.drop(columns=['KpiName', 'KpiId', 'CollectionFrequency', 'DataType'],inplace=True)
york_s_raw['Value'] = york_s_raw['Value'].str.split(' ', expand=True)[0]#.astype(float)
york_s_raw['Value'][york_s_raw['Value']=='NC']= np.nan
york_s_raw['Value'][york_s_raw['Value']=='nan']= np.nan
york_s_raw['Value'] = york_s_raw['Value'].astype(float)
york_s_raw= york_s_raw[np.array([york_s_raw['Period'].str.contains(monthString) for monthString in month_list]).T.sum(axis=1)==1]

## Clean high risk data
york_h.drop(columns=['KpiName', 'KpiId', 'CollectionFrequency', 'DataType'],inplace=True)
york_h['Value'] = york_h['Value'].str.split(' ', expand=True)[0]#.astype(float)
york_h['Value'][york_h['Value']=='NC']= np.nan
york_h['Value'][york_h['Value']=='nan']= np.nan
york_h['Value'] = york_h['Value'].astype(float)
york_h= york_h[np.array([york_h['Period'].str.contains(monthString) for monthString in month_list]).T.sum(axis=1)==1]

# only include between 2011-2015
start_date = "2010-12-31"
end_date = "2015-12-31"

after_start_date = york_overall["StartDate"] >= start_date
before_end_date = york_overall["StartDate"] <= end_date
between_two_dates = after_start_date & before_end_date
york_overall_filt = york_overall.loc[between_two_dates]
york_overall_filt['Period']= york_overall_filt['Period'].str.split('_', expand=True)[1]

after=york_s_raw["StartDate"]  >= start_date
before= york_s_raw["StartDate"] <= end_date
between_tro_dates= after & before
york_s_rawfilt= york_s_raw.loc[between_tro_dates]

york_s_rawfiltp= york_s_rawfilt['Period'].str.split('_', expand=True)[1]
york_s_rawfilt['Period']= york_s_rawfiltp

york_s_rawfilt= york_s_rawfilt.dropna()


aft=york_h["StartDate"]>= start_date
bef=york_h["StartDate"]<= end_date
ibt= aft & bef
york_hfilt= york_h.loc[ibt]
temp= york_hfilt['Period'].str.split('_', expand=True)[1]
york_hfilt['Period']= temp
york_hfilt= york_hfilt.dropna()

aft=york_reports["StartDate"]>= "2014-12-31"
bef=york_reports["StartDate"]<= "2018-12-31"
ibt= aft & bef
york_reportsf= york_reports.loc[ibt]

incident_date_yr= york_reportsf.StartDate
incident_month_yr= pd.DatetimeIndex(incident_date_yr).month
incident_year_yr= pd.DatetimeIndex(incident_date_yr).year

ymean_yr= york_reportsf.groupby(incident_year_yr)['Value'].transform('mean')
ymean_yr= ymean_yr.to_numpy()
# percentage increase
print('%increase of reported case=', (ymean_yr[-1]-ymean_yr[0])/(ymean_yr[0])*100)


incident_date_ym= york_data.StartDate
incident_month_ym= pd.DatetimeIndex(incident_date_ym).month
incident_year_ym= pd.DatetimeIndex(incident_date_ym).year

ymean= york_data.groupby(incident_year_ym)['Value'].transform('mean')
ymean= ymean.to_numpy()
# percentage increase
print('%increase=', (ymean[-1]-ymean[0])/(ymean[0])*100)



incident_year_ys= pd.DatetimeIndex(york_s_rawfilt.StartDate).year
incident_month_ys= pd.DatetimeIndex(york_s_rawfilt.StartDate).month

ysmean= york_s_rawfilt.groupby(incident_year_ys)['Value'].transform('mean')
ysmean= ysmean.to_numpy()
# percentage increase
print('%increase standard case=', (ysmean[-1]-ysmean[0])/(ysmean[0])*100)


dates_yd=[]
dates_td=[]
for yd in york_data.StartDate:
    dd=datetime.datetime.strptime(yd, '%Y-%m-%d')
    dtd= datetime.datetime.toordinal(dd)
    dates_yd.append(dd)
    dates_td.append(dtd)

dates_yr=[] 
dates_tr=[]
for ys in york_reportsf.StartDate:
    ds=datetime.datetime.strptime(ys, '%Y-%m-%d')
    dts= datetime.datetime.toordinal(ds)
    dates_yr.append(ds)
    dates_tr.append(dts)
    
dates_ys=[] 
dates_ts=[]
for ys in york_s_rawfilt.StartDate:
    ds=datetime.datetime.strptime(ys, '%Y-%m-%d')
    dts= datetime.datetime.toordinal(ds)
    dates_ys.append(ds)
    dates_ts.append(dts)

dates_hs=[] 
for yh in york_hfilt.StartDate:
    dates_hs.append( datetime.datetime.strptime(yh, '%Y-%m-%d'))
    
# correlation 
print(np.corrcoef(reported_case,  dates_td))
print(np.corrcoef(reported_case_ys,  dates_ts))
print(np.corrcoef(reported_case_yr,  dates_tr))

plt.figure()
ax=plt.subplot(211)
plt.title('Domestic violence case')
ax.plot(dates_ys, reported_case_ys, label='Standard')
ax.plot(dates_yd, reported_case, label='Medium')
ax.plot(dates_hs, york_hfilt.Value, label= 'High')
ax.legend(loc='best')
ax.xaxis.set_major_locator(years)
ax.xaxis.set_major_formatter(years_fmt)
ax.xaxis.set_minor_locator(months)

plt.subplot(212)
width=0.5
p1= plt.bar(york_s_rawfilt.Period, reported_case_ys, label= 'Standard')
p2= plt.bar(york_data.Period,reported_case, width, label= 'Medium' )
p3= plt.bar(york_hfilt.Period, york_hfilt.Value, 0.3, label= 'High')
plt.legend(loc= 'best')
