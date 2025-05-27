from typing import Optional

from hansken.connect import ProjectContext

from hmclib.hmc_plugin_class import HMCStandardPlugin
from hmclib.hansken_search import count_traces_of_type


class Notes(HMCStandardPlugin):

    def __init__(self, context: Optional[ProjectContext] = None, evidence_id: Optional[str] = None):
        name = 'phone_note_count'
        desc = 'Number of traces with the type note.'
        result_list = ['notes']
        super().__init__(name, desc, result_list, context, evidence_id)

    def collect_metrics(self):
        self.results.result_output['notes'] = self.count_notes()
        return self.results

    def count_notes(self):
        type_to_search = "note"
        count = count_traces_of_type(self.context, type_to_search, self.evidence_id)
        return count