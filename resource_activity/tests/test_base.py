# Copyright 2020 Coop IT Easy SC
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import SavepointCase


class TestResourceActivityBase(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner_demo = cls.env.ref("base.partner_demo")
        cls.main_location = cls.env.ref("resource_planning.main_location")
        cls.bike_category = cls.env.ref("resource_planning.resource_category_bike_demo")
        cls.ebike_category = cls.env.ref(
            "resource_planning.resource_category_ebike_demo"
        )
        cls.mtb_category = cls.env["resource.category"].create({"name": "MTB"})
        cls.bike_product = cls.env.ref(
            "resource_activity.product_product_bike_rent_demo"
        )
        cls.mtb_1 = cls.env["resource.resource"].create(
            {
                "name": "Mountain Bike Test 1",
                "serial_number": "MTBT1",
                "state": "available",
                "category_id": cls.mtb_category.id,
                "location": cls.main_location.id,
            }
        )
        cls.mtb_2 = cls.env["resource.resource"].create(
            {
                "name": "Mountain Bike Test 2",
                "serial_number": "MTBT2",
                "state": "available",
                "category_id": cls.mtb_category.id,
                "location": cls.main_location.id,
            }
        )
        cls.activity_type = cls.env.ref(
            "resource_activity.resource_activity_type_tour_demo"
        )
