import dask.dataframe as dd
import dask
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import pandas as pd
from file import FileManager

class CsvProcessing():
    
    def __init__(self, filename):
        self.file_name = 'coding_challenge_data.csv'

    # def read_csv(self):
    #     df = dd.read_csv(self.file_name)
    #     self.save_csv(df)
    #     df.to_csv('./test_saving/export-1.csv', single_file=True)
    #     return df

    # def read_csv(self):
    #     #try:
    #     df = dd.read_csv(self.file_name,
    #     encoding='iso-8859-1',
    #     # changed to output file format
    #     names=['search_term', 'match_type', 'added/excluded', 'campaign', 'ad_group', 'clicks', 'currency_code', 'cost', 'impressions', 'conversions', 'conversion_value'],
    #     dtype={'search_term': str,'match_type':str, 'added/excluded':str, 'campaign':str, 'ad_group':str, 'clicks':str, 'currency_code':str, 'cost':str, 'impressions':str, 'conversion_value':str},
    #     engine='c',
    #     sep='\t',
    #     header=0,
    #     low_memory=False
    #     )
        
    #     #df.columns = [c.replace(' ', '_').lower() for c in df.columns]

    #     df['conversion_value']=  df['conversion_value'].fillna(0).str.replace(',',"").astype(float)
    #     df['cost']=  df['cost'].fillna(0).str.replace(',',"").astype(float) # check later what to do cant fill it with
    #     #df['clicks']=  df['clicks'].fillna(0).str.replace(',',"").astype(int)
    #     #df['impressions']=  df['impressions'].fillna(0).str.replace(',',"").astype(int)
    #     df['roas'] = (df['conversion_value'] / df['cost'])

    #     #print(df['currency_code'].value_counts().compute())
     
    #     #file_object = FileManager(currency=currency)
    #     #file_object.check_processed_path()

    #     header = ['search_term', 'clicks', 'cost', 'impressions', 'conversion_value', 'roas']
    #     df.to_csv(f'./test_saving/{FileManager().generate_filename()}', sep='\t', encoding='utf-8', single_file=True, columns=header)

    #     #except Exception as ex:
    #     #    print("ovo je problem", ex)
    #     return "Finished"

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
        with dask.config.set(pool=ProcessPoolExecutor(16)):
            df = self.read_csv()
        return "Finished"

    def unique_cols(self, df):
        a = df.to_numpy() # df.values (pandas<0.24)
        return (a[0] == a).all(0)

    def save_csv(self, df):
        pass


    def check_folder():
        pass