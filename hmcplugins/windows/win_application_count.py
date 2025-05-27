from typing import Optional

from hansken.connect import ProjectContext

from hmclib.hmc_plugin_class import HMCStandardPlugin
from hmclib.hansken_search import count_children_of_registry_key


class WinApplicationCount(HMCStandardPlugin):

    def __init__(self, context: Optional[ProjectContext] = None, evidence_id: Optional[str] = None):
        name = 'windows_application_count'
        desc = 'Number of applications according to uninstall and app paths registry.'
        result_list = ['application_uninstall_registry', 'application_app_paths_registry']
        super().__init__(name, desc, result_list, context, evidence_id)

    def collect_metrics(self):
        self.results.result_output['application_uninstall_registry'] = self.count_applications_uninstall()
        self.results.result_output['application_app_paths_registry'] = self.count_applications_app_paths()
        return self.results

    def count_applications_uninstall(self) -> int | None:
        registry_key = '\'/Microsoft/Windows/CurrentVersion/Uninstall\''
        return count_children_of_registry_key(self.context, self.evidence_id, registry_key)

    def count_applications_app_paths(self) -> int | None:
        registry_key = '\'/Microsoft/Windows/CurrentVersion/App\ Paths\''
        return count_children_of_registry_key(self.context, self.evidence_id, registry_key)