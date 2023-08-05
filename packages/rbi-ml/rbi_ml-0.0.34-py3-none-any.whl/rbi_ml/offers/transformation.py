# import json
# import boto3
# from botocore.config import Config
import numpy as np
# import pandas as pd
from datetime import datetime, date
from datetime import timedelta
# from functools import reduce



scalerDict = {'freq_mean': 1.9587705306223417, 'freq_stddev': 2.5404163260992725, 'service_mode_mean': 0.11186028532189878, 'service_mode_stddev': 0.30772590017779755, 'avg_check_mean': 10.6798393706413, 'avg_check_stddev': 26.60265414227535, 'coupon_applied_mean': 0.672631486860397, 'coupon_applied_stddev': 0.43745654203641293}

centroidList = [[-0.1578989288361283, -0.3091407796089874, 0.0021443514126048163, -0.9378141118644834], [0.14138093480857145, -0.42836855304007876, -0.1371346205077106, 0.8818763574885143], [-0.010898790339505408, 0.9745306542737879, 0.06508153948905968, 0.2143259514561229], [0.4629525864206741, -0.26204164698593424, -0.024284297001413612, -0.8464155899382136], [0.8519611226775021, -0.3644163181256923, -0.11973663584118086, 0.35640725380839394], [-0.40741261073215634, -0.3924068300687248, -0.16559711078625497, 0.8078424606512511], [0.0036629008749804438, 0.8790320790375357, 0.07151676700826715, -0.4713539426129933], [0.9639526741615622, -0.1335701121601069, -0.05363611773324233, -0.22377987842702812], [-0.33869980689839496, -0.3758942961762893, 0.3811255338081403, 0.7737759665359102]]


# rules_1 = {
#     '0': {'br': 1, 'nbr': 1, 'h': 1, 'm': 1, 'l': 1},
#     '1': {'br': 1, 'nbr': 1, 'h': 1, 'm': 1, 'l': 1},
#     '2': {'br': 1, 'nbr': 1, 'h': 1, 'm': 1, 'l': 1},
#     '3': {'br': 1, 'nbr': 1, 'h': 1, 'm': 1, 'l': 1},
#     '4': {'br': 1, 'nbr': 1, 'h': 1, 'm': 1, 'l': 1},
#     '5': {'br': 1, 'nbr': 1, 'h': 1, 'm': 1, 'l': 1},
#     '6': {'br': 1, 'nbr': 1, 'h': 1, 'm': 1, 'l': 1},
#     '7': {'br': 1, 'nbr': 1, 'h': 1, 'm': 1, 'l': 1},
#     '8': {'br': 1, 'nbr': 1, 'h': 1, 'm': 1, 'l': 1},
#     '9': {'br': 1, 'nbr': 1, 'h': 1, 'm': 1, 'l': 1}
# }

# rules_3 = {
#     '0': {'br': 1, 'nbr': 2, 'h': 3, 'm': 3, 'l': 3},
#     '1': {'br': 0, 'nbr': 3, 'h': 3, 'm': 3, 'l': 3},
#     '2': {'br': 1, 'nbr': 2, 'h': 3, 'm': 3, 'l': 3},
#     '3': {'br': 1, 'nbr': 3, 'h': 3, 'm': 3, 'l': 3},
#     '4': {'br': 0, 'nbr': 3, 'h': 3, 'm': 3, 'l': 3},
#     '5': {'br': 1, 'nbr': 2, 'h': 3, 'm': 3, 'l': 3},
#     '6': {'br': 0, 'nbr': 3, 'h': 3, 'm': 3, 'l': 3},
#     '7': {'br': 0, 'nbr': 3, 'h': 3, 'm': 3, 'l': 3},
#     '8': {'br': 0, 'nbr': 3, 'h': 3, 'm': 3, 'l': 3},
#     '9': {'br': 0, 'nbr': 3, 'h': 3, 'm': 3, 'l': 3}
# }

