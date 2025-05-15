from abc import ABC, abstractmethod
import datetime
from typing import Optional, List

from hansken.connect import ProjectContext

class HMCStandardResult(object):

    def __init__(self, plugin_name, desc, result_list: List[str], context: ProjectContext, evidence_id: Optional[str] = None):
        self.context = context
        self.project_id = context.project_id if context else None
        self.evidence_id = evidence_id
        self.plugin_name = plugin_name
        self.desc = desc
        self.result_output = {}
        for result in result_list:
            self.result_output[result] = None
        self.time_created = str(datetime.datetime.now())

    def set_context(self, context: ProjectContext):
        self.context = context
        self.project_id = context.project_id

    def set_evidence_id(self, evidence_id: str):
        self.evidence_id = evidence_id

    def to_dict(self):
        return {'project': self.project_id,
                'evidence_id': self.evidence_id,
                'plugin': self.plugin_name,
                'description': self.desc,
                'time_created': self.time_created,
                'results': self.result_output
                }

    def results_to_dict(self):
        return {'plugin': self.plugin_name,
                'description': self.desc,
                'time_created': self.time_created,
                'results': self.result_output
                }

class HMCStandardPlugin(ABC):
    def __init__(self, name, description, result_list: List, context: Optional[ProjectContext] = None, evidence_id: Optional[str] = None):
        self.name = name
        self.description = description
        self.context = context
        self.project_id = context.project_id if context else None
        self.evidence_id = evidence_id
        self.results = HMCStandardResult(name, description, result_list, context, evidence_id)

    def set_evidence_id(self, evidence_id: str):
        self.evidence_id = evidence_id
        self.results.set_evidence_id(evidence_id)

    def set_context(self, context: ProjectContext):
        self.context = context
        self.project_id = context.project_id
        self.results.set_context(context)

    def plugin_metric_collection(self) -> HMCStandardResult|None:
        if self.context:
            return self.collect_metrics()
        else:
            print("No Project ID defined. Can't process evidence...")
            return None

    @abstractmethod
    def collect_metrics(self) -> HMCStandardResult|None:
        return None


