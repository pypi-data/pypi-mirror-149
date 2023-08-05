import os
import pandas as pd
import numpy as np
import mxnet as mx
from mxnet import nd, autograd, gluon
import boto3


# Helper Functions - Models

# Should be changed along with utils_offer_encoder.load_offer_id_from_pool
def load_offer_id_from_pool(offer_pool_path, active_offer_pool=None):
    offer_pool = pd.read_csv(offer_pool_path, dtype="str").dropna(subset=["Sanity ID"])
    offer_pool = offer_pool[~offer_pool["Sanity ID"].isin(["TBR", "TBD", "0", "5"])]
    offer_pool = offer_pool[~offer_pool["Sanity ID"].str.lower().str.contains("requested")]
    print("Offer Pool without TBD and NA: %d" % len(offer_pool))

    # offer pools
    weekly_offer_pool = offer_pool[
        # (offer_pool["Active/Inactive"] == "Active") &
        (offer_pool["Status"].isin(["Active", "Y"])) &
        # (offer_pool["Delivery/MO&P"] == "MO&P") &  # column removed
        # (offer_pool["National Offer Overlap?"] == "No") &  # column removed
        (offer_pool["Offer Type"].isin(["1_Personalized", "2_Personalized", "Lapsed_60", "Lapsed_90", "Default"]))
        # (offer_pool["L3"].isin(["Lapsed", "Segmented"])) &
        # (offer_pool["L4"].isin(["Default", "Personalized"]))
        ]["Sanity ID"].tolist()
    weekly_default_pool = offer_pool[
        # (offer_pool["Active/Inactive"] == "Active") &
        (offer_pool["Status"].isin(["Active", "Y"])) &
        # (offer_pool["Delivery/MO&P"] == "MO&P") &
        # (offer_pool["National Offer Overlap?"] == "No") &
        (offer_pool["Offer Type"] == "Default")
        # (offer_pool["L3"].isin(["Lapsed", "Segmented"])) &
        # (offer_pool["L4"].isin(["Default"]))
        ]["Sanity ID"].tolist()
    daily_offer_pool = offer_pool[
        # (offer_pool["Active/Inactive"] == "Active") &
        (offer_pool["Status"].isin(["Active", "Y"])) &
        # (offer_pool["Delivery/MO&P"] == "MO&P") &
        # (offer_pool["National Offer Overlap?"] == "No") &
        (offer_pool["Offer Type"] == "Daily")
        # (offer_pool["L3"] == "Daily Deals") &
        # (offer_pool["L4"].isin(["Default", "Personalized"]))
        ]["Sanity ID"].tolist()
    delivery_offer_pool = offer_pool[
        # (offer_pool["Active/Inactive"] == "Active") &
        (offer_pool["Status"].isin(["Active", "Y"])) &
        # (offer_pool["Delivery/MO&P"] == "Delivery") &
        (offer_pool["Offer Type"] == "Delivery")
        # (offer_pool["L3"].isin(["Lapsed", "Segmented", "Daily Deals"])) &
        # (offer_pool["L4"].isin(["Default", "Personalized"]))
        ]["Sanity ID"].tolist()
    if active_offer_pool:
        weekly_offer_pool = [offer_id for offer_id in weekly_offer_pool if offer_id in active_offer_pool]
        weekly_default_pool = [offer_id for offer_id in weekly_default_pool if offer_id in active_offer_pool]
        daily_offer_pool = [offer_id for offer_id in daily_offer_pool if offer_id in active_offer_pool]
        delivery_offer_pool = [offer_id for offer_id in delivery_offer_pool if offer_id in active_offer_pool]
    inactive_pool = offer_pool[
        offer_pool["Sanity ID"].isin([i for i in offer_pool["Sanity ID"].values
                                      if i not in weekly_offer_pool + daily_offer_pool + delivery_offer_pool])
    ]
    print("active weekly MO&P: %d" % len(weekly_offer_pool))
    print("active weekly MO&P default: %d" % len(weekly_default_pool))
    print("active daily MO&P: %d" % len(daily_offer_pool))
    print("active weekly Delivery: %d" % len(delivery_offer_pool))
    offer_pools = {
        "weekly": weekly_offer_pool,
        "default": weekly_default_pool,
        "daily": daily_offer_pool,
        "delivery": delivery_offer_pool,
        "inactive": inactive_pool,
    }

    # offer attributes
    offer_attributes = offer_pool[
        ["Sanity ID", "Coupon Name", "Offer Type", "Offer Structure", "Product Category", "Group Name",
         "Discount Level", "Personalized Offer Group"]
    ].set_index(keys="Sanity ID").fillna("NA").to_dict(orient="index")

    return offer_pools, offer_attributes