#TODO rules 4 has not been set
# rules_4 = {
#     "0": {"br": 1, "family": 1, "for2": 1, "1serve": 1, "snack": 1},  # 1.5% - Frequent + Delivery, offer indifferent
#     "1": {"br": 0, "family": 0, "for2": 2, "1serve": 2, "snack": 1},  # 40% - Small Check, offer driven
#     "2": {"br": 0, "family": 1, "for2": 2, "1serve": 1, "snack": 1},  # 18 - Medium Check, offer indifferent
#     "3": {"br": 0, "family": 2, "for2": 2, "1serve": 1, "snack": 0},  # 7% - Delivery, offer indifferent
#     "4": {"br": 0, "family": 1, "for2": 1, "1serve": 2, "snack": 1},  # 3% - Frequent, Offer indifferent
#     "5": {"br": 0, "family": 2, "for2": 2, "1serve": 1, "snack": 0},  # 5% - Delivery + Family, Offer Driven
#     "6": {"br": 0, "family": 0, "for2": 2, "1serve": 2, "snack": 1},  # 5% - Medium Check, Offer semi-driven
#     "7": {"br": 0, "family": 2, "for2": 2, "1serve": 1, "snack": 0},  # 11% - Family, offer driven
#     "8": {"br": 0, "family": 0, "for2": 1, "1serve": 3, "snack": 1},  # 6% - Frequent, offer driven
#     "9": {"br": 3, "family": 0, "for2": 1, "1serve": 1, "snack": 0},  # 6% - Breakfast
# }


rules_5 = {
    "0": {"br": 0, "family": 0, "for2": 2, "1serve": 0, "snack": 0},  # 20% - Medium Check, offer indifferent - FOR2
    "1": {"br": 0, "family": 0, "for2": 1, "1serve": 2, "snack": 0},  # 13% - Frequent, offer driven - SINGLE
    "2": {"br": 0, "family": 2, "for2": 0, "1serve": 0, "snack": 0},  # 3% - Family + Delivery, offer driven - FAMILY
    "3": {"br": 0, "family": 0, "for2": 2, "1serve": 0, "snack": 0},  # 3% - Medium Check, offer indifferent - FOR2
    "4": {"br": 0, "family": 0, "for2": 1, "1serve": 2, "snack": 0},  # 6% - Frequent, Offer indifferent - SINGLE
    "5": {"br": 0, "family": 0, "for2": 1, "1serve": 2, "snack": 0},  # 29% - Small Check, Offer Driven - SINGLE
    "6": {"br": 0, "family": 2, "for2": 0, "1serve": 0, "snack": 0},  # 8% - Delivery, Offer indifferent - FAMILY
    "7": {"br": 0, "family": 0, "for2": 1, "1serve": 2, "snack": 0},  # 3% - Frequent, semi-offer driven - SINGLE
    "8": {"br": 0, "family": 2, "for2": 0, "1serve": 0, "snack": 0},  # 9% - Family + Delivery, offer driven - FAMILY
    "9": {"br": 2, "family": 0, "for2": 0, "1serve": 1, "snack": 0},  # 6% - Breakfast - BREAKFAST
}

# rules_7 = {
#     '0': {'br': 2, 'nbr': 5, 'h': 7, 'm': 7, 'l': 7},
#     '1': {'br': 1, 'nbr': 6, 'h': 7, 'm': 7, 'l': 7},
#     '2': {'br': 2, 'nbr': 5, 'h': 7, 'm': 7, 'l': 7},
#     '3': {'br': 1, 'nbr': 7, 'h': 7, 'm': 7, 'l': 7},
#     '4': {'br': 1, 'nbr': 6, 'h': 7, 'm': 7, 'l': 7},
#     '5': {'br': 2, 'nbr': 5, 'h': 7, 'm': 7, 'l': 7},
#     '6': {'br': 1, 'nbr': 6, 'h': 7, 'm': 7, 'l': 7},
#     '7': {'br': 1, 'nbr': 6, 'h': 7, 'm': 7, 'l': 7},
#     '8': {'br': 1, 'nbr': 6, 'h': 7, 'm': 7, 'l': 7},
#     '9': {'br': 1, 'nbr': 6, 'h': 7, 'm': 7, 'l': 7}
# }

