import os
import logging
import warnings
import numpy as np
import pandas as pd
import mxnet as mx
from mxnet import gluon
from bert_serving.client import BertClient
import boto3


logger = logging.getLogger("offer_encoder")


# Helper functions

def load_s3_file(s3_bucket, s3_prefix, file_format="csv"):
    keys = []
    dfs = []
    s3 = boto3.client('s3')
    list_obj = s3.list_objects_v2(Bucket=s3_bucket, Prefix=s3_prefix)
    assert list_obj["KeyCount"] < 1000
    for content in list_obj["Contents"]:
        if content["Key"].endswith(file_format):
            keys.append(content["Key"])
    assert len(keys) == 1
    logger.info("Load %d %s files from %s" % (len(keys), file_format, os.path.dirname(keys[0])))
    for i, key in enumerate(keys):
        obj = s3.get_object(Bucket=s3_bucket, Key=key)
        if file_format == "csv":
            dfs.append(pd.read_csv(obj["Body"]))
        elif file_format == "json":
            dfs.append(pd.read_json(obj["Body"], lines=True))
        else:
            raise NotImplementedError()
    return pd.concat(dfs)


# Should be changed along with app_mxnet_inference.load_offer_id_from_pool
def load_offer_id_from_pool(offer_pool_path, active_offer_pool=None):
    offer_pool = pd.read_csv(offer_pool_path, dtype="str").dropna(subset=["Sanity ID"])
    offer_pool = offer_pool[~offer_pool["Sanity ID"].isin(["TBR", "TBD", "0", "5"])]
    offer_pool = offer_pool[~offer_pool["Sanity ID"].str.lower().str.contains("requested")]
    logger.info("Offer Pool without TBD and NA: %d" % len(offer_pool))

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
    logger.info("active weekly MO&P: %d" % len(weekly_offer_pool))
    logger.info("active weekly MO&P default: %d" % len(weekly_default_pool))
    logger.info("active daily MO&P: %d" % len(daily_offer_pool))
    logger.info("active weekly Delivery: %d" % len(delivery_offer_pool))
    offer_pools = {
        "weekly": weekly_offer_pool,
        "default": weekly_default_pool,
        "daily": daily_offer_pool,
        "delivery": delivery_offer_pool,
        "inactive": inactive_pool,
    }
    return offer_pools


def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except Exception as e:
        logging.error(e)
        return False
    return True


# Main functions

def load_offer_all(s3_bucket, s3_prefix_offer_mapping, s3_prefix_offer_history, offer_pool_path):
    """
    offer_pool_all:
    offer_id = Unique(offer_history + weekly_offer + daily_offer + delivery_offer)
    offer_name = offer_id --offer_id_mapping-> offer_name
    """
    offer_id_mapping = load_s3_file(s3_bucket=s3_bucket, s3_prefix=s3_prefix_offer_mapping)
    offer_id_mapping = offer_id_mapping.rename(columns={"id": "offer_id",
                                                        "name": "offer_name",
                                                        "localizedImageUrl": "offer_img"})
    # TODO: supplementary offer mapping
    offer_id_mapping_supp = pd.read_csv("./data/archived/sanity_prod_2021-10-12.csv").rename(
        columns={"id": "offer_id", "name": "offer_name", "localizedImageUrl": "offer_img"})
    offer_id_mapping = pd.concat([
        offer_id_mapping[["offer_id", "offer_name", "offer_img"]],
        offer_id_mapping_supp[["offer_id", "offer_name", "offer_img"]]
    ]).drop_duplicates(subset=["offer_id"], keep="first")

    offer_history = load_s3_file(
        s3_bucket=s3_bucket,
        s3_prefix=s3_prefix_offer_history,
        file_format="json").drop(columns=["offer_name"])
    logger.info("Load %d history offers from train/eval data" % len(offer_history))

    offer_pools = load_offer_id_from_pool(offer_pool_path=offer_pool_path,
                                          active_offer_pool=offer_id_mapping["offer_id"].tolist())
    active_pool = offer_pools["weekly"] + offer_pools["daily"] + offer_pools["delivery"]
    active_pool_not_in_history = [offer_id for offer_id in active_pool
                                  if offer_id not in offer_history["offer_id"].values]
    history_max_idx = offer_history["offer_idx"].max()
    offer_pool_not_in_history = pd.DataFrame(
        data=zip(active_pool_not_in_history,
                 range(history_max_idx + 1, history_max_idx + 1 + len(active_pool_not_in_history)),
                 ["false"] * len(active_pool_not_in_history)),
        columns=["offer_id", "offer_idx", "in_training"]
    )
    logger.info("Load %d (%d) active offers from offer pool (exclusively)" % (len(active_pool),
                                                                              len(active_pool_not_in_history)))

    offer_pool_all = pd.concat([offer_history, offer_pool_not_in_history]).merge(
        offer_id_mapping[["offer_id", "offer_name", "offer_img"]],
        on="offer_id",
        how="inner").sort_values(by=["offer_idx"]).reset_index(drop=True)
    logger.info("Process to %d distinct offers in offer features lookup" % len(offer_pool_all))
    assert len(offer_history) + len(offer_pool_not_in_history) == len(offer_pool_all), "Rows dropped during merging"
    assert offer_pool_all["offer_id"].isna().sum() == 0, "NA found in offer_id"
    assert offer_pool_all.dropna(subset=["offer_id"]).duplicated(subset=["offer_id"]).sum() == 0, "Duplicated offer_id"
    assert offer_pool_all["offer_name"].isna().sum() == 0, "NA found in offer_name"

    # add index 0
    offer_pool_all = pd.concat([pd.DataFrame(data=[["n/a", 0, "n/a", "n/a", "n/a"]],
                                             columns=offer_pool_all.columns), offer_pool_all])
    logger.info("Add 1 empty offer to pool")
    return offer_pool_all


