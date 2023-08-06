"""
Represents the MongoDb::Atlas::AwsIamDatabaseUser resource
"""

from troposphere import AWSObject, AWSProperty, PropsDictType


class ApiKeys(AWSProperty):
    """
    MongoDb::Atlas::AwsIamDatabaseUser::ApiKeys
    """

    props: PropsDictType = {"PublicKey": (str, True), "PrivateKey": (str, True)}


class MongoDbAwsIamDatabaseUser(AWSObject):
    """
    Class to represent in Troposphere the MongoDb::Atlas::AwsIamDatabaseUser resource
    """

    resource_type = "MongoDb::Atlas::AwsIamDatabaseUser"
    props: PropsDictType = {
        "AwsIamResource": (str, True),
        "ApiKeys": (ApiKeys, True),
        "ProjectId": (str, True),
        "Scopes": (dict, False),
        "DatabaseAccess": (dict, True),
    }
