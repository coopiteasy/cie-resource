# Copyright 2020 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


from odoo.tests import common


class TestResourceActivityBase(common.TransactionCase):
    def setUp(self):
        super(TestResourceActivityBase, self).setUp()
        self.partner_demo = self.browse_ref("base.partner_demo")
        self.bike_category = self.browse_ref(
            "resource_planning.resource_category_bike_demo"
        )
        self.bike_product = self.browse_ref(
            "resource_activity.product_product_bike_rent_demo"
        )
        self.main_location = self.browse_ref("resource_planning.main_location")
        self.activity_type = self.browse_ref(
            "resource_activity.resource_activity_type_tour_demo"
        )
