from typing import Optional

from hansken.connect import ProjectContext

from hmclib.hmc_plugin_class import HMCStandardPlugin
from hmclib.hansken_search import count_traces_of_type, count_traces_with_hql


class Calendar(HMCStandardPlugin):

    def __init__(self, context: Optional[ProjectContext] = None, evidence_id: Optional[str] = None):
        name = 'calendar'
        desc = 'Metrics related to calendars (number of calendars and calendar entries).'
        result_list = ['calendars', 'calendar_entries', 'calendars_icalendar', 'calendars_outlook']
        super().__init__(name, desc, result_list, context, evidence_id)

    def collect_metrics(self):
        self.results.result_output['calendars'] = self.count_calendars()
        self.results.result_output['calendar_entries'] = self.count_calendar_entries()
        self.results.result_output['calendars_icalendar'] = self.count_calendars_icalendar()
        self.results.result_output['calendars_outlook'] = self.count_calendars_outlook()
        return self.results

    def count_calendars(self):
        type_to_search = 'calendar'
        count = count_traces_of_type(self.context, type_to_search, self.evidence_id)
        return count


    def count_calendar_entries(self):
        type_to_search = 'calendarEntry'
        count = count_traces_of_type(self.context, type_to_search, self.evidence_id)
        return count

    def count_calendars_icalendar(self):
        type_to_search = 'calendar'
        hql_query = 'calendar.application:icalendar'
        count = count_traces_with_hql(self.context, hql_query, type_to_search, 'type', evidence_id=self.evidence_id)
        return count

    def count_calendars_outlook(self):
        type_to_search = 'calendar'
        hql_query = 'calendar.application:outlook'
        count = count_traces_with_hql(self.context, hql_query, type_to_search, 'type', evidence_id=self.evidence_id)
        return count