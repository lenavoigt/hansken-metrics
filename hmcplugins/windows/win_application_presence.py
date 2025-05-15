from typing import Optional, List

from hansken.connect import ProjectContext

from hmclib.hmc_plugin_class import HMCStandardPlugin
from util.hansken_search import bucket_name_present


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
        # print(self.results.result_output)
        return self.results

    def chrome_present(self):
        return self.application_present(['chrome'])

    def edge_present(self):
        return self.application_present(['msedge', 'iexplore'])

    def firefox_present(self):
        return self.application_present(['firefox', 'mozilla'])

    def application_present(self, application_names: List[str]):
        registry_keys = [r"'/Microsoft/Windows/CurrentVersion/App Paths'",
                         r"'/Microsoft/Windows/CurrentVersion/Uninstall'"]
        saw_false = False
        for each_registry_key in registry_keys:
            hql_query = r'parent->{type:registryEntry registryEntry.key:' + each_registry_key + r'}'
            present = bucket_name_present(self.context, hql_query, 'registryEntry.name', application_names,
                                          allow_partial_match=True,
                                          evidence_id=self.evidence_id)
            if present is True:
                return True
            elif present is False:
                saw_false = True

        if saw_false:
            return False

        return None
