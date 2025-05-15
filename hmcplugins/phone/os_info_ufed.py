from typing import Optional

from hansken.connect import ProjectContext

from hmclib.hmc_plugin_class import HMCStandardPlugin
from util.hansken_search import get_buckets_with_hql


class OSInfoUfed(HMCStandardPlugin):

    def __init__(self, context: Optional[ProjectContext] = None, evidence_id: Optional[str] = None):
        name = 'phone_os_info_ufed'
        desc = 'some info about the OS for devices acquired with ufed'
        result_list = ['os_type','os_version']
        super().__init__(name, desc, result_list, context, evidence_id)

    def collect_metrics(self):
        self.results.result_output['os_type'] = self.get_folder_misc_info('DeviceInfoOSType')
        self.results.result_output['os_version'] = self.get_folder_misc_info('DeviceInfoOSVersion')
        return self.results

    def get_folder_misc_info(self, value_name):
        hql_query = r"type:folder"
        facet_to_search = 'folder.misc.' + value_name
        misc_value_buckets = get_buckets_with_hql(self.context, hql_query, facet_to_search,
                                                  evidence_id=self.evidence_id)
        if len(misc_value_buckets) == 1:
            return misc_value_buckets[0][0]
        elif len(misc_value_buckets) < 1:
            return None
        else:
            os_versions = [os_type for (os_type, _) in misc_value_buckets]
            return os_versions