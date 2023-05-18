# Copyright 2020 Coop IT Easy SC
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from datetime import datetime

from odoo.tests import common


class TestResourcePlanning(common.TransactionCase):
    def setUp(self):
        super(TestResourcePlanning, self).setUp()
        self.main_location = self.browse_ref("resource_planning.main_location")
        self.test_category = self.env["resource.category"].create(
            {"name": "Test category"}
        )
        self.test_bike_1 = self.env["resource.resource"].create(
            {
                "name": "Test Bike 1",
                "serial_number": "TB1",
                "state": "available",
                "category_id": self.test_category.id,
                "location": self.main_location.id,
            }
        )

        self.partner_demo = self.env.ref("base.partner_demo")

    def test_allocate_resource_wizard_book_resource(self):
        allocation_obj = self.env["resource.allocation"]
        date_start = datetime(2023, 1, 1, 1, 0)
        date_end = datetime(2023, 1, 1, 2, 0)

        self.assertFalse(
            allocation_obj.get_allocations(
                date_start,
                date_end,
                self.main_location,
                resource=self.test_bike_1,
            )
        )

        wizard = self.env["allocate.resource.wizard"].create(
            {
                "date_start": date_start,
                "date_end": date_end,
                "location": self.main_location.id,
                "resource_type": "resource",
                "partner_id": self.partner_demo.id,
                "allocation_type": "booked",
            }
        )
        wizard.resources += self.test_bike_1
        wizard.search_resources()
        self.assertTrue(len(wizard.resources) > 0)
        self.assertTrue(wizard.booking_allowed)

        wizard.book_resources()
        self.assertTrue(
            allocation_obj.get_allocations(
                date_start,
                date_end,
                self.main_location,
                resource=self.test_bike_1,
            )
        )

    def test_allocate_resource_wizard_book_category(self):
        allocation_obj = self.env["resource.allocation"]
        date_start = datetime(2023, 1, 1, 1, 0)
        date_end = datetime(2023, 1, 1, 2, 0)

        self.assertFalse(
            allocation_obj.get_allocations(
                date_start,
                date_end,
                self.main_location,
                category=self.test_category,
            )
        )

        wizard = self.env["allocate.resource.wizard"].create(
            {
                "date_start": datetime(2023, 1, 1, 1, 0),
                "date_end": datetime(2023, 1, 1, 2, 0),
                "resource_type": "category",
                "location": self.main_location.id,
                "partner_id": self.partner_demo.id,
                "allocation_type": "booked",
                "resource_category_id": self.test_category.id,
            }
        )
        wizard.search_resources()
        self.assertTrue(len(wizard.resources) > 0)
        self.assertTrue(wizard.booking_allowed)

        wizard.book_resources()

        self.assertTrue(
            allocation_obj.get_allocations(
                date_start, date_end, self.main_location, category=self.test_category
            )
        )
