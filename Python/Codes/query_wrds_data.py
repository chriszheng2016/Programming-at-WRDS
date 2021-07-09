# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# # Using Python on WRDS Platform
# %% [markdown]
# ## Setup WRDS Python API
# * To be done before running this notebook
#   * run 'pip install wrds'
#   * Spyder or jupter

# %%
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 

# %% [markdown]
# ## Impport pre installed WRDS package

# %%
import wrds

# %% [markdown]
# ## Establish connection with WRDS server
# 
# * log in  using your WRDS username and password
# * setup a pgpass file to store username/password

# %%
db = wrds.Connection(wrds_username="cz2003")

# %% [markdown]
# ## List all libraries
# 
# * Library refers to database on WRDS: e.g. CRSP, Compustat
# * list_libraries() function to explore all subscribed databases

# %%
db_libs = db.list_libraries()
db_libs.sort()
type(db_libs)
print(db_libs)

# %% [markdown]
# ## List all datasets within a given library
#
# * Databases contain many datasets in
# * list_tables() function to list all datasets 
# * Specify which 'library/database'

# %%
tables_in_comp = db.list_tables(library='comp')
print(tables_in_comp)

# %% [markdown]
# ## Query Data from WRDS server
#
# * get_table() method
# * straightforward if getting data from one single dataset
# * specify which library/database and table/dataset to "get"
# * can slice data by:
#    * number of rows
#    * column names

# %%
company = db.get_table(library='comp', table='company', obs=5)
company.shape

company_narrow = db.get_table(library='comp', table='company', 
                              columns = ['conm', 'gvkey', 'cik'], obs=5)
company_narrow.shape
# %% [markdown]
# ## Subsetting Datasets
#
# * raw_sql() method
# * when "conditioning" is needed
# * familiar SQL syntax
# * can pre-specify date column forma

#%%
# Select one stock's monthly price
# from 2019 onwards

apple = db.raw_sql("""select permno, date, prc, ret, shrout 
                        from crsp.msf 
                        where permno = 14593
                        and date>='01/01/2019'""", 
                     date_cols=['date'])

apple

# %% [markdown]
# ## Join Multiple Datasets
#
# * again raw_sql() method
# * synatx similar to "proc sql" in SAS
# * handle conditioning statement

#%% 
apple_fund = db.raw_sql("""select a.gvkey, a.iid, a.datadate, a.tic, a.conm,
                            a.at, b.prccm, b.cshoq
                            
                            from comp.funda a 
                            inner join comp.secm b 
                            
                            on a.gvkey = b.gvkey
                            and a.iid = b.iid
                            and a.datadate = b.datadate
                        
                            where a.tic = 'AAPL' 
                            and a.datadate>='01/01/2010'
                            and a.datafmt = 'STD' 
                            and a.consol = 'C' 
                            and a.indfmt = 'INDL'
                            """, date_cols=['datadate'])

apple_fund.shape

#%% [markdown]
# ## Save Your Output
# 
# Pandas support flexible output format
# pickle for further python work,  csv or excel, even SAS data format

# %%
import pandas as pd
# pickle the dataframe
apple_fund.to_pickle("./Data/apple_fund.pkl")

# export the dataframe to csv format

apple_fund.to_csv('./Data/apple_fund.csv')

# export the dataframe to xlsx format

apple_fund.to_excel('./Data/apple_fund.xlsx')

# export the dataframe to dta format for STATA

apple_fund.to_stata('./Data/apple_fund.dta')
# %%
db.close()

# %%
