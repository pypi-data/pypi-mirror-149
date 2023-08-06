from datetime import datetime
from math import ceil

from saleboxdjango.lib.api import get
from saleboxdjango.management.commands.lib.log import log
from saleboxdjango.models import ProductVariant, KeyValueStore


class SaleboxPullInventory:
    def __init__(self):
        self.config = self.get_config()
        self.process_all()
        self.process_recent()
        self.set_config()

    def get_config(self):
        config = {"all": 0, "recent": 0}

        # get kvs from db
        kvs = KeyValueStore.objects.filter(key="sync_inventory").first()
        if kvs is not None:
            config = {**config, **kvs.value}

        return config

    def get_now(self):
        return datetime.utcnow().timestamp()

    def process_all(self):
        now = self.get_now()

        # bail if the sync has been done recently
        if (
            now - self.config["all"] < 60 * 60 * 6
        ):  # 6 hours - hardcoded now, but should be a config value
            return

        # retrieve the entire inventory
        r = get("/api/v1/inventory", {})
        if r.status_code != 200:
            log(
                "sync_inventory",
                f"API call failed, status: {r.status_code}, text: {r.text}",
                "ERROR",
            )
            return

        # update inventory database
        self.update_inventory(r.json()["inventory"])

        # set all AND recent timestamps
        self.config["all"] = now
        self.config["recent"] = now
        return

    def process_recent(self):
        now = self.get_now()

        # bail if the sync has been done recently
        diff = ceil(now - self.config["recent"])
        if diff < 30:  # 1 minute - hardcoded now, but should be a config value
            return

        # retrieve inventory changes: diff + 60 seconds
        r = get("/api/v1/inventory", {"seconds": diff + 60})
        if r.status_code != 200:
            log(
                "sync_inventory",
                f"API call failed, status: {r.status_code}, text: {r.text}",
                "ERROR",
            )
            return

        # update inventory database
        self.update_inventory(r.json()["inventory"])

        # set recent timestamp only
        self.config["recent"] = now
        return

    def set_config(self):
        kvs = KeyValueStore.objects.filter(key="sync_inventory").first()
        if kvs is None:
            KeyValueStore(key="sync_inventory", value=self.config).save()
        else:
            kvs.value = self.config
            kvs.save()

    def update_inventory(self, data):
        if len(data) == 0:
            return

        # update values in database
        lookup = {d[0]: d[1] for d in data}
        variants = ProductVariant.objects.filter(id__in=[d[0] for d in data])
        for pv in variants:
            if pv.stock_count != lookup[pv.id]:
                pv.stock_count = lookup[pv.id]
                pv.save()
