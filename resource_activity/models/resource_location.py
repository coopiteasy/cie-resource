# -*- coding: utf-8 -*-
# Copyright 2018 Coop IT Easy SCRLfs.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResourceLocation(models.Model):
    _inherit = "resource.location"
    trainers = fields.One2many(
        "res.partner",
        "resource_location_trainer",
        domain=[("is_trainer", "=", True)],
        string="Trainers",
    )
