from pandas import DataFrame, get_dummies
from ingestor.common.constants import CUSTOMER_ID, DURATION


class PreferenceGenerator:

    def __init__(
            self,
            feature=None,
            feature_cutoff=None,
            user_cutoff=None
    ):
        """
        :param feature: feature from the data
        for which preference needs to be computed
        :param feature_cutoff: All rankings in the lower
        1/feature_cutoff of a given feature's values
        would not be considered for preference generation.
        :param user_cutoff: All rankings in the lower
        1/user_cutoff of a given user's values
        would not be considered for preference generation.
        """
        self.feature = feature
        self.feature_cutoff = feature_cutoff
        self.user_cutoff = user_cutoff

    def filter_features(
            self,
            df: DataFrame,
    ) -> DataFrame:
        """
        Filter the feature set from the provided DataFrame
        to comprise of features important for preference
        generation. (identifier and duration features being
        the mandatory components)

        :param df: dataframe object pandas
        :return: filtered dataframe object pandas
        """
        return df[[CUSTOMER_ID, DURATION, self.feature]]

    def get_dummy_attributes(
            self,
            df: DataFrame
    ) -> DataFrame:
        """
        Generate dummy attributes for the considered feature

        :param df: dataframe object pandas
        :return: Binary encoded dataframe object pandas
        """
        return get_dummies(df, columns=[self.feature])

    @staticmethod
    def compute_weights(
            df: DataFrame
    ) -> DataFrame:
        """
        Computes weights for each dummy attribute using
        duration values from the data.

        :param df: dataframe object pandas
        :return: weighted dataframe object pandas
        """

        for feature in df.columns:
            if feature in [CUSTOMER_ID, DURATION]:
                continue
            df[feature] = df[feature] * df[DURATION]

        df.drop(columns=DURATION, inplace=True)
        weighted_df = df.groupby([CUSTOMER_ID]).sum()

        return weighted_df.reset_index()

    @staticmethod
    def compute_feature_level_ranking(
            df: DataFrame
    ) -> DataFrame:
        """
        For each weighted dummy attribute in the dataset,
        compute the ranking and replace against its
        constituent values.

        :param df: dataframe object pandas
        :return: weighted dataframe object pandas
        """
        for feature in df.columns:

            if feature == CUSTOMER_ID:
                continue

            df[feature] = df[feature].rank(method='min')
            df[feature] = df[feature].astype(int)

        return df

    @staticmethod
    def obtain_preference_candidates(
            values: list,
            cutoff: int
    ) -> list:
        """
        Return values that lie beyond the specified
        cutoff range.

        :param values: list of duration values
        :param cutoff: integer threshold
        :return: list of candidate duration values
        """
        values.sort()
        candidates = len(values) // cutoff

        return values[candidates:]

    def rank_attribute_values(
            self,
            df: DataFrame,
            feature: str
    ) -> DataFrame:
        """
        Rank the duration values for the
        considered feature.

        :param df: dataframe object pandas
        :param feature: attribute name
        :return: binary encoded preference
        indicative values for the feature
        """
        values = list(df[feature].unique())
        values = self.obtain_preference_candidates(
            values=values,
            cutoff=self.feature_cutoff
        )

        df[feature] = [1 if value in values else 0
                       for value in df[feature]]

        return df

    def rank_record_values(
            self,
            df: DataFrame,
            record: int
    ) -> DataFrame:
        """
        Rank the duration values for the considered
        user record.

        :param df: dataframe object pandas
        :param record: user record
        :return: binary encoded preference indicative
        values for the user record.
        """

        # ignoring identifier attribute at 0th index
        record_v = df.iloc[record, 1:]

        unique_v = list(set(record_v.values))
        unique_v = self.obtain_preference_candidates(
            values=unique_v,
            cutoff=self.user_cutoff
        )

        # updating all attributes except the identifier
        df.iloc[record, 1:] = [1 if value in unique_v else 0
                               for value in record_v]

        return df

    def get_feature_preference_encodings(
            self,
            df: DataFrame
    ) -> DataFrame:
        """
        For the weighted duration feature values, find the
        preference candidates.

        :param df: dataframe object pandas
        :return: preference encoded dataframe object pandas
        """
        for feature in df.columns:

            if feature == CUSTOMER_ID:
                continue
            df = self.rank_attribute_values(df, feature)

        return df

    def get_user_preference_encodings(
            self,
            df: DataFrame
    ) -> DataFrame:
        """
        For the weighted duration user record values, find
        the preference candidates.

        :param df: dataframe object pandas
        :return: preference encoded dataframe object pandas
        """
        for index in range(len(df)):
            df = self.rank_record_values(df, index)

        return df

    @staticmethod
    def get_preferences(
            cat_data: DataFrame,
            user_data: DataFrame
    ) -> DataFrame:
        """
        Computing feature preference values for the user by
        replicating boolean OR operation over the feature
        preference candidates and user preference candidates.

        :param cat_data: dataframe object pandas
        :param user_data: dataframe object pandas
        :return:
        """
        preferences = DataFrame(columns=user_data.columns)
        preferences[CUSTOMER_ID] = user_data[CUSTOMER_ID]

        for feature in preferences.columns:

            if feature == CUSTOMER_ID:
                continue

            preferences[feature] = user_data[feature] + cat_data[feature]
            preferences[feature] = [1 if pref_feature > 0 else 0
                                    for pref_feature in preferences[feature]]

        return preferences

    def controller(
            self,
            data: DataFrame
    ) -> DataFrame:
        """
        The driver method for member functions in
        PreferenceGenerator class. Uses the input path
        to read raw feature set to generate
        user-wise preferences for each of them.

        :param data: dataframe object pandas
        :return: preference encoded dataframe object
        """
        for column in data.columns:

            if column in [CUSTOMER_ID, DURATION]:
                continue

            data = self.filter_features(data)
            data = self.get_dummy_attributes(data)
            data = self.compute_weights(data)
            cat_d = self.compute_feature_level_ranking(data.copy())
            cat_d = self.get_feature_preference_encodings(cat_d)
            user_d = self.get_user_preference_encodings(data.copy())

            return self.get_preferences(cat_d, user_d)
