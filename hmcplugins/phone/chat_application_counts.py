from typing import Optional

from hansken.connect import ProjectContext

from hmclib.hmc_plugin_class import HMCStandardPlugin
from util.hansken_search import count_traces_of_type, count_traces_with_hql


class ChatApplicationCounts(HMCStandardPlugin):

    def __init__(self, context: Optional[ProjectContext] = None, evidence_id: Optional[str] = None):
        name = 'phone_chat_application_counts'
        desc = 'Metrics related to chats in different applications'
        result_list = ['native_chat_messages', 'whatsapp_chat_messages','instagram_chat_messages','telegram_chat_messages','snapchat_chat_messages','native_chat_conversations', 'whatsapp_chat_conversations','instagram_chat_conversations','telegram_chat_conversations','snapchat_chat_conversations', 'signal_chat_conversations','signal_chat_conversations']
        super().__init__(name, desc, result_list, context, evidence_id)

    def collect_metrics(self):
        self.results.result_output['native_chat_messages'] = self.count_chat_messages_of_application('native messages')
        self.results.result_output['whatsapp_chat_messages'] = self.count_chat_messages_of_application('whatsapp')
        self.results.result_output['instagram_chat_messages'] = self.count_chat_messages_of_application('instagram')
        self.results.result_output['telegram_chat_messages'] = self.count_chat_messages_of_application('telegram')
        self.results.result_output['snapchat_chat_messages'] = self.count_chat_messages_of_application('snapchat')
        self.results.result_output['signal_chat_messages'] = self.count_chat_messages_of_application('signal')
        self.results.result_output['native_chat_conversations'] = self.count_chat_conversation_of_application('native messages')
        self.results.result_output['whatsapp_chat_conversations'] = self.count_chat_conversation_of_application('whatsapp')
        self.results.result_output['instagram_chat_conversations'] = self.count_chat_conversation_of_application('instagram')
        self.results.result_output['telegram_chat_conversations'] = self.count_chat_conversation_of_application('telegram')
        self.results.result_output['snapchat_chat_conversations'] = self.count_chat_conversation_of_application('snapchat')
        self.results.result_output['signal_chat_conversations'] = self.count_chat_conversation_of_application('signal')
        return self.results

    def count_chat_messages_of_application(self, application_name):
        type_to_search = 'chatMessage'
        hql_query = r"chatMessage.application:" + application_name
        count = count_traces_with_hql(self.context, hql_query, type_to_search, 'type', evidence_id=self.evidence_id)
        return count

    def count_chat_conversation_of_application(self, application_name):
        type_to_search = 'chatConversation'
        hql_query = r"chatConversation.application:" + application_name
        count = count_traces_with_hql(self.context, hql_query, type_to_search, 'type', evidence_id=self.evidence_id)
        return count