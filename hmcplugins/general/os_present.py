from typing import Optional

from hansken.connect import ProjectContext

from hmclib.hmc_plugin_class import HMCStandardPlugin
from util.hansken_search import count_traces_of_type, count_traces_with_hql


class OSPresent(HMCStandardPlugin):

    def __init__(self, context: Optional[ProjectContext] = None, evidence_id: Optional[str] = None):
        name = 'os_present'
        desc = '(Very basic/fallback) check for the presence of different operating systems (Windows, MacOS, Linux, Android, iOS).'
        result_list = ['windows', 'macos', 'linux', 'ios', 'android']
        super().__init__(name, desc, result_list, context, evidence_id)

    def collect_metrics(self):
        self.results.result_output['windows'] = self.file_present(r"/Windows/System32/config/software")
        self.results.result_output['macos'] = self.file_present(r"/System/Library/CoreServices/SystemVersion.plist")
        self.results.result_output['linux'] = (self.file_present(r"/etc/os-release") or
            self.file_present(r"/etc/lsb-release") or
            self.file_present(r"/var/log/syslog") or
            self.file_present(r"/var/log/messages"))
        self.results.result_output['ios'] = (self.file_present(r"Keychain/*_keychain.plist") or self.file_present(r"*/private/var/mobile/Library/Preferences*"))
        self.results.result_output['android'] = (self.file_present(r"*system/build.prop") or self.file_present(r"*system/users/userlist.xml"))
        return self.results

    def file_present(self, file_path):
        hql_query = r"file.path='" + file_path + "'"
        win_present = count_traces_with_hql(self.context, hql_query, 'origin', 'type', evidence_id=self.evidence_id)
        if not win_present or win_present < 1:
            return False
        else:
            return True