# rules_9 = {
#     '0': {'br': 2, 'nbr': 7, 'h': 9, 'm': 9, 'l': 9},
#     '1': {'br': 1, 'nbr': 8, 'h': 9, 'm': 9, 'l': 9},
#     '2': {'br': 2, 'nbr': 7, 'h': 9, 'm': 9, 'l': 9},
#     '3': {'br': 2, 'nbr': 8, 'h': 9, 'm': 9, 'l': 9},
#     '4': {'br': 1, 'nbr': 8, 'h': 9, 'm': 9, 'l': 9},
#     '5': {'br': 2, 'nbr': 7, 'h': 9, 'm': 9, 'l': 9},
#     '6': {'br': 1, 'nbr': 8, 'h': 9, 'm': 9, 'l': 9},
#     '7': {'br': 1, 'nbr': 8, 'h': 9, 'm': 9, 'l': 9},
#     '8': {'br': 1, 'nbr': 8, 'h': 9, 'm': 9, 'l': 9},
#     '9': {'br': 1, 'nbr': 8, 'h': 9, 'm': 9, 'l': 9}
# }


# rules = {
#     '0': {'br': 1, 'nbr': 8, 'h': 4, 'm': 4, 'l': 1},
#     '1': {'br': 1, 'nbr': 8, 'h': 3, 'm': 4, 'l': 2},
#     '2': {'br': 3, 'nbr': 6, 'h': 2, 'm': 4, 'l': 3},
#     '3': {'br': 1, 'nbr': 8, 'h': 5, 'm': 2, 'l': 2},
#     '4': {'br': 2, 'nbr': 7, 'h': 4, 'm': 3, 'l': 2},
#     '5': {'br': 1, 'nbr': 8, 'h': 5, 'm': 3, 'l': 1},
#     '6': {'br': 2, 'nbr': 7, 'h': 2, 'm': 4, 'l': 3},
#     '7': {'br': 1, 'nbr': 8, 'h': 1, 'm': 3, 'l': 5},
#     '8': {'br': 1, 'nbr': 8, 'h': 4, 'm': 3, 'l': 2},
#     '9': {'br': 1, 'nbr': 8, 'h': 9, 'm': 9, 'l': 9}
# }

# rules_9 = {
#     '0': {'br': 1, 'nbr': 8, 'h': 4, 'm': 4, 'l': 1},
#     '1': {'br': 1, 'nbr': 8, 'h': 3, 'm': 4, 'l': 2},
#     '2': {'br': 3, 'nbr': 6, 'h': 2, 'm': 4, 'l': 3},
#     '3': {'br': 1, 'nbr': 8, 'h': 5, 'm': 2, 'l': 2},
#     '4': {'br': 2, 'nbr': 7, 'h': 4, 'm': 3, 'l': 2},
#     '5': {'br': 1, 'nbr': 8, 'h': 5, 'm': 3, 'l': 1},
#     '6': {'br': 2, 'nbr': 7, 'h': 2, 'm': 4, 'l': 3},
#     '7': {'br': 1, 'nbr': 8, 'h': 1, 'm': 3, 'l': 5},
#     '8': {'br': 1, 'nbr': 8, 'h': 4, 'm': 3, 'l': 2},
#     '9': {'br': 1, 'nbr': 8, 'h': 9, 'm': 9, 'l': 9}
# }

# rules_1 = {
#     '0': {'br': 1, 'nbr': 1, 'h': 0, 'm': 0, 'l': 1},
#     '1': {'br': 1, 'nbr': 1, 'h': 1, 'm': 0, 'l': 0},
#     '2': {'br': 1, 'nbr': 1, 'h': 0, 'm': 0, 'l': 1},
#     '3': {'br': 1, 'nbr': 1, 'h': 1, 'm': 0, 'l': 0},
#     '4': {'br': 1, 'nbr': 1, 'h': 0, 'm': 1, 'l': 0},
#     '5': {'br': 1, 'nbr': 1, 'h': 1, 'm': 0, 'l': 0},
#     '6': {'br': 1, 'nbr': 1, 'h': 1, 'm': 0, 'l': 0},
#     '7': {'br': 1, 'nbr': 1, 'h': 0, 'm': 1, 'l': 0},
#     '8': {'br': 1, 'nbr': 1, 'h': 1, 'm': 1, 'l': 1},
#     '9': {'br': 1, 'nbr': 1, 'h': 1, 'm': 1, 'l': 1}
# }

