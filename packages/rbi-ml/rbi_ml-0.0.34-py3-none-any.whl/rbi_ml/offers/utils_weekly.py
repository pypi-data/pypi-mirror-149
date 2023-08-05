from __future__ import print_function
import random
import boto3
from botocore.config import Config
from datetime import datetime
from .app_mxnet_inference import get_dma


def get_purchases(table, uid):
    get_purchase_ind = "n/a"
    try:
        response = table.get_item(Key={'userId': uid})
        if 'Item' in response:
            results = response['Item']['purchases']
            ind = 0
        else:
            results = []
            ind = 1
            get_purchase_ind = "noHistory"
    except Exception as e:
        results = []
        ind = 2
        get_purchase_ind = str(e)

    return results, ind, get_purchase_ind


def draw_test_group(test_group_weights):
    group_names = test_group_weights.get("groups")
    weights = test_group_weights.get("weights")
    assert len(group_names) == len(weights), "incomparable length groups and weights"

    groups = [
        random.choices(population=group_name, weights=weight)[0]
        for group_name, weight in zip(group_names, weights)
    ]
    return "-".join(groups)


def draw_national_group(national_group_weights):
    group_names = national_group_weights.get("groups")
    weights = national_group_weights.get("weights")
    assert len(group_names) == len(weights), "incomparable length groups and weights"

    group = random.choices(population=group_names, weights=weights)[0]
    return group


def draw_control(test_control_weights):
    return random.choices(
        population=[False, True],
        weights=[test_control_weights["test"], test_control_weights["control"]],
        k=1
    )[0]


def get_user_profile(uid, create_new_control, test_control_weights, rest_tz, access_key, secret_key):
    my_config = Config(region_name='us-east-1', connect_timeout=2, read_timeout=4, retries={'max_attempts': 2})
    dynamodb = boto3.resource('dynamodb', config=my_config,
                              aws_access_key_id=access_key, aws_secret_access_key=secret_key)
    profile_table = dynamodb.Table("digitalGuestProfile")
    try:
        response = profile_table.get_item(Key={'userId': uid})
        # user exists
        if 'Item' in response:
            # get purchase history
            if 'purchases' in response['Item']:
                purchase_history = response['Item']['purchases']
                get_purchase_ind = 'success'
                ind = 0
            else:
                purchase_history = []
                get_purchase_ind = 'noHistory'
                ind = 1

            # get loyalty_id
            loyalty_id = response.get("Item", {}).get("loyaltyId")

            # get control
            dt_now = datetime.utcnow()
            old_expires = response['Item'].get('assignedOffers', {}).get("weeklyOffersExpireOn", "2000-01-01T00:00:00")
            dt_old_expires = datetime.fromisoformat(old_expires.split(".")[0])
            is_newly_assigned_weekly = (dt_old_expires - dt_now).total_seconds() > 3600 * 24 * 4  # 4 days
            if "is_control" in response["Item"].get("assignedOffers", {}) and (
                    not create_new_control or is_newly_assigned_weekly):
                is_control = response["Item"].get("assignedOffers", {}).get("is_control")
                if type(is_control) != bool:
                    is_control = draw_control(test_control_weights=test_control_weights)
            else:
                is_control = draw_control(test_control_weights=test_control_weights)

            # # get group
            # if 'group' in response['Item'].get("assignedOffers", {}) and (
            #         not CREATE_NEW_GROUP or is_newly_assigned_weekly):
            #     control_group = response['Item']['assignedOffers']['group']
            #     get_group_ind = 'success'
            # else:
            #     control_group = draw_test_group(test_group_weights=TEST_GROUP_WEIGHTS)
            #     get_group_ind = 'newlyCreated'

            # get location
            user_location = response['Item'].get('user_attributes', {}).get('location', {})
        # user not exists
        else:
            loyalty_id = None
            user_attributes = None
            purchase_history = []
            user_location = {}
            get_purchase_ind = 'noHistory'
            is_newly_assigned_weekly = False
            ind = 1
            # control_group = draw_test_group(test_group_weights=TEST_GROUP_WEIGHTS)
            is_control = draw_control(test_control_weights=test_control_weights)
            # get_group_ind = 'newlyCreated'
    except Exception as e:
        loyalty_id = None
        user_attributes = None
        purchase_history = []
        user_location = {}
        ind = 2
        get_purchase_ind = str(e)
        is_newly_assigned_weekly = False
        # control_group = draw_test_group(test_group_weights=TEST_GROUP_WEIGHTS)
        is_control = draw_control(test_control_weights=test_control_weights)
        # get_group_ind = str(e) + 'newlyCreated'

    store_history = [str(purchase.get("bkid", "0")) for purchase in purchase_history]
    user_tier, is_phoenix = get_dma(store_ids=store_history, user_location=user_location, dim_rest=rest_tz)

    return loyalty_id, purchase_history, is_newly_assigned_weekly, get_purchase_ind, user_tier, is_control, is_phoenix


