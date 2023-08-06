from graphdb.schema import Node
from ingestor.common.constants import LABEL, PROPERTIES
from math import sqrt
from sklearn import preprocessing
from numpy import array

class SimilarityCommons:

    @staticmethod
    def get_node(
            label: str,
            properties: dict,
            db_graph
    ) -> Node:
        """
        Find a node in GraphDB. If that node
        exists, return the corresponding node
        object, else return None
        :param label: node label string
        :param properties: dictionary object
        for node properties
        :param db_graph: graphDB object
        :return: Node object is node exists,
         else None
        """
        node = Node(
            **{
                LABEL: label,
                PROPERTIES: properties
            }
        )
        node_in_graph = \
            db_graph.find_node(node)
        if len(node_in_graph) > 0:
            return node_in_graph[0]
        return None

    @staticmethod
    def get_distance(
            vector_a: list,
            vector_b: list
    ):
        """
        Compute Euclidean Distance between two vectors
        :param vector_a: Vector for user features
        :param vector_b: Vector for corresponding
        centroid features
        :return: Euclidean Distance
        """
        vector_a = [float(val) for val in vector_a]
        vector_b = [float(val) for val in vector_b]
        return sqrt(
            sum(
                [(va - vb) ** 2 for va, vb in zip(
                    vector_a, vector_b
                )]
            )
        )

    @staticmethod
    def normalize(
            vector
    ):
        """
        Perform vector normalization
        :param vector: input vector
        :return: normalized vector
        """
        scaler = preprocessing.MinMaxScaler()
        return scaler.fit_transform(
            array(vector).reshape(-1, 1))