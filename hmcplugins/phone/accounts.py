from typing import Optional

from hansken.connect import ProjectContext

from hmclib.hmc_plugin_class import HMCStandardPlugin
from hmclib.hansken_search import count_traces_of_type


class Accounts(HMCStandardPlugin):

    def __init__(self, context: Optional[ProjectContext] = None, evidence_id: Optional[str] = None):
        name = 'phone_accounts'
        desc = 'Number of traces with the type account.'
        result_list = ['accounts_all']
        super().__init__(name, desc, result_list, context, evidence_id)

    def collect_metrics(self):
        self.results.result_output['accounts_all'] = count_traces_of_type(self.context, 'account', self.evidence_id)
        return self.results