# Copyright 2018 Coop IT Easy SC.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResourceActivityType(models.Model):
    _name = "resource.activity.type"
    _description = "Resource Type"

    name = fields.Char(
        string="Type",
        required=True,
        translate=True,
    )
    code = fields.Char(string="Code")
    analytic_account = fields.Many2one(
        "account.analytic.account",
        string="Analytic account",
        groups="analytic.group_analytic_accounting",
    )
    product_ids = fields.Many2many("product.product", string="Product")
    location_ids = fields.Many2many("resource.location", string="Locations")
    active = fields.Boolean("Active", default=True)
