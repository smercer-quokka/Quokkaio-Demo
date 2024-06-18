import logging
import pandas as pd
import json
import csv
import os
from quokkaio.quokka import Quokka
from datetime import datetime

# Initialize the client with your API key from environment variable
api_key = os.getenv('QUOKKA_API_KEY')
if not api_key:
    raise ValueError("API key not found. Please set the QUOKKA_API_KEY environment variable.")
quokka = Quokka(key=api_key)

def setup_logger() -> logging.Logger:
    logger = logging.getLogger("Quokka")
    logger.setLevel(logging.DEBUG)
    fh = logging.StreamHandler()
    fh_formatter = logging.Formatter('%(asctime)s %(levelname)s %(lineno)d:%(filename)s(%(process)d) - %(message)s')
    fh.setFormatter(fh_formatter)
    logger.addHandler(fh)
    return logger

logger = setup_logger()

def transform_csv(input_file: str, output_file: str) -> None:
    """
    Transforms the input CSV file to the desired output format.
    """
    try:
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
    except FileNotFoundError as fnf_error:
        logger.error(f"File not found: {fnf_error}")
    except pd.errors.EmptyDataError as ede_error:
        logger.error(f"Empty data error: {ede_error}")
    except Exception as e:
        logger.error(f"An error occurred during CSV transformation: {e}")

def quokkaio_users() -> None:
    """
    Pulls the CSV file for user permissions then transforms to a desirable output.
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
            logger.error("Error retrieving results from Quokka API")
    except Exception as e:
        logger.error(f"An error occurred in quokkaio_users: {e}")

if __name__ == "__main__":
    quokkaio_users()