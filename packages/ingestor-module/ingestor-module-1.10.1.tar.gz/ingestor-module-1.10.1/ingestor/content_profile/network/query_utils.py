from ingestor.common.constants import HOMEPAGE_ID
# RELATIONSHIP NAME
from ingestor.content_profile.config import HAS_HOMEPAGE


class QueryUtils:

    @staticmethod
    def get_contents_based_on_homepage_id(content_homepage_id, graph):
        homepage_network = []
        query_network = graph.custom_query(f'''
                    g.V().has('{HOMEPAGE_ID}',{content_homepage_id}).in('{HAS_HOMEPAGE}').valueMap().by(unfold()).toList()
                    ''', payload={
            HOMEPAGE_ID: content_homepage_id,
            HAS_HOMEPAGE: HAS_HOMEPAGE
        })
        homepage_network.append(query_network)
        return homepage_network

    @staticmethod
    def get_all_content(content_label, graph):
        query = graph.custom_query(f'''
        g.V().hasLabel('{content_label}').valueMap().by(unfold()).toList()
        ''', payload={
            content_label: content_label
        })
        return query

    @staticmethod
    def get_all_synopsys(content_core_synopsis, graph):
        query = graph.custom_query(f'''
        g.V().hasLabel('{content_core_synopsis}').valueMap().by(unfold()).toList()
        ''', payload={
            content_core_synopsis: content_core_synopsis
        })
        return query