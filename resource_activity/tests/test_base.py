# Copyright 2020 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


from odoo.tests import common


class TestResourceActivityBase(common.TransactionCase):
    def setUp(self):
        super(TestResourceActivityBase, self).setUp()
        self.partner_demo = self.browse_ref("base.partner_demo")
        self.main_location = self.browse_ref("resource_planning.main_location")
        self.bike_category = self.browse_ref(
            "resource_planning.resource_category_bike_demo"
        )
        self.ebike_category = self.browse_ref(
            "resource_planning.resource_category_ebike_demo"
        )
        self.mtb_category = self.env["resource.category"].create({"name": "VTT"})
        self.bike_product = self.browse_ref(
            "resource_activity.product_product_bike_rent_demo"
        )
        self.mtb_1 = self.env["resource.resource"].create(
            {
                "name": "Mountain Bike 3",
                "serial_number": "MTB3",
                "state": "available",
                "category_id": self.mtb_category.id,
                "location": self.main_location.id,
            }
        )
        self.mtb_2 = self.env["resource.resource"].create(
            {
                "name": "Mountain Bike 4",
                "serial_number": "MTB4",
                "state": "available",
                "category_id": self.mtb_category.id,
                "location": self.main_location.id,
            }
        )
        self.activity_type = self.browse_ref(
            "resource_activity.resource_activity_type_tour_demo"
        )
