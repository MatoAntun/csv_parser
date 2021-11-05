# monitor file (thread)
# process file (multiprocess) spawn subprocess
# if multiple file spawn multi processes
# precent core dumps
# calculate ROAS
# create python deamon
# output file format and path
# handle corrupt .csv files and individual rows ( chekc for prices EUR, GBP maybe sort by it or something like that)
# handle multiple file added in close proximity
# packing in venv 
# create docker
# maybe basic testing

import dask.dataframe as dd
import dask
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from distributed import scheduler
import pandas as pd

class CsvProcessing():
    def __init__(self, filename):
        self.file_name = filename


    
    def read_csv(self):
        df = dd.read_csv(self.file_name,
        encoding='iso-8859-1',
        # changed to output file format
        names=['search_term', 'match_type', 'added/excluded', 'campaign', 'ad_group', 'clicks', 'currency_code', 'cost', 'impressions', 'conversions', 'conversion_value'],
        dtype={'search_term': str,'match_type':str, 'added/excluded':str, 'campaign':str, 'ad_group':str, 'clicks':str, 'currency_code':str, 'cost':str, 'impressions':str, 'conversion_value':str},
        engine='c',
        sep='\t',
        header=0,
        low_memory=False
        )
        
        #df.columns = [c.replace(' ', '_').lower() for c in df.columns]

        df['conversion_value']=  df['conversion_value'].fillna(0).str.replace(',',"").astype(float)
        df['cost']=  df['cost'].fillna(0).str.replace(',',"").astype(float) # check later what to do cant fill it with
        # Probably littlebit cheating while using string for clicks and impr. but we do not need it for analysing right now
        # and we are saving some time on processing
        df['clicks']=  df['clicks'].fillna(0).str.replace(',',"").astype(int)
        df['impressions']=  df['impressions'].fillna(0).str.replace(',',"").astype(int)
        
        df['roas'] = (df['conversion_value'] / df['cost'])
        print(df.head())
        header = ['search_term', 'clicks', 'cost', 'impressions', 'conversion_value', 'roas']
        df.to_csv('./test_saving/export-1.csv', sep='\t', encoding='utf-8', single_file=True, columns=header)

        return "Finished"

    def read_csv_single_threaded(self):
        with dask.config.set(scheduler="single-threaded"):
            df = self.read_csv()
        return "Finished threded"

    def read_csv_threads(self):
        #dask.config.set(scheduler="threads")
        with dask.config.set(pool=ThreadPoolExecutor(32)):
            df = self.read_csv()
        return "Finished test"

    def read_csv_processes(self):
        with dask.config.set(pool=ProcessPoolExecutor(8)):
            df = self.read_csv()
        return "Finished"

# def main():
#     #test1 = "1,041.44"
#     #test1.split()
#     #test = (test1.split()).replace(',', '')
#     #print("ovo je test ", test)
#     filename = "coding_challenge_data.csv"
#     print("\n Prvi:")
#     start = datetime.now()
#     print(CsvProcessing(filename).read_csv())
#     first_time = datetime.now() - start
#     print("Time needed for basic", first_time)
#     print("\n Drugi:")
#     start = datetime.now()
#     print(CsvProcessing(filename).read_csv_single_threaded())
#     snd_time = datetime.now() - start
#     print("Time needed single threaded", snd_time)
#     print("\n Treci:")
#     start = datetime.now()
#     print(CsvProcessing(filename).read_csv_threads())
#     third =  datetime.now() - start
#     print("Time needed threded", third)
#     print("\n Cetvrti:")
#     start = datetime.now()
#     print(CsvProcessing(filename).read_csv_processes())
#     forth =  datetime.now() - start
#     print("Time needed processes", forth)
#     print(f"\nOvo su kupna vremena \n Prvo:{first_time}\n Drugo {snd_time} \n Trece {third} \n Cetvrto {forth}\n")

# if __name__ == "__main__":
#     main()