def generate_lookup_dict(df, key_col, value_col):
    """Generate int2int lookup dict from given dataframe."""
    return df[[key_col, value_col]].set_index(key_col).to_dict()[value_col]


def transform_raw_to_history(history_raw):
    """
    Transform user raw_history to processed recent history
    :param history_raw: list of user offer redeemed events
    :return: processed recent history of the user
    """
    # filtered_history = [v for v in raw_history if v.get("orderType") == "restaurant order"]
    sorted_history = sorted(history_raw, key=lambda v: v.get("timeStamp", "0000-00-00T00:00:00"))
    sorted_offer_id = list(map(lambda v: v.get("couponID", "n/a"), sorted_history))
    len_history = len(sorted_offer_id)
    if len(sorted_history) == 0:
        sorted_history.append({})
    history_processed = {
        "platform": sorted_history[-1].get("platform", "n/a"),
        "dma": sorted_history[-1].get("dma", "n/a"),
        "device_carrier": sorted_history[-1].get("carrier", "n/a"),
        "device_model": sorted_history[-1].get("deviceModel", "n/a"),
        "offer_id": sorted_offer_id[max(0, len_history - 5):] + ["n/a"] * max(0, 5 - len_history),
    }
    return history_processed


def transform_history_to_mxnet_in(history, offerid2idx, platform2idx, dma2idx, carrier2idx, model2idx):
    offer_idx = [offerid2idx.get(offer_id, 0) for offer_id in history["offer_id"]]
    platform_idx = platform2idx.get(history["platform"], 0)  # web is 1
    dma_idx = dma2idx.get(history["dma"], 0)
    device_carrier_idx = carrier2idx.get(history["device_carrier"], 0)
    device_model_idx = model2idx.get(history["device_model"], 0)
    valid_len = max(list(np.nonzero(offer_idx)[0]) + [-1]) + 1

    model_input = mx.io.NDArrayIter(data={'data0': np.asarray([offer_idx]),
                                          'data1': np.asarray([int(valid_len)]),
                                          'data2': np.asarray([int(device_carrier_idx)]),
                                          'data3': np.asarray([int(device_model_idx)]),
                                          'data4': np.asarray([int(dma_idx)]),
                                          'data5': np.asarray([int(platform_idx)])},
                                    batch_size=1)
    return model_input


def transform_mxnet_out_to_offer(model_out, idx2offer):
    topk_idx = model_out.argsort().flatten()[::-1]
    topk_offer = [idx2offer.get(idx, 0) for idx in topk_idx if idx != 0]
    return topk_offer


# Helper Functions - Recommend Rules

def is_offer_type_in(offer_attr_lookup, offer_id, offer_type_list):
    return offer_attr_lookup.get(offer_id, {}).get("Offer Type") in offer_type_list


def is_lapsed(offer_attr_lookup, offer_id):
    return offer_attr_lookup.get(offer_id, {}).get("Offer Type") in ["Lapsed_60", "Lapsed_90"]


def is_offer_type_group_breakfast(offer_attr_lookup, offer_id):
    return offer_attr_lookup.get(offer_id, {}).get("Group Name") == "Breakfast"


def is_offer_type_group_family(offer_attr_lookup, offer_id):
    return offer_attr_lookup.get(offer_id, {}).get("Group Name") == "Family"


def is_offer_type_group_single_serve(offer_attr_lookup, offer_id):
    return offer_attr_lookup.get(offer_id, {}).get("Group Name") == "Single Serve"


def is_offer_type_group_for2(offer_attr_lookup, offer_id):
    return offer_attr_lookup.get(offer_id, {}).get("Group Name") == "For 2"


def is_offer_type_group_snack(offer_attr_lookup, offer_id):
    return offer_attr_lookup.get(offer_id, {}).get("Group Name") == "Snack"


def is_structure_bundle(offer_attr_lookup, offer_id):
    return offer_attr_lookup.get(offer_id, {}).get("Offer Structure") == "Bundle"


def is_structure_sides(offer_attr_lookup, offer_id):
    return offer_attr_lookup.get(offer_id, {}).get("Offer Structure") == "Side/Dessert"