# rules_3 = {
#     '0': {'br': 1, 'nbr': 2, 'h': 0, 'm': 1, 'l': 2},
#     '1': {'br': 0, 'nbr': 3, 'h': 2, 'm': 1, 'l': 1},
#     '2': {'br': 1, 'nbr': 2, 'h': 1, 'm': 1, 'l': 2},
#     '3': {'br': 1, 'nbr': 3, 'h': 2, 'm': 1, 'l': 1},
#     '4': {'br': 0, 'nbr': 3, 'h': 1, 'm': 2, 'l': 1},
#     '5': {'br': 1, 'nbr': 2, 'h': 2, 'm': 1, 'l': 1},
#     '6': {'br': 0, 'nbr': 3, 'h': 2, 'm': 1, 'l': 1},
#     '7': {'br': 0, 'nbr': 3, 'h': 1, 'm': 2, 'l': 1},
#     '8': {'br': 0, 'nbr': 3, 'h': 3, 'm': 3, 'l': 3},
#     '9': {'br': 0, 'nbr': 3, 'h': 3, 'm': 3, 'l': 3}
# }

# rules_5 = {
#     '0': {'br': 2, 'nbr': 3, 'h': 1, 'm': 2, 'l': 3},
#     '1': {'br': 1, 'nbr': 4, 'h': 3, 'm': 1, 'l': 1},
#     '2': {'br': 2, 'nbr': 3, 'h': 1, 'm': 2, 'l': 2},
#     '3': {'br': 1, 'nbr': 4, 'h': 2, 'm': 2, 'l': 1},
#     '4': {'br': 1, 'nbr': 4, 'h': 1, 'm': 3, 'l': 1},
#     '5': {'br': 2, 'nbr': 3, 'h': 3, 'm': 2, 'l': 1},
#     '6': {'br': 1, 'nbr': 4, 'h': 3, 'm': 2, 'l': 1},
#     '7': {'br': 1, 'nbr': 4, 'h': 1, 'm': 3, 'l': 2},
#     '8': {'br': 1, 'nbr': 4, 'h': 3, 'm': 2, 'l': 3},
#     '9': {'br': 1, 'nbr': 4, 'h': 5, 'm': 5, 'l': 5}
# }

# rules_7 = {
#     '0': {'br': 2, 'nbr': 5, 'h': 2, 'm': 3, 'l': 4},
#     '1': {'br': 1, 'nbr': 6, 'h': 4, 'm': 2, 'l': 2},
#     '2': {'br': 2, 'nbr': 5, 'h': 2, 'm': 2, 'l': 3},
#     '3': {'br': 1, 'nbr': 7, 'h': 3, 'm': 3, 'l': 2},
#     '4': {'br': 1, 'nbr': 6, 'h': 2, 'm': 4, 'l': 2},
#     '5': {'br': 2, 'nbr': 5, 'h': 4, 'm': 3, 'l': 2},
#     '6': {'br': 1, 'nbr': 6, 'h': 3, 'm': 2, 'l': 2},
#     '7': {'br': 1, 'nbr': 6, 'h': 2, 'm': 3, 'l': 2},
#     '8': {'br': 1, 'nbr': 6, 'h': 3, 'm': 2, 'l': 2},
#     '9': {'br': 1, 'nbr': 6, 'h': 7, 'm': 7, 'l': 7}
# }

# rules_9 = {
#     '0': {'br': 2, 'nbr': 7, 'h': 1, 'm': 3, 'l': 5},
#     '1': {'br': 1, 'nbr': 8, 'h': 5, 'm': 2, 'l': 2},
#     '2': {'br': 2, 'nbr': 7, 'h': 2, 'm': 3, 'l': 4},
#     '3': {'br': 2, 'nbr': 8, 'h': 4, 'm': 3, 'l': 2},
#     '4': {'br': 1, 'nbr': 8, 'h': 2, 'm': 5, 'l': 2},
#     '5': {'br': 2, 'nbr': 7, 'h': 5, 'm': 3, 'l': 1},
#     '6': {'br': 1, 'nbr': 8, 'h': 4, 'm': 3, 'l': 2},
#     '7': {'br': 1, 'nbr': 8, 'h': 2, 'm': 4, 'l': 3},
#     '8': {'br': 1, 'nbr': 8, 'h': 4, 'm': 3, 'l': 2},
#     '9': {'br': 1, 'nbr': 8, 'h': 9, 'm': 9, 'l': 9}
# }
#
# rules_12 = {
#     '0': {'br': 3, 'nbr': 9, 'h': 2, 'm': 4, 'l': 6},
#     '1': {'br': 1, 'nbr': 11, 'h': 6, 'm': 3, 'l': 3},
#     '2': {'br': 3, 'nbr': 9, 'h': 3, 'm': 4, 'l': 5},
#     '3': {'br': 2, 'nbr': 10, 'h': 5, 'm': 4, 'l': 3},
#     '4': {'br': 1, 'nbr': 11, 'h': 3, 'm': 6, 'l': 3},
#     '5': {'br': 3, 'nbr': 9, 'h': 6, 'm': 4, 'l': 2},
#     '6': {'br': 1, 'nbr': 11, 'h': 5, 'm': 4, 'l': 3},
#     '7': {'br': 1, 'nbr': 11, 'h': 3, 'm': 5, 'l': 4},
#     '8': {'br': 1, 'nbr': 11, 'h': 5, 'm': 4, 'l': 3},
#     '9': {'br': 1, 'nbr': 11, 'h': 12, 'm': 12, 'l': 12}
# }

