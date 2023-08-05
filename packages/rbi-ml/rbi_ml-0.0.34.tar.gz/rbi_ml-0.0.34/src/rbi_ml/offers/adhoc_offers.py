

def get_anitta_meal(purchase_history_id):
    # Anitta meal
    if "a04ac236-7876-40e6-816f-5451052e4448" in purchase_history_id:
        adhoc_offer = "XbQHVtlrnQ8pZHzm0qwzCp"  # $6 Impossible™ Whopper Combo Meal
    else:
        adhoc_offer = "n/a"
    return adhoc_offer


def get_ff_og_hb(purchase_history_id):
    # $1 Any Size French Fries, Onion Rings or Hash Browns purchaser
    ff = {"item_539", "item_540", "item_541"}  # French Fries
    og = {"item_686", "item_687", "item_688"}  # Onion Rings
    # hb = {"item_568", "item_569", "item_570"}  # Hash Browns
    if "23354564-7c6f-494f-b56c-8f156e530aaf" in purchase_history_id:
        purchase_cart = purchase_history_id["23354564-7c6f-494f-b56c-8f156e530aaf"]
        if len(og.intersection(purchase_cart)) > 0:
            adhoc_offer = "b2b74622-5746-4945-be1b-c0044757adf6"  # $1 Large Onion Rings
        elif len(ff.intersection(purchase_cart)) > 0:
            adhoc_offer = "99477cec-ca61-4851-98c2-4f87539e0a11"  # $1 Large French Fries
        else:
            adhoc_offer = "99477cec-ca61-4851-98c2-4f87539e0a11"  # $1 Large French Fries
    else:
        adhoc_offer = "99477cec-ca61-4851-98c2-4f87539e0a11"  # $1 Large French Fries
    return adhoc_offer


def get_sd_ic_hc(purchase_history_id):
    # $1 Any Size Hot Coffee, Iced Coffee, or Soft Drink
    sd = {
        "item_113", "item_376", "item_377", "item_379",
        # SM
        "item_43086", "item_52523", "item_43091", "item_52533", "item_43116", "item_43096", "item_52538", "item_43111",
        "item_43121", "item_43126", "item_43101", "item_52548", "item_43141", "item_43146", "item_43106", "item_52543",
        "item_43151", "item_43156",
        # MED
        "item_43087", "item_52524", "item_43092", "item_52534", "item_43097", "item_52539", "item_43107", "item_52544",
        "item_43112", "item_43117", "item_43122", "item_43102", "item_52549", "item_43122", "item_43127", "item_43142",
        "item_43147", "item_43152", "item_43157", "item_43137", "item_884", "item_879",
        # LG
        "item_43088", "item_52525", "item_43093", "item_52535", "item_43098", "item_52540", "item_43108", "item_52545",
        "item_43113", "item_43118", "item_43123", "item_43128", "item_43103", "item_52550", "item_43143", "item_43148",
        "item_43153", "item_43158",
    }
    ic = {
        # SM
        "item_580", "item_577", "item_583", "item_576", "item_42099",
        # MED
        "item_581", "item_578", "item_584", "item_575", "item_42112",
        # LG
        "item_582", "item_579", "item_585", "item_574", "item_42113",
    }
    hc = {
        # SM
        "item_49485", "item_49510",
        # MED
        "item_49508", "item_49511",
        # LG
        "item_49509", "item_49512",
    }
    if "e2e6f181-b069-4871-baab-aef10b90e394" in purchase_history_id:
        purchase_cart = purchase_history_id["e2e6f181-b069-4871-baab-aef10b90e394"]
        if len(sd.intersection(purchase_cart)) > 0:
            adhoc_offer = "29c77c38-0059-4981-9334-6936d03416ee"  # $1 Any Size Soft Drink
        elif len(ic.intersection(purchase_cart)) > 0:
            adhoc_offer = "ca0abc40-7f78-40c6-99cf-fe8482c6e300"  # $1 Small Iced Coffee
        elif len(hc.intersection(purchase_cart)) > 0:
            adhoc_offer = "1145dcc9-2fdc-4ee7-89a4-4f37cabc2374"  # $1 Any Size Coffee - Delivery Eligible
        else:
            adhoc_offer = "b2b74622-5746-4945-be1b-c0044757adf6"  # $1 Large Onion Rings
    else:
        adhoc_offer = "b2b74622-5746-4945-be1b-c0044757adf6"  # $1 Large Onion Rings
    return adhoc_offer


def get_adhoc_offers(purchase_history):
    purchase_history_id = {
        purchase.get("couponID", "n/a"): purchase.get("cart", [])
        for purchase in purchase_history
    }
    adhoc_offer_func = [
        # get_anitta_meal,
        get_ff_og_hb,
        get_sd_ic_hc,
    ]

    adhoc_offers = [
        func(purchase_history_id)
        for func in adhoc_offer_func
    ]
    adhoc_offers = [
        oid
        for oid in adhoc_offers
        if oid != "n/a"
    ]
    return adhoc_offers
