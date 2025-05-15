from typing import Optional

from hansken.connect import ProjectContext

from hmclib.hmc_plugin_class import HMCStandardPlugin
from util.hansken_search import count_traces_of_type


class CaseImages(HMCStandardPlugin):

    def __init__(self, context: Optional[ProjectContext] = None):
        name = 'case_image_count'
        desc = 'Number of images within a case.'
        result_list = ['case_images']
        super().__init__(name, desc, result_list, context)

    def collect_metrics(self):
        self.results.result_output['case_images'] = self.count_images_in_case()
        return self.results

    def count_images_in_case(self):
        type_to_search = "image"
        count = count_traces_of_type(self.context, type_to_search)
        return count
