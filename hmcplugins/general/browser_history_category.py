import json
from typing import Optional

from hansken.connect import ProjectContext

from hmclib.hmc_plugin_class import HMCStandardPlugin
from hmclib.hansken_search import count_traces_with_hql


# according to category matching in resources/browser_categories.json with sources provided in resources/browser_category_sources.txt
class BrowserHistoryCategory(HMCStandardPlugin):
    browser_categories = None
    def __init__(self, context: Optional[ProjectContext] = None, evidence_id: Optional[str] = None):
        name = 'browser_history_category'
        desc = 'Number of browser history entries that match different categories.'
        result_list = ['banking', 'cryptocurrency', 'data_transfer', 'insurance', 'messaging',
                       'news', 'search_engines', 'shopping', 'social_media', 'streaming', 'travel', 'webmail', 'darkweb']
        super().__init__(name, desc, result_list, context, evidence_id)
        if BrowserHistoryCategory.browser_categories is None:
            with open('resources/browser_categories.json', 'r') as f:
                BrowserHistoryCategory.browser_categories = json.load(f)

    def collect_metrics(self):
        self.results.result_output['banking'] = self.count_urls("Banking")
        self.results.result_output['cryptocurrency'] = self.count_urls("Cryptocurrency")
        self.results.result_output['data_transfer'] = self.count_urls("Data Transfer")
        self.results.result_output['insurance'] = self.count_urls("Insurance")
        self.results.result_output['messaging'] = self.count_urls("Messaging")
        self.results.result_output['news'] = self.count_urls("News")
        self.results.result_output['search_engines'] = self.count_urls("Search Engines")
        self.results.result_output['shopping'] = self.count_urls("Shopping")
        self.results.result_output['social_media'] = self.count_urls("Social Media")
        self.results.result_output['streaming'] = self.count_urls("Streaming")
        self.results.result_output['travel'] = self.count_urls("Travel")
        self.results.result_output['webmail'] = self.count_urls("Webmail")
        self.results.result_output['darkweb'] = self.count_darkweb()
        return self.results


    @staticmethod
    def has_tld(url: str) -> bool:
        # very simplified check for tld being included in the url from the url list
        # (which would be desirable for all urls but is not the case e.g for societegenerale, barclays, etc
        return '.' in url


    def count_urls(self, category_name: str) -> int:
        urls = BrowserHistoryCategory.browser_categories.get(category_name, [])
        hql_query = ' OR '.join(
            f"(type:browserHistory AND (browserHistory.url:{url}{'' if self.has_tld(url) else '*'} OR browserHistory.url:*.{url}{'' if self.has_tld(url) else '*'} OR browserHistory.url:'{url}{'' if self.has_tld(url) else '*'}/*' OR browserHistory.url:'*.{url}{'' if self.has_tld(url) else '*'}/*'  OR url.host:{url}{'' if self.has_tld(url) else '*'} OR url.host:*.{url}{'' if self.has_tld(url) else '*'}))"
            # there is most likely a nicer way to do this ...
            # Things to consider (trying to find a good balance between false negatives and false positives)
            # - dont get bing.com for ing.com
            # - get access.ing.com for ing.com
            # - dont get https://www.facebook.com/?[...]gmail.com[...] for gmail.com
            for url in urls
        )
        count = count_traces_with_hql(self.context, hql_query, 'browserHistory', 'type', evidence_id=self.evidence_id)
        return count


    def count_darkweb(self):
        # simply counting .onion links
        hql_query = r"type:browserHistory AND ((browserHistory.url:*.onion OR browserHistory.url:*'.onion/'*) AND url.host:*.onion)"
        count = count_traces_with_hql(self.context, hql_query, 'browserHistory', 'type', evidence_id=self.evidence_id)
        return count
