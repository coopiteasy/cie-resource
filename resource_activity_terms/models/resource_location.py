# Copyright 2018 Coop IT Easy SC.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResourceLocation(models.Model):
    _inherit = "resource.location"

    terms_ids = fields.One2many("resource.location.terms", "location_id")
