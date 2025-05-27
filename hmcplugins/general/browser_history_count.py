from typing import Optional

from hansken.connect import ProjectContext

from hmclib.hmc_plugin_class import HMCStandardPlugin
from hmclib.hansken_search import count_traces_of_type, count_traces_with_hql


class BrowserHistoryCount(HMCStandardPlugin):

    def __init__(self, context: Optional[ProjectContext] = None, evidence_id: Optional[str] = None):
        name = 'browser_history_count'
        desc = 'Number of browser history entries (overall and with at least one visit) and traces related to browser searches, bookmark, cookies.'
        result_list = ['browser_history_all', 'browser_history_w_visit', 'browser_bookmarks', 'cookies',
                       'cookie_archives', 'search_traces', 'browser_searches_complex']
        super().__init__(name, desc, result_list, context, evidence_id)

    def collect_metrics(self):
        self.results.result_output['browser_history_all'] = self.count_browser_history_entries_all()
        self.results.result_output['browser_history_w_visit'] = self.count_browser_history_entries_with_visits()
        self.results.result_output['browser_bookmarks'] = self.count_bookmarks()
        self.results.result_output['search_traces'] = self.count_search_traces()
        self.results.result_output['cookies'] = self.count_cookies()
        self.results.result_output['cookie_archives'] = self.count_cookie_archives()
        self.results.result_output['browser_searches_complex'] = self.count_searches_complex()
        return self.results

    def count_browser_history_entries_all(self):
        type_to_search = "browserHistory"
        count = count_traces_of_type(self.context, type_to_search, self.evidence_id)
        return count

    def count_browser_history_entries_with_visits(self):
        type_to_search = "browserHistory"
        facet_to_search = 'type'
        hql_query = r"browserHistory.visitCount>=1"
        count = count_traces_with_hql(self.context, hql_query, type_to_search, facet_to_search,
                                      evidence_id=self.evidence_id)
        return count

    def count_bookmarks(self):
        type_to_search = "bookmark"
        count = count_traces_of_type(self.context, type_to_search, self.evidence_id)
        return count

    def count_search_traces(self):
        type_to_search = "search"
        count = count_traces_of_type(self.context, type_to_search, self.evidence_id)
        return count

    def count_searches_complex(self):
        # adding search engine visits (in particular searches) to search count
        # only checking for google, bing, duckduckgo, ecosia and startpage right now
        hql_query = (r"type:search OR ((url.query:* OR url.queries:*) AND ((type:browserHistory AND "
                     r"(browserHistory.url:google* OR url.host:google*) AND url.path:'/search') OR "
                     r"(browserHistory.url:Bing* OR url.host:Bing*) OR (browserHistory.url:DuckDuckGo* OR "
                     r"url.host:DuckDuckGo*) OR (browserHistory.url:Ecosia* OR url.host:Ecosia*) OR "
                     r"(browserHistory.url:Startpage* OR url.host:Startpage*)))")
        type_to_search = 'browserHistory'
        facet_to_search = 'type'
        count = count_traces_with_hql(self.context, hql_query, type_to_search, facet_to_search,
                                      evidence_id=self.evidence_id)
        return count

    def count_cookies(self):
        type_to_search = "cookie"
        count = count_traces_of_type(self.context, type_to_search, self.evidence_id)
        return count

    def count_cookie_archives(self):
        type_to_search = "cookieArchive"
        count = count_traces_of_type(self.context, type_to_search, self.evidence_id)
        return count
