# Copyright 2020 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp.addons.resource_activity.tests import test_base
from datetime import datetime, timedelta


class TestSaleOrder(test_base.TestResourceActivityBase):
    def setUp(self):
        super(TestSaleOrder, self).setUp()
        company = self.env.user.company_id

        self.default_terms = self.env["res.company.note"].create(
            {
                "company_id": company.id,
                "name": "Default terms",
                "content": "Default company terms content",
            }
        )
        company.sale_note_html_id = self.default_terms
        self.location_terms = self.browse_ref(
            "resource_activity_terms.res_company_note_demo"
        )
        # self.location_terms = self.env["res.company.note"].create(
        #     {
        #         "company_id": company.id,
        #         "name": "Location terms",
        #         "content": "Location_specific terms content",
        #     }
        # )
        # self.env["resource.location.terms"].create(
        #     {
        #         "location_id": self.main_location.id,
        #         "activity_type_id": self.activity_type.id,
        #         "note_id": self.location_terms.id,
        #     }
        # )

    def test_default_note_assigned_to_sale_order(self):
        date_start = datetime.now()
        date_end = date_start + timedelta(hours=2)
        some_activity = self.env["resource.activity.type"].create(
            {"name": "Some Test Activity"}
        )
        registration = {
            "attendee_id": self.partner_demo.id,
            "quantity": 2,
            "quantity_needed": 2,
            "booking_type": "booked",
            "resource_category": self.bike_category.id,
            "product_id": self.bike_product.id,
        }
        activity = self.env["resource.activity"].create(
            {
                "date_start": date_start,
                "date_end": date_end,
                # set by _onchange_allocation_start in real life
                "resource_allocation_start": date_start,
                # set by _onchange_allocation_end in real life
                "resource_allocation_end": date_end,
                "location_id": self.main_location.id,
                "registrations": [(0, 0, registration)],
                "activity_type": some_activity.id,
            }
        )
        activity.create_sale_order()
        # should be only one sale order
        sale_order = activity.sale_orders
        self.assertEquals(sale_order.note_html_id, self.default_terms)

    def test_location_note_assigned_to_sale_order(self):
        date_start = datetime.now()
        date_end = date_start + timedelta(hours=2)
        registration = {
            "attendee_id": self.partner_demo.id,
            "quantity": 2,
            "quantity_needed": 2,
            "booking_type": "booked",
            "resource_category": self.bike_category.id,
            "product_id": self.bike_product.id,
        }
        activity = self.env["resource.activity"].create(
            {
                "date_start": date_start,
                "date_end": date_end,
                # set by _onchange_allocation_start in real life
                "resource_allocation_start": date_start,
                # set by _onchange_allocation_end in real life
                "resource_allocation_end": date_end,
                "location_id": self.main_location.id,
                "registrations": [(0, 0, registration)],
                "activity_type": self.activity_type.id,
            }
        )
        activity.create_sale_order()
        # should be only one sale order
        sale_order = activity.sale_orders
        self.assertEquals(sale_order.note_html_id, self.location_terms)