def is_breakfast(offer_attr_lookup, offer_id):
    return offer_attr_lookup.get(offer_id, {}).get("Product Category") == "Breakfast"


def is_discount_low(offer_attr_lookup, offer_id):
    return offer_attr_lookup.get(offer_id, {}).get("Discount Level") == "Low"


def is_discount_med(offer_attr_lookup, offer_id):
    return offer_attr_lookup.get(offer_id, {}).get("Discount Level") == "Med"


def is_discount_high(offer_attr_lookup, offer_id):
    return offer_attr_lookup.get(offer_id, {}).get("Discount Level") == "High"


def is_discount_na(offer_attr_lookup, offer_id):
    return offer_attr_lookup.get(offer_id, {}).get("Discount Level") == "NA"


def get_offer_group(offer_attr_lookup, offer_id):
    return offer_attr_lookup.get(offer_id, {}).get("Personalized Offer Group", "0")


def get_offer_type(offer_attr_lookup, offer_id):
    return offer_attr_lookup.get(offer_id, {}).get("Offer Type")


def get_offer_attributes(offer_attr_lookup, offer_id):
    offer_attributes = {
        "offer_group": get_offer_group(offer_attr_lookup, offer_id),
        # "breakfast": None,
        # "discount_level": None,
        # "offer_structure": None,
        "offer_type_group": None,
        "offer_type": get_offer_type(offer_attr_lookup, offer_id)
    }
    # offer_structure
    if is_offer_type_group_breakfast(offer_attr_lookup, offer_id):
        offer_attributes["offer_type_group"] = "br"
    elif is_offer_type_group_family(offer_attr_lookup, offer_id):
        offer_attributes["offer_type_group"] = "family"
    elif is_offer_type_group_single_serve(offer_attr_lookup, offer_id):
        offer_attributes["offer_type_group"] = "1serve"
    elif is_offer_type_group_for2(offer_attr_lookup, offer_id):
        offer_attributes["offer_type_group"] = "for2"
    elif is_offer_type_group_snack(offer_attr_lookup, offer_id):
        offer_attributes["offer_type_group"] = "snack"
    else:
        offer_attributes["offer_type_group"] = "other"
    # # breakfast
    # if is_breakfast(offer_attr_lookup, offer_id):
    #     offer_attributes["breakfast"] = "br"
    # else:
    #     offer_attributes["breakfast"] = "nbr"
    # # discount_level
    # if is_discount_high(offer_attr_lookup, offer_id):
    #     offer_attributes["discount_level"] = "h"
    # elif is_discount_med(offer_attr_lookup, offer_id):
    #     offer_attributes["discount_level"] = "m"
    # elif is_discount_low(offer_attr_lookup, offer_id):
    #     offer_attributes["discount_level"] = "l"
    # else:
    #     offer_attributes["discount_level"] = "na"
    # # offer_structure
    # if is_structure_bundle(offer_attr_lookup, offer_id):
    #     offer_attributes["offer_structure"] = "bundle"
    # elif is_structure_sides(offer_attr_lookup, offer_id):
    #     offer_attributes["offer_structure"] = "sides"
    # else:
    #     offer_attributes["offer_structure"] = "other"
    return offer_attributes


def update_cluster_rules(topk_offer_attr, cluster_rules, offer_attr_lookup, offer_id, use_cluster_rules=True):
    offer_attributes = get_offer_attributes(offer_attr_lookup, offer_id)
    group = offer_attributes["offer_group"]
    # br_nbr = offer_attributes["breakfast"]
    # h_m_l = offer_attributes["discount_level"]
    # structure = offer_attributes["offer_structure"]
    type_group = offer_attributes["offer_type_group"]
    offer_type = offer_attributes["offer_type"]
    topk_offer_attr = topk_offer_attr.copy()
    if use_cluster_rules:
        # satisfy_rule = (topk_offer_attr.get(br_nbr, 0) < cluster_rules.get(br_nbr, 999)
        #                 and topk_offer_attr.get(h_m_l, 0) < cluster_rules.get(h_m_l, -1)
        #                 and (group == "0" or group not in topk_offer_attr["groups"]))
        satisfy_rule = (
                (topk_offer_attr.get(type_group, 0) < cluster_rules.get(type_group, 999))
                and (group == "0" or group not in topk_offer_attr["groups"])
        )
    else:
        satisfy_rule = (group == "0" or group not in topk_offer_attr["groups"])
    if satisfy_rule:
        # topk_offer_attr[br_nbr] += 1
        # topk_offer_attr[h_m_l] += 1
        # topk_offer_attr[structure] += 1
        topk_offer_attr[type_group] += 1
        topk_offer_attr["groups"].append(group)
        topk_offer_attr[offer_type] += 1
    return satisfy_rule, topk_offer_attr


