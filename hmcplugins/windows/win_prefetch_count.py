from statistics import mean
from typing import Optional

from hansken.connect import ProjectContext

from hmclib.hmc_plugin_class import HMCStandardPlugin
from hmclib.hansken_search import count_traces_with_hql, get_buckets_with_hql


class WinPrefetchCount(HMCStandardPlugin):

    def __init__(self, context: Optional[ProjectContext] = None, evidence_id: Optional[str] = None):
        name = 'windows_prefetch_count'
        desc = 'Number of prefetch files.'
        result_list = ['prefetch_files_all', 'prefetch_events_hansken', 'prefetch_max_run_count',
                       'prefetch_sum_run_count', 'prefetch_mean_run_count']
        super().__init__(name, desc, result_list, context, evidence_id)

    def collect_metrics(self):
        self.results.result_output['prefetch_files_all'] = self.count_prefetch_files_all()
        self.results.result_output['prefetch_events_hansken'] = self.count_prefetch_events_hansken()
        self.results.result_output['prefetch_max_run_count'] = self.prefetch_max_run_count()
        self.results.result_output['prefetch_sum_run_count'] = self.prefetch_sum_run_count()
        self.results.result_output['prefetch_mean_run_count'] = self.prefetch_mean_run_count()
        return self.results

    def count_prefetch_files_all(self):
        hql_query = r"file.path='*/Windows/Prefetch/*' file.extension:pf"
        count = count_traces_with_hql(context=self.context, hql_query=hql_query, facet_value_to_count='file',
                                      evidence_id=self.evidence_id)
        return count

    def count_prefetch_events_hansken(self):
        hql_query = r"event.type:'Prefetch File'"
        count = count_traces_with_hql(context=self.context, hql_query=hql_query, facet_value_to_count='file',
                                      evidence_id=self.evidence_id)
        return count

    def prefetch_max_run_count(self):
        hql_query = r"event.type:'Prefetch File'"
        hansken_buckets = get_buckets_with_hql(context=self.context, hql_query=hql_query,
                                               facet_for_filtering='event.runCount', use_range_facet=True,
                                               evidence_id=self.evidence_id)
        max_run_count = max(prefetch[0] for prefetch in hansken_buckets) if len(hansken_buckets) > 0 else None
        return max_run_count

    def prefetch_sum_run_count(self):
        hql_query = r"event.type:'Prefetch File'"
        hansken_buckets = get_buckets_with_hql(context=self.context, hql_query=hql_query,
                                               facet_for_filtering='event.runCount', use_range_facet=True,
                                               evidence_id=self.evidence_id)
        sum_run_count = sum(prefetch[0] for prefetch in hansken_buckets) if len(hansken_buckets) > 0 else None
        return sum_run_count

    def prefetch_mean_run_count(self):
        hql_query = r"event.type:'Prefetch File'"
        hansken_buckets = get_buckets_with_hql(context=self.context, hql_query=hql_query,
                                               facet_for_filtering='event.runCount', use_range_facet=True,
                                               evidence_id=self.evidence_id)
        mean_run_count = round(mean(prefetch[0] for prefetch in hansken_buckets), 2) if len(
            hansken_buckets) > 0 else None
        return mean_run_count

