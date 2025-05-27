from typing import Optional

from hansken.connect import ProjectContext

from hmclib.hmc_plugin_class import HMCStandardPlugin
from hmclib.hansken_search import count_traces_of_type


class General(HMCStandardPlugin):

    def __init__(self, context: Optional[ProjectContext] = None, evidence_id: Optional[str] = None):
        name = 'general'
        desc = 'Metrics related to general structure of the fs/device.'
        result_list = ['file_system', 'volume']
        super().__init__(name, desc, result_list, context, evidence_id)

    def collect_metrics(self):
        self.results.result_output['file_system'] = self.count_file_system()
        self.results.result_output['volume'] = self.count_volume()
        return self.results

    def count_file_system(self):
        type_to_search = 'filesystem'
        count = count_traces_of_type(self.context, type_to_search, self.evidence_id)
        return count


    def count_volume(self):
        type_to_search = 'volume'
        count = count_traces_of_type(self.context, type_to_search, self.evidence_id)
        return count