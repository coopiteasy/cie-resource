# Copyright 2018 Coop IT Easy SC.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class AllocateResourceWizard(models.TransientModel):
    _name = "allocate.resource.wizard"
    _description = "Allocate Resource Wizard"

    date_start = fields.Datetime(string="Date Start", required=True)
    date_end = fields.Datetime(string="Date End", required=True)
    resources = fields.Many2many(comodel_name="resource.resource", string="Resources")
    allocation_type = fields.Selection(
        [
            ("booked", "Book"),
            ("option", "Option"),
            ("maintenance", "Maintenance"),
        ],
        string="Allocation type",
        default="booked",
        required=True,
    )
    resource_type = fields.Selection(
        [("resource", "Resource"), ("category", "Category")],
        string="Allocate on",
        default="resource",
        required=True,
    )
    resource_category_id = fields.Many2one(
        comodel_name="resource.category", string="Resource Category"
    )
    booking_allowed = fields.Boolean(
        string="Booking Allowed",
        default=False,
    )
    partner_id = fields.Many2one(
        comodel_name="res.partner", string="Allocate to", required=True
    )
    date_lock = fields.Date(string="Date Lock")
    display_error = fields.Boolean(string="Display error")
    location = fields.Many2one(comodel_name="resource.location", string="Location")

    @api.model
    def default_get(self, fields):
        result = super(AllocateResourceWizard, self).default_get(fields)
        result["resources"] = self._context.get("active_ids", False)

        return result

    @api.onchange("date_start", "date_end", "location", "resource_category_id")
    def onchange_search_fields(self):
        self.booking_allowed = False

    @api.multi
    def search_resources(self):
        if self.resource_type == "resource":
            res = self.resources.check_availabilities(
                self.date_start, self.date_end, self.location
            )
        else:
            res = self.resource_category_id.resources.check_availabilities(
                self.date_start, self.date_end, self.location
            )
        if res:
            self.resources = self.env["resource.resource"].browse(res)
            self.booking_allowed = True
        else:
            self.resources = None
            self.booking_allowed = False

        action = self.env.ref("resource_planning.action_view_allocate_resource")
        return {
            "name": action.name,
            "help": action.help,
            "type": action.type,
            "view_type": action.view_type,
            "view_mode": action.view_mode,
            "target": action.target,
            "res_model": action.res_model,
            "res_id": self.id,
        }

    @api.multi
    def book_resources(self):
        self.ensure_one()
        for resource in self.resources:
            # cf resource.check_availabilities(
            #  this function returns resource.available records
            #  nothing was done with it here
            #  hope book_resources is called right after search_resources

            self.env["resource.allocation"].create(
                {
                    "resource_id": resource.id,
                    "date_start": self.date_start,
                    "date_end": self.date_end,
                    "date_lock": self.date_lock,
                    "state": self.allocation_type,
                    "partner_id": self.partner_id.id,
                    "location": self.location.id,
                }
            )