def transform_offer_attr(offer_attr):
    offer_attr_log = (
            "br-{},family-{},for2-{},1serve-{},snack-{},other-{}|".format(offer_attr["br"], offer_attr["family"],
                                                                          offer_attr["for2"], offer_attr["1serve"],
                                                                          offer_attr["snack"], offer_attr["other"])
            + "P1-{},P2-{},L60-{},L90-{}|".format(offer_attr["1_Personalized"], offer_attr["2_Personalized"],
                                                  offer_attr["Lapsed_60"], offer_attr["Lapsed_90"])
            + "groups-{}".format(str(offer_attr["groups"]))
    )
    # offer_attr_log = (
    #     "br-{},nbr-{}|".format(offer_attr["br"], offer_attr["nbr"])
    #     + "h-{},m-{},l-{},na-{}|".format(offer_attr["h"], offer_attr["m"], offer_attr["l"], offer_attr["na"])
    #     + "bundle-{},sides-{},other-{}|".format(offer_attr["bundle"], offer_attr["sides"], offer_attr["other"])
    #     + "P1-{},P2-{},L60-{},L90-{}|".format(offer_attr["1_Personalized"], offer_attr["2_Personalized"],
    #                                           offer_attr["Lapsed_60"], offer_attr["Lapsed_90"])
    #     + "groups-{}".format(str(offer_attr["groups"]))
    # )
    return offer_attr_log


# Main functions

def load_model(model_dir, model_name, model_prefix, model_epoch, context_lookup_names, sequence_lookup_name):
    # lookup tables
    model_path = os.path.join(model_dir, model_name, model_prefix)
    lookup_paths = {
        k: os.path.join(model_dir, model_name, k + "_lookup.csv") for k in context_lookup_names + [sequence_lookup_name]
    }
    lookup_tables = {
        k: pd.read_csv(lookup_paths[k]) for k in context_lookup_names + [sequence_lookup_name]
    }
    context_to_idx = {
        k: generate_lookup_dict(lookup_tables[k], key_col=k, value_col=k + "_idx") for k in context_lookup_names
    }
    sequence_to_idx = generate_lookup_dict(df=lookup_tables[sequence_lookup_name],
                                           key_col=sequence_lookup_name + "_id",
                                           value_col=sequence_lookup_name + "_idx")
    idx_to_sequence = generate_lookup_dict(df=lookup_tables[sequence_lookup_name],
                                           key_col=sequence_lookup_name + "_idx",
                                           value_col=sequence_lookup_name + "_id")

    # model
    model = mx.model.FeedForward.load(prefix=model_path, epoch=model_epoch, ctx=mx.cpu())
    return model, (context_to_idx, sequence_to_idx, idx_to_sequence),


def load_offer_metadata(offer_pool_path, s3_id_mapping_bucket, s3_id_mapping_prefix, s3_rest_tz_bucket,
                        s3_rest_tz_prefix, access_key, secret_key):
    # id_mapping
    keys = []
    id_mapping_dfs = []
    s3 = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)
    list_obj = s3.list_objects_v2(Bucket=s3_id_mapping_bucket, Prefix=s3_id_mapping_prefix)
    assert list_obj["KeyCount"] < 1000
    for content in list_obj["Contents"]:
        if content["Key"].endswith(".csv"):
            keys.append(content["Key"])
    assert len(keys) == 1
    print("Load %d csv files from %s" % (len(keys), os.path.dirname(keys[0])))
    for i, key in enumerate(keys):
        obj = s3.get_object(Bucket=s3_id_mapping_bucket, Key=key)
        id_mapping_dfs.append(pd.read_csv(obj["Body"], dtype="str"))
    offer_id_mapping_df = pd.concat(id_mapping_dfs)
    active_offer_pool = offer_id_mapping_df[offer_id_mapping_df["activeOffer"] == "Y"]["id"].tolist()
    offer_id_mapping = offer_id_mapping_df[
        ["id", "name", "localizedImageUrl"]].fillna("n/a").set_index(keys="id").to_dict(orient="index")

    # offer pool and offer attributes
    offer_pools, offer_attributes = load_offer_id_from_pool(offer_pool_path, active_offer_pool)

    # rest_tz
    keys = []
    rest_tz_dfs = []
    s3 = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)
    list_obj = s3.list_objects_v2(Bucket=s3_rest_tz_bucket, Prefix=s3_rest_tz_prefix)
    assert list_obj["KeyCount"] < 1000
    for content in list_obj["Contents"]:
        if content["Key"].endswith(".csv"):
            keys.append(content["Key"])
    assert len(keys) == 1
    print("Load %d csv files from %s" % (len(keys), os.path.dirname(keys[0])))
    for i, key in enumerate(keys):
        obj = s3.get_object(Bucket=s3_rest_tz_bucket, Key=key)
        rest_tz_dfs.append(pd.read_csv(obj["Body"], dtype="str"))
    rest_tz_df = pd.concat(rest_tz_dfs)

    return (offer_pools, offer_attributes), (active_offer_pool, offer_id_mapping), rest_tz_df


