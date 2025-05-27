import os
import struct
import tempfile
from datetime import datetime, timedelta
from typing import Optional

from hansken.connect import ProjectContext
from hansken.recipes import export

from hmclib.hmc_plugin_class import HMCStandardPlugin
from utils.datetime_conversions import get_year_month_day_str, get_time_delta_days
from hmclib.hansken_search import get_registry_value


class WinLifeTime(HMCStandardPlugin):

    def __init__(self, context: Optional[ProjectContext] = None, evidence_id: Optional[str] = None):
        name = 'windows_life_time'
        desc = 'Life time of the Windows Operating System installed'
        result_list = ['install_year_month_day', 'shutdown_year_month_day', 'life_time_days']
        super().__init__(name, desc, result_list, context, evidence_id)

    def collect_metrics(self):
        self.results.result_output['install_year_month_day'] = self.win_install_year_month_day()
        self.results.result_output['shutdown_year_month_day'] = self.win_shutdown_year_month_day()
        self.results.result_output['life_time_days'] = self.win_life_days()
        return self.results

    def win_install_year_month_day(self) -> str | None:
        install_time = self.win_install_time()
        if install_time:
            install_str = get_year_month_day_str(install_time)
            return install_str
        else:
            return None

    def win_shutdown_year_month_day(self) -> str | None:
        shutdown_time = self.win_shutdown_time()
        if shutdown_time:
            shutdown_str = get_year_month_day_str(shutdown_time)
            return shutdown_str
        else:
            return None

    def win_life_days(self) -> float | None:
        win_life = self.win_life_time()
        if win_life:
            win_life_days = round(get_time_delta_days(win_life),1)
            return win_life_days
        else:
            return None

    def win_life_time(self) -> timedelta | None:
        install = self.win_install_time()
        shutdown = self.win_shutdown_time()
        if shutdown is not None and install is not None:
            diff_datetime = shutdown - install
        else:
            diff_datetime = None
        return diff_datetime

    def win_install_time(self) -> datetime | None:
        if not self.evidence_id:
            return None
        registry_key = '\'/Microsoft/Windows\ NT/CurrentVersion/InstallDate\''
        registry_value = get_registry_value(self.context, self.evidence_id, registry_key)
        for trace in registry_value:
            unix_install = int(trace.previews['text/plain'])
            install = datetime.utcfromtimestamp(unix_install)
            return install
        return None

    def win_shutdown_time(self) -> datetime | None:
        if not self.evidence_id:
            return None
        registry_key = '\'/controlset*/control/windows/shutdowntime\''
        registry_value = get_registry_value(self.context, self.evidence_id, registry_key)
        project_dir = os.getcwd()
        for trace in registry_value:
            with tempfile.NamedTemporaryFile(mode="wb+", dir=project_dir, delete=True) as temp:
                export.to_file(trace, temp.name)
                temp.seek(0)
                reg_data = temp.read()
                time_int = struct.unpack("<Q", reg_data)[0]
                as_unix = (time_int - 116444736000000000) / 10000000
                res = datetime.utcfromtimestamp(as_unix)
            return res
        return None
