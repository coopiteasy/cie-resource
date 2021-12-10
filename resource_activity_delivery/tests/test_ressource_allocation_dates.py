# Copyright 2021 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from datetime import datetime, timedelta

from odoo.fields import Datetime
from odoo.tests import Form

from odoo.addons.resource_activity.tests.test_base import (
    TestResourceActivityBase,
)


class TestAllocationDates(TestResourceActivityBase):
    def setUp(self):
        super().setUp()
        self.delivery_product = self.browse_ref(
            "resource_activity_delivery.product_product_delivery_demo"
        )

    def test_resource_allocation_dates_no_delivery(self):
        date_start = datetime.now()
        date_end = datetime.now() + timedelta(hours=1)
        with Form(self.env["resource.activity"]) as activity:
            activity.date_start = date_start
            activity.date_end = date_end
            activity.activity_type = self.activity_type

        self.assertEquals(activity.date_start, activity.resource_allocation_start)
        self.assertEquals(activity.date_end, activity.resource_allocation_end)

    def test_resource_allocation_dates_on_delivery_whole_day(self):
        date_start = datetime.now()
        date_end = date_start + timedelta(hours=1)
        delivery_time = date_start - timedelta(minutes=30)
        pickup_time = date_end + timedelta(minutes=30)

        with Form(self.env["resource.activity"]) as activity:
            activity.date_start = date_start
            activity.date_end = date_end
            activity.need_delivery = True
            activity.delivery_product_id = self.delivery_product
            activity.delivery_place = "departure place"
            activity.delivery_time = delivery_time
            activity.pickup_place = "pickup place"
            activity.pickup_time = pickup_time
            activity.activity_type = self.activity_type

        date_start_midnight = delivery_time.replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        date_end_next_midnight = (pickup_time + timedelta(days=1)).replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        # activity fields are strings since they come from Form and not
        # RecordSet
        self.assertEquals(
            date_start_midnight,
            Datetime.to_datetime(activity.resource_allocation_start),
        )
        self.assertEquals(
            date_end_next_midnight,
            Datetime.to_datetime(activity.resource_allocation_end),
        )

    def test_resource_allocation_dates_on_delivery_set_span(self):
        date_start = datetime.now()
        date_end = date_start + timedelta(hours=1)
        delivery_time = date_start - timedelta(minutes=30)
        pickup_time = date_end + timedelta(minutes=30)

        with Form(self.env["resource.activity"]) as activity:
            activity.date_start = date_start
            activity.date_end = date_end
            activity.need_delivery = True
            activity.delivery_product_id = self.delivery_product
            activity.delivery_place = "departure place"
            activity.delivery_time = delivery_time
            activity.pickup_place = "pickup place"
            activity.pickup_time = pickup_time
            activity.activity_type = self.activity_type
            activity.set_allocation_span = True

        expected_allocation_start = date_start - timedelta(minutes=90)
        expected_allocation_end = date_end + timedelta(minutes=90)
        # activity fields are strings since they come from Form and not
        # RecordSet
        self.assertEquals(
            Datetime.to_string(expected_allocation_start),
            activity.resource_allocation_start,
        )
        self.assertEquals(
            Datetime.to_string(expected_allocation_end),
            activity.resource_allocation_end,
        )
