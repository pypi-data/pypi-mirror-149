from pandas import DataFrame
from ingestor.common.constants import CUSTOMER_ID, DUMMY_ATTRIBUTE_SPLIT_ON


class RelationshipExtractor:

    def __init__(
            self,
            data: DataFrame
    ):
        """
        Accept the dataframe object with
        dummy attributes
        :param data: dataframe object
        """
        self.data = data

        #initializing feature name for the result
        self.original_title = ''

    def get_original_feature_title(
            self
    ):
        """
        Finding the feature name for result dataframe
        from one of the current dummy attributes
        :return: None, simply updates the instance
        member of the class
        """
        for feature in self.data.columns:

            if feature == CUSTOMER_ID:
                continue

            self.original_title = feature.rsplit(
                DUMMY_ATTRIBUTE_SPLIT_ON, 1)[0]

            # all dummy features will return the
            # same value, therefore no need to iterate for
            # more than one attribute
            break

    def get_original_feature_values(
            self
    ):
        """
        Obtain the relation nodes to which the customer
        node will be connected to. This will be found by
        choosing all the dummy features with a
        value = 1 for a given customer_id
        :return:None, simply updates the instance
        member of the class
        """
        for feature in self.data.columns:

            if feature == CUSTOMER_ID:
                continue

            feature_val = feature.rsplit(
                DUMMY_ATTRIBUTE_SPLIT_ON, 1
            )

            self.data.rename(
                columns={feature: feature_val[1]},
                inplace=True
            )

    def add_relation(
            self,
            df: DataFrame,
            customer_id: str,
            original_feature_val: str
    ):
        """
        Create a new record in the result df
        :param df: result dataframe object
        :param customer_id: customer id in
        result df record
        :param original_feature_val: connect
        customer_id to this node
        :return:
        """
        record_count = len(df)

        df.loc[record_count,
               CUSTOMER_ID] = customer_id

        df.loc[record_count,
               self.original_title] = original_feature_val

    def get_preference_relationships(
            self
    ):
        """
        Find all the relationships from dummy
        attribute dataframe
        :return: non-dummified dataframe with
        customer id and records with its preferences
        for the specific feature values
        """

        result = DataFrame(
            columns=[CUSTOMER_ID,
                     self.original_title]
        )

        for index in range(len(self.data)):
            customer_id = self.data.loc[index, CUSTOMER_ID]

            for feature in self.data.columns:

                # if this attribute value is a user
                # preference, create a new record between
                # this customer id and preference value
                if self.data.loc[index, feature] == 1:
                    self.add_relation(
                        df=result,
                        customer_id=customer_id,
                        original_feature_val=feature
                    )

        return result

    def controller(
            self
    ):
        """
        Driver function
        :return: non-dummified dataframe with
        customer id and records with its preferences
        for the feature values
        """
        self.get_original_feature_title()
        self.get_original_feature_values()
        return self.get_preference_relationships()