# def get_purchases_and_offers(table, uid):
#     get_purchase_ind = "n/a"
#     try:
#         response = table.get_item(Key={'userId': uid})
#         if 'Item' in response:
#             results = response['Item']['purchases']
#             assigned_offers = response["Item"]["assignedOffers"]
#             ind = 0
#         else:
#             results = []
#             assigned_offers = {}
#             ind = 1
#             get_purchase_ind = "noHistory"
#     except Exception as e:
#         results = []
#         assigned_offers = {}
#         ind = 2
#         get_purchase_ind = str(e)
#
#     return results, ind, get_purchase_ind, assigned_offers


def update_profile_offers(uid, assigned_offers, access_key, secret_key):
    my_config = Config(region_name='us-east-1', connect_timeout=2, read_timeout=4, retries={'max_attempts': 2})
    dynamodb = boto3.resource('dynamodb', config=my_config,
                              aws_access_key_id=access_key, aws_secret_access_key=secret_key)
    table = dynamodb.Table("digitalGuestProfile")

    update_expression = "set #attrName = :attrValue"
    expr_attr_names = {"#attrName": "assignedOffers"}
    expr_attr_values = {":attrValue": assigned_offers}
    # if loyalty_id:
    #     update_expression += ", #attrNameA = :attrValue1"
    #     expr_attr_names.update({"#attrNameA": "loyaltyId"})
    #     expr_attr_values.update({":attrValue1": loyalty_id})
    # if user_attributes:
    #     update_expression += ", #attrNameB = :attrValue2"
    #     expr_attr_names.update({"#attrNameB": "user_attributes"})
    #     expr_attr_values.update({":attrValue2": user_attributes})

    try:
        update_response = table.update_item(
            Key={
                'userId': uid
            },
            UpdateExpression=update_expression,
            ExpressionAttributeNames=expr_attr_names,
            ExpressionAttributeValues=expr_attr_values,
            ReturnValues="UPDATED_NEW"
        )
        status_code = update_response['ResponseMetadata']['HTTPStatusCode']
    except Exception as e:
        status_code = str(e)
    return status_code


def get_test_group(default_offers, test_group_weights, is_control, user_tier, has_history):
    k1 = "control" if is_control else "personalized" if has_history else "default"
    k2 = "tier1" if user_tier == "1" else "tier2"
    price_tier = "1_Personalized" if k2 == "tier1" else "2_Personalized"
    group_names = test_group_weights.get(k1, {}).get(k2, {}).get("names", ["n/a"])
    weights = test_group_weights.get(k1, {}).get(k2, {}).get("weights", [1.0])
    topk = test_group_weights.get(k1, {}).get(k2, {}).get("topk", [5])
    assert len(group_names) == len(weights), "incomparable length groups and weights"
    # groups = [
    #     random.choices(population=group_name, weights=weight)[0]
    #     for group_name, weight in zip(group_names, weights)
    # ]
    test_group = random.choices(population=group_names, weights=weights, k=1)[0]
    topk_weekly = topk[group_names.index(test_group)]
    default_weekly = default_offers.get(k2, {}).get(test_group, [])
    return price_tier, test_group, topk_weekly, default_weekly
