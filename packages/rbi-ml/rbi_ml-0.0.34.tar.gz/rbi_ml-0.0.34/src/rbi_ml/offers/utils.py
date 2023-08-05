import os
import logging
from datetime import datetime
import pandas as pd
# import torch
import boto3
# from torch.utils.data import Dataset


# def get_device(device="auto") -> torch.device:
#     """
#     Retrieve PyTorch device.
#     It checks that the requested device is available first.
#     For now, it supports only cpu and cuda.
#     By default, it tries to use the gpu.
#     :param device: One for 'auto', 'cuda', 'cpu'
#     :return:
#     """
#     # Cuda by default
#     if device == "auto":
#         device = "cuda"
#     # Force conversion to torch.device
#     device = torch.device(device)
#
#     # Cuda not available
#     if device.type == torch.device("cuda").type and not torch.cuda.is_available():
#         return torch.device("cpu")
#
#     return device


# class OfferDatasetS3(Dataset):
#     # TODO: add 0 as missing store id into store_lookup in databricks
#     def __init__(self, s3_bucket, s3_data, s3_offer_lookup, s3_platform_lookup, s3_dma_lookup,
#                  s3_device_carrier_lookup, s3_device_model_lookup, parts_num=999):
#         self.logger = logging.getLogger("order_dataset")
#         self.logger.info("Load data and lookup tables directly from s3")
#         if parts_num == 0:
#             self.data = None
#         else:
#             self.data = self.load_s3_data(s3_bucket, s3_data, parts_num)
#         self.offer_lookup = self.load_s3_lookup(s3_bucket, s3_offer_lookup, file_type="json")
#         self.platform_lookup = self.load_s3_lookup(s3_bucket, s3_platform_lookup)
#         self.dma_lookup = self.load_s3_lookup(s3_bucket, s3_dma_lookup)
#         self.device_carrier_lookup = self.load_s3_lookup(s3_bucket, s3_device_carrier_lookup)
#         self.device_model_lookup = self.load_s3_lookup(s3_bucket, s3_device_model_lookup)
#
#     def __len__(self):
#         return len(self.data)
#
#     def __getitem__(self, idx):
#         context_col_names = ["platform_idx", "device_carrier_idx", "device_model_idx"]  # TODO: dma_idx
#         if torch.is_tensor(idx):
#             idx = idx.tolist()
#         order_context = [torch.tensor([self.data.iloc[idx][k]]) for k in context_col_names]
#         order_seq = torch.tensor(self.data.iloc[idx]["offer_idx"])
#         order_target = self.data.iloc[idx]["target_offer_idx"]
#         return order_context, order_seq, order_target
#
#     def load_s3_data(self, s3_bucket, s3_data, parts_num):
#         keys = []
#         dfs = []
#         s3 = boto3.client('s3')
#         list_obj = s3.list_objects_v2(Bucket=s3_bucket, Prefix=s3_data)
#         if list_obj["KeyCount"] > 1000:
#             self.logger.error("Found more than 1000 keys and only read partial data")
#         for content in list_obj["Contents"]:
#             if content["Key"].endswith(".json"):
#                 keys.append(content["Key"])
#         self.logger.info("Load %d json files from %s" % (min(parts_num, len(keys)), os.path.dirname(keys[0])))
#         for i, key in enumerate(keys):
#             if i < parts_num:
#                 obj = s3.get_object(Bucket=s3_bucket, Key=key)
#                 dfs.append(pd.read_json(obj["Body"], orient="columns", lines=True))
#         return pd.concat(dfs)
#
#     def load_s3_lookup(self, s3_bucket, s3_lookup, file_type="csv"):
#         keys = []
#         s3 = boto3.client('s3')
#         list_obj = s3.list_objects_v2(Bucket=s3_bucket, Prefix=s3_lookup)
#         if list_obj["KeyCount"] > 1000:
#             self.logger.error("Found more than 1000 keys and only read partial data")
#         for content in list_obj["Contents"]:
#             if content["Key"].endswith(file_type):
#                 keys.append(content["Key"])
#         if len(keys) > 1:
#             self.logger.error("Found more than 1 lookup %s" % file_type)
#         obj = s3.get_object(Bucket=s3_bucket, Key=keys[0])
#         self.logger.info("Load lookup table from %s" % keys[0])
#         if file_type == "csv":
#             df = pd.read_csv(obj["Body"])
#         elif file_type == "json":
#             df = pd.read_json(obj["Body"])
#         else:
#             raise ValueError("file_type can only be \"csv\" or \"json\"")
#         return df


def generate_lookup_dict(df, key_col, value_col):
    """Generate int2int lookup dict from given dataframe."""
    return df[[key_col, value_col]].set_index(key_col).to_dict()[value_col]


def load_s3_table(s3_bucket, s3_prefix, file_type="csv"):
    logger = logging.getLogger("load_s3")
    keys = []
    s3 = boto3.client('s3')
    list_obj = s3.list_objects_v2(Bucket=s3_bucket, Prefix=s3_prefix)
    if list_obj["KeyCount"] > 1000:
        logger.error("Found more than 1000 keys and only read partial data")
    for content in list_obj["Contents"]:
        if content["Key"].endswith(file_type):
            keys.append(content["Key"])
    if len(keys) > 1:
        logger.error("Found more than 1 lookup %s" % file_type)
    obj = s3.get_object(Bucket=s3_bucket, Key=keys[0])
    logger.info("Load s3 table from %s" % keys[0])
    if file_type == "csv":
        df = pd.read_csv(obj["Body"])
    elif file_type == "json":
        df = pd.read_json(obj["Body"], lines=True)
    else:
        raise ValueError("file_type can only be \"csv\" or \"json\"")
    return df


def item2name(item_code, item_lookup):
    item_code = int(item_code)
    if item_code == 0:
        return None
    else:
        item_names = item_lookup[item_lookup["item_code"] == item_code]["item_name_clean"]
        if len(item_names) != 1:
            print("WARNING - %d names were found for item %d" % (len(item_names), item_code))
        else:
            return item_names.iloc[0]

