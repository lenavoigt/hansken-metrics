from typing import Optional

from hansken.connect import ProjectContext

from hmclib.hmc_plugin_class import HMCStandardPlugin
from util.hansken_search import count_traces_of_type, count_traces_with_hql


class Contacts(HMCStandardPlugin):

    def __init__(self, context: Optional[ProjectContext] = None, evidence_id: Optional[str] = None):
        name = 'contact_count'
        desc = 'Metrics related to contacts (number of contacts and contact related to selected applications)'
        result_list = ['contacts_all', 'contacts_native', 'contacts_snapchat', 'contacts_whatsapp', 'contacts_telegram',
                       'contacts_signal', 'contacts_instagram']
        super().__init__(name, desc, result_list, context, evidence_id)

    def collect_metrics(self):
        self.results.result_output['contacts_all'] = self.count_contacts()
        self.results.result_output['contacts_native'] = self.count_contacts_native()
        self.results.result_output['contacts_snapchat'] = self.count_contacts_application('snapchat')
        self.results.result_output['contacts_whatsapp'] = self.count_contacts_application('whatsapp')
        self.results.result_output['contacts_telegram'] = self.count_contacts_application('telegram')
        self.results.result_output['contacts_signal'] = self.count_contacts_application('signal')
        self.results.result_output['contacts_instagram'] = self.count_contacts_application('instagram')
        return self.results

    def count_contacts(self):
        type_to_search = 'contact'
        count = count_traces_of_type(self.context, type_to_search, self.evidence_id)
        return count

    def count_contacts_application(self, application_name: str):
        type_to_search = 'contact'
        hql_query = r'contact.application:' + application_name
        count = count_traces_with_hql(self.context, hql_query, type_to_search, 'type', evidence_id=self.evidence_id)
        return count

    def count_contacts_native(self):
        type_to_search = 'contact'
        hql_query = r'contact.application:*'
        count_application_contacts = count_traces_with_hql(self.context, hql_query, type_to_search, 'type',
                                                           evidence_id=self.evidence_id)
        count_all_contacts = self.count_contacts()
        count = count_all_contacts - count_application_contacts
        return count