# Copyright 2020 Coop IT Easy SC
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


from datetime import datetime

from odoo.exceptions import ValidationError
from odoo.tests import Form, common


class TestResourcePlanning(common.TransactionCase):
    def setUp(self):
        super(TestResourcePlanning, self).setUp()
        self.main_location = self.browse_ref("resource_planning.main_location")
        # todo use test data rather than demo data
        self.alloc_1 = self.browse_ref("resource_planning.resource_allocation_1_demo")
        self.alloc_2 = self.browse_ref("resource_planning.resource_allocation_2_demo")
        self.alloc_3 = self.browse_ref("resource_planning.resource_allocation_3_demo")
        self.alloc_4 = self.browse_ref("resource_planning.resource_allocation_4_demo")
        self.alloc_5 = self.browse_ref("resource_planning.resource_allocation_5_demo")
        self.alloc_6 = self.browse_ref("resource_planning.resource_allocation_6_demo")

        self.calendar = self.env.ref("resource.resource_calendar_std")
        self.user_1 = self.env["res.users"].create(
            {
                "name": "user - test 01",
                "email": "test01@test.com",
                "login": "test01@test.com",
            }
        )

    def test_get_allocations(self):
        allocation_obj = self.env["resource.allocation"]

        allocations = allocation_obj.get_allocations(
            date_start="2020-11-23 14:30",
            date_end="2020-11-23 16:00",
            location=self.main_location,
        )
        self.assertIn(self.alloc_1, allocations)
        self.assertIn(self.alloc_3, allocations)
        self.assertIn(self.alloc_6, allocations)

        allocations = allocation_obj.get_allocations(
            date_start="2020-11-23 19:30",
            date_end="2020-11-23 20:00",
            location=self.main_location,
        )
        self.assertIn(self.alloc_2, allocations)

        allocations = allocation_obj.get_allocations(
            date_start="2020-11-24 19:30",
            date_end="2020-11-24 20:00",
            location=self.main_location,
        )
        self.assertEquals(len(allocations), 0)

    def test_get_available_categories(self):
        category_obj = self.env["resource.category"]

        categories = category_obj.get_available_categories(
            date_start="2020-11-23 14:30",
            date_end="2020-11-23 16:00",
            location=self.main_location,
        )
        self.assertEquals({}, categories)

        categories = category_obj.get_available_categories(
            date_start="2020-11-23 19:30",
            date_end="2020-11-23 20:00",
            location=self.main_location,
        )
        self.assertEquals({1: 1, 2: 1}, categories)

        categories = category_obj.get_available_categories(
            date_start="2020-11-23 17:00",
            date_end="2020-11-23 17:30",
            location=self.main_location,
        )
        self.assertEquals({1: 2}, categories)

        categories = category_obj.get_available_categories(
            date_start="2020-11-24 19:30",
            date_end="2020-11-24 20:00",
            location=self.main_location,
        )
        self.assertEquals({1: 2, 2: 1}, categories)

    def test_resource_type_constraint_on_material_resource(self):
        self.env["resource.resource"].create(
            {
                "name": "material resource",
                "resource_type": "material",
                "user_id": False,
                "calendar_id": False,
            }
        )

    def test_resource_type_constraint_on_user_resource(self):
        with self.assertRaises(ValidationError):
            self.env["resource.resource"].create(
                {
                    "name": "human resource 1",
                    "resource_type": "user",
                    "user_id": self.user_1.id,
                    "calendar_id": False,
                }
            )

        with self.assertRaises(ValidationError):
            self.env["resource.resource"].create(
                {
                    "name": "human resource 2",
                    "resource_type": "user",
                    "user_id": False,
                    "calendar_id": self.calendar.id,
                }
            )

        self.env["resource.resource"].create(
            {
                "name": "human resource 3",
                "resource_type": "user",
                "user_id": self.user_1.id,
                "calendar_id": self.calendar.id,
            }
        )

    def test_check_resource_allocation_raises_if_conflict(self):
        bike_1 = self.env.ref("resource_planning.resource_resource_bike_1_demo")
        self.env["resource.allocation"].create(
            {
                "resource_id": bike_1.id,
                "date_start": datetime(2023, 1, 1, 12, 0),
                "date_end": datetime(2023, 1, 1, 14, 0),
            }
        )
        with self.assertRaises(ValidationError):
            self.env["resource.allocation"].create(
                {
                    "resource_id": bike_1.id,
                    "date_start": datetime(2023, 1, 1, 13, 0),
                    "date_end": datetime(2023, 1, 1, 14, 30),
                }
            )

        allocation_1 = self.env["resource.allocation"].create(
            {
                "resource_id": bike_1.id,
                "date_start": datetime(2024, 1, 1, 12, 0),
                "date_end": datetime(2024, 1, 1, 14, 0),
            }
        )

        with self.assertRaises(ValidationError):
            allocation_1.date_start = datetime(2023, 1, 1, 11, 0)

        with Form(allocation_1) as allocation_2_form:
            allocation_2_form.date_start = datetime(2023, 1, 1, 11, 0)
            allocation_2_form.date_end = datetime(2023, 1, 1, 11, 30)

        bike_2 = self.env.ref("resource_planning.resource_resource_bike_2_demo")
        allocation_2 = self.env["resource.allocation"].create(
            {
                "resource_id": bike_2.id,
                "date_start": datetime(2023, 1, 1, 12, 0),
                "date_end": datetime(2023, 1, 1, 14, 0),
            }
        )

        with self.assertRaises(ValidationError):
            allocation_2.resource_id = bike_1

    def test_check_resource_allocation_ignore_cancelled(self):
        """
        Test that updating the end date of a cancelled allocation does not
        trigger a conflict error if another non-cancelled allocation exists.
        """
        bike_1 = self.env.ref("resource_planning.resource_resource_bike_1_demo")
        allocation_1 = self.env["resource.allocation"].create(
            {
                "resource_id": bike_1.id,
                "date_start": datetime(2023, 1, 1, 12, 0),
                "date_end": datetime(2023, 1, 1, 14, 0),
                "state": "cancel",
            }
        )
        self.env["resource.allocation"].create(
            {
                "resource_id": bike_1.id,
                "date_start": datetime(2023, 1, 1, 12, 0),
                "date_end": datetime(2023, 1, 1, 14, 0),
                "state": "booked",
            }
        )
        # this should not raise a ValidationError.
        allocation_1.date_end = datetime(2023, 1, 1, 13, 0)
