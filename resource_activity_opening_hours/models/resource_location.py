# Copyright 2018 Coop IT Easy SC.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResourceLocation(models.Model):
    _inherit = "resource.location"

    opening_hours_ids = fields.Many2many(
        "activity.opening.hours", string="Opening Hours"
    )
