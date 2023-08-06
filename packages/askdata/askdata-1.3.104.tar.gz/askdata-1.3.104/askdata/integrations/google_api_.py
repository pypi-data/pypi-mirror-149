#required !pip install googleads -q


import pandas as pd
import numpy as np
import datetime
import io
import os
import glob
import sys
from googleads import adwords
from datetime import datetime, timedelta


import _locale


"""
MANDATORY INPUT:

start_date, end_date as string "yyyy-mm-dd"

OPTIONAL INPUTS: 



- yaml_file_path: the path of 'googleads.yaml'. 
                Optional, but mandatory to have it in same folder script if used the default parameter.

"""


def get_google_ads(start_date, end_date, admin_account,
                   
                   
                   ## optional
                   
                   yaml_file_path = 'googleads.yaml'
                  ):

    _locale._getdefaultlocale = (lambda *args: ['en_US', 'UTF-8'])

    



    def run_Hour0fDay_kip_report(key, acc_id, start_date, end_date):
    # Define output as a string
        output= io.StringIO()
        adwords_client = adwords.AdWordsClient.LoadFromStorage(yaml_file_path)
        adwords_client.SetClientCustomerId(acc_id)    
        report_downloader = adwords_client.GetReportDownloader(version='v201809')
        report_query = (adwords.ReportQueryBuilder()
                          .Select(
                              'Month'
                              ,'Date'
                            #   ,'AccountId'
                              ,'CampaignId'
                              ,'ExternalCustomerId'
                              ,'CampaignName'
                              ,'CampaignStatus'
                            #   ,'CampaignType'
                              ,'Amount'
                              ,'AccountCurrencyCode'
                              ,'Clicks'
                              ,'Impressions'
                              ,'Ctr'
                              ,'AverageCpc'
                              ,'Cost'
                              ,'Conversions'
                              ,'ViewThroughConversions'
                              ,'CostPerConversion'
                              ,'ConversionRate'
                              ,'AverageCpm'
                              )
                          .From('CAMPAIGN_PERFORMANCE_REPORT')
                        #   .Where('CampaignStatus').In('ENABLED')
                          .During(start_date+ ','+end_date) 
                          .Build())

        report_downloader.DownloadReportWithAwql(report_query, 'CSV', output, skip_report_header=True,
                  skip_column_header=False, skip_report_summary=True,
                  include_zero_impressions=False)

        output.seek(0)

        types= { 'CampaignId':pd.np.int64, 'Clicks': pd.np.float64, 'Impressions': pd.np.float64,
                 'Cost': pd.np.float64,'Conversions': pd.np.float64,'ConversionValue': pd.np.float64  }

        df = pd.read_csv(output,low_memory=False, dtype= types, na_values=[' --'])
        # delete the first and last column
        df['Brand']=key
        # micro amount 1000000
        df['Cost']=df.Cost/1000000
        print(df.head())
        return df


    google_ads = pd.DataFrame(columns = ['Month', 'Day', 'Campaign ID', 'Customer ID', 'Campaign',
           'Campaign state', 'Budget', 'Currency', 'Clicks', 'Impressions', 'CTR',
           'Avg. CPC', 'Cost', 'Conversions', 'View-through conv.', 'Cost / conv.',
           'Conv. rate', 'Avg. CPM', 'Brand'])



    for k, v in admin_account.items():

        df=run_Hour0fDay_kip_report(k, v,start_date, end_date)

        google_ads = pd.concat([google_ads, df])
        
        
    return google_ads