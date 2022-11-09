# Copyright 2020 Coop IT Easy SC
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


from odoo.exceptions import ValidationError
from odoo.tests import common


class TestResourcePlanning(common.TransactionCase):
    def setUp(self):
        super(TestResourcePlanning, self).setUp()
        self.main_location = self.browse_ref("resource_planning.main_location")
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
