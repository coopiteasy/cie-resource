# Copyright 2018 Coop IT Easy SCRLfs.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResourceActivityTheme(models.Model):
    _name = "resource.activity.theme"
    _description = "Resource Theme"

    name = fields.Char(
        string="Type",
        required=True,
        translate=True,
    )
    code = fields.Char(string="Code")
    active = fields.Boolean("Active", default=True)