def mxnet_predict(model, history_raw, offer2idx, idx2offer, carrier2idx, dma2idx, model2idx, platform2idx):
    """
    API post -> raw -> idx_in -> model -> idx_out -> raw -> API
    """
    history_processed = transform_raw_to_history(history_raw=history_raw)
    model_in = transform_history_to_mxnet_in(history=history_processed,
                                             offerid2idx=offer2idx,
                                             platform2idx=platform2idx,
                                             dma2idx=dma2idx,
                                             carrier2idx=carrier2idx,
                                             model2idx=model2idx)
    model_out = model.predict(model_in)
    recommended_offer_id = transform_mxnet_out_to_offer(model_out=model_out, idx2offer=idx2offer)

    return recommended_offer_id


def filter_raw_by_rules(offer_attr_lookup, weekly_pool, sorted_offer_id, national_adhoc_offers, price_tier, lapsed,
                        topk, lapsed_rule, cluster_rules, price_tier_mapper, top_performance_offers):
    """
    Filter sorted model_out by rules generated by user cluster
    :param offer_attr_lookup: offer_attr_lookup table containing offer info
    :param weekly_pool: list of weekly SENDABLE offer_id
    :param sorted_offer_id: list of sorted offer_id, descending
    :param national_adhoc_offers: list of national offer_id that has already been assigned
    :param price_tier: str "1_Personalized" (high) or "2_Personalized" (low)
    :param lapsed: str "0", "30", "60" or "90"
    :param topk: number of offers returned
    :param lapsed_rule: number of lapsed offer assigned to lapsed user
    :param cluster_rules:
    :param price_tier_mapper: {"1to2": {oid1: oid2}, "2to1": {oid2: oid1}}
    :param top_performance_offers:
    :return: list of sorted and filtered offer_id that satisfies all given rules
    """
    topk_offer_id = []
    topk_offer_attr = {
        # "br": 0,
        # "nbr": 0,
        # "h": 0,
        # "m": 0,
        # "l": 0,
        # "na": 0,
        # "bundle": 0,
        # "sides": 0,
        "br": 0,
        "family": 0,
        "1serve": 0,
        "for2": 0,
        "snack": 0,
        "other": 0,
        "1_Personalized": 0,
        "2_Personalized": 0,
        "Lapsed_60": 0,
        "Lapsed_90": 0,
        "groups": [],
    }

    # TODO: remove this in future
    if price_tier == "1_Personalized":
        # manually select personalized offers from top performance offers - 4 out of 5
        manual_assigned = [
            top_performance_offers["tier1"]["br"][0],
            top_performance_offers["tier1"]["family"][0],
            top_performance_offers["tier1"]["for2"][0],
            top_performance_offers["tier1"]["1serve"][0],
        ]
        topk_offer_id += manual_assigned
        # TODO: update using update_cluster_rule
        # update topk_offer_attr
        topk_offer_attr["br"] = 1
        topk_offer_attr["family"] = 1
        topk_offer_attr["for2"] = 1
        topk_offer_attr["1serve"] = 1
        topk_offer_attr["1_Personalized"] = 4
    else:
        # manually select personalized offers from top performance offers - 4 out of 5
        manual_assigned = [
            top_performance_offers["tier2"]["family"][0],
            top_performance_offers["tier2"]["for2"][0],
            top_performance_offers["tier2"]["1serve"][0],
            top_performance_offers["tier2"]["1serve"][1],
        ]
        topk_offer_id += manual_assigned
        # TODO: update using update_cluster_rule
        # update topk_offer_attr
        topk_offer_attr["family"] = 1
        topk_offer_attr["for2"] = 1
        topk_offer_attr["1serve"] = 2
        topk_offer_attr["2_Personalized"] = 4
    mandatory_offers_actual = national_adhoc_offers.copy() + topk_offer_id.copy()
    mandatory_offer_groups = [
        get_offer_group(offer_attr_lookup, oid)
        for oid in mandatory_offers_actual
    ]
    topk_offer_attr["groups"] = mandatory_offer_groups

    # filter SENDABLE
    if lapsed == "90":
        offer_type_list = [price_tier, "Lapsed_90", "Lapsed_60"]
    elif lapsed == "60":
        offer_type_list = [price_tier, "Lapsed_60"]
    else:
        offer_type_list = [price_tier]
    # TODO: add adhoc: let tier1 offers flow to tier2 users - DONE
    if price_tier == "2_Personalized":
        offer_type_list.append("1_Personalized")
    ####
    if price_tier == "1_Personalized":
        price_tier_mapping = price_tier_mapper["2to1"]
    elif price_tier == "2_Personalized":
        price_tier_mapping = price_tier_mapper["1to2"]
    else:
        price_tier_mapping = price_tier_mapper["1to2"]
    offer_id_sendable_sorted = [
        price_tier_mapping.get(oid, oid)
        for oid in sorted_offer_id
    ]
    offer_id_sendable_sorted = [
        oid
        for oid in offer_id_sendable_sorted
        if oid in weekly_pool
        and oid not in mandatory_offers_actual
        and oid not in topk_offer_id
        and is_offer_type_in(offer_attr_lookup, oid, offer_type_list)
    ]

    # filter LAPSED
    if str(lapsed) == "90":
        lapsed_count = 0
        for offer_id in offer_id_sendable_sorted:
            if is_offer_type_in(offer_attr_lookup, offer_id, ["Lapsed_90", "Lapsed_60"]):
                satisfy_rule, topk_offer_attr = update_cluster_rules(topk_offer_attr=topk_offer_attr,
                                                                     cluster_rules=cluster_rules,
                                                                     offer_attr_lookup=offer_attr_lookup,
                                                                     offer_id=offer_id,
                                                                     use_cluster_rules=True)
                if satisfy_rule:
                    # print(offer_id, "lapsed", topk_offer_attr)
                    topk_offer_id.append(offer_id)
                    lapsed_count += 1
                    if lapsed_count >= lapsed_rule or len(topk_offer_id) >= topk:
                        break
    elif str(lapsed) == "60":
        lapsed_count = 0
        for offer_id in offer_id_sendable_sorted:
            if is_offer_type_in(offer_attr_lookup, offer_id, ["Lapsed_60"]):
                satisfy_rule, topk_offer_attr = update_cluster_rules(topk_offer_attr=topk_offer_attr,
                                                                     cluster_rules=cluster_rules,
                                                                     offer_attr_lookup=offer_attr_lookup,
                                                                     offer_id=offer_id,
                                                                     use_cluster_rules=True)
                if satisfy_rule:
                    # print(offer_id, "lapsed", topk_offer_attr)
                    topk_offer_id.append(offer_id)
                    lapsed_count += 1
                    if lapsed_count >= lapsed_rule or len(topk_offer_id) >= topk:
                        break

    # # filter base rules: 1 bundle and 1 sides
    # offer_id_sendable_sorted = list(filter(
    #     lambda x: (x not in topk_offer_id) and (not is_lapsed(offer_attr_lookup, x)),
    #     offer_id_sendable_sorted
    # ))
    # if len(topk_offer_id) < topk and topk_offer_attr["bundle"] < 1:
    #     for offer_id in offer_id_sendable_sorted:
    #         if is_structure_bundle(offer_attr_lookup, offer_id):
    #             satisfy_rule, topk_offer_attr = update_cluster_rules(topk_offer_attr=topk_offer_attr,
    #                                                                  cluster_rules=cluster_rules,
    #                                                                  offer_attr_lookup=offer_attr_lookup,
    #                                                                  offer_id=offer_id,
    #                                                                  use_cluster_rules=True)
    #             if satisfy_rule:
    #                 # print(offer_id, "bundle", topk_offer_attr)
    #                 topk_offer_id.append(offer_id)
    #                 break
    # offer_id_sendable_sorted = list(filter(lambda x: x not in topk_offer_id, offer_id_sendable_sorted))
    # if len(topk_offer_id) < topk and topk_offer_attr["sides"] < 1:
    #     for offer_id in offer_id_sendable_sorted:
    #         if is_structure_sides(offer_attr_lookup, offer_id):
    #             satisfy_rule, topk_offer_attr = update_cluster_rules(topk_offer_attr=topk_offer_attr,
    #                                                                  cluster_rules=cluster_rules,
    #                                                                  offer_attr_lookup=offer_attr_lookup,
    #                                                                  offer_id=offer_id,
    #                                                                  use_cluster_rules=True)
    #             if satisfy_rule:
    #                 # print(offer_id, "sides", topk_offer_attr)
    #                 topk_offer_id.append(offer_id)
    #                 break

    # filter cluster rules
    offer_id_sendable_sorted = list(filter(lambda x: x not in topk_offer_id, offer_id_sendable_sorted))
    if len(topk_offer_id) < topk:
        for offer_id in offer_id_sendable_sorted:
            if is_offer_type_in(offer_attr_lookup, offer_id, [price_tier]):
                satisfy_rule, topk_offer_attr = update_cluster_rules(topk_offer_attr=topk_offer_attr,
                                                                     cluster_rules=cluster_rules,
                                                                     offer_attr_lookup=offer_attr_lookup,
                                                                     offer_id=offer_id,
                                                                     use_cluster_rules=True)
                if satisfy_rule:
                    # print(offer_id, "cluster", topk_offer_attr)
                    topk_offer_id.append(offer_id)
                    if len(topk_offer_id) >= topk:
                        break

    # fill rest of the array
    if len(topk_offer_id) < topk:
        # print("drop cluster rules")
        offer_id_sendable_sorted = list(filter(lambda x: x not in topk_offer_id, offer_id_sendable_sorted))
        for offer_id in offer_id_sendable_sorted:
            if is_offer_type_in(offer_attr_lookup, offer_id, [price_tier]):
                satisfy_rule, topk_offer_attr = update_cluster_rules(topk_offer_attr=topk_offer_attr,
                                                                     cluster_rules=cluster_rules,
                                                                     offer_attr_lookup=offer_attr_lookup,
                                                                     offer_id=offer_id,
                                                                     use_cluster_rules=False)
                if satisfy_rule:
                    # print(offer_id, "cluster", topk_offer_attr)
                    topk_offer_id.append(offer_id)
                    if len(topk_offer_id) >= topk:
                        break

    return topk_offer_id, transform_offer_attr(topk_offer_attr)


