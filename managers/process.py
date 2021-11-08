"""Csv processing module"""
import logging
import time
from collections import Counter
from concurrent.futures import ProcessPoolExecutor

import dask
import pandas as pd

from managers.file import FileManager

class CsvProcessing():
    """Class we will use to process .csv file"""

    def __init__(self, filename):
        """Constructor for file name in this case we get it from watchdog"""
        self.file_name = filename #filename

    def parse_csv(self):
        """Reading csv, calculating currency and returning a data frame"""
        #pylint: disable=unsupported-assignment-operation, unsubscriptable-object
        with dask.config.set(pool=ProcessPoolExecutor(4)):
            time.sleep(0.2)
            data_frame = pd.read_csv(self.file_name,
            encoding = 'utf-16',
            names = self.header_names(),
            dtype = self.columns_dtype(),
            engine = 'c',
            sep = '\t',
            header = 0,
            low_memory = False
            )

            header_parser = self.parsed_header_naming()
            # Planned to use filna on specific rows but droping rows with Nan seems better option
            data_frame.dropna(axis='index', how='all', subset=header_parser.remove('roas'))

            data_frame['conversation_value'] =  data_frame['conversation_value'].str.replace(
                ',',"").astype(float) #.fillna(0)
            data_frame['cost'] =  data_frame['cost'].str.replace(',',"").astype(float)
            data_frame['roas'] = (data_frame['conversation_value'] / data_frame['cost'])

            data_frame['roas'] = data_frame['roas'].map('{0:g}'.format)#pylint: disable=consider-using-f-string
            data_frame['conversation_value'] = data_frame['conversation_value'].map('{0:g}'.format)#pylint: disable=consider-using-f-string

            currency = self.currency_filename(data_frame['currency_code'])
            try:
                if not self.save_csv(data_frame, currency, header_parser):
                    logging.error("Problems with saving csv")
            except Exception as ex: #pylint: disable=broad-except
                logging.info("Problem with saving .csv file %s", str(ex))

    def currency_filename(self, currency_dataframe: pd.DataFrame) -> str:
        """Check if currency is unique find currency and return currency string"""
        if not self.check_currency(currency_dataframe):
            # we could just use Counter() and check it insted to use set() but i suppose .csv will mostly be correct
            # so this is in special cases which are rarer also Counter() (≈0.055) is 50% slower thans set() (≈0.035)
            # trying to get littlebit better performance for wrong case it will take ≈0.1 to check set() and Counter()
            currency_occurrance = self.count_objects(currency_dataframe)
            currency = max(currency_occurrance, key=currency_occurrance.get)
        else:
            currency = currency_dataframe[0]
        return currency

    @staticmethod
    def check_currency(data_frame: pd.DataFrame):#pylint: disable=no-self-use
        """Check if currency row has only one value which is same in column and return bool"""
        return len(set(data_frame)) <=1

    @staticmethod
    def count_objects(objects: pd.DataFrame) -> dict:#pylint: disable=no-self-use
        """Checking number of repeating  elements in column return Dict"""
        # If one .csv can only have the same currency if we get another then its problem
        # 3 different thought processes:
        # 1. split it in 2 files with lets say EUR and GBP
        # 2. see EUR as a mistake and save GBP instead
        # 3. simplest is see other currency as needed data in that file but save with most occurrence extension
        return Counter(objects)

    @staticmethod
    def save_csv(data_frame: pd.DataFrame, currency: str, columns: list) -> bool:#pylint: disable=no-self-use
        """ Checks folder structure and create .csv file if everything is ok"""
        file_manager = FileManager(currency)
        if file_manager.check_processed_path():
            data_frame.reset_index().to_csv(
                file_manager.generated_filepath(), index=False, sep='\t', encoding='utf-16', columns=columns)
            return True
        return False

    # splited in seperate functions for easier readability
    @staticmethod
    def header_names() -> str:
        """Returns header naming"""
        return [
            'search_term',
            'match_type',
            'added/excluded',
            'campaign',
            'ad_group',
            'clicks',
            'currency_code',
            'cost',
            'impressions',
            'conversions',
            'conversation_value'
            ]

    @staticmethod
    def parsed_header_naming() -> str:
        """Returns header naming for parsed csv """
        return [
            'search_term',
            'clicks',
            'cost',
            'impressions',
            'conversation_value',
            'roas'
            ]

    @staticmethod
    def columns_dtype() -> str:
        """Returns dtype casting"""
        return {
        'search_term': str,
        'conversation_value':str,
        'clicks':str, 'cost':str,
        'converstaions': str,
        'impressions':str,
        'currency_code':str
        }
