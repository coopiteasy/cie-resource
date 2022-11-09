# Copyright 2021 Coop IT Easy SC
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


from odoo import fields, models


class ResourceLocation(models.Model):
    _inherit = "resource.location"

    trainers = fields.One2many(
        "res.partner",
        "resource_location_trainer",
        domain=[("is_trainer", "=", True)],
        string="Trainers",
    )
