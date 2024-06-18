import logging
import pandas as pd
import json
import csv
import os
from quokkaio.quokka import Quokka
from datetime import datetime


# Initialize the client with your API key from environment variable
api_key = os.getenv('QUOKKA_API_KEY', 'default_api_key')
quokka = Quokka(key=api_key)

def setup_logger():
    logger = logging.getLogger("Quokka")
    logger.setLevel(logging.DEBUG)
    fh = logging.StreamHandler()
    fh_formatter = logging.Formatter('%(asctime)s %(levelname)s %(lineno)d:%(filename)s(%(process)d) - %(message)s')
    fh.setFormatter(fh_formatter)
    logger.addHandler(fh)
    return logger

logger = setup_logger()

def transform_csv(input_file, output_file):
    # Load the CSV file
    data = pd.read_csv(input_file)
    
    # Initialize an empty list to store the transformed data
    transformed_data = []
    
    # Iterate through each row in the dataframe
    for index, row in data.iterrows():
        email = row['Email']
        for column in data.columns[4:]:  # Start from the 5th column onwards
            if row[column] == 'yes':
                transformed_data.append([email, column])
    
    # Create a new dataframe from the transformed data
    transformed_df = pd.DataFrame(transformed_data, columns=['Email', 'Permission'])
    
    # Save the transformed dataframe to a new CSV file
    transformed_df.to_csv(output_file, index=False)
    logger.info(f"CSV file has been saved as {output_file}")

def quokkaio_users():
    """
    Pull the csv file for user permission then transfrom to a desireable output
    """
    try:
        response = quokka.get_users()
        if response:
            now = datetime.now()
            date_string = now.strftime("%Y-%m-%d")
            input_file = f'{date_string}-group_user_data.csv'
            output_file = f'{date_string}-transformed_user_data.csv'
            transform_csv(input_file=input_file, output_file=output_file)
        else:
            logger.error("Error retriving results")
        
    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    quokkaio_users()