# Copyright 2021 Coop IT Easy SC
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


from odoo import fields, models


class ResourceActivity(models.Model):
    _inherit = "resource.activity"

    trainers = fields.Many2many(
        comodel_name="res.partner",
        relation="activity_trainer",
        column1="activity_id",
        column2="trainer_id",
        string="Trainer",
        domain=[("is_trainer", "=", True)],
    )
