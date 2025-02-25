# -*- coding: utf-8 -*-
"""solar.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1CyEJ4D0wb9a9IkxpT19M-gIBhNuCO7QF
"""

import pandas as pd
import numpy as np
from scipy import stats
from scipy.stats import spearmanr
from sklearn.preprocessing import LabelEncoder
import seaborn as sns
import matplotlib.pyplot as plt
from itertools import product
import datetime

"""# Подготовка датасета по солнечной активности

### Считываем и объединяем датасеты за 11 месяцев 2011 года
"""

files = ['ratyng_1.csv', 'ratyng_2.csv', 'ratyng_3.csv', 'ratyng_4.csv', 'ratyng_5.csv', 'ratyng_6.csv', 'ratyng_7.csv', 'ratyng_8.csv', 'ratyng_9.csv', 'ratyng_10.csv', 'ratyng_11.csv']
dfs = [pd.read_csv(file) for file in files]

final_df = pd.concat(dfs)
final_df

final_df.info()

"""### Добавляем id"""

from uuid import uuid4
final_df['uuid'] = final_df.index.to_series().map(lambda x: uuid4())
final_df.head()

new_df = final_df['date'].str.split(expand=True)
new_df.head()

new_df.columns=['1', '2', '3', '4', 'dey', 'month', 'year']
new_df.head()

final_df1 = pd.concat([final_df,new_df],axis=1)
final_df1.head()

"""### Удаление лишних столбцов"""

final_df1.drop(final_df1.columns[[0, 2, 3, 4, 5, 6]], axis=1, inplace=True)
final_df1.head()

"""### Меняем название месяца на цифровое представление"""

d = {'января': 1, 'февраля': 2, 'марта': 3, 'апреля': 4, 'мая': 5, 'июня': 6, 'июля': 7, 'августа': 8, 'сентября': 9, 'октября': 10, 'ноября': 11,}

final_df1.month = final_df1.month.map(d)
final_df1.head()

final_df1.info()

final_df1[['dey', 'month', 'year']] = final_df1[['dey', 'month', 'year']].astype (int)
final_df1.head()

"""### Подготовка данных для пребразование в формат datetime"""

import io

final_df1["month"] = final_df1.month.map("{:02}".format)

final_df1["dey"] = final_df1.dey.map("{:02}".format)

final_df1.head()

final_df1[['dey', 'month', 'year']] = final_df1[['dey', 'month', 'year']].astype (str)
final_df1.head()

final_df1.info()

final_df1['date'] = final_df1['year'].map(str) + final_df1['month'].map(str) +  final_df1['dey'].map(str)
final_df1.head()

""" ### Конвертация в формат Datetime"""

final_df1['date'] = pd.to_datetime(final_df1['date'], format='%Y%m%d')
final_df1.head()

"""# Подготовка датасета по дорожно-транспортные происшествия в Барселоне"""

df = pd.read_csv('accidents_opendata.csv')
df.head()

df.info()

"""### Удаление лишних строк. Оставляем данные за 2011 год."""

df1 = df[df['year'] > 2010]

df2 = df1[df1['year'] < 2012]

"""### Удаление лишних столбцов"""

df2.drop(df2.columns[[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 13, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26]], axis=1, inplace=True)

df2.info()

df2.head()

df2[['year', 'month', 'day']] = df2[['year', 'month', 'day']].astype (int)
df2.info()

"""### Подготовка данных для пребразование в формат datetime

Добавление нуля перед днём и месяцем прописаных 1 цифрой
"""

df2["month"] = df2.month.map("{:02}".format)

df2["day"] = df2.day.map("{:02}".format)

df2.head()

df2['date'] = df2['year'].map(str) + df2['month'].map(str) +  df2['day'].map(str)
df2.head()

"""### Конвертация в формат Datetime"""

df2['date'] = pd.to_datetime(df2['date'], format='%Y%m%d')
df2.head()

"""### Создаем столбец с количеством эпизодов"""

df2['count']= 1
df2.head()

"""### вычислить совокупную сумму по датам"""

df2['count_sum'] = df2.groupby(['date'])['count']. cumsum ()

mask_ = df2['count_sum'] == df2.groupby('date')['count_sum'].transform('max')
sum_df2 = df2[mask_]
sum_df2.head()

"""### Удаляем лишние столбцы"""

sum_df2.drop(sum_df2.columns[[0, 1, 2, 4]], axis=1, inplace=True)
sum_df2.head()

sum_df2.info()

"""# Объединяем датасеты"""

merged_df = pd.merge_ordered(sum_df2, final_df1)
merged_df

"""### Удаляем строки со значением NaN, оставляя тем самым данные за 11 месяцев 2011 года"""

merged_df = merged_df.dropna()
merged_df

"""### Приведение данных по мощности вспышек в формат float"""

def power_res(power):

  if power[0] == "X":
    return float(power[1::]) * 10
  elif power[0] == "M":
    return float(power[1::])
  elif power[0] == "C":
    return float(power[1::]) / 10
  elif power[0] == "B":
    return float(power[1::]) / 100

merged_df["power_res"] = merged_df["power"].apply(power_res)
merged_df.head()

"""### Сохранение объединённого датасета в формае csv"""

merged_df.to_csv('merged_df.csv')

"""### Отрисовка полученых данных на графике"""

merged_df.plot(x='date', y=['count_sum', 'power_res'], kind='bar', title="V comp", figsize=(40,8), ylabel='V', rot=0)

merged_df['count_sum'].describe().round(2)

merged_df['power_res'].describe().round(2)

plt.figure(figsize=(8, 6))
sns.boxplot(data=merged_df, y='count_sum')
plt.title('count_sum')
plt.ylabel('')
plt.show()

plt.figure(figsize=(8, 6))
sns.boxplot(data=merged_df, y='power_res')
plt.title('power_res')
# plt.ylabel('')
plt.show()

"""### Обнаружение и обработка выбросов"""

z_scores = np.abs(stats.zscore(merged_df.select_dtypes(include=np.number)))
merged_df = merged_df[(z_scores < 3).all(axis=1)]

plt.figure(figsize=(8, 6))
sns.boxplot(data=merged_df, y='count_sum')
plt.title('count_sum')
plt.ylabel('')
plt.show()

plt.figure(figsize=(8, 6))
sns.boxplot(data=merged_df, y='power_res')
plt.title('power_res')
# plt.ylabel('')
plt.show()

merged_df.plot(x='date', y=['count_sum', 'power_res'], kind='bar', title="V comp", figsize=(40,8), ylabel='V', rot=0)