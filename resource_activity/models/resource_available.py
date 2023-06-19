# Copyright 2018 Coop IT Easy SC.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import logging

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class ResourceAvailable(models.Model):
    _name = "resource.available"
    _description = "Resource Available"

    @api.depends("allocation_id", "allocation_id.resource_id")
    def _compute_resource_id(self):
        for record in self:
            if record.allocation_id:
                record.resource_id = record.allocation_id.resource_id

    def _dummy_set_method(self):
        # this is necessary to allow to set the value and store it while
        # allocation_id is not set.
        pass

    @api.model
    def convert_allocation_state(self, state):
        if state == "cancel":
            return "cancelled"
        return "selected"

    @api.depends("allocation_id", "allocation_id.state")
    def _compute_state(self):
        for record in self:
            if record.allocation_id:
                record.state = self.convert_allocation_state(record.allocation_id.state)

    name = fields.Char(related="resource_id.serial_number", string="Name")
    resource_id = fields.Many2one(
        comodel_name="resource.resource",
        string="Resource",
        required=True,
        compute=_compute_resource_id,
        inverse=_dummy_set_method,
        store=True,
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
        compute=_compute_state,
        inverse=_dummy_set_method,
        store=True,
    )

    def write(self, vals):
        # resource_id and state may only be set when allocation_id is not set.
        # once allocation_id is set, these fields are computed from
        # allocation_id.
        allocation_id = self.allocation_id
        if not allocation_id and "allocation_id" in vals:
            allocation_id = self.env["resource.allocation"].browse(
                vals["allocation_id"]
            )
        if allocation_id:
            if (
                "resource_id" in vals
                and vals["resource_id"] != allocation_id.resource_id.id
            ):
                raise ValidationError(
                    _("The resource cannot be changed once an allocation is set")
                )
            if "state" in vals and vals["state"] != self.convert_allocation_state(
                allocation_id.state
            ):
                raise ValidationError(
                    _("The state cannot be changed once an allocation is set")
                )
        return super().write(vals)

    @api.multi
    def action_reserve(self):
        # this code works because it is called from
        # a list view on an activity form after button search_resource
        # was called.
        # In other cases, registration might not be set
        for available_resource in self.filtered(lambda record: record.state == "free"):
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

    @api.multi
    def action_cancel(self):
        self.ensure_one()
        # do not unlink to keep the resource available
        # displayed in the user interface
        if self.allocation_id:
            self.allocation_id.action_cancel()
        return True
