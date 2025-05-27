from typing import Optional

from hansken.connect import ProjectContext

from hmclib.hmc_plugin_class import HMCStandardPlugin
from hmclib.hansken_search import count_traces_of_type, count_traces_with_hql


class PhoneCalls(HMCStandardPlugin):

    def __init__(self, context: Optional[ProjectContext] = None, evidence_id: Optional[str] = None):
        name = 'phone_call_count'
        desc = 'Number of traces with the type phoneCall.'
        result_list = ['phone_calls', 'phone_calls_incoming']
        super().__init__(name, desc, result_list, context, evidence_id)

    def collect_metrics(self):
        self.results.result_output['phone_calls'] = self.count_phone_calls()
        self.results.result_output['phone_calls_incoming'] = self.count_phone_calls_incoming()
        return self.results

    def count_phone_calls(self):
        type_to_search = "phoneCall"
        count = count_traces_of_type(self.context, type_to_search, self.evidence_id)
        return count

    def count_phone_calls_incoming(self):
        type_to_search = 'phoneCall'
        hql_query = r"phoneCall.from:*"
        count = count_traces_with_hql(self.context, hql_query, type_to_search, 'type', evidence_id=self.evidence_id)
        return count