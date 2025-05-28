from typing import Optional, List

from hansken.connect import ProjectContext

from hmclib.hansken_search import get_children_of_registry_key
from hmclib.hmc_plugin_class import HMCStandardPlugin


class WinApplicationPresence(HMCStandardPlugin):

    def __init__(self, context: Optional[ProjectContext] = None, evidence_id: Optional[str] = None):
        name = 'windows_application_presence'
        desc = 'Presence of selected applications according to uninstall and app paths registry.'
        result_list = ['chrome', 'edge', 'firefox']
        super().__init__(name, desc, result_list, context, evidence_id)

    def collect_metrics(self):
        chrome_present = self.chrome_present()
        self.results.result_output['chrome'] = chrome_present
        self.results.result_output['edge'] = self.edge_present() if chrome_present is not None else None
        self.results.result_output['firefox'] = self.firefox_present() if chrome_present is not None else None
        return self.results

    def chrome_present(self):
        return self.application_present(['chrome'])

    def edge_present(self):
        return self.application_present(['msedge', 'iexplore'])

    def firefox_present(self):
        return self.application_present(['firefox', 'mozilla'])

    def application_present(self, application_names: List[str]) -> bool | None:
        registry_keys = [r"'/Microsoft/Windows/CurrentVersion/App Paths'",
                         r"'/Microsoft/Windows/CurrentVersion/Uninstall'"]

        registry_exists = False  # Indicates whether any of the registry keys were found
        for each_registry_key in registry_keys:
            registry_children = get_children_of_registry_key(self.context, each_registry_key, self.evidence_id)
            if registry_children:  # If the list is not empty, the key exists
                registry_exists = True

            for registry_child in registry_children:
                if any(each_application_name.lower() in registry_child.lower() for
                       each_application_name
                       in application_names):
                    return True  # Found a match for one of the application names
        if registry_exists:
            return False  # Registry keys exist, but no matching application found
        else:
            return None  # Registry keys do not exist