def filter_randomized(offer_attr_lookup, sorted_offer_id, national_adhoc_offers, price_tier, lapsed, lapsed_rule, topk):
    topk_offer_id = []
    topk_offer_attr = {
        "br": 0,
        "family": 0,
        "1serve": 0,
        "for2": 0,
        "snack": 0,
        "other": 0,
        "1_Personalized": 0,
        "2_Personalized": 0,
        "Lapsed_60": 0,
        "Lapsed_90": 0,
        "groups": [],
    }
    national_adhoc_offers_groups = [
        get_offer_group(offer_attr_lookup, oid)
        for oid in national_adhoc_offers
    ]
    topk_offer_attr["groups"] = national_adhoc_offers_groups

    # filter SENDABLE
    if lapsed == "90" or lapsed == "60":
        offer_type_list = [price_tier, "Lapsed_90", "Lapsed_60"]
    elif lapsed == "60":
        offer_type_list = [price_tier, "Lapsed_60"]
    else:
        offer_type_list = [price_tier]
    offer_id_sendable = [
        oid
        for oid in sorted_offer_id
        if oid not in national_adhoc_offers
        and is_offer_type_in(offer_attr_lookup, oid, offer_type_list)
    ]

    if str(lapsed) == "90":
        lapsed_count = 0
        for offer_id in offer_id_sendable:
            if is_offer_type_in(offer_attr_lookup, offer_id, ["Lapsed_90", "Lapsed_60"]):
                satisfy_rule, topk_offer_attr = update_cluster_rules(topk_offer_attr=topk_offer_attr,
                                                                     cluster_rules={},
                                                                     offer_attr_lookup=offer_attr_lookup,
                                                                     offer_id=offer_id,
                                                                     use_cluster_rules=False)
                if satisfy_rule:
                    # print(offer_id, "lapsed", topk_offer_attr)
                    topk_offer_id.append(offer_id)
                    lapsed_count += 1
                    if lapsed_count >= lapsed_rule or len(topk_offer_id) >= topk:
                        break
    elif str(lapsed) == "60":
        lapsed_count = 0
        for offer_id in offer_id_sendable:
            if is_offer_type_in(offer_attr_lookup, offer_id, ["Lapsed_60"]):
                satisfy_rule, topk_offer_attr = update_cluster_rules(topk_offer_attr=topk_offer_attr,
                                                                     cluster_rules={},
                                                                     offer_attr_lookup=offer_attr_lookup,
                                                                     offer_id=offer_id,
                                                                     use_cluster_rules=False)
                if satisfy_rule:
                    # print(offer_id, "lapsed", topk_offer_attr)
                    topk_offer_id.append(offer_id)
                    lapsed_count += 1
                    if lapsed_count >= lapsed_rule or len(topk_offer_id) >= topk:
                        break

    # fill rest of the array
    if len(topk_offer_id) < topk:
        for offer_id in offer_id_sendable:
            if is_offer_type_in(offer_attr_lookup, offer_id, [price_tier]):
                satisfy_rule, topk_offer_attr = update_cluster_rules(topk_offer_attr=topk_offer_attr,
                                                                     cluster_rules={},
                                                                     offer_attr_lookup=offer_attr_lookup,
                                                                     offer_id=offer_id,
                                                                     use_cluster_rules=False)
                if satisfy_rule:
                    # print(offer_id, "cluster", topk_offer_attr)
                    topk_offer_id.append(offer_id)
                    if len(topk_offer_id) >= topk:
                        break

    return topk_offer_id, transform_offer_attr(topk_offer_attr)


