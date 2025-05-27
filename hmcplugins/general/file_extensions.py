from typing import Optional, List

from hansken.connect import ProjectContext

from hmclib.hmc_plugin_class import HMCStandardPlugin
from hmclib.hansken_search import count_traces_with_hql


class FileExtensions(HMCStandardPlugin):

    def __init__(self, context: Optional[ProjectContext] = None, evidence_id: Optional[str] = None):
        name = 'file_extension_count'
        desc = 'Number of files for selected file extensions.'
        result_list = ['pdf', 'doc', 'odt', 'rtf', 'xls', 'ppt', 'rar', 'sqlite', 'edb', 'db', 'vmdk', 'vmx', 'iso', 'ova', 'img', 'dd', 'e01', 'vhd', 'hdd', 'virtual_all']
        super().__init__(name, desc, result_list, context, evidence_id)

    def collect_metrics(self):
        self.results.result_output['pdf'] = self.count_pdf()
        self.results.result_output['doc'] = self.count_doc()
        self.results.result_output['odt'] = self.count_odt()
        self.results.result_output['rtf'] = self.count_rtf()
        self.results.result_output['xls'] = self.count_xls()
        self.results.result_output['ppt'] = self.count_ppt()
        self.results.result_output['rar'] = self.count_rar()
        self.results.result_output['sqlite'] = self.count_sqlite()
        self.results.result_output['edb'] = self.count_edb()
        self.results.result_output['db'] = self.count_db()
        self.results.result_output['vmdk'] = self.count_extension(['vmdk'])
        self.results.result_output['vmx'] = self.count_extension(['vmx'])
        self.results.result_output['iso'] = self.count_extension(['iso'])
        self.results.result_output['ova'] = self.count_extension(['ova'])
        self.results.result_output['img'] = self.count_extension(['img'])
        self.results.result_output['dd'] = self.count_extension(['dd'])
        self.results.result_output['e01'] = self.count_extension(['e01'])
        self.results.result_output['vhd'] = self.count_extension(['vhd'])
        self.results.result_output['hdd'] = self.count_extension(['hdd'])
        self.results.result_output['virtual_all'] = self.count_extension(['vmdk', 'vmx', 'iso', 'ova', 'img', 'dd', 'e01', 'vhd', 'hdd'])
        return self.results

    def count_extension(self, extensions: List[str]):
        type_to_search = "file"
        hql_query = None
        for each_extension in extensions:
            if not hql_query:
                hql_query = "file.extension:\'" + each_extension + "\'"
            else:
                hql_query = hql_query + "OR file.extension:\'" + each_extension + "\'"

        count = count_traces_with_hql(self.context, hql_query, type_to_search, evidence_id=self.evidence_id)
        return count

    def count_db(self):
        return self.count_extension(['db'])

    def count_pdf(self):
        return self.count_extension(['pdf'])

    def count_odt(self):
        return self.count_extension(['odt'])

    def count_rtf(self):
        return self.count_extension(['rtf'])

    def count_rar(self):
        return self.count_extension(['rar'])

    def count_sqlite(self):
        return self.count_extension(['sqlite'])

    def count_edb(self):
        return self.count_extension(['edb'])

    def count_doc(self):
        return self.count_extension(['doc', 'docx'])

    def count_xls(self):
        return self.count_extension(['xls', 'xlsx'])

    def count_ppt(self):
        return self.count_extension(['ppt', 'pptx'])



