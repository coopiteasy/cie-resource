# Copyright 2021 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    sale_note_html_id = fields.Many2one(
        comodel_name="res.company.note",
        string="Rich Terms and Conditions",
        config_parameter="resource_activity_terms.default_sale_note_html_id",
    )
