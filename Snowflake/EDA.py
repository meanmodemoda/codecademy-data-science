# The Snowpark package is required for Python Worksheets. 
# You can add more packages by selecting them using the Packages control and then importing them.

import snowflake.snowpark as snowpark
import numpy as np
import pandas as pd
from snowflake.snowpark.functions import col

def main(session: snowpark.Session): 
    # Your code goes here, inside the "main" handler   
    df = session.table("analysis_database.analysis_schema.item_detail")
    # Convert the Snowpark DataFrame to a Pandas DataFrame
    df_pd = df.to_pandas()

    # Filter date
    df_pd['SUBMITTED_DATE']=pd.to_datetime(df_pd['SUBMITTED_DATE'])
    df_pd = df_pd[df_pd['SUBMITTED_DATE'] == '2024-07-01']

    # Drop datatime columns
    # datetime_cols = [col for col in df_pd.columns if pd.api.types.is_datetime64_any_dtype(df_pd[col])]
    # df_pd = df_pd.drop(columns=datetime_cols)

    # The AT exclusion is hacky, need to improve
    # columns_to_drop = [col for col in df_pd.columns if 'AT' in col]
    # df_category=df_pd.drop(columns=columns_to_drop)
    # df_numeric=df_pd.drop(columns=columns_to_drop)
    
    # Calculate the description statistics
    # description = df_numeric.describe().reset_index()
    # description.columns = ['statistic'] + list(description.columns[1:])
    # Add index as a column before transposing
    # description['statistic'] = description['statistic'].astype(str)
    
    # Transpose the summary statistics
    # description_transposed = description.set_index('statistic').T
    # description_transposed.reset_index(inplace=True)
    # description_transposed.columns.name = None  # Remove the columns name

    # Calculate null counts
    nullcount = df_pd.isnull().sum().reset_index()
    nullcount.columns = ['column', 'null_count']

    # Calculate summary statistics for categorical data
    # categorical_data = df_category.select_dtypes(include=['object'])
    
    # categorical_summary = {}
    # for column in categorical_data.columns:
    #     categorical_summary[column] = categorical_data[column].value_counts().reset_index()
    #     categorical_summary[column].columns = ['value', 'count']


    # Convert the description statistics to a Snowpark DataFrame
    # description_snowpark_df = session.create_dataframe(description_transposed)

    # Convert the null counts to a Snowpark DataFrame
    nullcount_snowpark_df = session.create_dataframe(nullcount, schema=['column', 'null_count'])

     # Combine categorical summaries into a single DataFrame for Snowpark
    # categorical_summary_combined = pd.concat(categorical_summary.values(), keys=categorical_summary.keys(), names=['column'])
    # Remove the unwanted 'level_1' column
    # categorical_summary_snowpark_df = session.create_dataframe(categorical_summary_combined.reset_index(), schema=['column', 'value', 'count'])

    
    # Print a sample of the DataFrames to standard output
    # description_snowpark_df.show()
    nullcount_snowpark_df.show()
    # categorical_summary_snowpark_df.show()

    # Return both DataFrames
    return nullcount_snowpark_df
    # return description_snowpark_df
    # return categorical_summary_snowpark_df
    
