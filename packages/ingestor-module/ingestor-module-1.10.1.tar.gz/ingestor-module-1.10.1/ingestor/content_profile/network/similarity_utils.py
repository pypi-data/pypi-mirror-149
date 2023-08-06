from ast import literal_eval

from graphdb.schema import Node

from ingestor.common.constants import LABEL, PROPERTIES, CONTENT_ID, CC_SIMILARITY_SCORE, ALL_SIMILARITY_SCORE, \
     CONTENT_CORE_SYNOPSIS
from ingestor.content_profile.content_similarity import cluster_data_to_df, generate_new_features, \
    generate_tfidf_matrix, calculate_cosine_similarity, cluster_data_to_single_df, combine_features, create_tfidf_df, \
    calculate_single_cosine_similarity
from ingestor.content_profile.network.query_utils import QueryUtils


class SimilarityUtils:

    @staticmethod
    def prepare_similarity_based_on_all_content(content_label, homepage_id, graph):
        all_content_cluster = QueryUtils.get_all_content(content_label, graph)
        all_content_df = cluster_data_to_single_df(all_content_cluster)
        all_content_core_synopsys = QueryUtils.get_all_synopsys(CONTENT_CORE_SYNOPSIS, graph)
        all_content_new_df = combine_features(all_content_df, graph, content_label, homepage_id,
                                              all_content_core_synopsys, all_content=True)
        all_content_tfidf = create_tfidf_df(all_content_new_df)
        all_content_dict_cos_sim = calculate_single_cosine_similarity(all_content_tfidf)

        return all_content_dict_cos_sim

    @staticmethod
    def prepare_similarity_based_on_homepage_id(content_label, content_homepage_id, graph):
        try:
            list_homepage_network = QueryUtils.get_contents_based_on_homepage_id(content_homepage_id, graph)

            list_dataframe_homepage = cluster_data_to_df(list_homepage_network)

            list_new_df_homepage = generate_new_features(list_dataframe_homepage, graph, content_label,
                                                         content_homepage_id)

            list_tfidf_df = generate_tfidf_matrix(list_new_df_homepage)

            list_dict_content_similarities = calculate_cosine_similarity(list_tfidf_df)

        except Exception as e:
            print(e)
            print('Not able to add content similarity based on home page id')
        return list_dict_content_similarities
