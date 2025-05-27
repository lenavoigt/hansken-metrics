from typing import Optional

from hansken.connect import ProjectContext

from hmclib.hmc_plugin_class import HMCStandardPlugin
from hmclib.hansken_search import get_buckets_with_hql


class LifeTimeInfoUfed(HMCStandardPlugin):

    def __init__(self, context: Optional[ProjectContext] = None, evidence_id: Optional[str] = None):
        name = 'phone_life_time_info_ufed'
        desc = 'Some information that might help estimate the device life time for devices acquired with ufed'
        result_list = ['factory_reset', 'last_hotspot_activity']
        super().__init__(name, desc, result_list, context, evidence_id)

    def collect_metrics(self):
        self.results.result_output['factory_reset'] = self.get_folder_misc_info(r"folder.misc.Factory Reset",
                                                                                r'folder.misc.Factory\ Reset:*')
        self.results.result_output['last_hotspot_activity'] = self.get_folder_misc_info(
            r'folder.misc.DeviceInfoLastHotspotActivity', r'folder.misc.DeviceInfoLastHotspotActivity:*')
        return self.results

    def get_folder_misc_info(self, facet_name, hql_query):
        misc_value_buckets = get_buckets_with_hql(self.context, hql_query, facet_name,
                                                  evidence_id=self.evidence_id)
        if len(misc_value_buckets) == 1:
            return misc_value_buckets[0][0]
        elif len(misc_value_buckets) < 1:
            return None
        else:
            os_versions = [os_type for (os_type, _) in misc_value_buckets]
            return os_versions
