from typing import Optional

from hansken.connect import ProjectContext

from hmclib.hmc_plugin_class import HMCStandardPlugin
from util.hansken_search import get_registry_value


class WinVersion(HMCStandardPlugin):

    def __init__(self, context: Optional[ProjectContext] = None, evidence_id: Optional[str] = None):
        name = 'windows_version'
        desc = 'Detail about Windows version from Registry.'
        result_list = ['win_build', 'win_build_inferred_os', 'win_version_id', 'win_version_str']
        super().__init__(name, desc, result_list, context, evidence_id)

    def collect_metrics(self):
        win_build = self.get_win_build()
        self.results.result_output['win_build'] = win_build
        self.results.result_output['win_build_inferred_os'] = self.get_win_build_inferred_os(win_build) if win_build else None
        win_version_id = self.get_win_version_id()
        win_version_str = self.get_win_version_str()
        self.results.result_output['win_version_str'] = win_version_str
        self.results.result_output['win_version_id'] = win_version_id
        return self.results

    def get_win_build(self) -> str|None:
        registry_key = '\'/Microsoft/Windows\ NT/CurrentVersion/CurrentBuild\''
        registry_value = get_registry_value(self.context, self.evidence_id, registry_key)
        for trace in registry_value:
            build_bytes = trace.previews['text/plain']
            build = build_bytes.decode('utf-8')
            if build == '1.511.1 () (Obsolete data - do not use)':
                registry_key = '\'/Microsoft/Windows\ NT/CurrentVersion/BuildLab\''
                registry_value = get_registry_value(self.context, self.evidence_id, registry_key)
                for trace_2 in registry_value:
                    build_lab_val = trace_2.previews['text/plain']
                    build_lab_str = build_lab_val.split('.')[0]
                    build = build_lab_str
            return build
        return None

    @staticmethod
    def get_win_build_inferred_os(win_build: str | None):
        win_build_inferred_os = 'unknown'
        try:
            win_build_int = int(win_build)
            # https://en.wikipedia.org/wiki/List_of_Microsoft_Windows_versions
            if win_build_int >= 22000:
                win_build_inferred_os = 'Windows 11'
            elif win_build_int >= 10240:
                win_build_inferred_os = 'Windows 10'
            elif win_build_int == 9600:
                win_build_inferred_os = 'Windows 8.1'
            elif win_build_int == 9200:
                win_build_inferred_os = 'Windows 8'
            elif win_build_int == 7600 or win_build_int == 7601:
                win_build_inferred_os = 'Windows 7'
            elif win_build_int == 6002:
                win_build_inferred_os = 'Windows Vista'
            elif win_build_int == 2600 or win_build_int == 2700 or win_build_int == 2710 or win_build_int == 3790:
                win_build_inferred_os = 'Windows XP'
            elif win_build_int == 3000:
                win_build_inferred_os = 'Windows ME'
            elif win_build_int == 2195:
                win_build_inferred_os = 'Windows 2000'
            elif win_build_int == 1998:
                win_build_inferred_os = 'Windows 2000'
            elif win_build_int == 1057:
                win_build_inferred_os = 'Windows NT 3.51'
            elif win_build_int == 807:
                win_build_inferred_os = 'Windows NT 3.5'
        except ValueError:
            if win_build == '2222A':
                win_build_inferred_os = 'Windows 98 SE'

        return win_build_inferred_os

    def get_win_version_id(self):
        registry_key = '\'/Microsoft/Windows\ NT/CurrentVersion/CurrentVersion\''
        registry_value = get_registry_value(self.context, self.evidence_id, registry_key)
        for trace in registry_value:
            win_version_id = trace.previews['text/plain'].decode('utf8')
            return str(win_version_id)
        return None

    def get_win_version_str(self):
        registry_key = '\'/Microsoft/Windows\ NT/CurrentVersion/ProductName\''
        registry_value = get_registry_value(self.context, self.evidence_id, registry_key)
        for trace in registry_value:
            win_version_str = trace.previews['text/plain'].decode('utf8')
            return str(win_version_str)
        return None


