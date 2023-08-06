import networkx as nx
from typing import List, Any
from ingestor.common.constants import \
    CUSTOMER_ID
from pandas import DataFrame, concat
from collections import ChainMap
from ingestor.user_profile.similarity.config import \
    CLUSTER_NODE_LABEL, SOURCE_NODE_LABEL, \
    USER1, USER2, SCORE, LABEL
import itertools

class SimilarityUtils:
    def __init__(
            self,
            db_graph,
            sim_cutoff: int
    ):
        """
        Inherits inputs from parent class
        :param db_graph: graphDB connection object
        :param sim_cutoff: similarity threshold
        """
        self.db_graph = db_graph
        self.sim_cutoff = sim_cutoff
        self.similarity_score = DataFrame(
            columns=[USER1, USER2, SCORE]
        )

    def get_node_names(
            self,
            dest_node_property,
            elements,
            path
    ) -> List[str]:
        """
        For a given path returned from custom query,
        retrieve the source and destination node labels
        :param dest_node_property: Property name for
        destination node
        :param elements: path list
        :return: Destination node name and
        Source node name
        """
        for all_elements in path:
            if CUSTOMER_ID in all_elements.keys():
                source_name = all_elements[CUSTOMER_ID]
                break
        dest_name = elements[dest_node_property]
        return dest_name, source_name

    def get_cluster_paytv_property(
            self,
            is_paytv: bool
    ) -> str:
        """
        returns paytv property for which t
        he cluster labels are to be looked up for
        :param is_paytv: boolean indicator
        :return: query substring
        """
        cluster_paytv_property = \
            ".has('is_paytv','" + str(is_paytv) + "')" \
                if is_paytv is not None else ''
        return cluster_paytv_property

    def get_source_nodes_from_networkx(
            self,
            network
    ) -> List:
        """
        Retrieve source nodes (user nodes)
        from networkx instance
        :param network: networkx instance
        :return: list of source nodes
        """
        source_nodes = []
        for (node, properties) in \
                network.nodes(data=True):
            if properties[LABEL] == \
                    SOURCE_NODE_LABEL:
                source_nodes.append(node)
        return source_nodes

    def get_graphdb_network(
            self,
            cluster_id: int,
            is_paytv: bool
    ) -> list:
        """
        Retrieve all users nodes belonging to a
        single cluster along with all the nodes
        to which the users are connected. In a
        nutshell, this method include the custom
        query to return all nodes within 2 hops
        from the cluster label node.
        :param cluster_id: cluster label node
        :param is_paytv: boolean indicator
        :return: paths within the cluster
        """
        cluster_paytv_property = \
            self.get_cluster_paytv_property(is_paytv)

        network = self.db_graph.custom_query(
            query="g.V().has(" +
                  "'" + CLUSTER_NODE_LABEL + "', " +
                  str(cluster_id) + ")" +
                  cluster_paytv_property
                  + ".repeat" +
                  "(" +
                  "bothE().bothV()" +
                  ".simplePath()" +
                  ")" +
                  ".emit().times(2).path()." +
                  "by(elementMap())"
        )

        return list(itertools.chain.from_iterable(network))

    def get_cluster_labels(
            self,
            is_paytv: bool
    ):
        """
        Obtain and return the set of cluster labels
        :return: list of cluster labels
        """
        cluster_paytv_property = \
            self.get_cluster_paytv_property(is_paytv)

        clusters = self.db_graph.custom_query(
            query="g.V().hasLabel('" + CLUSTER_NODE_LABEL
                  + "')" + cluster_paytv_property
                  + ".path().by(elementMap())")[0]

        for index in range(len(clusters)):
            path = dict(ChainMap(*clusters[index]))
            clusters[index] = path[CLUSTER_NODE_LABEL]

        return clusters

    def get_undirected_network(
            self,
            network
    ) -> Any:
        """
        Converts a given directed network to an
        undirected network.
        :param network: Input networkx instance
        :return: undirected networkx instance
        """
        return network.to_undirected()

    def get_networkx_structure(
            self,
            edges: None,
            dest_node_label: str,
            dest_node_property: str,
            relationship: str
    ) -> object:
        """
        Get NetworkX instance for the paths
        retrieved from Gremlin queries
        :param edges: list of paths
        :param dest_node_label: Label name
        :param dest_node_property: Property name
        :param relationship: relationship name
        :return: NetworkX instance
        """
        network = nx.DiGraph()
        for index, path in enumerate(edges):

            for elements in path:
                if dest_node_label in elements.keys():
                    dest_name, source_name = \
                        self.get_node_names(
                            dest_node_property,
                            elements,
                            path
                        )

                    network = self.update_network(
                        dest_name,
                        dest_node_label,
                        network,
                        relationship,
                        source_name)
        return network

    def update_network(
            self,
            dest_name,
            dest_node_label,
            network,
            relationship,
            source_name
    ) -> Any:
        """
        Method called internally to add nodes
        and relations to the NetworkX instance
        :param dest_name: Node name
        :param dest_node_label: Node label
        :param network: NetworkX instance
        :param relationship: relation name
        :param source_name: Node name
        :return: updated networkx instance
        """
        network.add_node(
            source_name,
            label=SOURCE_NODE_LABEL
        )
        network.add_node(
            dest_name,
            label=dest_node_label
        )
        network.add_edge(
            source_name,
            dest_name,
            elabel=relationship
        )
        return network

    def get_neighbors_count(
            self,
            neighbors_customer1,
            neighbors_customer2
    ):
        """
        Get number of neighbors for source
        node and destination node
        :param neighbors_customer1: customer1 neighbors
        :param neighbors_customer2: customer2 neighbors
        :return: customer1, customer2 respective
        neighbor counts
        """
        neighbors_customer1_count = len(
            [element for element in neighbors_customer1]
        )
        neighbors_customer2_count = len(
            [element for element in neighbors_customer2]
        )
        return neighbors_customer1_count, \
            neighbors_customer2_count

    def get_neighborhood_overlap(
            self,
            neighbors_customer1_count,
            neighbors_customer2_count,
            network,
            user1,
            user2
    ) -> float:
        """
        Calculates and returns neighborhood overlap
        using the number of common neighbors between
        any given set of nodes. This count is then
        divided by the minimum neighbor count
        of the 2 nodes
        :param neighbors_customer1_count: count value
        :param neighbors_customer2_count: count value
        :param network: networkx instance
        :param user1: one of the two nodes to be
        considered in calculation
        :param user2: one of the two nodes to be
        considered in calculation
        :return: neighborhood overlap float value
        """
        return len(
            sorted(
                nx.common_neighbors(
                    network,
                    user1,
                    user2
                ))
        ) / max(1, min(
                 neighbors_customer2_count,
                 neighbors_customer1_count
                )
        )

    def validate_overlap(
            self,
            overlap,
            relation_similarity_scores,
            user1,
            user2
    ):
        """
        Assess the similarity score to decide
        whether or not to consider this relation
        while umping into the graphDB.
        :param overlap: similarity_score
        :param relation_similarity_scores:
        dataframe object pandas
        :param user1: one of the two nodes to be
        considered in calculation
        :param user2: one of the two nodes to be
        considered in calculation
        :return:
        """
        if overlap > self.sim_cutoff:
            users = sorted([user1, user2])
            relation_similarity_scores.loc[
                len(relation_similarity_scores)] = \
                [users[0], users[1], overlap]

    def update_similarity_table(
            self,
            relation_similarity_scores,
            feature_weight: float
    ):
        """
        Remove duplicate relations and update
        the master similarity scores dataframe object
        :param relation_similarity_scores: dataframe
        object pandas
        :param feature_weight: feature similarity
        contribution weight
        :return: None, updates the instance member
        of the class
        """
        relation_similarity_scores = \
            relation_similarity_scores.drop_duplicates(
                subset=[USER1, USER2]
            ).reset_index(drop=True)

        relation_similarity_scores[SCORE] *= feature_weight

        self.similarity_score = concat(
            [
                self.similarity_score,
                relation_similarity_scores
             ], axis=0
        ).reset_index(drop=True)
