import os
import random
import json
import pandas as pd
import torch
import boto3
from botocore.config import Config
from src.torch_layers import TxTFeaturesExtractor


def generate_lookup_dict(df, key_col, value_col):
    """Generate int2int lookup dict from given dataframe."""
    return df[[key_col, value_col]].set_index(key_col).to_dict()[value_col]


def load_lookup_model(model_name, offer_lookup_dynamodb_table="digitalOfferLookup"):
    """
    Load lookup tables from local directory
    :param model_name: root directory all model files
    :param offer_lookup_dynamodb_table: table name of offer_lookup table in DynamoDB
    :return: lookup tables and TxT model
    """
    # read offer_lookup from DynamoDB
    my_config = Config(region_name='us-east-1', connect_timeout=5, read_timeout=5, retries={'max_attempts': 10})
    dynamodb = boto3.resource('dynamodb', config=my_config)
    digital_offer_lookup = dynamodb.Table(offer_lookup_dynamodb_table)
    response = digital_offer_lookup.scan()
    items = response['Items']
    while 'LastEvaluatedKey' in response:
        response = digital_offer_lookup.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        items.extend(response['Items'])
    offer_lookup = pd.DataFrame({'data': items})
    offer_lookup.loc[:, "OFFER_ID"] = offer_lookup.loc[:, "data"].apply(lambda x: x.get("OFFER_ID"))
    offer_lookup.loc[:, "OFFER_IDX"] = offer_lookup.loc[:, "data"].apply(lambda x: int(x.get("OFFER_IDX")))
    offer_lookup.loc[:, "SENDABLE"] = offer_lookup.loc[:, "data"].apply(lambda x: x.get("SENDABLE"))
    offer_lookup.loc[:, "BREAKFAST"] = offer_lookup.loc[:, "data"].apply(lambda x: x.get("BREAKFAST"))
    offer_lookup.loc[:, "LAPSED_90"] = offer_lookup.loc[:, "data"].apply(lambda x: x.get("LAPSED_90"))
    offer_lookup.loc[:, "OFFER_STRUCTURE"] = offer_lookup.loc[:, "data"].apply(lambda x: x.get("OFFER_STRUCTURE"))
    offer_lookup.loc[:, "OFFER_URL"] = offer_lookup.loc[:, "data"].apply(lambda x: x.get("OFFER_URL"))
    offer_lookup.loc[:, "GPM_OFFER"] = offer_lookup.loc[:, "data"].apply(lambda x: x.get("GPM_OFFER"))
    offer_lookup.loc[:, "OFFER_NAME_FINALIZED"] = offer_lookup.loc[:, "data"].apply(
        lambda x: x.get("OFFER_NAME_FINALIZED")
    )
    offer_lookup.loc[:, "OFFER_NAME_FORMATTED"] = offer_lookup.loc[:, "data"].apply(
        lambda x: x.get("OFFER_NAME_FORMATTED")
    )
    offer_lookup.loc[:, "OFFER_NAME"] = offer_lookup.loc[:, "data"].apply(lambda x: x.get("OFFER_NAME"))
    offer_lookup = offer_lookup.drop(columns=["data"])
    offer_lookup_img = offer_lookup[["OFFER_ID", "OFFER_NAME_FORMATTED", "OFFER_URL"]].copy()
    # print("Load offer lookup table from DynamoDB table %s" % offer_lookup_dynamodb_table)

    # Paths
    model_path = os.path.join("models/", model_name, "model.pt")
    platform_lookup_path = os.path.join("models/", model_name, "platform_lookup.csv")
    dma_lookup_path = os.path.join("models/", model_name, "dma_lookup.csv")
    device_carrier_lookup_path = os.path.join("models/", model_name, "device_carrier_lookup.csv")
    device_model_lookup_path = os.path.join("models/", model_name, "device_model_lookup.csv")

    # Load lookup table
    platform_lookup = pd.read_csv(platform_lookup_path)
    dma_lookup = pd.read_csv(dma_lookup_path)
    device_carrier_lookup = pd.read_csv(device_carrier_lookup_path)
    device_model_lookup = pd.read_csv(device_model_lookup_path)
    idx2offerid = generate_lookup_dict(offer_lookup, key_col="OFFER_IDX", value_col="OFFER_ID")
    idx2offername = generate_lookup_dict(offer_lookup, key_col="OFFER_IDX", value_col="OFFER_NAME_FINALIZED")
    offerid2idx = generate_lookup_dict(offer_lookup, key_col="OFFER_ID", value_col="OFFER_IDX")
    offername2idx = generate_lookup_dict(offer_lookup, key_col="OFFER_NAME_FINALIZED", value_col="OFFER_IDX")
    platform2idx = generate_lookup_dict(platform_lookup, key_col="PLATFORM", value_col="PLATFORM_IDX")
    dma2idx = generate_lookup_dict(dma_lookup, key_col="DMA", value_col="DMA_IDX")
    carrier2idx = generate_lookup_dict(device_carrier_lookup, key_col="DEVICE_CARRIER", value_col="DEVICE_CARRIER_IDX")
    model2idx = generate_lookup_dict(device_model_lookup, key_col="DEVICE_MODEL", value_col="DEVICE_MODEL_IDX")
    # print("Load platform lookup table from %s" % platform_lookup_path)
    # print("Load dma lookup table from %s" % dma_lookup_path)
    # print("Load device_carrier lookup table from %s" % device_carrier_lookup_path)
    # print("Load device_model lookup table from %s" % device_model_lookup_path)
    lookup_tables = {
        "idx2offerid": idx2offerid,
        "idx2offername": idx2offername,
        "offerid2idx": offerid2idx,
        "offername2idx": offername2idx,
        "platform2idx": platform2idx,
        "dma2idx": dma2idx,
        "carrier2idx": carrier2idx,
        "model2idx": model2idx,
    }

    # Load model
    model = torch.load(model_path, map_location=torch.device("cpu"))
    model.eval()
    # print("Load model from %s" % model_path)
    return offer_lookup_img, offer_lookup.set_index("OFFER_ID"), lookup_tables, model


