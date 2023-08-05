NA_RULES = {
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

SEGMENT_RULES = {
    "n/a": {
        "1": NA_RULES,
        "2": NA_RULES,
    },
    # real stuffs
    "6": {
        "1": {
            "0": {"br": 1, "family": 1, "for2": 2, "1serve": 3, "snack": 1},
            "1": {"br": 1, "family": 1, "for2": 2, "1serve": 3, "snack": 1},
            "2": {"br": 1, "family": 3, "for2": 2, "1serve": 2, "snack": 0},
            "3": {"br": 1, "family": 1, "for2": 3, "1serve": 2, "snack": 1},
            "4": {"br": 1, "family": 1, "for2": 1, "1serve": 3, "snack": 2},
            "5": {"br": 1, "family": 1, "for2": 1, "1serve": 3, "snack": 2},
            "6": {"br": 1, "family": 3, "for2": 2, "1serve": 2, "snack": 0},
            "7": {"br": 1, "family": 1, "for2": 2, "1serve": 3, "snack": 1},
            "8": {"br": 1, "family": 3, "for2": 3, "1serve": 1, "snack": 0},
            "9": {"br": 3, "family": 1, "for2": 1, "1serve": 2, "snack": 1},
        },
        "2": {
            "0": {"br": 0, "family": 1, "for2": 2, "1serve": 3, "snack": 1},
            "1": {"br": 0, "family": 1, "for2": 2, "1serve": 3, "snack": 1},
            "2": {"br": 0, "family": 3, "for2": 2, "1serve": 2, "snack": 0},
            "3": {"br": 0, "family": 1, "for2": 3, "1serve": 2, "snack": 1},
            "4": {"br": 0, "family": 1, "for2": 1, "1serve": 3, "snack": 2},
            "5": {"br": 0, "family": 1, "for2": 1, "1serve": 3, "snack": 2},
            "6": {"br": 0, "family": 3, "for2": 2, "1serve": 2, "snack": 0},
            "7": {"br": 0, "family": 1, "for2": 2, "1serve": 3, "snack": 1},
            "8": {"br": 0, "family": 3, "for2": 2, "1serve": 2, "snack": 0},
            "9": {"br": 0, "family": 1, "for2": 2, "1serve": 3, "snack": 1},
        }
    },
    "9": {
        "1": {
            "0": {"br": 1, "family": 1, "for2": 3, "1serve": 4, "snack": 2},
            "1": {"br": 1, "family": 1, "for2": 3, "1serve": 4, "snack": 2},
            "2": {"br": 1, "family": 4, "for2": 3, "1serve": 2, "snack": 1},
            "3": {"br": 1, "family": 2, "for2": 4, "1serve": 3, "snack": 1},
            "4": {"br": 1, "family": 1, "for2": 2, "1serve": 4, "snack": 3},
            "5": {"br": 1, "family": 1, "for2": 2, "1serve": 4, "snack": 3},
            "6": {"br": 1, "family": 4, "for2": 3, "1serve": 2, "snack": 1},
            "7": {"br": 1, "family": 1, "for2": 3, "1serve": 4, "snack": 2},
            "8": {"br": 1, "family": 4, "for2": 3, "1serve": 3, "snack": 0},
            "9": {"br": 4, "family": 1, "for2": 2, "1serve": 3, "snack": 1},
        },
        "2": {
            "0": {"br": 0, "family": 1, "for2": 3, "1serve": 4, "snack": 2},
            "1": {"br": 0, "family": 1, "for2": 3, "1serve": 4, "snack": 2},
            "2": {"br": 0, "family": 4, "for2": 3, "1serve": 2, "snack": 1},
            "3": {"br": 0, "family": 2, "for2": 4, "1serve": 3, "snack": 1},
            "4": {"br": 0, "family": 1, "for2": 2, "1serve": 4, "snack": 3},
            "5": {"br": 0, "family": 1, "for2": 2, "1serve": 4, "snack": 3},
            "6": {"br": 0, "family": 4, "for2": 3, "1serve": 2, "snack": 1},
            "7": {"br": 0, "family": 1, "for2": 3, "1serve": 4, "snack": 2},
            "8": {"br": 0, "family": 4, "for2": 3, "1serve": 3, "snack": 0},
            "9": {"br": 0, "family": 1, "for2": 3, "1serve": 4, "snack": 2},
        }
    },
}


def get_segment_rules(topk_weekly, user_tier, cluster_id):
    if str(topk_weekly) not in SEGMENT_RULES:
        topk_weekly = "n/a"
    return SEGMENT_RULES.get(str(topk_weekly), {}).get(str(user_tier), {}).get(str(cluster_id), {})
