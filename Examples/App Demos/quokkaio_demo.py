import logging
import json
import csv
import os
from quokkaio.quokka import Quokka

# Initialize the client with your API key from environment variable
api_key = os.getenv('QUOKKA_API_KEY')
if not api_key:
    raise ValueError("API key not found. Please set the QUOKKA_API_KEY environment variable.")
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

def parse_results(data: dict) -> None:
    """
    Parse the results from the Quokka API response and write filtered data to a CSV file.
    """
    try:
        filtered_data = []
        for issue in data.get('parsedAppIssues', []):
            if issue.get('found'):
                filtered_data.append({
                    'positive_finding_text': issue.get('positive_finding_text'),
                    'risk': issue.get('risk'),
                    'category': issue.get('category'),
                    'cvss_score': issue.get('cvss_score'),
                    'cue': issue.get('description')  # Assuming 'cue' corresponds to 'description'
                })
        
        csv_fields = ['positive_finding_text', 'risk', 'category', 'cvss_score', 'cue']
        csv_file_path = 'filtered_issues.csv'
        
        # Using context manager to handle file writing
        with open(csv_file_path, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_fields)
            writer.writeheader()
            writer.writerows(filtered_data)
        
        logger.info(f"Filtered issues have been saved to {csv_file_path}")
    except Exception as e:
        logger.error(f"An error occurred while parsing results: {e}")

def quokkaio_demo() -> None:
    """
    Demonstrate the basic usage of the Quokka API by pushing a scan, waiting for completion,
    retrieving results, and downloading a PDF report.
    """
    try:
        # Example: Fetching some data
        subgroups = []
        scan_response, platform = quokka.push_scan('InsecureShop_release.apk', subgroups)
        uuid = scan_response['uuid']
        quokka.wait_for_scan_complete(uuid)
        results_response = quokka.get_app_issue(uuid)
        findings = json.loads(results_response)
        parse_results(findings)
        quokka.download_pdf(uuid)
        logger.info("Demo completed successfully")
    except json.JSONDecodeError as json_error:
        logger.error(f"JSON decode error: {json_error}")
    except FileNotFoundError as fnf_error:
        logger.error(f"File not found: {fnf_error}")
    except Exception as e:
        logger.error(f"An error occurred in quokkaio_demo: {e}")

if __name__ == "__main__":
    quokkaio_demo()