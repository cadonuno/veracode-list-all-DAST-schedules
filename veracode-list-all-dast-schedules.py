import argparse
import csv
from veracode_api_py import Analyses, BusinessUnits

def get_scan_info(analysis, business_unit, urls):
    scan_info = { "name": analysis["name"], "business_unit": business_unit, "URLs": urls, "schedule_frequency": analysis["schedule_frequency"]["frequency_type"] }
    if "schedule_summary" in analysis:
        schedule = analysis["schedule_summary"]
        scan_info["schedule_status"] = schedule["schedule_status"]
        scan_info["schedule_start"] = schedule["start_date"]
        scan_info["schedule_duration"] = f"{schedule["duration"]["length"]} {schedule["duration"]["unit"].lower()}s"
        if "scan_recurrence_schedule" in schedule:
            recurrence = schedule["scan_recurrence_schedule"]
            scan_info["recurrence_type"] = recurrence["recurrence_type"].lower()
            scan_info["recurrence_interval"] = recurrence["recurrence_interval"]
            if scan_info["recurrence_type"] == "monthly":
                scan_info["recurrence_info"] = f"{recurrence["week_of_month"].lower()} {recurrence["day_of_week"].lower()} of the month"
            else:
                scan_info["recurrence_info"] = f"{recurrence["day_of_week"].lower()}s"
            scan_info["recurrence_end_after"] = f"{recurrence["schedule_end_after"]} {'months' if scan_info["recurrence_type"] == 'monthly' else 'weeks'}"
    
    return scan_info

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
        all_dast_scans.append(get_scan_info(analysis, business_unit, urls))

    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Name", "Business Unit", "URLs", "Schedule Frequency", "Schedule Status", "Schedule Start", "Schedule Duration", "Scan Recurrence Type", "Scan Recurrence Interval", "Scan Recurrence", "Scan Recurrence schedule End After"])
        for entry in all_dast_scans:
            csv_writer.writerow([entry["name"], entry["business_unit"], entry["URLs"], entry["schedule_frequency"], entry.get("schedule_status", ""), entry.get("schedule_start", ""), entry.get("schedule_duration", ""), entry.get("recurrence_type", ""), entry.get("recurrence_interval", ""), entry.get("recurrence_info", ""), entry.get("recurrence_end_after", "")])
if __name__ == '__main__':
    main()