# Copyright 2021 Coop IT Easy SC
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


from odoo import fields, models


class ResourceLocation(models.Model):
    _inherit = "resource.location"

    guides = fields.One2many(
        "res.partner",
        "resource_location_guide",
        domain=[("is_guide", "=", True)],
        string="Guides",
    )
