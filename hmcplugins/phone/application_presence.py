from typing import Optional, List

from hansken.connect import ProjectContext

from hmclib.hmc_plugin_class import HMCStandardPlugin
from util.hansken_search import bucket_name_present


class ApplicationPresence(HMCStandardPlugin):

    def __init__(self, context: Optional[ProjectContext] = None, evidence_id: Optional[str] = None):
        name = 'phone_application_presence'
        desc = 'Presence of selected applications (identified by package name).'
        result_list = ['whatsapp_present', 'signal_present', 'telegram_present']
        super().__init__(name, desc, result_list, context, evidence_id)

    def collect_metrics(self):
        self.results.result_output['whatsapp_present'] = self.whatsapp_present()
        self.results.result_output['signal_present'] = self.signal_present()
        self.results.result_output['telegram_present'] = self.telegram_present()
        return self.results

    def application_present(self, package_names: List[str]):
        hql_query = r'type:application'
        return bucket_name_present(self.context, hql_query, 'application.package', package_names, allow_partial_match=False, evidence_id=self.evidence_id)

    def whatsapp_present(self):
        return self.application_present(['com.whatsapp', 'net.whatsapp.WhatsApp'])

    def signal_present(self):
        return self.application_present(['org.thoughtcrime.securesms'])

    def telegram_present(self):
        return self.application_present(['org.telegram.messenger', 'ph.telegra.Telegraph'])



