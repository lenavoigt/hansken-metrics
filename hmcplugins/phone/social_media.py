from typing import Optional

from hansken.connect import ProjectContext

from hmclib.hmc_plugin_class import HMCStandardPlugin
from hmclib.hansken_search import count_traces_with_hql


class SocialMedia(HMCStandardPlugin):

    def __init__(self, context: Optional[ProjectContext] = None, evidence_id: Optional[str] = None):
        name = 'phone_social_media'
        desc = 'Number of trace related to social media activity'
        result_list = ['social_media_activity']
        super().__init__(name, desc, result_list, context, evidence_id)

    def collect_metrics(self):
        self.results.result_output['social_media_activity'] = self.count_social_media_activity()
        return self.results

    # as done in hansken tactical user interface
    def count_social_media_activity(self):
        hql_query = r"event.misc.model_type:SocialMediaActivity"
        count = count_traces_with_hql(self.context, hql_query, 'origin', 'type', evidence_id=self.evidence_id)
        return count
