# Copyright 2018 Coop IT Easy SC.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ResourceLocation(models.Model):
    _name = "resource.location"
    _inherit = "mail.thread"
    _description = "Resource Location"

    @api.multi
    @api.depends("resources")
    def _compute_available_resources(self):
        for location in self:
            resources = self.env["resource.resource"].search(
                [("location", "=", location.id)]
            )
            location.resource_categories = resources.mapped("category_id")
        return True

    name = fields.Char(string="Name")
    main_location = fields.Boolean(default=False)
    address = fields.Many2one("res.partner", string="Address")
    partner_bank_id = fields.Many2one("res.partner.bank", string="Bank Account")
    customers = fields.One2many(
        comodel_name="res.partner",
        inverse_name="resource_location",
        domain=[("customer", "=", True)],
        string="Customers",
    )
    resources = fields.One2many(
        comodel_name="resource.resource", inverse_name="location", string="Resources"
    )
    users = fields.One2many(
        comodel_name="res.users", inverse_name="resource_location", string="Users"
    )
    resource_categories = fields.Many2many(
        comodel_name="resource.category",
        string="Available Categories",
        compute=_compute_available_resources,
        store=True,
    )
    active = fields.Boolean("Active", default=True, track_visibility="onchange")
