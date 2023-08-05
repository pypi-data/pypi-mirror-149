import json
import random
import pandas as pd


class NationalOffer:
    def __init__(self, offer):
        group = offer.get("group", "n/a")
        sanity_id = offer.get("sanity_id", "n/a")
        name = offer.get("name", "n/a")
        tier = offer.get("tier", "n/a")
        lapsed = offer.get("lapsed", "n/a")
        cluster = offer.get("cluster", "n/a")
        test_group_negate = offer.get("test_group_negate", "n/a").split("|")
        prob = offer.get("prob", 0)
        all_tier = ["1_Personalized", "2_Personalized"]
        all_lapsed = ["0", "30", "60", "90"]
        all_cluster = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        assert tier in all_tier + ["all"], "Incorrect tier value"
        assert lapsed in all_lapsed + ["all"], "Incorrect lapsed value"
        assert cluster in all_cluster + ["all"], "Incorrect cluster value"
        assert 0 < prob <= 1, "Incorrect prob value"
        self.group = group
        self.sanity_id = sanity_id
        self.name = name
        self.tier = tier
        self.lapsed = lapsed
        self.cluster = cluster
        self.test_group_negate = test_group_negate
        self.prob = prob

    def __repr__(self):
        return json.dumps({
            "group": self.group,
            "sanity_id": self.sanity_id,
            "name": self.name,
            "tier": self.tier,
            "lapsed": self.lapsed,
            "cluster": self.cluster,
            "test_group_negate": self.test_group_negate,
            "prob": self.prob,
        })

    def satisfy_rule(self, tier=None, lapsed=None, cluster=None, test_group=None):
        return True if all([
            self.is_tier(tier),
            self.has_lapsed(lapsed),
            self.has_cluster(cluster),
            self.is_test_group(test_group),
        ]) else False

    def is_tier(self, tier):
        return True if tier is None or self.tier == "all" or tier == self.tier else False

    def has_lapsed(self, lapsed):
        return True if lapsed is None or self.lapsed == "all" or lapsed == self.lapsed else False

    def has_cluster(self, cluster):
        return True if cluster is None or self.cluster == "all" or cluster == self.cluster else False

    def is_test_group(self, test_group):
        return True if test_group is None \
            or "none" in self.test_group_negate \
            or test_group not in self.test_group_negate \
            else False


class NationalOfferGroup:
    def __init__(self, group):
        self.group = self.load_dict(group)
        self.num = len(self.group)

    def pick(self, tier=None, lapsed=None, cluster=None, test_group=None):
        offers = [
            offer for offer in self.group
            if offer.satisfy_rule(tier=tier, lapsed=lapsed, cluster=cluster, test_group=test_group)
        ]
        probs = [offer.prob for offer in offers]
        if len(offers) > 0:
            selected_offer = random.choices(population=offers, weights=probs, k=1)[0]
            selected_id = selected_offer.sanity_id
            selected_name = selected_offer.name
        else:
            selected_id = "n/a"
            selected_name = "n/a"
        return selected_id, selected_name

    def list_offers(self, attr="id", tier=None, lapsed=None, cluster=None, test_group=None):
        offers = [
            offer for offer in self.group
            if offer.satisfy_rule(tier=tier, lapsed=lapsed, cluster=cluster, test_group=test_group)
        ]
        if attr == "id" or attr == "sanity_id":
            offer_attr = list(set([offer.sanity_id for offer in offers]))
        elif attr == "name":
            offer_attr = list(set([offer.name for offer in offers]))
        else:
            raise NotImplementedError()
        return offer_attr

    def load_dict(self, group):
        return [
            NationalOffer(offer=offer)
            for offer in group
        ]


class NationalOfferPool:
    def __init__(self, pool, source="csv"):
        if source == "csv":
            self.pool = self.load_csv(pool)
        elif source == "dict":
            self.pool = self.load_dict(pool)
        else:
            raise NotImplementedError()
        self.max_num = len(self.pool)

    def pick(self, tier=None, lapsed=None, cluster=None, test_group=None):
        return [
            group.pick(tier=tier, lapsed=lapsed, cluster=cluster, test_group=test_group)
            for group in self.pool
        ]

    def list_offers(self, attr="id", tier=None, lapsed=None, cluster=None, test_group=None):
        return [
            offer
            for group in self.pool
            for offer in group.list_offers(attr=attr, tier=tier, lapsed=lapsed, cluster=cluster, test_group=test_group)
        ]

    def load_csv(self, pool):
        df = pd.read_csv(pool)
        assert all(df.groupby(by=["group", "tier", "lapsed", "cluster", "test_group_negate"]).sum("prob").values == 1)
        assert not df.isna().any().any()
        all_groups = df["group"].unique()
        dict_pool = [
            df[df["group"] == group].to_dict(orient="records")
            for group in all_groups
        ]
        return self.load_dict(pool=dict_pool)

    def load_dict(self, pool):
        return [
            NationalOfferGroup(group=group)
            for group in pool
        ]

# class PromotionalOffer:
#     def __init__(self, offer):
#
#
# class PromotionalOfferPool:
