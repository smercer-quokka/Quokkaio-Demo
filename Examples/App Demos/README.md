
# Quokka.io Demo Script

This script demonstrates the basic usage of the Quokka.io API for mobile security analysis. It includes functionalities such as pushing a scan, waiting for its completion, retrieving results, and downloading a PDF report. The results are also parsed and saved to a CSV file.

## Requirements

- Python 3.x
- `quokkaio` package
- `logging` package (standard library)
- `json` package (standard library)
- `csv` package (standard library)
- `os` package (standard library)
- `pandas` package (standard library)

## Setup

1. Install the required packages:
    ```sh
    pip install quokkaio
    ```

2. Set up your environment variable for the Quokka.io API key:
    ```sh
    export QUOKKA_API_KEY='your_api_key_here'
    ```

3. Ensure you have the APK file `InsecureShop_release.apk` available in the script's directory or provide the correct path to it in the script.

## Usage

1. Clone this repository or download the script file.

2. Run the script:
    ```sh
    python quokkaio_demo.py
    ```

3. The script will perform the following actions:
    - Push a scan for the APK file.
    - Wait for the scan to complete.
    - Retrieve the results and parse them.
    - Save the parsed results to `filtered_issues.csv`.
    - Download a PDF report of the scan.

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

### Parsing Results

The `parse_results` function extracts relevant information from the API response and writes it to a CSV file.

```python
def parse_results(data):
    filtered_data = []
    for issue in data.get('parsedAppIssues', []):
        if issue.get('found'):
            filtered_data.append({
                'positive_finding_text': issue.get('positive_finding_text'),
                'risk': issue.get('risk'),
                'category': issue.get('category'),
                'cvss_score': issue.get('cvss_score'),
                'cue': issue.get('description')
            })

    csv_fields = ['positive_finding_text', 'risk', 'category', 'cvss_score', 'cue']
    csv_file_path = 'filtered_issues.csv'
    
    with open(csv_file_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_fields)
        writer.writeheader()
        writer.writerows(filtered_data)
```

### Main Function

The `quokkaio_demo` function demonstrates the primary workflow of interacting with the Quokka.io API.

```python
def quokkaio_demo():
    try:
        subgroups = []
        scan_response, platform = quokka.push_scan('InsecureShop_release.apk', subgroups)
        uuid = scan_response['uuid']
        quokka.wait_for_scan_complete(uuid)
        results_response = quokka.get_app_issue(uuid)
        findings = json.loads(results_response)
        parse_results(findings)
        quokka.download_pdf(uuid)
        
    except Exception as e:
        logger.error(f"An error occurred: {e}")
```

### Execution

The script is executed with the main guard to ensure it runs only when executed directly.

```python
if __name__ == "__main__":
    quokkaio_demo()
```


