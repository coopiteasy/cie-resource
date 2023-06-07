# Copyright 2020 Coop IT Easy SC
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from datetime import datetime, timedelta

from freezegun import freeze_time

from odoo.exceptions import UserError

from . import test_base


class TestResourceActivity(test_base.TestResourceActivityBase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.registration_1_vals = {
            "attendee_id": cls.partner_demo.id,
            "quantity": 1,
            "quantity_needed": 1,
            "booking_type": "booked",
            "resource_category": cls.mtb_category.id,
            "product_id": cls.bike_product.id,
        }
        cls.registration_2_vals = {
            "attendee_id": cls.partner_demo.id,
            "quantity": 1,
            "quantity_needed": 1,
            "booking_type": "booked",
            "resource_category": cls.mtb_category.id,
            "product_id": cls.bike_product.id,
        }

    def test_compute_available_resources(self):
        activity_obj = self.env["resource.activity"]
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
        self.assertEquals({self.bike_category: 2, self.mtb_category: 2}, categories)

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
        # self.assertEquals(activity.sale_orders.amount_total, 100)

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
                    (0, 0, self.registration_1_vals),
                    (0, 0, self.registration_2_vals),
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
                    (0, 0, self.registration_1_vals),
                    (0, 0, self.registration_2_vals),
                ],
            }
        )
        activity_not_finished.search_all_resources()
        activity_not_finished.reserve_needed_resource()
        activity_not_finished.action_draft_to_sale()
        activity_not_finished.action_done()
        for registration_date_end in activity_not_finished.registrations.mapped(
            "allocations"
        ).mapped("date_end"):
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
                    (0, 0, self.registration_1_vals),
                    (0, 0, self.registration_2_vals),
                ],
            }
        )
        activity_not_finished.search_all_resources()
        activity_not_finished.reserve_needed_resource()
        activity_not_finished.action_draft_to_sale()
        activity_not_finished.action_done()
        for registration_date_end in activity_not_finished.registrations.mapped(
            "allocations"
        ).mapped("date_end"):
            self.assertEqual(date_end, registration_date_end)
        activity_not_finished.unreserve_resources()

    def test_unlink_registrations_raises_user_error_if_not_cancelled(self):
        registration = self.env["resource.activity.registration"].create(
            self.registration_1_vals
        )
        registration.search_resources()
        registration.reserve_needed_resource()
        with self.assertRaises(UserError):
            registration.action_unlink()

    def test_cancel_registration_cancels_allocations(self):
        registration = self.env["resource.activity.registration"].create(
            self.registration_1_vals
        )
        registration.search_resources()
        registration.reserve_needed_resource()
        registration.action_cancel()
        self.assertEquals(registration.state, "cancelled")
        self.assertEquals(registration.quantity_allocated, 0)
        self.assertFalse(registration.resources_available)
        self.assertTrue(
            all(lambda a: a.state == "cancelled" for a in registration.allocations)
        )

    def test_modified_reservations_are_cancelled_by_activity(self):
        date_start = datetime(2023, 1, 1, 16, 0)
        date_end = datetime(2023, 1, 1, 18, 0)

        # book mtb_1
        mtb_1_allocation = self.env["resource.allocation"].create(
            {
                "resource_id": self.mtb_1.id,
                "date_start": date_start,
                "date_end": date_end,
                # "location_id": self.main_location.id,
                # "partner_id": self.partner_demo.id,
            }
        )
        mtb_1_allocation.action_confirm()

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
                    (
                        0,
                        0,
                        {
                            "attendee_id": self.partner_demo.id,
                            "quantity": 1,
                            "quantity_needed": 1,
                            "booking_type": "booked",
                            "resource_category": self.mtb_category.id,
                            "product_id": self.bike_product.id,
                        },
                    ),
                ],
            }
        )
        activity.search_all_resources()
        activity.reserve_needed_resource()
        registration = activity.registrations[0]
        self.assertEqual(registration.state, "booked")
        self.assertEqual(registration.quantity_allocated, 1)
        allocation = registration.allocations[0]
        self.assertEqual(allocation.resource_id, self.mtb_2)
        self.assertEqual(allocation.state, "booked")

        allocation.resource_id = self.mtb_1
        activity.unreserve_resources()
        self.assertEqual(registration.quantity_allocated, 0)
        self.assertEqual(allocation.state, "cancel")

        activity.search_all_resources()
        activity.reserve_needed_resource()
        self.assertEqual(registration.quantity_allocated, 1)

    def test_compute_quantity_allocated(self):
        registration = self.env["resource.activity.registration"].create(
            self.registration_1_vals
        )
        self.assertEquals(registration.quantity_allocated, 0)
        registration.search_resources()
        registration.reserve_needed_resource()
        self.assertEquals(registration.quantity_allocated, 1)

        registration.action_cancel()
        self.assertEquals(registration.quantity_allocated, 0)

        registration.action_draft()
        registration.search_resources()
        registration.reserve_needed_resource()
        self.assertEquals(registration.quantity_allocated, 1)

        registration.allocations.action_cancel()
        self.assertEquals(registration.quantity_allocated, 0)

    def test_compute_state(self):
        activity = self.env["resource.activity"].create(
            {
                "date_start": datetime.today(),
                "resource_allocation_start": datetime.today(),
                "date_end": datetime.today() + timedelta(days=1),
                "resource_allocation_end": datetime.today() + timedelta(days=1),
                "location_id": self.main_location.id,
                "activity_type": self.activity_type.id,
            }
        )
        registration_vals = {
            "resource_activity_id": activity.id,
            "attendee_id": self.partner_demo.id,
            "quantity": 1,
            "quantity_needed": 2,
            "booking_type": "booked",
            "resource_category": self.mtb_category.id,
            "product_id": self.bike_product.id,
        }
        registration = self.env["resource.activity.registration"].create(
            registration_vals
        )
        self.assertEquals(registration.state, "draft")
        registration.search_resources()
        self.assertEquals(registration.state, "available")
        registration.reserve_needed_resource()
        self.assertEquals(registration.state, "booked")

        waiting_registration = self.env["resource.activity.registration"].create(
            registration_vals
        )
        waiting_registration.search_resources()
        self.assertEquals(waiting_registration.state, "waiting")
        waiting_registration.reserve_needed_resource()

        registration.action_cancel()
        self.assertEquals(registration.state, "cancelled")
