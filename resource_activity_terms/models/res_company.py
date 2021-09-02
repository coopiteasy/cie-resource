# Copyright 2018 Coop IT Easy SCRLfs.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    sale_note_html_id = fields.Many2one(
        comodel_name="res.company.note",
        string="Default Terms and Conditions",
    )
