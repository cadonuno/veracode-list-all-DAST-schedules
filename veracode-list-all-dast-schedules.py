import argparse
import csv
from veracode_api_py import Analyses, BusinessUnits, Scans, Occurrences

def get_actual_start_date(analysis):
    return analysis["actual_start_date"] if "actual_start_date" in analysis else "NONE"

def get_scheduled_start_date(analysis):
    return analysis["start_date"] if "start_date" in analysis else "NONE"

def get_create_date(base_analysis):
    return base_analysis["created_on"] if "created_on" in base_analysis else "NONE"

def get_actual_end_date(analysis):
    return analysis["actual_end_date"] if "actual_end_date" in analysis else "NONE"

def get_scheduled_end_date(analysis):
    return analysis["end_date"] if "end_date" in analysis else "NONE"

def get_status(analysis):
    if "status" in analysis and "status_type" in analysis["status"]:
        return analysis["status"]["status_type"]
    return 'No status found'

def main():
    parser = argparse.ArgumentParser(
        description="Lists the configured SCHEDULE for ALL DAST scans available to the current user."
    )

    parser.add_argument(
        "-o",
        "--output_file",
        help="Name of the CSV file to save (default: 'DAST_Schedules.csv').",
        required=False
    )

    args =  parser.parse_args()
    output_file = args.output_file

    if not output_file:
        output_file = "DAST_Schedules.csv"

    print("Fetching list of DAST scans")
    all_dast_scans = []
    all_analyses = Analyses().get_all()

    business_unit_map = dict()
    for bu in BusinessUnits().get_all():
        business_unit_map.update({str(bu["bu_legacy_id"]): bu["bu_name"]})

    for analysis in all_analyses:
        bu_id = analysis["org_info"]["business_unit_id"] if ("org_info" in analysis and "business_unit_id" in analysis["org_info"]) else None
        business_unit = business_unit_map[bu_id] if str(bu_id) in business_unit_map else "No Business Unit"
        scans = Analyses().get_scans(analysis["analysis_id"])
        urls = []
        for scan in scans:
            urls.append(scan["target_url"])
        all_dast_scans.append({ "name": analysis["name"], "business_unit": business_unit, "URLs": urls, "schedule_frequency": analysis["schedule_frequency"], "schedule_summary": analysis["schedule_summary"] if "schedule_summary" in analysis else "" })

    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Name", "Business Unit", "Create Date", "URLs", "Schedule Frequency", "Schedule Summary"])
        for entry in all_dast_scans:
            csv_writer.writerow([entry["name"], entry["business_unit"], entry["URLs"], entry["schedule_frequency"], entry["schedule_summary"]])

if __name__ == '__main__':
    main()