# Hansken Metric Collector

The Hansken Metric Collector (HMC) is a tool that automates the collection of metrics from Hansken cases via the Hansken Python API, summarizing the results in a csv file.

## Usage

To retrieve metrics from Hansken cases, run the following command within **your project's virtual environment** (see setup instructions below):

```
$ python hmc.py [case_id1 case_id2 ...] [--extract_evidence_names]
```

- ```case_id1 case_id2 ...``` (optional) — One or more Hansken case IDs for which to retrieve metrics. You can provide a space-separated list. If omitted, metrics will be retrieved for all cases in the current Hansken context.

- ```--extract_evidence_names``` (optional) — Include this flag to also extract and include evidence item names in the output table (besides the evidence id). This can be useful when generating metrics for internal analysis or reporting.

## Preparation

Before you can run the metric collection with HMC, you need to:

0. Set up a virtual environment and install the dependencies from `requirements.txt`.
1. Create a configuration file `evironment_config.py` file for Hansken's Python API access to your Hansken context.
2. *(Optionally)* Select the plugins that should be enabled in your metric collection run. Per default, all currently supported plugins are enabled.

These steps are detailed below.

## Virtual Environment Setup and Dependency Installation

## Creation and Modification of an `environment_config.py`

## Selection of Plugins