def get_dma(store_ids, user_location, dim_rest):
    """
    :param store_ids: list of store_id strings
    :param user_location: user location parsed from dynamodb
    :param dim_rest: pandas dataframe of rest_tz_bk_full
    :return: string of the most frequent dma
    """
    tier_1_dma = [
        {'name': 'AK', 'tlog': 29, 'geoip': 745},
        {'name': 'HI', 'tlog': 340, 'geoip': 744},
        {'name': 'Chico-Redding', 'tlog': 148, 'geoip': 868},
        {'name': 'Fresno-Visalia', 'tlog': 284, 'geoip': 866},
        {'name': 'Hartford-New Haven', 'tlog': 332, 'geoip': 533},
        {'name': 'Las Vegaas', 'tlog': 420, 'geoip': 839},
        {'name': 'Long Island', 'tlog': 531, 'geoip': 501},
        {'name': 'Los Angeles', 'tlog': 444, 'geoip': 803},
        {'name': 'Medford-Klamath Falls', 'tlog': 476, 'geoip': 813},
        {'name': 'New Jersey - Sub', 'tlog': 530, 'geoip': 501},
        {'name': 'NYC Sub', 'tlog': 529, 'geoip': 501},
        {'name': 'Phoenix', 'tlog': 584, 'geoip': 753},
        {'name': 'San Diego', 'tlog': 684, 'geoip': 825},
        {'name': 'San Francisco-Oak-San Jose', 'tlog': 688, 'geoip': 807},
        {'name': 'Santa Barbara', 'tlog': 696, 'geoip': 855},
        {'name': 'Springfield-Holyoke', 'tlog': 728, 'geoip': 543},
        {'name': 'Tucson-Nogales', 'tlog': 772, 'geoip': 789},
        {'name': 'Providence-New Beford', 'tlog': 608, 'geoip': 521},
        {'name': 'Palm Springs', 'tlog': 564, 'geoip': 804},
        {'name': 'Boston', 'tlog': 96, 'geoip': 807},
    ]
    lookup = dict(zip(dim_rest.rest_no.map(str), dim_rest.dma_no))
    dma_nos = [lookup.get(_) for _ in store_ids if _ in lookup]
    if dma_nos:
        user_dma = max(set(dma_nos), key=dma_nos.count)
        user_tier = "1" if user_dma in [str(dma.get("tlog")) for dma in tier_1_dma] else "2"
        is_phoenix = True if user_dma in ["584", "772"] else False
    elif user_location:
        user_dma = str(user_location.get('dmaCode'))
        user_tier = "1" if user_dma in [str(dma.get("geoip")) for dma in tier_1_dma] else "2"
        is_phoenix = True if user_dma in ["753", "789"] else False
    else:
        # user_dma = "n/a"
        user_tier = "2"
        is_phoenix = False
    return user_tier, is_phoenix
