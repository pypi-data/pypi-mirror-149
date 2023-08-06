from datetime import datetime
from rawquery import RawQuery

from django.conf import settings
from saleboxdjango.lib.api import post
from saleboxdjango.management.commands.lib.log import log
from saleboxdjango.models import KeyValueStore


class SaleboxPushFootfall:
    def __init__(self):
        if not settings.SALEBOX["ANALYTICS"]["SEND"]:
            return

        self.config = self.get_config()
        self.send_footfall()
        self.set_config()

    def get_config(self):
        config = {"last_update": 0}

        # get kvs from db
        kvs = KeyValueStore.objects.filter(key="sync_footfall").first()
        if kvs is not None:
            config = {**config, **kvs.value}

        return config

    def get_now(self):
        return datetime.utcnow().timestamp()

    def send_footfall(self):
        now = self.get_now()

        # bail if the sync has been done recently
        if (
            now - self.config["last_update"] < 60 * 2
        ):  # 2 minutes - hardcoded now, but should be a config value
            return

        sql = """
            SELECT          COUNT(*) AS visitor_count
                            ,DATE_PART('hour', first_seen AT TIME ZONE 'UTC')::int AS hour
                            ,DATE_PART('day', first_seen AT TIME ZONE 'UTC')::int AS day
                            ,DATE_PART('month', first_seen AT TIME ZONE 'UTC')::int AS month
                            ,DATE_PART('year', first_seen AT TIME ZONE 'UTC')::int AS year
            FROM            saleboxdjango_analytic
            WHERE           first_seen >= TIMESTAMP 'yesterday' AT TIME ZONE 'UTC'
            AND             ua_is_bot = false
            GROUP BY        hour, day, month, year;
        """

        rq = RawQuery()
        payload = {"visitors": rq.multiple_rows(sql)}
        r = post("/api/v1/footfall/ecommerce", payload)
        if r.status_code != 200:
            log(
                "sync_footfall",
                f'API call failed: "/api/v1/footfall/ecommerce" status: {r.status_code}',
                "ERROR",
            )
            self.error = True
            return

        if r.status_code == 200:
            self.config["last_update"] = now

    def set_config(self):
        kvs = KeyValueStore.objects.filter(key="sync_footfall").first()
        if kvs is None:
            KeyValueStore(key="sync_footfall", value=self.config).save()
        else:
            kvs.value = self.config
            kvs.save()
