from typing import Optional

from hansken.connect import ProjectContext

from hmclib.hmc_plugin_class import HMCStandardPlugin
from util.hansken_search import count_traces_of_type, count_traces_with_hql


class Emails(HMCStandardPlugin):

    def __init__(self, context: Optional[ProjectContext] = None, evidence_id: Optional[str] = None):
        name = 'email_count'
        desc = 'Number of traces with the type email.'
        result_list = ['emails_all', 'emails_w_attachment', 'email_folders', 'email_archives']
        super().__init__(name, desc, result_list, context, evidence_id)

    def collect_metrics(self):
        self.results.result_output['emails_all'] = self.count_emails()
        self.results.result_output['email_folders'] = self.count_email_folders()
        self.results.result_output['email_archives'] = self.count_email_archives()
        self.results.result_output['emails_w_attachment'] = self.count_emails_w_attachment()
        return self.results

    def count_emails(self):
        type_to_search = "email"
        count = count_traces_of_type(self.context, type_to_search, self.evidence_id)
        return count

    def count_emails_w_attachment(self):
        type_to_search = "email"
        hql_query = r'email.hasAttachment:true'
        count = count_traces_with_hql(self.context, hql_query, type_to_search, 'type', evidence_id=self.evidence_id)
        return count

    def count_email_folders(self):
        type_to_search = "emailFolder"
        count = count_traces_of_type(self.context, type_to_search, self.evidence_id)
        return count

    def count_email_archives(self):
        type_to_search = "emailArchive"
        count = count_traces_of_type(self.context, type_to_search, self.evidence_id)
        return count