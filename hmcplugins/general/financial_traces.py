from typing import Optional

from hansken.connect import ProjectContext

from hmclib.hmc_plugin_class import HMCStandardPlugin
from hmclib.hansken_search import count_traces_of_type, count_traces_with_hql


class FinancialTraces(HMCStandardPlugin):

    def __init__(self, context: Optional[ProjectContext] = None, evidence_id: Optional[str] = None):
        name = 'financial'
        desc = 'Metrics/Counts related to cards (e.g. credit cards), wallets, and other traces falling into the financial category.'
        result_list = ['cards', 'card_archive', 'cards_debit', 'cards_credit', 'crypto_currency_wallet', 'crypto_key', 'crypto_key_info', 'crypto_key_pair', 'bid']
        super().__init__(name, desc, result_list, context, evidence_id)

    def collect_metrics(self):
        self.results.result_output['cards'] = self.count_cards()
        self.results.result_output['card_archive'] = self.count_card_archive()
        self.results.result_output['cards_debit'] = self.count_cards_debit()
        self.results.result_output['cards_credit'] = self.count_cards_credit()
        self.results.result_output['crypto_currency_wallet'] = self.count_crypto_wallet()
        self.results.result_output['crypto_key'] = self.count_crypto_key()
        self.results.result_output['crypto_key_info'] = self.count_crypto_key_info()
        self.results.result_output['crypto_key_pair'] = self.count_crypto_key_pair()
        self.results.result_output['bid'] = self.count_bid()
        return self.results

    def count_cards(self):
        type_to_search = 'cards'
        count = count_traces_of_type(self.context, type_to_search, self.evidence_id)
        return count


    def count_card_archive(self):
        type_to_search = 'cardArchive'
        count = count_traces_of_type(self.context, type_to_search, self.evidence_id)
        return count

    def count_crypto_wallet(self):
        type_to_search = 'cryptoCurrencyWallet'
        count = count_traces_of_type(self.context, type_to_search, self.evidence_id)
        return count

    def count_crypto_key(self):
        type_to_search = 'cryptoKey'
        count = count_traces_of_type(self.context, type_to_search, self.evidence_id)
        return count

    def count_crypto_key_info(self):
        type_to_search = 'cryptoKeyInfo'
        count = count_traces_of_type(self.context, type_to_search, self.evidence_id)
        return count

    def count_crypto_key_pair(self):
        type_to_search = 'cryptoKeyPair'
        count = count_traces_of_type(self.context, type_to_search, self.evidence_id)
        return count

    def count_cards_debit(self):
        type_to_search = 'card'
        hql_query = r'card.type=debit'
        count = count_traces_with_hql(self.context, hql_query, type_to_search, 'type', evidence_id=self.evidence_id)
        return count

    def count_cards_credit(self):
        type_to_search = 'card'
        hql_query = r'card.type=credit'
        count = count_traces_with_hql(self.context, hql_query, type_to_search, 'type', evidence_id=self.evidence_id)
        return count

    def count_bid(self):
        type_to_search = 'bid'
        count = count_traces_of_type(self.context, type_to_search, self.evidence_id)
        return count