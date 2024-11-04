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
        
        # Loop through each run to find the 'Merlin' tool
        for run in data.get('runs', []):
            tool_name = run.get('tool', {}).get('driver', {}).get('name', '')
            if tool_name.lower() == 'merlin':
                # Extract results only for the 'Merlin' tool
                for result in run.get('results', []):
                    message_text = result.get('message', {}).get('text', '')
                    level = result.get('level', '')
                    rule_id = result.get('ruleId', '')
                    properties = result.get('properties', {})
                    
                    # Extract threat details
                    threat_level = properties.get('threatLevel', '')
                    threat_types = properties.get('threatTypes', {})
                    family_name = properties.get('familyName', '')

                    # Flatten the 'threatTypes' dictionary into a single string for CSV output
                    threat_types_str = ', '.join([f"{key}: {value}" for key, value in threat_types.items()])

                    filtered_data.append({
                        'message_text': message_text,
                        'level': level,
                        'rule_id': rule_id,
                        'threat_level': threat_level,
                        'family_name': family_name,
                        'threat_types': threat_types_str
                    })

        if not filtered_data:
            logger.warning("No results found for the 'Merlin' tool.")
            return
        
        logger.info(filtered_data)
        csv_fields = ['message_text', 'level', 'rule_id', 'threat_level', 'family_name', 'threat_types']
        csv_file_path = 'merlin_parsed_results.csv'
        
        # Using context manager to handle file writing
        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_fields)
            writer.writeheader()
            writer.writerows(filtered_data)
        
        logger.info(f"Parsed results from the 'Merlin' tool have been saved to {csv_file_path}")
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
        results_response = quokka.get_sarif(uuid)
        # results_response = quokka.get_sarif('819dfd45-e148-4777-837a-abc30202f07a')
        findings = json.loads(results_response)
        parse_results(findings)
        logger.info("Demo completed successfully")
    except json.JSONDecodeError as json_error:
        logger.error(f"JSON decode error: {json_error}")
    except FileNotFoundError as fnf_error:
        logger.error(f"File not found: {fnf_error}")
    except Exception as e:
        logger.error(f"An error occurred in quokkaio_demo: {e}")

if __name__ == "__main__":
    quokkaio_demo()