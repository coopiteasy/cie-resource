# Copyright 2018 Coop IT Easy SC.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ResourceResource(models.Model):
    _name = "resource.resource"
    _inherit = ["resource.resource", "mail.thread"]

    @api.model
    def _get_default_location(self):
        location = self.env.user.resource_location
        if not location:
            location = self.env.ref("resource_planning.main_location", False)
        return location

    category_id = fields.Many2one("resource.category", string="Category")
    # todo is this needed ? couldn't it be dealt w/ active field ?
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("available", "Available"),
            ("unavailable", "Unavailable"),
        ],
        string="State",
        default="draft",
    )
    resource_type = fields.Selection(
        default="material",
    )
    calendar_id = fields.Many2one(
        # override resource.resource default function
        default=False,
        required=False,
    )
    allocations = fields.One2many(
        "resource.allocation", "resource_id", string="Booking lines"
    )
    serial_number = fields.Char(string="ID number")
    location = fields.Many2one(
        comodel_name="resource.location",
        string="Location",
        default=_get_default_location,
        required=False,
    )

    _sql_constraints = [
        (
            "name_uniq",
            "unique (name)",
            "The name of the resource must be unique !",
        )
    ]

    @api.multi
    @api.constrains("resource_type", "calendar_id", "user_id")
    def _check_user_type_fields(self):
        for resource in self:
            if resource.resource_type == "user":
                if not resource.calendar_id or not resource.user_id:
                    raise ValidationError(
                        _(
                            "Working Time and User must be set on Human type "
                            "resources."
                        )
                    )

    @api.multi
    def action_unavailable(self):
        self.write({"state": "unavailable"})

    @api.multi
    def action_available(self):
        self.write({"state": "available"})

    @api.multi
    def action_draft(self):
        self.write({"state": "draft"})

    @api.multi
    def check_availabilities(self, date_start, date_end, location):
        # fixme use resource.allocation.get_allocations
        #  resource.available is not defined in this module
        if date_end < date_start:
            raise ValidationError(
                _(
                    "End date is preceding start date. Please "
                    "choose an end date after a start date "
                )
            )

        available_resources = self.filtered(lambda r: r.state == "available")
        if location:
            available_resources = available_resources.filtered(
                lambda r: r.location.id == location.id
            )
        available_resources_ids = available_resources.ids

        conflicting_allocation_domain = [
            ("resource_id", "in", available_resources_ids),
            ("state", "!=", "cancel"),
            "!",
            "|",
            ("date_end", "<=", date_start),
            ("date_start", ">=", date_end),
        ]

        conflicting_allocations = self.env["resource.allocation"].search(
            conflicting_allocation_domain
        )
        unavailable_resources_ids = conflicting_allocations.mapped("resource_id.id")
        for resource_id in unavailable_resources_ids:
            available_resources_ids.remove(resource_id)
        return available_resources_ids
