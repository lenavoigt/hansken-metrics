import json
from typing import Optional, List

from hansken.connect import ProjectContext

from hmclib.hmc_plugin_class import HMCStandardPlugin
from hmclib.hansken_search import count_traces_with_hql


# according to category matching in resources/application_categories.json with sources provided in resources/application_category_sources.txt
class ApplicationCategory(HMCStandardPlugin):
    application_categories = None
    def __init__(self, context: Optional[ProjectContext] = None, evidence_id: Optional[str] = None):
        name = 'phone_application_category'
        desc = 'Number of applications that match different categories (identified by package name).'
        result_list = [
            "messaging",
            "social_media",
            "shopping",
            "streaming",
            "webmail",
            "news",
            "travel",
            "insurance",
            "search_engines",
            "games",
            "education",
            "health_and_fitness",
            "finance",
            "productivity"
        ]
        super().__init__(name, desc, result_list, context, evidence_id)
        if ApplicationCategory.application_categories is None:
            with open('resources/application_categories.json', 'r') as f:
                ApplicationCategory.application_categories = json.load(f)

    def collect_metrics(self):
        self.results.result_output['messaging'] = self.count_applications("Messaging")
        self.results.result_output['social_media'] = self.count_applications("Social Media")
        self.results.result_output['shopping'] = self.count_applications("Shopping")
        self.results.result_output['streaming'] = self.count_applications("Streaming")
        self.results.result_output['webmail'] = self.count_applications("Webmail")
        self.results.result_output['news'] = self.count_applications("News")
        self.results.result_output['travel'] = self.count_applications("Travel")
        self.results.result_output['insurance'] = self.count_applications("Insurance")
        self.results.result_output['search_engines'] = self.count_applications("Search Engines")
        self.results.result_output['games'] = self.count_applications("Games")
        self.results.result_output['education'] = self.count_applications("Education")
        self.results.result_output['health_and_fitness'] = self.count_applications("Health and Fitness")
        self.results.result_output['finance'] = self.count_applications("Finance")
        self.results.result_output['productivity'] = self.count_applications("Productivity")
        return self.results

    def count_applications(self, category_name):
        category_data = ApplicationCategory.application_categories.get(category_name, {})
        package_names = category_data.get("android", []) + category_data.get("ios", [])
        hql_query = ' OR '.join(
            f"(application.package:{package})" for package in package_names)
        count = count_traces_with_hql(self.context, hql_query, 'application', 'type', evidence_id=self.evidence_id)
        return count

    def count_instant_messaging(self):
        application_names = ['org.telegram.messenger', 'ph.telegra.Telegraph', 'org.thoughtcrime.securesms', 'com.whatsapp', 'net.whatsapp.WhatsApp', 'com.facebook.orca', 'com.snapchat.android']
        return self.count_applications(application_names)

    def count_games(self):
        application_names = ['com.king.candycrushsaga']
        return self.count_applications(application_names)

    def count_social_media(self):
        application_names = [' com.facebook.katana', 'com.instagram.android', 'com.burbn.instagram']
        return self.count_applications(application_names)

    # https://gist.github.com/imbudhiraja/5b0a485fb7f36fb16c9d7d5f19b6ee40


