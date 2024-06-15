# %%
# https://github.com/TeoMeWhy/teomerefs
import pandas as pd

# %%
dt = pd.read_excel(r'D:\github\py_codes\pandas_weight_data.xls')
dt.head()
dt.columns
dt.info(memory_usage='deep')
dt.shape

# %%
dt['date'].iloc[3]
dt.iloc[3]

dt.loc[3]

dt.describe()

# %%
filtro_abaixo_media = dt['body_weight_kg'] < dt['body_weight_kg'].mean()
dt_low_weight = dt[filtro_abaixo_media]
dt_low_weight.head()

# %%
filtro_no_outliers = (dt['body_weight_kg'] > 68) & (dt['body_weight_kg'] < 70)
dt_no_outliers = dt[filtro_no_outliers]
dt_no_outliers.head()

# %%
dt['imc'] = round(dt['body_weight_kg'] / (1.78 ** 2), 2)
dt.head()

# %% 
# https://www.uptodate.com/contents/calculator-body-mass-index-bmi-for-adults-metric-patient-education
def classes_imc(imc):
    if imc < 18.5:
        return 'Under weight'
    elif imc < 24.9:
        return 'Healthy weight'
    elif imc < 29.9:
        return 'Overweight'
    else:
        return 'Obese'

dt['imc_class'] = dt['imc'].apply(classes_imc)
dt.sample(10)

# %%
nmb_hw = len(dt[dt['imc_class']=='Healthy weight'])
print('Number of healthy weight registered:', nmb_hw, 'out of 647 days.', )

# %%
dt[['date', 'body_weight_kg']].groupby(pd.Grouper(key='date', axis=0, freq='Y')).mean()

# %%
month_wb = dt[['date', 'body_weight_kg']].groupby(pd.Grouper(key='date', axis=0, freq='M')).mean()
ax = month_wb.plot(kind = 'line', style='*:r')
dt.plot(x='date', y='body_weight_kg', kind = 'scatter', ax=ax)

# %%
dt.plot(x='date', y='body_weight_kg', kind = 'scatter')

# %%
dt.plot(x='date', y='body_weight_kg', kind = 'hist')

# %%
dt.plot(x='date', y='body_weight_kg', kind = 'box')

# %%
dt['diff_days'] = dt['date'].diff()
dt.sample(10)
# %%
dt[dt['diff_days']<pd.Timedelta(0, units='Days')]

# %%
oneday_wdiff = dt[dt['diff_days']==pd.Timedelta(1, unit='Days')]
oneday_wdiff.sample(10)
# %%
oneday_wdiff['weight_daily_diff'] = oneday_wdiff['body_weight_kg'].diff()
oneday_wdiff.sample(10)
# %%
oneday_wdiff.plot(x='date', y='weight_daily_diff', kind = 'hist')
# %%
oneday_wdiff['weight_daily_diff'].plot(kind = 'box')
# %%
oneday_wdiff['weight_daily_diff'].describe()