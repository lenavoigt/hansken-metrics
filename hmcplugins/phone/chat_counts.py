from typing import Optional

from hansken.connect import ProjectContext

from hmclib.hmc_plugin_class import HMCStandardPlugin
from util.hansken_search import count_traces_of_type, count_traces_with_hql


class ChatCounts(HMCStandardPlugin):

    def __init__(self, context: Optional[ProjectContext] = None, evidence_id: Optional[str] = None):
        name = 'phone_chat_count'
        desc = 'Metrics related to chats and texts (number of conversations, messages, delivered messages)'
        result_list = ['chat_conversations', 'chat_messages', 'chat_messages_delivered', 'text_messages']
        super().__init__(name, desc, result_list, context, evidence_id)

    def collect_metrics(self):
        self.results.result_output['chat_conversations'] = self.count_chat_conversations()
        self.results.result_output['chat_messages'] = self.count_chat_messages()
        self.results.result_output['chat_messages_delivered'] = self.count_chat_messages_delivered()
        self.results.result_output['text_messages'] = self.count_text_messages()
        return self.results

    def count_chat_messages(self):
        type_to_search = 'chatMessage'
        count = count_traces_of_type(self.context, type_to_search, self.evidence_id)
        return count

    def count_chat_conversations(self):
        type_to_search = 'chatConversation'
        count = count_traces_of_type(self.context, type_to_search, self.evidence_id)
        return count

    def count_chat_messages_delivered(self):
        type_to_search = 'chatMessage'
        hql_query = r"chatMessage.deliveredOn:*"
        count = count_traces_with_hql(self.context, hql_query, type_to_search, 'type', evidence_id=self.evidence_id)
        return count

    def count_text_messages(self):
        type_to_search = 'textMessage'
        count = count_traces_of_type(self.context, type_to_search, self.evidence_id)
        return count