# rules_14 = {
#     '0': {'br': 1, 'nbr': 13, 'h': 6, 'm': 6, 'l': 2},
#     '1': {'br': 1, 'nbr': 13, 'h': 5, 'm': 6, 'l': 3},
#     '2': {'br': 3, 'nbr': 11, 'h': 3, 'm': 6, 'l': 5},
#     '3': {'br': 2, 'nbr': 12, 'h': 7, 'm': 4, 'l': 3},
#     '4': {'br': 3, 'nbr': 11, 'h': 6, 'm': 5, 'l': 3},
#     '5': {'br': 2, 'nbr': 12, 'h': 7, 'm': 5, 'l': 2},
#     '6': {'br': 3, 'nbr': 11, 'h': 3, 'm': 6, 'l': 5},
#     '7': {'br': 2, 'nbr': 12, 'h': 2, 'm': 5, 'l': 7},
#     '8': {'br': 2, 'nbr': 12, 'h': 6, 'm': 5, 'l': 3},
#     '9': {'br': 2, 'nbr': 12, 'h': 14, 'm': 14, 'l': 14}
# }


result = {
"purchases": [
{
"bkid": "3426",
"carrier": "verizon",
"cart": [
"item_54613",
"a80686be-611f-47b7-8147-ffa46be55e9c"
],
"couponID": "83ea8a93-e575-450f-889c-5f98914cd900",
"device": "apple",
"orderType": "mobile order",
"platform": "ios",
"revenue": 15.48,
"serviceMode": "delivery",
"timeStamp": "2020-11-20 09:30:42",
"upsellTotal": 0
},
{
"bkid": "3426",
"carrier": "verizon",
"cart": [
"item_54613",
"a80686be-611f-47b7-8147-ffa46be55e9c"
],
"couponID": "83ea8a93-e575-450f-889c-5f98914cd900",
"device": "apple",
"orderType": "mobile order",
"platform": "ios",
"revenue": 21.85,
"serviceMode": "delivery",
"timeStamp": "2021-09-10 18:22:42",
"upsellTotal": 0
},
{
"bkid": "3426",
"carrier": "verizon",
"cart": [
"item_52471",
"27ee336b-5caf-49d8-862f-1a6e704f4b8c"
],
"couponID": "",
"device": "apple",
"orderType": "mobile order",
"platform": "ios",
"revenue": 2,
"serviceMode": "drive thru",
"timeStamp": "2021-09-03 14:23:22",
"upsellTotal": 0
},
{
"bkid": "unknown",
"carrier": "verizon",
"cart": [],
"couponID": "",
"device": "apple",
"orderType": "mobile order",
"platform": "ios",
"revenue": 1,
"serviceMode": "drive thru",
"timeStamp": "2021-04-07 17:50:20",
"upsellTotal": 0
},
{
"bkid": "3426",
"carrier": "verizon",
"cart": [
"item_54613",
"a80686be-611f-47b7-8147-ffa46be55e9c"
],
"couponID": "",
"device": "apple",
"orderType": "mobile order",
"platform": "ios",
"revenue": 31.94,
"serviceMode": "delivery",
"timeStamp": "2021-04-08 19:56:42",
"upsellTotal": 0
}
],
"userId": "1fffb62f-9fa5-49a3-814f-614508b2bc35"
}['purchases']


