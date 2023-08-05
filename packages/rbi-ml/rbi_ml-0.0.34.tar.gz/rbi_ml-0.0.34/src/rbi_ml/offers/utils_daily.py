import json
import random
from datetime import datetime
import requests
import boto3
from botocore.config import Config
from .app_mxnet_inference import get_dma
from .utils_ncf import get_ncf_ranked_offers


def get_assigned_offers(uid, rest_tz):
    my_config = Config(region_name='us-east-1', connect_timeout=2, read_timeout=2, retries={'max_attempts': 2})
    dynamodb = boto3.resource('dynamodb', config=my_config)
    table = dynamodb.Table("digitalGuestProfile")
    try:
        response = table.get_item(Key={'userId': uid})
        if response.get("ResponseMetadata", {}).get("HTTPStatusCode", "") == 200:
            if "Item" in response and "assignedOffers" in response["Item"]:
                get_assigned_offers_ind = "success"
                assigned_offers = response["Item"].get("assignedOffers", {})
                user_location = response['Item'].get('user_attributes', {}).get('location', {})
                # get loyalty_id
                loyalty_id = response["Item"].get("loyaltyId")
                if "purchases" in response["Item"]:
                    purchase_history = response['Item'].get('purchases', [])
                else:
                    purchase_history = []
            elif "Item" not in response:
                user_location = {}
                purchase_history = []
                get_assigned_offers_ind = "userNotExisted"
                assigned_offers = {}
                loyalty_id = None
            elif "assignedOffers" not in response.get("Item", []):
                user_location = {}
                purchase_history = []
                get_assigned_offers_ind = "userNoAssignedOffers"
                assigned_offers = {}
                loyalty_id = None
            else:
                user_location = {}
                purchase_history = []
                get_assigned_offers_ind = "implementError"
                assigned_offers = {}
                loyalty_id = None
        else:
            user_location = {}
            purchase_history = []
            get_assigned_offers_ind = response.get("ResponseMetadata", {}).get("HTTPStatusCode", "")
            assigned_offers = {}
            loyalty_id = None
    except Exception as e:
        user_location = {}
        purchase_history = []
        get_assigned_offers_ind = str(e)
        assigned_offers = {}
        loyalty_id = None
    store_history = [str(purchase.get("bkid", "0")) for purchase in purchase_history]
    user_tier, is_phoenix = get_dma(store_ids=store_history, user_location=user_location, dim_rest=rest_tz)
    return purchase_history, assigned_offers, get_assigned_offers_ind, user_tier, loyalty_id


def get_daily_offer(offer_pools, offer_attributes, uid, user_tier, assigned_offers, cluster, lapsed_category, daily_personalized_k,
                    daily_lapsed_k, daily_offer_id, daily_lapsed_id, offer_group_lookup, daily_offer_id_backup):
    dt_now = datetime.utcnow()
    daily_expires_on = assigned_offers.get("dailyOffersExpireOn", "2000-01-01T00:00:00")
    dt_old_daily_expires = datetime.fromisoformat(daily_expires_on.split(".")[0])
    is_newly_assigned_daily = (dt_old_daily_expires - dt_now).total_seconds() > 3600 * 12  # 12 hours
    assigned_offer_groups = [
        offer_group_lookup.get(offer_id, "0")
        for offer_id in assigned_offers.get("weeklyOffers", [])
    ]
    if not is_newly_assigned_daily:
        price_tier = "1_Personalized" if user_tier == "1" else "2_Personalized"
        # rank offers - randomly
        daily_offer_ranked_random = random.sample(daily_offer_id, len(daily_offer_id))
        daily_lapsed_ranked_random = random.sample(daily_lapsed_id, len(daily_lapsed_id))
        daily_offer_sup_random = random.sample(daily_offer_id_backup[user_tier], len(daily_offer_id_backup[user_tier]))

        # rank offers - NCF
        daily_offer_ranked_ncf, get_assigned_offers_ind_ncf, user_group_ncf = get_ncf_ranked_offers(
            rbi_cognito_id=uid,
            table_name="bk-us-ncf-pred"
        )
        if get_assigned_offers_ind_ncf == "success" and user_group_ncf == "test":
            daily_offer_ranked = [
                oid
                for oid in daily_offer_ranked_ncf
                if oid in offer_pools["weekly"]
                and offer_attributes.get(oid, {}).get("Offer Type", "") == price_tier
            ]
            daily_lapsed_ranked = [
                oid
                for oid in daily_offer_ranked_ncf
                if oid in offer_pools["weekly"]
                if offer_attributes.get(oid, {}).get("Offer Type", "") in ["Lapsed_60", "Lapsed_90"]
            ]
        else:
            daily_offer_ranked = daily_offer_ranked_random
            daily_lapsed_ranked = daily_lapsed_ranked_random
        daily_offer_ranked += daily_offer_sup_random

        # pick ranked offers
        selected_personalized_offers = []
        for offer_id in daily_offer_ranked:
            offer_group = offer_group_lookup.get(offer_id, "0")
            if offer_group == "0" or offer_group not in assigned_offer_groups:
                selected_personalized_offers.append(offer_id)
                assigned_offer_groups.append(offer_group)
                if len(selected_personalized_offers) >= daily_personalized_k:
                    break
        selected_lapsed_offers = []
        if lapsed_category in ["60", "90"]:
            for offer_id in daily_lapsed_ranked:
                offer_group = offer_group_lookup.get(offer_id, "0")
                if offer_group == "0" or offer_group not in assigned_offer_groups:
                    selected_lapsed_offers.append(offer_id)
                    assigned_offer_groups.append(offer_group)
                    if len(selected_lapsed_offers) >= daily_lapsed_k:
                        break
        selected_offers = selected_personalized_offers + selected_lapsed_offers
    else:
        selected_offers = assigned_offers.get("dailyOffers", ["n/a"])
    return selected_offers, assigned_offer_groups


def update_profile_offers(uid, assigned_offers):
    my_config = Config(region_name='us-east-1', connect_timeout=2, read_timeout=2, retries={'max_attempts': 2})
    dynamodb = boto3.resource('dynamodb', config=my_config)
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
            ReturnValues="UPDATED_NEW",
        )
        status_code = update_response['ResponseMetadata']['HTTPStatusCode']
    except Exception as e:
        status_code = str(e)
    return status_code


def update_amplitude_event(uid, attributes_d):
    amplitude_data = {
        "events":
            [
                {
                    "data": {
                        "custom_event_type": "user_preference",
                        "event_name": "Daily Offer Personalization",
                        "custom_attributes": attributes_d
                    },
                    "event_type": "custom_event"
                }
            ],
        "environment": "production",
        "user_identities": {"customer_id": uid}
    }
    amplitude_json_data = json.dumps(amplitude_data)
    amplitude_response = requests.post('https://s2s.mparticle.com/v2/events',
                                       auth=requests.auth.HTTPBasicAuth(
                                           'us1-9e24f161c6023f4e8e2d9a52ad8c6b37',
                                           'gplReWa5XTlIQ5_zO_78p0X4habcNjfaj-N6xDipT3ayp9jGJevvyI52pD2_n5gK'),
                                       data=amplitude_json_data)
    try:
        amplitude_response_code = str(amplitude_response.status_code)
    except Exception as e:
        amplitude_response_code = 'exceptionError'
    return amplitude_response_code


def draw_national_group(national_group_weights):
    group_names = national_group_weights.get("groups")
    weights = national_group_weights.get("weights")
    assert len(group_names) == len(weights), "incomparable length groups and weights"

    group = random.choices(population=group_names, weights=weights)[0]
    return group
