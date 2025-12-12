# veracode-list-all-DAST-schedules
Lists the configured schedule for all DAST scans available to the current user

## Requirements:
- Python 3.12+

## Setup

Clone this repository:

    git clone https://github.com/cadonuno/veracode-list-all-DAST-schedules

Install dependencies:

    cd veracode-list-all-DAST-schedules
    pip install -r requirements.txt

(Optional) Save Veracode API credentials in `~/.veracode/credentials`

    [default]
    veracode_api_key_id = <YOUR_API_KEY_ID>
    veracode_api_key_secret = <YOUR_API_KEY_SECRET>


## Run
If you have saved credentials as above you can run:

    python veracode-list-all-dast-schedules.py (arguments)

Otherwise you will need to set environment variables:

    export VERACODE_API_KEY_ID=<YOUR_API_KEY_ID>
    export VERACODE_API_KEY_SECRET=<YOUR_API_KEY_SECRET>
    python veracode-list-all-dast-schedules.py (arguments)

## Supported Arguments:
- `-o`, `--output_file` - Name of the CSV file to save (default: 'DAST_Schedules.csv')
