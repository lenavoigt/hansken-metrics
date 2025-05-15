from typing import Optional

from hansken.connect import ProjectContext

from hmclib.hmc_plugin_class import HMCStandardPlugin
from util.hansken_search import count_traces_of_type, count_traces_with_hql


class TraceTypes(HMCStandardPlugin):

    def __init__(self, context: Optional[ProjectContext] = None, evidence_id: Optional[str] = None):
        name = 'trace_type_count'
        desc = 'Number of different trace types.'
        result_list = ['file', 'folder', 'picture', 'picture_camera', 'picture_screenshot','audio', 'video',
                       'encrypted', 'executable', 'file_transfer', 'file_archive', 'file_transfer_log', 'ticket', 'ticket_archive']
        super().__init__(name, desc, result_list, context, evidence_id)

    def collect_metrics(self):
        self.results.result_output['file'] = self.count_files()
        self.results.result_output['folder'] = self.count_folders()
        self.results.result_output['picture'] = self.count_pictures()
        self.results.result_output['picture_camera'] = self.count_pictures_camera()
        self.results.result_output['picture_screenshot'] = self.count_pictures_screenshots()
        self.results.result_output['audio'] = self.count_audio()
        self.results.result_output['video'] = self.count_videos()
        self.results.result_output['encrypted'] = self.count_encrypted()
        self.results.result_output['executable'] = self.count_executable()
        self.results.result_output['file_transfer'] = self.count_file_transfer()
        self.results.result_output['file_transfer_log'] = self.count_file_transfer_log()
        self.results.result_output['file_archive'] = self.count_file_archive()
        self.results.result_output['ticket'] = self.count_ticket()
        self.results.result_output['ticket_archive'] = self.count_ticket_archive()
        return self.results

    def count_files(self):
        type_to_search = 'file'
        count = count_traces_of_type(self.context, type_to_search, self.evidence_id)
        return count

    def count_folders(self):
        type_to_search = 'folder'
        count = count_traces_of_type(self.context, type_to_search, self.evidence_id)
        return count

    def count_pictures(self):
        type_to_search = 'picture'
        count = count_traces_of_type(self.context, type_to_search, self.evidence_id)
        return count

    def count_audio(self):
        type_to_search = 'audio'
        count = count_traces_of_type(self.context, type_to_search, self.evidence_id)
        return count

    def count_videos(self):
        type_to_search = 'video'
        count = count_traces_of_type(self.context, type_to_search, self.evidence_id)
        return count

    def count_encrypted(self):
        type_to_search = 'encrypted'
        count = count_traces_of_type(self.context, type_to_search, self.evidence_id)
        return count

    def count_executable(self):
        type_to_search = 'executable'
        count = count_traces_of_type(self.context, type_to_search, self.evidence_id)
        return count

    def count_pictures_camera(self):
        hql_query = r"picture.camera:*"
        count = count_traces_with_hql(self.context, hql_query, 'origin', 'type', evidence_id=self.evidence_id)
        return count

    # as done in hansken tactical user interface
    def count_pictures_screenshots(self):
        hql_query = r"file.name:screenshot AND data.raw.mimeClass:picture -file.path:'*icon*' picture.width > 100 picture.height > 100"
        count = count_traces_with_hql(self.context, hql_query, 'origin', 'type', evidence_id=self.evidence_id)
        return count

    # as done in hansken tactical user interface

    def count_file_transfer(self):
        type_to_search = 'fileTransfer'
        count = count_traces_of_type(self.context, type_to_search, self.evidence_id)
        return count

    def count_file_transfer_log(self):
        type_to_search = 'fileTransferLog'
        count = count_traces_of_type(self.context, type_to_search, self.evidence_id)
        return count

    def count_file_archive(self):
        type_to_search = 'fileArchive'
        count = count_traces_of_type(self.context, type_to_search, self.evidence_id)
        return count

    def count_ticket(self):
        type_to_search = 'ticket'
        count = count_traces_of_type(self.context, type_to_search, self.evidence_id)
        return count

    def count_ticket_archive(self):
        type_to_search = 'ticketArchive'
        count = count_traces_of_type(self.context, type_to_search, self.evidence_id)
        return count
