from typing import Optional

from hansken.connect import ProjectContext

from hmclib.hmc_plugin_class import HMCStandardPlugin
from util.hansken_search import count_traces_with_hql


class WinEventLogCount(HMCStandardPlugin):

    def __init__(self, context: Optional[ProjectContext] = None, evidence_id: Optional[str] = None):
        name = 'windows_event_log_count'
        desc = 'Number of occurrences of different event types in the event log (currently Security.evtx only).'
        result_list = ['evtx_win_startup_4608',
                       'evtx_success_logins_4624_2',
                       'evtx_failed_logins_4625',
                       'evtx_unlocks_4624_7',
                       'evtx_clock_change_4616']
        super().__init__(name, desc, result_list, context, evidence_id)

    def collect_metrics(self):
        self.results.result_output['evtx_win_startup_4608'] = self.count_events_with_id('4608')
        self.results.result_output['evtx_success_logins_4624_2'] = self.count_events_with_id('4624', 'event.misc.LogonType:2')
        self.results.result_output['evtx_user_initiated_logoff_4647'] = self.count_events_with_id('4647')
        self.results.result_output['evtx_failed_logins_4625'] =  self.count_events_with_id('4625')
        self.results.result_output['evtx_unlocks_4624_7'] = self.count_events_with_id('4624', 'event.misc.LogonType:7')
        self.results.result_output['evtx_clock_change_4616'] = self.count_events_with_id('4616')
        return self.results

    def count_events_with_id(self, event_id: str, further_restriction = None):
        hql_query = r"event.id:" + event_id
        if further_restriction:
            hql_query = hql_query + ' ' + further_restriction
        count = count_traces_with_hql(context=self.context, hql_query=hql_query, facet_value_to_count='event',
                                      facet_for_filtering='type', evidence_id=self.evidence_id)
        return count

