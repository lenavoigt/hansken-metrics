# data.raw.mimeClass='document'

from typing import Optional, List

from hansken.connect import ProjectContext

from hmclib.hmc_plugin_class import HMCStandardPlugin
from util.hansken_search import get_buckets_with_hql


class MimeClasses(HMCStandardPlugin):

    def __init__(self, context: Optional[ProjectContext] = None, evidence_id: Optional[str] = None):
        name = 'file_mime_class_count'
        desc = 'Dynamic Plugin! (i.e., no predefined result list) Number of files for different mime types.'
        result_list = []
        super().__init__(name, desc, result_list, context, evidence_id)

    def collect_metrics(self):
        mime_class_counts = get_buckets_with_hql(self.context, 'type:file', 'data.raw.mimeClass',
                                                 evidence_id=self.evidence_id)
        for each_mime_class, each_mime_class_count in mime_class_counts:
            self.results.result_output[each_mime_class] = each_mime_class_count
        return self.results
