from pandas import DataFrame
from ingestor.user_profile.similarity.config import \
    ASSIGN_CLUSTER_FEATURES, GENDER_MAP
from ingestor.common.constants import PAYTVPROVIDER_ID, GENDER, AGE
from graphdb.graph import GraphDb

class ClusterAllocatorUtils:

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
        self.connection_object = connection_object
        self.graph = GraphDb.from_connection(
            connection_object
        )

    def filter_features(
            self,
            data=DataFrame
    ) -> DataFrame:
        """
        Filter the dataframe object to only keep
        the features used for identifying
        the cluster labels
        :param data: dataframe object pandas
        :return dataframe object pandas
        """
        return data[ASSIGN_CLUSTER_FEATURES]

    def user_has_paytv(
            self,
            paytv_val
    ) -> bool:
        """
        Check whether the user is of paytv
        type or non-paytv type
        :param paytv_val: paytv provider
        value in the user record
        :return: boolean indicator
        """
        if paytv_val == -1:
            return False
        return True

    def process_user_centroid_records(
            self,
            centroids: DataFrame,
            user: DataFrame
    ):
        """
        Remove unnecessary features from user
        and centroid dataframe objects
        :param centroids: dataframe object pandas
        :param user: dataframe object pandas
        :return: processed centroid and user
        objects
        """
        user = user.reset_index(drop=True)
        user = self.filter_features(data=user)
        user = user.loc[0, :].values.tolist()
        centroids = self.filter_features(
            data=centroids
        )
        return centroids, user

    def process_paytv_feature(
            self,
            users: DataFrame
    ):
        """
        Process the paytvprovider_id field for
        user records
        :param users: dataframe object pandas
        :return: dataframe object pandas
        """
        users[PAYTVPROVIDER_ID] = \
            users[PAYTVPROVIDER_ID].fillna(-1)

        for index in range(len(users)):
            if not isinstance(
                    users.loc[index, PAYTVPROVIDER_ID],
                    int
            ):
                paytv = (
                    users.loc[index, PAYTVPROVIDER_ID])[0]
                users.loc[index, PAYTVPROVIDER_ID] = \
                    paytv[PAYTVPROVIDER_ID]

        return users

    def get_paytv_wise_users(
            self,
            users
    ):
        """
        Segregate users dataframe object into
        paytv and non-paytv users
        :param users: dataframe object pandas
        :return: paytv and nonpaytv users
        dataframe objects
        """
        paytv_users = users[users[PAYTVPROVIDER_ID] != -1] \
            .reset_index(drop=True)
        nonpaytv_users = users[users[PAYTVPROVIDER_ID] == -1] \
            .reset_index(drop=True)

        return nonpaytv_users, paytv_users

    def preprocess_user_attributes(
            self,
            users: DataFrame
    ):
        users[GENDER] = [GENDER_MAP[gender]
                         for gender in users[GENDER]]
        users[AGE] = users[AGE].fillna(-1)
        users = self.process_paytv_feature(
            users=users
        )
        return users
