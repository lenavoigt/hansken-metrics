from typing import Optional

from hansken.connect import ProjectContext

from hmclib.hmc_plugin_class import HMCStandardPlugin
from util.hansken_search import count_traces_of_type, count_traces_with_hql


class TextInput(HMCStandardPlugin):

    def __init__(self, context: Optional[ProjectContext] = None, evidence_id: Optional[str] = None):
        name = 'phone_text_input'
        desc = 'Number of trace related to text inputs'
        result_list = ['text_input_all', 'text_input_dictionary_words', 'text_input_autofill']
        super().__init__(name, desc, result_list, context, evidence_id)

    def collect_metrics(self):
        self.results.result_output['text_input_all'] = self.count_text_input()
        self.results.result_output['text_input_dictionary_words'] = self.count_text_input_dictionary()
        self.results.result_output['text_input_autofill'] = self.count_text_input_autofill()
        return self.results

    # as done in hansken tactical user interface
    def count_text_input(self):
        type_to_search = 'textInput'
        count = count_traces_of_type(self.context, type_to_search, self.evidence_id)
        return count

    def count_text_input_dictionary(self):
        hql_query = r"textInput.type:'dictionary word'"
        count = count_traces_with_hql(self.context, hql_query, 'origin', 'type', evidence_id=self.evidence_id)
        return count

    def count_text_input_autofill(self):
        hql_query = r"textInput.type:'autofill'"
        count = count_traces_with_hql(self.context, hql_query, 'origin', 'type', evidence_id=self.evidence_id)
        return count