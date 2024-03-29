# Copyright 2018 Coop IT Easy SC.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResourceActivityLang(models.Model):
    _name = "resource.activity.lang"
    _description = "Resource Language"

    name = fields.Char(
        string="Lang",
        required=True,
        translate=True,
    )
    code = fields.Char(string="Code")
    active = fields.Boolean("Active", default=True)