def get_bert_features(offer_pool_all):
    logger.info("Found %d NA or empty offer names" % (offer_pool_all["offer_name"].isna().sum()
                                                      + sum(offer_pool_all["offer_name"] == "")))
    offer_names_lower = offer_pool_all[offer_pool_all["offer_name"] != "n/a"]["offer_name"].str.lower().tolist()
    bc = BertClient(timeout=10000)
    bert_features = bc.encode(offer_names_lower)
    bert_features = np.concatenate([np.zeros((1, bert_features.shape[1]), dtype="float32"),
                                    bert_features])
    logger.info("Generate %s BERT features" % (bert_features.shape,))
    return bert_features


def get_resnet_features(offer_pool_all, local_img_dir="./data/offer_img/"):
    if not os.path.exists(local_img_dir):
        os.makedirs(local_img_dir)
    ctx = mx.cpu()
    net = gluon.model_zoo.vision.resnet50_v1(pretrained=True, ctx=ctx)
    net.hybridize(static_alloc=True, static_shape=True)
    resnet_features = []
    warnings.filterwarnings("ignore")
    for i, (offer_id, offer_url) in offer_pool_all[["offer_id", "offer_img"]].iterrows():
        try:
            img_path = gluon.utils.download(url="https://" + offer_url,
                                            path=os.path.join(local_img_dir, "%s.png" % offer_id),
                                            overwrite=True)
        except Exception as e:
            img_path = ""
        try:
            img = mx.image.imread(img_path)
        except Exception as e:
            if img_path == "":
                logger.info("Offer image url NA: %s" % offer_id)
            else:
                logger.info("Offer image read failed: %s" % offer_id)
            img = mx.ndarray.zeros((224, 224, 3), dtype="uint8")
        img = mx.image.imresize(img, 224, 224)  # resize
        img = mx.image.color_normalize(img.astype(dtype='float32') / 255,
                                       mean=mx.nd.array([0.485, 0.456, 0.406]),
                                       std=mx.nd.array([0.229, 0.224, 0.225]))  # normalize
        img = img.transpose((2, 0, 1))  # channel first
        img = img.expand_dims(axis=0)  # batchify
        img = img.as_in_context(ctx)
        img_features = net.features(img).asnumpy().flatten()
        resnet_features.append(img_features)
    resnet_features = np.array(resnet_features)
    logger.info("Generate %s ResNet features" % (resnet_features.shape,))
    return resnet_features


def save_embedding(net, train_iter, ctx, offer_pool_all, local_net_path, local_offer_lookup_path,
                   local_embed_csv_path, local_embed_json_path, s3_bucket, s3_embed_csv_path, s3_embed_json_path):
    train_iter.reset()
    data_x = train_iter.next().data[0].as_in_context(ctx)
    data_h = net.encoder(data_x)
    data_mu = mx.nd.split(data_h, axis=1, num_outputs=2)[0]
    # data_lv = mx.nd.split(data_h, axis=1, num_outputs=2)[1]
    net.save_parameters(local_net_path)
    logger.info("Save VAE net to %s" % local_net_path)

    # embed csv
    offer_embed_embedding_csv = pd.DataFrame(data=data_mu.asnumpy(),
                                             columns=["embed_%d" % i for i in range(data_mu.shape[1])])
    offer_embed_csv = offer_pool_all.merge(offer_embed_embedding_csv, left_index=True, right_index=True, how="left")
    offer_embed_csv.to_csv(local_embed_csv_path, index=False)
    offer_embed_csv.to_csv(local_offer_lookup_path, index=False)
    upload_file(local_embed_csv_path, s3_bucket, s3_embed_csv_path)
    logger.info("Save offer embed to %s" % local_embed_csv_path)
    logger.info("Save offer lookup to %s" % local_offer_lookup_path)
    logger.info("Upload offer embed to s3: %s/%s" % (s3_bucket, s3_embed_csv_path))

    # embed json
    offer_embed_embedding_json = pd.DataFrame(data=[[embed.tolist()] for embed in data_mu.asnumpy()], columns=["embed"])
    offer_embed_json = offer_pool_all.merge(offer_embed_embedding_json, left_index=True, right_index=True, how="left")
    offer_embed_json.to_json(local_embed_json_path, orient="records", lines=True)
    upload_file(local_embed_json_path, s3_bucket, s3_embed_json_path)
    logger.info("Save offer embed to %s" % local_embed_json_path)
    logger.info("Upload offer embed to s3 :%s/%s" % (s3_bucket, s3_embed_json_path))
    return data_mu







