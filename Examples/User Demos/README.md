
# Quokka.io User Demo Script

This script demonstrates a user-specific example of interacting with the Quokka.io API. It retrieves user data, transforms it, and saves the transformed data to a CSV file.

## Requirements

- Python 3.x
- `quokkaio` package
- `logging` package (standard library)
- `json` package (standard library)
- `csv` package (standard library)
- `os` package (standard library)
- `pandas` package
- `datetime` package (standard library)

## Setup

1. Install the required packages:
    ```sh
    pip install quokkaio pandas
    ```

2. Set up your environment variable for the Quokka.io API key:
    ```sh
    export QUOKKA_API_KEY='your_api_key_here'
    ```

## Usage

1. Clone this repository or download the script file.

2. Run the `quokkaio_user_demo.py` script:
    ```sh
    python quokkaio_user_demo.py
    ```

3. The script will perform the following actions:
    - Retrieve user data using the Quokka.io API.
    - Transform the retrieved data to a desired format.
    - Save the transformed data to a new CSV file.

## Script Details

### Initialization

The script initializes the Quokka.io client using an API key stored in an environment variable.

```python
api_key = os.getenv('QUOKKA_API_KEY', 'default_api_key')
quokka = Quokka(key=api_key)
```

### Logging Setup

A logger is set up to provide detailed logs during the execution.

```python
def setup_logger():
    logger = logging.getLogger("Quokka")
    logger.setLevel(logging.DEBUG)
    fh = logging.StreamHandler()
    fh_formatter = logging.Formatter('%(asctime)s %(levelname)s %(lineno)d:%(filename)s(%(process)d) - %(message)s')
    fh.setFormatter(fh_formatter)
    logger.addHandler(fh)
    return logger

logger = setup_logger()
```

### Transforming CSV Data

The `transform_csv` function loads a CSV file, transforms the data, and saves it to a new CSV file.

```python
def transform_csv(input_file, output_file):
    data = pd.read_csv(input_file)
    transformed_data = []
    for index, row in data.iterrows():
        email = row['Email']
        for column in data.columns[4:]:
            if row[column] == 'yes':
                transformed_data.append([email, column])
    transformed_df = pd.DataFrame(transformed_data, columns=['Email', 'Permission'])
    transformed_df.to_csv(output_file, index=False)
    logger.info(f"CSV file has been saved as {output_file}")
```

### Main Function

The `quokkaio_users` function demonstrates the primary workflow of retrieving user data, transforming it, and saving the result.

```python
def quokkaio_users():
    try:
        response = quokka.get_users()
        if response:
            now = datetime.now()
            date_string = now.strftime("%Y-%m-%d")
            input_file = f'{date_string}-group_user_data.csv'
            output_file = f'{date_string}-transformed_user_data.csv'
            transform_csv(input_file=input_file, output_file=output_file)
        else:
            logger.error("Error retrieving results")
    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == "__main__":`
    quokkaio_users()
```

