# Copyright 2021 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    is_trainer = fields.Boolean(string="Trainer")
    # todo rename trainer_location_id
    resource_location_trainer = fields.Many2one(
        comodel_name="resource.location", string="Trainer location"
    )
