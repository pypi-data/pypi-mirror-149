from ingestor.user_profile.main.config import \
    TO_READ_FROM_S3_PREFERENCES, TO_READ_FROM_S3_CLUSTERING_LABELS
from pandas import DataFrame
from ingestor.user_profile.similarity.config import \
    CLUSTER_NODE_LABEL, GENDER_MAP, SCORE, DEFAULT_CLUSTER_LABEL
from ingestor.common.constants import CUSTOMER_ID, \
    GENDER, AGE, USER_LABEL, PROPERTIES
from ingestor.user_profile.similarity.all_users_generator \
    import SimilarityGenerator
from ingestor.user_profile.similarity.common import \
    SimilarityCommons
import logging
logging.basicConfig(level=logging.INFO)

class StreamingUsersSimilarity(SimilarityGenerator):

    def __init__(
            self,
            connection_object,
            similarity_cutoff: int
    ):
        """
        Constructor to create graph object using
        the input connection details
        :param connection_object: graph
        connection object
        """
        SimilarityGenerator.__init__(
            self,
            db_graph=connection_object,
            sim_cutoff=similarity_cutoff
        )

    def get_property_vector(
            self,
            node: dict
    ) -> list:
        """
        Returns the property vector to be
        used for similarity computation
        :param node: node properties
        :return: list of properties
        """
        return [GENDER_MAP[node[GENDER]],
                node[AGE]]

    def filter_most_similar_relationships(
            self
    ):
        """
        Normalize and filter out relationships
        with similarity scores greater than the
        specified threshold
        :return: None, updates the data member
        dataframe object
        """
        self.similarity_score[SCORE] = \
            SimilarityCommons.normalize(
                self.similarity_score[SCORE].tolist()
            )
        self.similarity_score = \
            self.similarity_score[
                self.similarity_score[SCORE] > self.sim_cutoff
                ].reset_index(drop=True)

    def update_similarity_scores(
            self,
            existing_user,
            existing_user_vector,
            new_user,
            new_user_vector,
    ):
        """
        Compute Euclidean Distance between the
        new user and the currently considered existing user
        :param existing_user: customer_id
        :param existing_user_vector: user properties
        :param new_user: customer_id
        :param new_user_vector: user properties
        :return: None, updates the data member
        dataframe object
        """
        score = 1 - SimilarityCommons.get_distance(
            vector_a=new_user_vector,
            vector_b=existing_user_vector
        )
        self.similarity_score.loc[
            len(self.similarity_score)] = \
            [new_user, existing_user, score]

    def get_similarity_features(
            self
    ):
        """
        Get relationships to be considered for
        similarity computation
        :return: list of preferences
        """
        preferences = TO_READ_FROM_S3_PREFERENCES
        clusters = TO_READ_FROM_S3_CLUSTERING_LABELS
        preferences.update(clusters)
        return preferences

    def one_to_all_similarity(
            self,
            new_user: str,
            all_users: list
    ):
        """
        Calculate similarity scores for the new user
         with rest of the users from the same
         user profile cluster
        :param new_user: customer_id
        :param all_users: list of all users
        :return: None, updates the data member
        dataframe object
        """

        # obtain the node for the newly added user
        new_user_node = dict(SimilarityCommons.get_node(
            label=USER_LABEL,
            properties={CUSTOMER_ID: new_user},
            db_graph=self.db_graph))[PROPERTIES]

        if new_user_node is None:
            logging.info("The streaming user does not exist!")
            return

        # obtain the property vector for the
        # newly added user
        new_user_vector = self.get_property_vector(
            node=new_user_node)

        # for each user in the same cluster as
        # the newly added user
        for existing_user in all_users:

            # get user node for the existing user
            existing_user_node = \
                dict(SimilarityCommons.get_node(
                    label=USER_LABEL,
                    properties={CUSTOMER_ID: existing_user},
                    db_graph=self.db_graph))[PROPERTIES]

            if existing_user_node is None:
                logging.info("The historical user does not exist!")
                continue

            # obtain the property vector the existing user
            existing_user_vector = \
                self.get_property_vector(
                    node=existing_user_node)

            # calculate the similarity score between the
            # newly added user the existing user considered
            # in this iteration
            self.update_similarity_scores(
                existing_user=existing_user,
                existing_user_vector=existing_user_vector,
                new_user=new_user,
                new_user_vector=new_user_vector,
            )

    def streaming_similarity_controller(
            self,
            data: DataFrame,
            is_paytv: bool
    ):
        """
        Driver function for computing similarity
        relationships for the newly added user
        with rest of the users in the same user
        profile cluster
        :param data: dataframe object pandas
        :param is_paytv: boolean indicator
        :return: None, plots the relationships
        in graphDB
        """
        preferences = self.get_similarity_features()

        for index in range(len(data)):

            customer_id = data.loc[index, CUSTOMER_ID]
            cluster_label = data.loc[index, CLUSTER_NODE_LABEL]
            if cluster_label == DEFAULT_CLUSTER_LABEL:
                logging.info("The user belongs to default cluster..." +
                             "skipping similarity computation")
                continue

            # retrieve all 2-hop edges from cluster label node
            edges = self.get_graphdb_network(
                cluster_id=cluster_label,
                is_paytv=is_paytv
            )

            cluster_members = []

            for feature in list(preferences.keys()):

                # generate NetworkX object from the edges
                G = self.get_networkx_structure(
                    edges=edges,
                    dest_node_label=feature,
                    dest_node_property=(preferences[feature])[1],
                    relationship=(preferences[feature])[0]
                )

                # get all source (i.e. user) nodes
                cluster_members.extend(
                    self.get_source_nodes_from_networkx(network=G))

            self.one_to_all_similarity(
                new_user=customer_id,
                all_users=list(set(cluster_members))
            )

            # filter out the relationships with similarity scores
            # greater than the specified threshold
            self.filter_most_similar_relationships()

            # plot the newly calculated similarity relationships
            self.plot_similarity_relations()
