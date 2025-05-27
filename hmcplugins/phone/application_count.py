from typing import Optional

from hansken.connect import ProjectContext

from hmclib.hmc_plugin_class import HMCStandardPlugin
from hmclib.hansken_search import count_traces_of_type, count_traces_with_hql


class ApplicationCount(HMCStandardPlugin):

    def __init__(self, context: Optional[ProjectContext] = None, evidence_id: Optional[str] = None):
        name = 'phone_application_count'
        desc = 'Number of applications (overall and where the name field has a value).'
        result_list = ['application_all', 'application_w_name']
        super().__init__(name, desc, result_list, context, evidence_id)

    def collect_metrics(self):
        self.results.result_output['application_all'] = self.count_applications_all()
        self.results.result_output['application_w_name'] = self.count_applications_w_name()
        return self.results

    def count_applications_all(self):
        type_to_search = "application"
        count = count_traces_of_type(self.context, type_to_search, self.evidence_id)
        return count

    def count_applications_w_name(self):
        type_to_search = "application"
        hql_query = r"application.name:*"
        count = count_traces_with_hql(self.context, hql_query, type_to_search, 'type', evidence_id=self.evidence_id)
        return count
