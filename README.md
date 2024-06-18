
# Quokka.io Examples

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

