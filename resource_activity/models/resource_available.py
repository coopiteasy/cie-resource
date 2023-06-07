# Copyright 2018 Coop IT Easy SC.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class ResourceAvailable(models.Model):
    _name = "resource.available"
    _description = "Resource Available"

    name = fields.Char(related="resource_id.serial_number", string="Name")
    resource_id = fields.Many2one(
        comodel_name="resource.resource", string="Resource", required=True
    )
    registration_id = fields.Many2one(
        comodel_name="resource.activity.registration", string="Registration"
    )
    allocation_id = fields.Many2one(
        comodel_name="resource.allocation", string="Allocation"
    )
    activity_id = fields.Many2one(
        related="registration_id.resource_activity_id",
        string="Activity",
        readonly=True,
    )
    state = fields.Selection(
        [
            ("free", "Free"),
            ("not_free", "Not free"),
            ("selected", "Selected"),
            ("cancelled", "Cancelled"),
        ],
        string="State",
        readonly=True,
    )

    @api.multi
    def action_reserve(self):
        # this code works because it is called from
        # a list view on an activity form after button search_resource
        # was called.
        # In other cases, registration might not be set
        for available_resource in self:
            if not available_resource.registration_id:
                raise ValueError(
                    "Registration is not set on resource availability record %s."
                    % available_resource.id
                )

            available_resource.allocation_id = self.env["resource.allocation"].create(
                {
                    "resource_id": available_resource.resource_id.id,
                    "partner_id": available_resource.registration_id.attendee_id.id,
                    "date_start": available_resource.registration_id.date_start,
                    "date_end": available_resource.registration_id.date_end,
                    "date_lock": available_resource.registration_id.date_lock,
                    "state": available_resource.registration_id.booking_type,
                    "location": available_resource.registration_id.location_id.id,
                    "activity_registration_id": available_resource.registration_id.id,
                }
            )
            available_resource.state = "selected"
            available_resource.activity_id.registrations.action_refresh()

    @api.multi
    def action_cancel(self):
        self.ensure_one()
        # do not unlink to keep the resource available
        # displayed in the user interface
        self.state = "cancelled"
        if self.allocation_id:
            self.allocation_id.action_cancel()
        return True
