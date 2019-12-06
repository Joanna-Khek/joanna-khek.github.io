# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 09:10:47 2019

@author: Joanna Khek Cuina
"""

# import libraries
import pandas as pd
import numpy as np
import datetime

# read data
data1 = pd.read_csv("1990-1999_resale.csv")
data2 = pd.read_csv("2000-2012_resale.csv")
data3 = pd.read_csv("2012-2014_resale.csv")
data4 = pd.read_csv("2015-2016_resale.csv")
data5 = pd.read_csv("2017_onwards_resale.csv")

# ----------------------- CLEANING UP DATA -------------------------- #
# rename columns
cols = ['date', 'town', 'flat_type', 'block', 'street_name', 'storey_range',
       'floor_area_sqm', 'flat_model', 'lease_commence_date', 'resale_price']

data1.columns = cols
data2.columns = cols
data3.columns = cols
data4 = data4.rename(columns = {"month":"date"})
data5 = data5.rename(columns = {"month":"date"})

def get_year_month(data):
    data["year"] = data["date"].apply(lambda x: x.split("-")[0])
    data["month"] = data["date"].apply(lambda x: x.split("-")[1])
    return data

data1 = get_year_month(data1)
data2 = get_year_month(data2)
data3 = get_year_month(data3)
data4 = get_year_month(data4)
data5 = get_year_month(data5)

# change data type
def change_data_type(data):
    data["year"] = data["year"].astype(int)
    data["month"] = data["month"].astype(int)
    return data

data1 = change_data_type(data1)
data2 = change_data_type(data2)
data3 = change_data_type(data3)
data4 = change_data_type(data4)
data5 = change_data_type(data5)

# create remaining lease column for data1, data2, data3

def remaining_lease(data):
    remaining_lease = []
    for i in range(0, len(data)):
        remaining_lease.append(99 - (data["year"][i] - data["lease_commence_date"][i]))
    data["remaining_lease"] = remaining_lease
    return data

remaining_lease(data1)
remaining_lease(data2)
remaining_lease(data3)

# re-arrange columns
cols = ['date', 'year', 'month', 'town', 'flat_type', 'block', 'street_name', 'storey_range',
       'floor_area_sqm', 'flat_model', 'lease_commence_date', 'resale_price',
       'remaining_lease']

data1 = data1[cols]
data2 = data2[cols]
data3 = data3[cols]
data4 = data4[cols]
data5 = data5[cols]

# merge all together
# =============================================================================
# full_data = pd.concat([data1, data2], axis=0)
# full_data = pd.concat([full_data, data3], axis=0)
# full_data = pd.concat([full_data, data4], axis=0)
# full_data = pd.concat([full_data, data5], axis=0)
# =============================================================================
full_data = pd.concat([data2, data3], axis=0)
full_data = pd.concat([full_data, data4], axis=0)
full_data = pd.concat([full_data, data5], axis=0)
full_data = full_data.drop(full_data[full_data["flat_type"] == "MULTI GENERATION"].index, axis=0)
full_data = full_data.drop(full_data[full_data["flat_type"] == "MULTI-GENERATION"].index, axis=0)

full_data["date"] = pd.to_datetime(full_data["date"])
full_data["date"].dt.month

# write csv
full_data.to_csv("full_resale_flat.csv")