def preprocessing(result, scalerDict, centroidList):
    purchases = []
    times = []

    for _ in result:
        if ('timeStamp' in _) and (_['timeStamp'] is not None) and (_['timeStamp'] != '') and (_['timeStamp'] != 'none') \
                and (_['timeStamp'] != 'n/a') and (len(_['timeStamp']) == 19) \
                and (_['timeStamp'] >= str(datetime.now() - timedelta(days=180))):
            if ('revenue' in _) and (_['revenue'] is not None) and (_['revenue'] != 'n/a') \
                    and (_['revenue'] != 'none') and (_['revenue'] != ''):
                if ('couponID' in _):
                    purchases.append(_)
                    times.append(_['timeStamp'])
    if purchases:
        currentTime = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        currentTime = datetime.strptime(currentTime, '%Y-%m-%d %H:%M:%S')
        latest = datetime.strptime(max(times), '%Y-%m-%d %H:%M:%S')
        timeDelta = date(currentTime.year, currentTime.month, currentTime.day) - date(latest.year, latest.month,
                                                                                      latest.day)
        diff = timeDelta.days
        if 0 <= diff < 30:
            lapsedCategory = 0
        elif 30 <= diff < 60:
            lapsedCategory = 30
        elif 60 <= diff < 90:
            lapsedCategory = 60
        else:
            lapsedCategory = 90

        #Check if breakfast %
        breakfast_window = 0
        for purchase in purchases:
            timestamp = purchase['timeStamp'].split(' ')[1]
            hrmin = timestamp[0:2] + timestamp[3:5]
            if hrmin > '0600' and hrmin < '1030':
                breakfast_window += 1
                
        breakfast_window /= len(purchases)

        #if 60% in breakfast window, assign to breakfast immediately
        if breakfast_window > 0.6:
            cluster = 9
        else:
            #get kmeans attr, and scale to assign segment
            #avg check
            avg_check = np.mean([purchase['revenue'] for purchase in purchases])
            #coupon %
            coupon_applied = np.mean([0 if purchase['couponID'] == 'n/a' else 1 for purchase in purchases])
            #delivery %
            service_mode = np.mean([1 if purchase['serviceMode'] == 'delivery' else 0 for purchase in purchases])
            #number purchases in last 55 days
            #Due to limited data, will eventually be 60 or 90
            today = datetime.today()
            freq_55 = np.sum([1 if (today - datetime.strptime(purchase['timeStamp'], '%Y-%m-%d %H:%M:%S')).days <= 55 else 0 for purchase in purchases])

            data = [freq_55, service_mode, avg_check, coupon_applied]
            # print(data)

            #scale data
            scaled_data = [0, 0, 0, 0]
            scaled_data[0] = (float(data[0]) - scalerDict['freq_mean']) / scalerDict['freq_stddev']
            scaled_data[1] = (float(data[1]) - scalerDict['service_mode_mean']) / scalerDict['service_mode_stddev']
            scaled_data[2] = (float(data[2]) - scalerDict['avg_check_mean']) / scalerDict['avg_check_stddev']
            scaled_data[3] = (float(data[3]) - scalerDict['coupon_applied_mean']) / scalerDict['coupon_applied_stddev']
            
            
            #Get cosine similarity with each centroid and find closest segment
            max_cos_sim = -1
            max_segment = -1
            current_segment = 0
            for center in centroidList:
                cos_sim = np.dot(scaled_data, center)/(np.linalg.norm(scaled_data)*np.linalg.norm(center))
                if cos_sim > max_cos_sim:
                    max_cos_sim = cos_sim 
                    max_segment = current_segment
                current_segment += 1
            #assign cluster to closest segment
            cluster = max_segment

        #assign rule
        # if topk_weekly == 4:
        #     rule = rules_4[str(cluster)]
        # if topk_weekly == 5:
        #     rule = rules_5[str(cluster)]
        # else:
        #     rule = rules_5[str(cluster)]

        return 'false', str(cluster), str(lapsedCategory), purchases
    else:
        # print('No valid purchases history left after filtering')
        return 'false', 'none', 'default', []


# print(preprocessing(result, scalerDict, centroidList, 5))
