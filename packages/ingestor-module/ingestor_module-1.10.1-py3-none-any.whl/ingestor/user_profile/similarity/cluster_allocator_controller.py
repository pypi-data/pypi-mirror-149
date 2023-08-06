from pandas import DataFrame
from ingestor.user_profile.similarity.config import \
    CLUSTER_NODE_LABEL, \
    DEFAULT_CLUSTER_LABEL, NEW_USER_CLUSTER_RELATIONSHIP_LABEL, SIMILARITY_THRESHOLD
from ingestor.common.constants import CUSTOMER_ID, USER_LABEL, \
    PAYTVPROVIDER_ID, GENDER, AGE, IS_PAYTV
from ingestor.user_profile.network.plot_relations import PlotRelations
from ingestor.user_profile.similarity.cluster_allocator_utils import \
    ClusterAllocatorUtils
from ingestor.user_profile.similarity.streaming_users import StreamingUsersSimilarity
from ingestor.user_profile.similarity.common import SimilarityCommons

class ClusterAllocatorController(ClusterAllocatorUtils):

    def __init__(
            self,
            connection_object
    ):
        """
        Constructor to create graph object using
        the input connection details
        :param connection_object: graph
        connection object
        """

        ClusterAllocatorUtils.__init__(
            self,
            connection_object=connection_object
        )

    def get_centroids(
            self
    ):
        """
        Retrieve all the centroids for a
        particular cluster type from GraphDB
        :return: list of centroids and
        their properties
        """
        return self.graph.custom_query(
            query="g.V().hasLabel('centroid').has('" +
                  CLUSTER_NODE_LABEL +
                  "').path().by(elementMap())"
        )[0]

    def filter_centroids(
            self,
            is_paytv: bool,
            centroids: list
    ) -> list:
        """
        Filter out the centroids that do not belong
        to the same paytv type as that of the user
        :param is_paytv: paytv indicator boolean
        :param centroids: list of centroids
        :return: list of centroids that are to be
        proceeded with
        """
        centroids_to_keep = []

        for centroid in centroids:
            for node_property, val in centroid[0].items():
                if (node_property == IS_PAYTV and
                        val == str(is_paytv)):
                    centroids_to_keep.append(centroid[0])
                    break
        return centroids_to_keep

    def get_paytv_filtered_centroids(
            self
    ):
        """
        Retrieve all centroids and filter them
        as per their respective paytv types
        into a dictionary. Dictionary key True
        holds centroids with is_paytv flag set
        to True and False for the rest
        :return: dictionary object
        """
        centroid_nodes = self.get_centroids()
        return {
            'True': self.filter_centroids(
                is_paytv=True,
                centroids=centroid_nodes
            ),
            'False': self.filter_centroids(
                is_paytv=False,
                centroids=centroid_nodes
            )
        }

    def compute_user_centroid_scores(
            self,
            centroids: DataFrame,
            user: list
    ) -> list:
        """
        Calculate Euclidean Distance scores between
        the considered user and all the centroids
        of the same paytv type.
        :param centroids: Dataframe object pandas
        :param user: list of features for the user
        :return: list of centroid scores
        """
        scores = []
        for index in range(len(centroids)):
            centroid = \
                centroids.loc[index, :].values.tolist()
            scores.append(
                SimilarityCommons.get_distance(
                    vector_a=user,
                    vector_b=centroid
                )
            )
        return scores

    def find_centroid_for_user(
            self,
            user: DataFrame,
            centroids: DataFrame
    ) -> int:
        """
        Find the index of the most suitable
        centroid to be assigned for the user
        :param user: dataframe object pandas
        :param centroids: dataframe object pandas
        :return: integer value for the
        centroid index
        """
        centroids, user = \
            self.process_user_centroid_records(
                centroids=centroids,
                user=user
            )
        scores = \
            self.compute_user_centroid_scores(
                centroids=centroids,
                user=user
            )
        min_value = min(scores)
        return scores.index(min_value)

    def check_features_available(
            self,
            users: DataFrame,
            index: int
    ) -> bool:
        """
        Check if any feature values are available for the user
        :param users: dataframe object pandas
        :param index: user record index
        :return: Boolean indicator
        """
        if (users.loc[index, GENDER] == -1 and (
             users.loc[index, PAYTVPROVIDER_ID] == -1 and (
             users.loc[index, AGE] == -1
        ))):
            return False
        return True

    def dump_relations(
            self,
            is_paytv: bool,
            data=DataFrame
    ):
        """
        Dump user-centroid relations
        :param is_paytv: boolean indicator
        :param data: dataframe object pandas
        :return: None, updates the relationships
         in graphDB
        """
        if len(data) == 0:
            return

        data[CLUSTER_NODE_LABEL] = \
            data[CLUSTER_NODE_LABEL].astype(int)

        pr = PlotRelations(
            data=data,
            label=NEW_USER_CLUSTER_RELATIONSHIP_LABEL,
            connection_uri=self.connection_object
        )

        pr.controller(
            destination_prop_label=CLUSTER_NODE_LABEL,
            is_paytv=is_paytv
        )

    def controller(
            self,
            users=DataFrame
    ):
        """
        Driver function for finding cluster labels
        for new users
        :param users: dataframe object pandas
        :return: None, updates the relationships in graphDB
        """
        users = self.preprocess_user_attributes(users)

        ispaytv_filtered_centroids = \
            self.get_paytv_filtered_centroids()

        for index in range(len(users)):

            if not self.check_features_available(
                    users=users,
                    index=index
            ):
                users.loc[index, CLUSTER_NODE_LABEL] = \
                    DEFAULT_CLUSTER_LABEL
                continue
            # find if the user node exists or not
            user_node = SimilarityCommons.get_node(
                label=USER_LABEL,
                properties={
                    CUSTOMER_ID: users.loc[index,
                                           CUSTOMER_ID
                    ]},
                db_graph=self.graph
            )
            if user_node is None:
                continue
            # check the paytv type for the user
            is_paytv = \
                self.user_has_paytv(
                    paytv_val=users.loc[index,
                                        PAYTVPROVIDER_ID
                    ])
            # filter centroids as per paytv indicator
            centroids = \
                DataFrame(
                    ispaytv_filtered_centroids[
                        str(is_paytv)
                    ]
                )
            if len(centroids) == 0:
                users.loc[index, CLUSTER_NODE_LABEL] = \
                    DEFAULT_CLUSTER_LABEL
                continue

            users.loc[index, CLUSTER_NODE_LABEL] = \
                self.find_centroid_for_user(
                user=DataFrame(users.loc[index, :]).T,
                centroids=centroids
            )

        nonpaytv_users, paytv_users = \
            self.get_paytv_wise_users(users)

        self.dump_relations(
            is_paytv=True,
            data=paytv_users[
                [CUSTOMER_ID, CLUSTER_NODE_LABEL]
            ])
        self.dump_relations(
            is_paytv=False,
            data=nonpaytv_users[
                [CUSTOMER_ID, CLUSTER_NODE_LABEL]
            ])

        streaming_users_similarity = StreamingUsersSimilarity(
            connection_object=self.connection_object,
            similarity_cutoff=SIMILARITY_THRESHOLD
        )

        streaming_users_similarity.streaming_similarity_controller(
            data=paytv_users,
            is_paytv=True
        )
        streaming_users_similarity.streaming_similarity_controller(
            data=nonpaytv_users,
            is_paytv=False
        )
