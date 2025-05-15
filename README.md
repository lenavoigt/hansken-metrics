# Hansken Metric Collector

The Hansken Metric Collector (HMC) is a tool that automates the collection of metrics from Hansken cases via the [Hansken Python API](https://training.hansken.org/docs/python/), summarizing the results in a csv file.

## Usage

To retrieve metrics from Hansken cases, run the following command within **your project's virtual environment** (see setup instructions below):
```
$ python hmc.py case_id1 [case_id2 ...] [--extract_evidence_names]
```
or, to retrieve metrics for **all** cases in the current Hansken context:
```
$ python hmc.py all [--extract_evidence_names]
```

- ```case_id1 case_id2 ...``` — A space-separated list of one or more Hansken case IDs for which to retrieve metrics. Alternatively, use `all` to process all cases available in the current context.

- ```--extract_evidence_names``` (optional) — Include this flag to also extract and include evidence item names in the csv output table (besides the evidence id). This can be useful when generating metrics for internal analysis or reporting.

## Preparation

Before you can run the metric collection with HMC, you need to:

0. Set up a virtual environment and install the dependencies from `requirements.txt`.
1. Create a configuration file `evironment_config.py` file for Hansken's Python API access to your Hansken context.
2. *(Optionally)* Select the plugins that should be enabled in your metric collection run. Per default, all currently supported plugins are enabled.

These steps are detailed below.

## Virtual Environment Setup and Dependency Installation

We recommend setting up a virtual environment to use HMC and installing the dependencies with the following commands:

```
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

## Creation and Modification of an `environment_config.py`

The file `environment_config.example.py` is provided as a template. Before you can run HMC you need to copy it to `environment_config.py`:
```
$ cp config/environment_config.example.py environment_config.py

Afterward, you need to modify the config file as follows ... (tbd)
```
## Selection of Plugins

The file `config/plugins_config.py` contains a list of all currently supported metrics. By thefault, they are all enabled. To disable a plugin, comment out the respective line of the list (using `#`):
```
enabled_plugins = [
    ...
    # "browser_history_count", 	# disabled metric
    "calendar",			# enabled metric	  	
    "contacts",			# enabled metric
    ...
    ]
```

