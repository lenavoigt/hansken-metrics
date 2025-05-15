from typing import Optional

from hansken.connect import ProjectContext

from hmclib.hmc_plugin_class import HMCStandardPlugin
from util.hansken_search import count_traces_with_hql


class WinLnkCount(HMCStandardPlugin):

    def __init__(self, context: Optional[ProjectContext] = None, evidence_id: Optional[str] = None):
        name = 'windows_lnk_count'
        desc = 'Number of lnk files.'
        result_list = ['recent_lnk', 'lnk_in_user_folder', 'start_menu_lnk']
        super().__init__(name, desc, result_list, context, evidence_id)

    def collect_metrics(self):
        self.results.result_output['recent_lnk'] = self.count_recent_lnk()
        self.results.result_output['lnk_in_user_folder'] = self.count_link_in_user_folder()
        self.results.result_output['start_menu_lnk'] = self.count_start_menu_lnk()
        return self.results

    def count_recent_lnk(self):
        hql_query = r"file.path='*/AppData/Roaming/Microsoft/Windows/Recent/*' file.extension:lnk"
        count = count_traces_with_hql(context=self.context, hql_query=hql_query, facet_value_to_count='file',
                                      evidence_id=self.evidence_id)
        # for Windows XP
        if not count:
            hql_query = r"file.path='*/Documents and Settings/*/Recent/*' file.extension:lnk"
            count = count_traces_with_hql(context=self.context, hql_query=hql_query, facet_value_to_count='file',
                                        evidence_id=self.evidence_id)
        return count

    def count_link_in_user_folder(self):
        hql_query = r"file.path:'/users/*' file.extension:lnk"
        count = count_traces_with_hql(context=self.context, hql_query=hql_query, facet_value_to_count='file',
                                      evidence_id=self.evidence_id)
        return count

    def count_start_menu_lnk(self):
        hql_query = r"file.path='*/AppData/Roaming/Microsoft/Windows/Start Menu/*' file.extension:lnk"
        count = count_traces_with_hql(context=self.context, hql_query=hql_query, facet_value_to_count='file',
                                      evidence_id=self.evidence_id)
        return count