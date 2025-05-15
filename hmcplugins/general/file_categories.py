from typing import Optional

from hansken.connect import ProjectContext

from hmclib.hmc_plugin_class import HMCStandardPlugin
from util.hansken_search import count_traces_with_hql, count_traces_of_type


# according to categories as seen in hansken tactical ui
class FileCategories(HMCStandardPlugin):

    def __init__(self, context: Optional[ProjectContext] = None, evidence_id: Optional[str] = None):
        name = 'file_category'
        desc = 'Number of files that match different categories.'
        result_list = ['archive', 'database', 'deleted', 'documents', 'encrypted', 'executable', 'multimedia',
                       'pictures', 'presentations', 'spreadsheets']
        super().__init__(name, desc, result_list, context, evidence_id)

    def collect_metrics(self):
        self.results.result_output['archive'] = count_traces_of_type(self.context,'fileArchive', self.evidence_id)
        self.results.result_output['deleted'] = count_traces_of_type(self.context,'deleted', self.evidence_id)
        self.results.result_output['documents'] = count_traces_of_type(self.context,'document', self.evidence_id)
        self.results.result_output['encrypted'] = count_traces_of_type(self.context,'encrypted', self.evidence_id)
        self.results.result_output['multimedia'] = self.count_multimedia()
        self.results.result_output['pictures'] = self.count_pictures()
        self.results.result_output['presentations'] = self.count_presentations()
        self.results.result_output['spreadsheets'] = self.count_spreadsheets()
        return self.results


    def count_multimedia(self):
        hql_query = r"(type:audio OR type:video OR type:picture)"
        count = count_traces_with_hql(self.context, hql_query, 'origin', 'type', evidence_id=self.evidence_id)
        return count

    def count_pictures(self):
        hql_query = r"type:picture AND NOT file.extension:db AND NOT type:video"
        count = count_traces_with_hql(self.context, hql_query, 'picture', 'type', evidence_id=self.evidence_id)
        return count

    def count_presentations(self):
        hql_query = r"document.type:presentation"
        count = count_traces_with_hql(self.context, hql_query, 'document', 'type', evidence_id=self.evidence_id)
        return count

    def count_spreadsheets(self):
        hql_query = r"document.type:spreadsheet"
        count = count_traces_with_hql(self.context, hql_query, 'document', 'type', evidence_id=self.evidence_id)
        return count