def transform_raw_to_history(raw_history):
    """
    Transform user raw_history to processed recent history
    :param raw_history: list of user offer redeemed events
    :return: processed recent history of the user
    """
    # filtered_history = [v for v in raw_history if v.get("orderType") == "restaurant order"]
    sorted_history = sorted(raw_history, key=lambda v: v["timeStamp"])
    sorted_offer_id = list(map(lambda v: v["couponID"], sorted_history))
    len_history = len(sorted_offer_id)
    processed_history = {
        "platform": sorted_history[-1].get("platform", "n/a"),
        # "dma": "Miami-Ft. Lauderdale, FL",
        "device_carrier": sorted_history[-1].get("carrier", "n/a"),
        "device_model": sorted_history[-1].get("deviceModel", "n/a"),
        "offer_id": sorted_offer_id[max(0, len_history - 5):] + ["n/a"] * max(0, 5 - len_history),
    }
    return processed_history


def transform_history_to_model_in(history, offerid2idx, platform2idx, dma2idx, carrier2idx, model2idx):
    """
    Transform readable recent history to indexed model_input
    :param history: processed recent history of the user
    :param offerid2idx: dict of offer_id => idx
    :param platform2idx: dict of platform => idx
    :param dma2idx:
    :param carrier2idx:
    :param model2idx:
    :return:
    """
    # TODO: all in-coming str are lowercased
    offer_idx = [offerid2idx.get(offer_id, 0) for offer_id in history["offer_id"]]
    platform_idx = platform2idx.get(history["platform"], 1)  # web is 1
    # dma_idx = dma2idx.get(history["dma"], 0)
    device_carrier_idx = carrier2idx.get(history["device_carrier"], 0)
    device_model_idx = model2idx.get(history["device_model"], 0)

    context_in = [torch.tensor([[context]])
                  for context in [platform_idx, device_carrier_idx, device_model_idx]]  # TODO: no DMA for now
    sequence_in = torch.tensor([offer_idx])
    return context_in, sequence_in


def transform_model_out_to_offer_id(model_out, idx2offerid):
    sorted_idx = model_out.argsort(descending=True).flatten()
    sorted_offer_id = [idx2offerid.get(idx.item(), 0) for idx in sorted_idx]
    return [offer_id for offer_id in sorted_offer_id if offer_id != 0]


def is_lapsed(offer_lookup, offer_id):
    return offer_lookup.loc[offer_id]["LAPSED_90"] == "Y"


def is_structure_bundle(offer_lookup, offer_id):
    return offer_lookup.loc[offer_id]["OFFER_STRUCTURE"] == "Bundle"


def is_structure_sides(offer_lookup, offer_id):
    return offer_lookup.loc[offer_id]["OFFER_STRUCTURE"] == "Sides / Desserts"


