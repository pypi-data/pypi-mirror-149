from botocore.config import Config
import boto3


def get_ncf_ranked_offers(rbi_cognito_id, table_name, access_key, secret_key):
    my_config = Config(region_name='us-east-1', connect_timeout=2, read_timeout=2, retries={'max_attempts': 2})
    dynamodb = boto3.resource('dynamodb', config=my_config,
                              aws_access_key_id=access_key, aws_secret_access_key=secret_key)
    ncf_pred_table = dynamodb.Table(table_name)
    try:
        response = ncf_pred_table.get_item(Key={'rbi_cognito_id': rbi_cognito_id})
        if response.get("ResponseMetadata", {}).get("HTTPStatusCode", "") == 200:
            if "Item" in response and "ranked_offers" in response["Item"] and "group" in response["Item"]:
                user_group = response["Item"]["group"]
                ranked_offers = response["Item"]["ranked_offers"]
                get_assigned_offers_ind = "success"
            elif "Item" not in response:
                ranked_offers = []
                user_group = ""
                get_assigned_offers_ind = "userNotInNCF"
            elif "ranked_offers" not in response.get("Item", []):
                ranked_offers = []
                user_group = ""
                get_assigned_offers_ind = "noRankedOffer"
            elif "user_group" not in response.get("Item", []):
                ranked_offers = []
                user_group = ""
                get_assigned_offers_ind = "noGroupAssigned"
            else:
                ranked_offers = []
                user_group = ""
                get_assigned_offers_ind = "implementError"
        else:
            ranked_offers = []
            user_group = ""
            get_assigned_offers_ind = response.get("ResponseMetadata", {}).get("HTTPStatusCode", "")
    except Exception as e:
        ranked_offers = []
        user_group = ""
        get_assigned_offers_ind = str(e)
    return ranked_offers, get_assigned_offers_ind, user_group
