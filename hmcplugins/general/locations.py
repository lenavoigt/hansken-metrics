from typing import Optional

from hansken.connect import ProjectContext

from hmclib.hmc_plugin_class import HMCStandardPlugin
from util.hansken_search import count_traces_of_type, count_traces_with_hql


class Locations(HMCStandardPlugin):

    def __init__(self, context: Optional[ProjectContext] = None, evidence_id: Optional[str] = None):
        name = 'locations'
        desc = 'Counts of location and gps traces as well as file types that correspond to location data.'
        result_list = ['gps_traces', 'gps_logs', 'gpx_files', 'mime_class_location', 'gps_track', 'location_traces']
        super().__init__(name, desc, result_list, context, evidence_id)

    def collect_metrics(self):
        self.results.result_output['gps_traces'] = self.count_gps()
        self.results.result_output['gps_logs'] = self.count_gps_log()
        self.results.result_output['gpx_files'] = self.count_gpx_files()
        self.results.result_output['mime_class_location'] = self.count_mime_class_location()
        self.results.result_output['gps_track'] = self.count_gps_track()
        self.results.result_output['location_traces'] = self.count_locations()

        return self.results

    def count_gps(self):
        type_to_search = 'gps'
        count = count_traces_of_type(self.context, type_to_search, self.evidence_id)
        return count


    def count_gps_log(self):
        type_to_search = 'gpsLog'
        count = count_traces_of_type(self.context, type_to_search, self.evidence_id)
        return count

    def count_gpx_files(self):
        type_to_search = 'file'
        hql_query = r'file.extension:gpx'
        count = count_traces_with_hql(self.context, hql_query, type_to_search, 'type', evidence_id=self.evidence_id)
        return count

    def count_mime_class_location(self):
        type_to_search = 'file'
        hql_query = r"data.mimeClass:'location'"
        count = count_traces_with_hql(self.context, hql_query, type_to_search, 'type', evidence_id=self.evidence_id)
        return count

    def count_gps_track(self):
        type_to_search = 'track'
        count = count_traces_of_type(self.context, type_to_search, self.evidence_id)
        return count

    # as done in hansken tactical user interface
    def count_locations(self):
        type_to_search = 'gps'
        hql_query = r"gps.latlong:* NOT gps.latlong:(-0.5,-0.5)..(0.5,0.5)"
        count = count_traces_with_hql(self.context, hql_query, type_to_search, 'type', evidence_id=self.evidence_id)
        return count