# Copyright 2020 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from datetime import datetime, timedelta

from freezegun import freeze_time

from . import test_base


class TestResourceActivity(test_base.TestResourceActivityBase):
    def setUp(self):
        super().setUp()

        self.registration_1 = {
            "attendee_id": self.partner_demo.id,
            "quantity": 1,
            "quantity_needed": 1,
            "booking_type": "booked",
            "resource_category": self.mtb_category.id,
            "product_id": self.bike_product.id,
        }
        self.registration_2 = {
            "attendee_id": self.partner_demo.id,
            "quantity": 1,
            "quantity_needed": 1,
            "booking_type": "booked",
            "resource_category": self.mtb_category.id,
            "product_id": self.bike_product.id,
        }

    def test_compute_available_resources(self):
        activity_obj = self.env["resource.activity"]
        # todo test should not rely on resource allocation demo data
        #   from other module. It should rely only on basic entity
        #   demo data
        activity = activity_obj.create(
            {
                "date_start": "2020-11-23 14:30",
                "date_end": "2020-11-23 16:00",
                "location_id": self.main_location.id,
                "activity_type": self.activity_type.id,
            }
        )
        self.assertEquals(len(activity.available_category_ids), 1)

        activity = activity_obj.create(
            {
                "date_start": "2020-11-23 19:30",
                "date_end": "2020-11-23 20:00",
                "location_id": self.main_location.id,
                "activity_type": self.activity_type.id,
            }
        )
        categories = {
            av_categ.category_id: av_categ.nb_resources
            for av_categ in activity.available_category_ids
        }

        self.assertEquals(
            {
                self.bike_category: 1,
                self.ebike_category: 1,
                self.mtb_category: 2,
            },
            categories,
        )

        activity = activity_obj.create(
            {
                "date_start": "2020-11-23 17:00",
                "date_end": "2020-11-23 17:30",
                "location_id": self.main_location.id,
                "activity_type": self.activity_type.id,
            }
        )
        categories = {
            av_categ.category_id: av_categ.nb_resources
            for av_categ in activity.available_category_ids
        }
        self.assertEquals(
            {self.bike_category: 2, self.mtb_category: 2}, categories
        )

        activity = activity_obj.create(
            {
                "date_start": "2020-11-24 19:30",
                "date_end": "2020-11-24 20:00",
                "location_id": self.main_location.id,
                "activity_type": self.activity_type.id,
            }
        )
        categories = {
            av_categ.category_id: av_categ.nb_resources
            for av_categ in activity.available_category_ids
        }
        self.assertEquals(
            {
                self.bike_category: 2,
                self.ebike_category: 1,
                self.mtb_category: 2,
            },
            categories,
        )

    def test_activity_w_booked_resources(self):
        date_start = datetime.now()
        date_end = date_start + timedelta(hours=2)

        registration = {
            "attendee_id": self.partner_demo.id,
            "quantity": 2,
            "quantity_needed": 2,
            "booking_type": "booked",
            "resource_category": self.mtb_category.id,
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
                "activity_type": self.activity_type.id,
                "registrations": [(0, 0, registration)],
            }
        )

        activity.search_all_resources()
        activity.reserve_needed_resource()

        activity.create_sale_order()
        sale_order = activity.sale_orders
        self.assertEquals(len(sale_order.order_line), 1)
        # not sure when tax is applied in test or not
        self.assertEquals(activity.sale_orders.amount_total, 100)

    def test_state_changes_when_action_done(self):
        # Test that update_resource_registration_date_end does nothing
        # when activity date_end is past
        date_start = datetime.now() - timedelta(days=2)
        date_end = date_start + timedelta(days=4)

        activity = self.env["resource.activity"].create(
            {
                "date_start": date_start,
                "date_end": date_end,
                # set by _onchange_allocation_start in real life
                "resource_allocation_start": date_start,
                # set by _onchange_allocation_end in real life
                "resource_allocation_end": date_end,
                "location_id": self.main_location.id,
                "activity_type": self.activity_type.id,
                "registrations": [
                    (0, 0, self.registration_1),
                    (0, 0, self.registration_2),
                ],
            }
        )
        # activity.action_draft()
        activity.action_draft_to_sale()
        activity.action_done()
        self.assertEqual(activity.state, "done")

    @freeze_time("2022-2-2 12:00:01")
    def test_update_resource_registration_date_end_when_action_done(self):
        date_start = datetime.now() - timedelta(days=2)
        date_end = date_start + timedelta(days=4)

        activity_not_finished = self.env["resource.activity"].create(
            {
                "date_start": date_start,
                "date_end": date_end,
                # set by _onchange_allocation_start in real life
                "resource_allocation_start": date_start,
                # set by _onchange_allocation_end in real life
                "resource_allocation_end": date_end,
                "location_id": self.main_location.id,
                "activity_type": self.activity_type.id,
                "registrations": [
                    (0, 0, self.registration_1),
                    (0, 0, self.registration_2),
                ],
            }
        )
        activity_not_finished.search_all_resources()
        activity_not_finished.reserve_needed_resource()
        activity_not_finished.action_draft_to_sale()
        activity_not_finished.action_done()
        for (
            registration_date_end
        ) in activity_not_finished.registrations.mapped("allocations").mapped(
            "date_end"
        ):
            self.assertEqual(datetime.now(), registration_date_end)
        activity_not_finished.unreserve_resources()

    @freeze_time("2022-2-2 12:00:01")
    def test_no_update_resource_registration_date_end_when_action_done_after_date_end(
        self,
    ):
        date_start = datetime.now() - timedelta(days=4)
        date_end = date_start + timedelta(days=2)

        activity_not_finished = self.env["resource.activity"].create(
            {
                "date_start": date_start,
                "date_end": date_end,
                # set by _onchange_allocation_start in real life
                "resource_allocation_start": date_start,
                # set by _onchange_allocation_end in real life
                "resource_allocation_end": date_end,
                "location_id": self.main_location.id,
                "activity_type": self.activity_type.id,
                "registrations": [
                    (0, 0, self.registration_1),
                    (0, 0, self.registration_2),
                ],
            }
        )
        activity_not_finished.search_all_resources()
        activity_not_finished.reserve_needed_resource()
        activity_not_finished.action_draft_to_sale()
        activity_not_finished.action_done()
        for (
            registration_date_end
        ) in activity_not_finished.registrations.mapped("allocations").mapped(
            "date_end"
        ):
            self.assertEqual(date_end, registration_date_end)
        activity_not_finished.unreserve_resources()
