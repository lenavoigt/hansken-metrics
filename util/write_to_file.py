import csv
import json
import os
from datetime import datetime
from typing import List, Dict


def generate_result_file_names():
    os.makedirs('results', exist_ok=True)
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    json_filename = f"results/summary_dict_{timestamp}.jsonl"
    tsv_filename = f"results/data_table_{timestamp}.tsv"
    return json_filename, tsv_filename, f"results/{timestamp}.log"


def write_single_evidence_results_to_json(project_id: str, evidence_id: str, result_list: List[dict],
                                          json_file_name: str):
    print(f'    Writing results to {json_file_name}')
    single_evidence_json_dump = json.dumps({
        "project": project_id,
        "evidence_id": evidence_id,
        "results": result_list
    })

    with open(json_file_name, "a") as f:
        f.write(single_evidence_json_dump + "\n")


def write_single_evidence_results_to_tsv(project_id: str, evidence_id: str, result_list: List[dict],
                                         csv_file_name: str):
    print(f'    Writing summary data table to {csv_file_name}.')
    pe_id = f"{project_id.split('-')[0]}:{evidence_id.split('-')[0]}"
    new_row = {'id': pe_id}
    new_fields = set()

    # Build the new row and collect new field names
    for each_result in result_list:
        plugin = each_result['plugin']
        for key, value in each_result['results'].items():
            field_name = f"{plugin}-{key}"
            new_row[field_name] = value
            new_fields.add(field_name)

    if not os.path.exists(csv_file_name):
        # File doesn't exist: create it with headers
        all_fields = ['id'] + sorted(new_fields)
        with open(csv_file_name, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, delimiter='\t', fieldnames=all_fields, restval='')
            writer.writeheader()
            writer.writerow(new_row)
        return

    # File exists: read just the header (first line)
    with open(csv_file_name, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter='\t')
        existing_fieldnames = reader.fieldnames or []
        existing_rows = list(reader)

    existing_field_set = set(existing_fieldnames)
    total_fields = existing_field_set | new_fields

    if total_fields == existing_field_set:
        # No new fields: safe to just append
        with open(csv_file_name, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, delimiter='\t', fieldnames=existing_fieldnames, restval='')
            writer.writerow(new_row)
    else:
        # New fields added: rewrite entire file
        combined_fields = ['id'] + sorted(total_fields - {'id'})
        with open(csv_file_name, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, delimiter='\t', fieldnames=combined_fields, restval='')
            writer.writeheader()
            for row in existing_rows:
                writer.writerow(row)
            writer.writerow(new_row)

def write_evidence_names_to_csv(evidence_id_name_mapping: Dict[str, str], csv_file_name: str) -> None:
    """
    Adds a column with evidence names to a TSV file, using pe_id as the key.

    The pe_id is expected to be in the first column of the TSV file, in the format "projectPrefix:evidencePrefix".

    :param evidence_id_name_mapping: Mapping from pe_id to evidence name.
    :param   csv_file_name: Path to the TSV file to update.
    """
    temp_path = csv_file_name + ".tmp"

    with open(csv_file_name, "r", newline="") as infile, open(temp_path, "w", newline="") as outfile:
        reader = csv.reader(infile, delimiter='\t')
        writer = csv.writer(outfile, delimiter='\t')

        header = next(reader)
        header.insert(1, "evidence_name")
        writer.writerow(header)

        for row in reader:
            pe_id = row[0]
            evidence_name = evidence_id_name_mapping.get(pe_id, "")
            row.insert(1, evidence_name)
            writer.writerow(row)

    os.replace(temp_path, csv_file_name)