def is_breakfast(offer_lookup, offer_id):
    return offer_lookup.loc[offer_id]["BREAKFAST"] == "Y"


def is_discount_low(offer_lookup, offer_id):
    return offer_lookup.loc[offer_id]["GPM_OFFER"] == "L"


def is_discount_medium(offer_lookup, offer_id):
    return offer_lookup.loc[offer_id]["GPM_OFFER"] == "M"


def is_discount_high(offer_lookup, offer_id):
    return offer_lookup.loc[offer_id]["GPM_OFFER"] == "H"


def get_offer_attributes(offer_lookup, offer_group_lookup, offer_id):
    offer_attributes = {
        "offer_group": offer_group_lookup[offer_id],
        "breakfast": None,
        "discount_level": None,
        "offer_structure": None,
    }
    # breakfast
    if is_breakfast(offer_lookup, offer_id):
        offer_attributes["breakfast"] = "br"
    else:
        offer_attributes["breakfast"] = "nbr"
    # discount_level
    if is_discount_high(offer_lookup, offer_id):
        offer_attributes["discount_level"] = "h"
    elif is_discount_medium(offer_lookup, offer_id):
        offer_attributes["discount_level"] = "m"
    else:
        offer_attributes["discount_level"] = "l"
    # offer_structure
    if is_structure_bundle(offer_lookup, offer_id):
        offer_attributes["offer_structure"] = "bundle"
    elif is_structure_sides(offer_lookup, offer_id):
        offer_attributes["offer_structure"] = "sides"
    else:
        offer_attributes["offer_structure"] = "other"
    return offer_attributes


def update_cluster_rules(topk_offer_attr, cluster_rules, offer_lookup,
                         offer_group_lookup, offer_id, use_cluster_rules=True):
    offer_attributes = get_offer_attributes(offer_lookup, offer_group_lookup, offer_id)
    group = offer_attributes["offer_group"]
    br_nbr = offer_attributes["breakfast"]
    h_m_l = offer_attributes["discount_level"]
    structure = offer_attributes["offer_structure"]
    topk_offer_attr = topk_offer_attr.copy()
    if use_cluster_rules:
        satisfy_rule = (topk_offer_attr[br_nbr] < cluster_rules[br_nbr]
                        and topk_offer_attr[h_m_l] < cluster_rules[h_m_l]
                        and (group == 0 or group not in topk_offer_attr["groups"]))
    else:
        satisfy_rule = (group == 0 or group not in topk_offer_attr["groups"])
    if satisfy_rule:
        topk_offer_attr[br_nbr] += 1
        topk_offer_attr[h_m_l] += 1
        topk_offer_attr[structure] += 1
        topk_offer_attr["groups"].append(group)
    return satisfy_rule, topk_offer_attr


def transform_offer_attr(offer_attr):
    offer_attr_log = "br-{},nbr-{},h-{},m-{},l-{}|bundle-{},sides-{},other-{}|groups-{}".format(
        offer_attr["br"],
        offer_attr["nbr"],
        offer_attr["h"],
        offer_attr["m"],
        offer_attr["l"],
        offer_attr["bundle"],
        offer_attr["sides"],
        offer_attr["other"],
        str(offer_attr["groups"])
    )
    return offer_attr_log


