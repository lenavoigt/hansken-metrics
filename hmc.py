import argparse
import logging
import sys
import time
from typing import List

from hansken.connect import connect_project, connect
from hansken.remote import ProjectContext

from config import environment_config
from config.environment_config import interactive, verify
from config.plugins_config import enabled_plugins
from hmclib.hmc_plugin_class import HMCStandardResult, HMCStandardPlugin
from hmclib.plugin_registry import plugin_registry
from util.hansken_search import get_evidence_ids
from util.write_to_file import write_single_evidence_results_to_tsv, write_single_evidence_results_to_json, \
    generate_result_file_names, write_evidence_names_to_csv


def load_enabled_plugins():
    plugins = []

    for name in enabled_plugins:
        plugin_class = plugin_registry.get(name)
        if plugin_class:
            plugins.append(plugin_class())
        else:
            print(f"Plugin not found in registry: {name} \nSkipping...")

    return plugins


def run_plugins(context: ProjectContext, evidence_id: str, plugins: List[HMCStandardPlugin],
                error_summary: List[dict]) -> List[HMCStandardResult]:
    results = []
    for each_plugin in plugins:
        try:
            print(f'    - Running {each_plugin.name} ... ', end='')
            each_plugin.set_context(context)
            each_plugin.set_evidence_id(evidence_id)
            res = each_plugin.plugin_metric_collection()
            results.append(res)
            print('Success.')
        except Exception as _:
            print(f"!! FAILURE !! - see log")
            logging.exception(
                f"An error occurred for  {each_plugin.name} Plugin in case {context.project_id} evidence {evidence_id}.")
            error_summary.append({
                "case_id": context.project_id,
                "evidence_id": evidence_id,
                "plugin": each_plugin.name
            })
    return results


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("case_ids", nargs='+', help="One or more case IDs")
    parser.add_argument("--extract_evidence_names", action="store_true", help="Optionally extract evidence names.")

    if len(sys.argv) == 1:
        parser.error("Cannot collect metrics. At least one case ID must be provided.")

    return parser.parse_args()


def get_case_ids(connection, input_ids):
    if len(input_ids) == 1 and input_ids[0] == 'all':
        return [case_id['id'] for case_id in connection.projects()]
    return input_ids


def setup_logging(log_filename):
    logging.basicConfig(
        filename=log_filename,
        filemode='a',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )


def log_errors(current_error_summary):
    if current_error_summary:
        logging.error("Summary of errors:")
        print("Errors encountered:")
        for error in current_error_summary:
            logging.error(
                f"Case ID: {error['case_id']}, Evidence ID: {error['evidence_id']}, Plugin: {error['plugin']}")
            print(f" - Case ID: {error['case_id']}, Evidence ID: {error['evidence_id']}, Plugin: {error['plugin']}")


def log_summary(num_plugins, num_cases, start_time):
    elapsed_time = time.time() - start_time
    hours = int(elapsed_time // 3600)
    minutes = int((elapsed_time % 3600) // 60)
    seconds = int(elapsed_time % 60)
    print('#####################')
    print('#####################')
    print(
        f"Processed *{num_plugins}* plugin(s) for *{num_cases}* cases in {hours}h {minutes}min {seconds}s.")
    logging.info(f"Processed:\n"
                 f" - Number of plugins: {num_plugins}\n"
                 f" - Number of cases: {num_cases}\n"
                 f" - Runtime: {hours:02d}:{minutes:02d}:{seconds:02d}")


def run_main():
    args = parse_args()

    end_point = environment_config.gatekeeper
    key_store = environment_config.keystore
    user_name = environment_config.username
    password = environment_config.password

    connection = connect(endpoint=end_point,
                         keystore=key_store,
                         username=user_name,
                         password=password,
                         interactive=interactive,
                         verify=verify)

    case_ids = get_case_ids(connection, args.case_ids)
    plugin_classes = load_enabled_plugins()

    json_filename, csv_filename, log_filename = generate_result_file_names()

    setup_logging(log_filename)

    evidence_id_name_mapping = {}
    current_error_summary = []

    start_time = time.time()

    for each_case_id in case_ids:
        current_context = connect_project(endpoint=end_point,
                                          project=each_case_id,
                                          keystore=key_store,
                                          username=user_name,
                                          password=password,
                                          interactive=interactive,
                                          verify=verify)

        with current_context:

            evidence_ids = get_evidence_ids(current_context)

            print('#####################')
            print(
                f"Collecting metrics from {len(plugin_classes)} plugins for {len(evidence_ids)} evidence items in context {each_case_id}.")
            print('#####################')

            if args.extract_evidence_names:
                print("Extracting evidence names...")
                project_prefix = current_context.project_id.split('-')[0]
                for each_evidence_id in evidence_ids:
                    pe_id = f"{project_prefix}:{each_evidence_id.split('-')[0]}"
                    evidence_id_name_mapping[pe_id] = current_context.image_name(each_evidence_id)

            for each_evidence in evidence_ids:
                print(f" > Processing evidence item with id {each_evidence}:")
                each_evidence_standard_result_object_list = run_plugins(current_context, each_evidence, plugin_classes,
                                                                        current_error_summary)
                each_evidence_result_list = [res.results_to_dict() for res in each_evidence_standard_result_object_list]
                write_single_evidence_results_to_json(current_context.project_id, each_evidence,
                                                      each_evidence_result_list,
                                                      json_filename)
                write_single_evidence_results_to_tsv(current_context.project_id, each_evidence,
                                                     each_evidence_result_list,
                                                     csv_filename)

    if args.extract_evidence_names:
        write_evidence_names_to_csv(evidence_id_name_mapping, csv_filename)

    log_errors(current_error_summary)
    log_summary(len(plugin_classes), len(case_ids), start_time)


if __name__ == '__main__':
    run_main()