def filter_raw_by_rules(sorted_offer_id, lapsed, offer_lookup, topk, lapsed_rule, cluster_rules, offer_group_lookup):
    """
    Filter sorted model_out by rules generated by user cluster
    :param offer_group_lookup:
    :param sorted_offer_id: list of sorted offer_id, descending
    :param lapsed: int 0, 30, 60 or 90
    :param offer_lookup: offer_lookup table containing offer info
    :param topk: number of offers returned
    :param lapsed_rule: number of lapsed offer assigned to lapsed user
    :param cluster_rules: [(br, nbr), (H, M, L)]
    :return: list of sorted and filtered offer_id that satisfies all given rules
    """
    topk_offer_id = []
    topk_offer_attr = {
        "br": 0,
        "nbr": 0,
        "h": 0,
        "m": 0,
        "l": 0,
        "bundle": 0,
        "sides": 0,
        "other": 0,
        "groups": [],
    }
    # filter SENDABLE
    offer_id_sendable = offer_lookup[offer_lookup["SENDABLE"] == "Y"].index.values
    # TODO: add active filter
    offer_id_sendable_sorted = list(filter(lambda x: x in offer_id_sendable, sorted_offer_id))

    # filter LAPSED
    if lapsed == "90":
        lapsed_count = 0
        for offer_id in offer_id_sendable_sorted:
            if is_lapsed(offer_lookup, offer_id):
                satisfy_rule, topk_offer_attr = update_cluster_rules(topk_offer_attr,
                                                                     cluster_rules,
                                                                     offer_lookup,
                                                                     offer_group_lookup,
                                                                     offer_id,
                                                                     use_cluster_rules=True)
                if satisfy_rule:
                    # print(offer_id, "lapsed", topk_offer_attr)
                    topk_offer_id.append(offer_id)
                    lapsed_count += 1
                    if lapsed_count >= lapsed_rule:
                        break

    # filter base rules
    offer_id_sendable_sorted = list(filter(
        lambda x: (x not in topk_offer_id) and (not is_lapsed(offer_lookup, x)),
        offer_id_sendable_sorted
    ))
    if topk_offer_attr["bundle"] < 1:
        for offer_id in offer_id_sendable_sorted:
            if is_structure_bundle(offer_lookup, offer_id):
                satisfy_rule, topk_offer_attr = update_cluster_rules(topk_offer_attr,
                                                                     cluster_rules,
                                                                     offer_lookup,
                                                                     offer_group_lookup,
                                                                     offer_id,
                                                                     use_cluster_rules=True)
                if satisfy_rule:
                    # print(offer_id, "bundle", topk_offer_attr)
                    topk_offer_id.append(offer_id)
                    break
    offer_id_sendable_sorted = list(filter(lambda x: x not in topk_offer_id, offer_id_sendable_sorted))
    if topk_offer_attr["sides"] < 1:
        for offer_id in offer_id_sendable_sorted:
            if is_structure_sides(offer_lookup, offer_id):
                satisfy_rule, topk_offer_attr = update_cluster_rules(topk_offer_attr,
                                                                     cluster_rules,
                                                                     offer_lookup,
                                                                     offer_group_lookup,
                                                                     offer_id,
                                                                     use_cluster_rules=True)
                if satisfy_rule:
                    # print(offer_id, "sides", topk_offer_attr)
                    topk_offer_id.append(offer_id)
                    break

    # filter cluster rules
    offer_id_sendable_sorted = list(filter(lambda x: x not in topk_offer_id, offer_id_sendable_sorted))
    for offer_id in offer_id_sendable_sorted:
        satisfy_rule, topk_offer_attr = update_cluster_rules(topk_offer_attr,
                                                             cluster_rules,
                                                             offer_lookup,
                                                             offer_group_lookup,
                                                             offer_id,
                                                             use_cluster_rules=True)
        if satisfy_rule:
            # print(offer_id, "cluster", topk_offer_attr)
            topk_offer_id.append(offer_id)
            if len(topk_offer_id) >= topk:
                break

    # fill rest of the array
    if len(topk_offer_id) < topk:
        offer_id_sendable_sorted = list(filter(lambda x: x not in topk_offer_id, offer_id_sendable_sorted))
        for offer_id in offer_id_sendable_sorted:
            satisfy_rule, topk_offer_attr = update_cluster_rules(topk_offer_attr,
                                                                 cluster_rules,
                                                                 offer_lookup,
                                                                 offer_group_lookup,
                                                                 offer_id,
                                                                 use_cluster_rules=False)
            if satisfy_rule:
                # print(offer_id, "cluster", topk_offer_attr)
                topk_offer_id.append(offer_id)
                if len(topk_offer_id) >= topk:
                    break

    return topk_offer_id, transform_offer_attr(topk_offer_attr)


def filter_by_offer_groups(available_offers, selected_offers, offer_group_lookup):
    selected_offers_groups = [offer_group_lookup[offer_id] for offer_id in selected_offers]
    filtered_available_offers = [
        offer_id for offer_id in available_offers
        if offer_group_lookup[offer_id] == 0 or offer_group_lookup[offer_id] not in selected_offers_groups
    ]
    return filtered_available_offers


def get_delivery_offer(delivery_offers, selected_offers, offer_group_lookup):
    filtered_available_offers = filter_by_offer_groups(available_offers=delivery_offers,
                                                       selected_offers=selected_offers,
                                                       offer_group_lookup=offer_group_lookup)
    personalized_delivery_offers = [random.choice(filtered_available_offers)]
    personalized_delivery_offer_attr = {
        "groups": [offer_group_lookup[offer] for offer in personalized_delivery_offers]
    }
    return personalized_delivery_offers, str(personalized_delivery_offer_attr)
