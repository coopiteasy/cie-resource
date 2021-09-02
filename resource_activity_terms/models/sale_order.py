# Copyright 2018 Coop IT Easy SCRLfs.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.model
    def _default_note_html(self):
        note_id = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("resource_activity_terms.default_sale_note_html_id")
        )
        note = self.env["res.company.note"].browse(int(note_id))
        return note.content

    note_html = fields.Html(
        string="Rich Terms and conditions",
        default=lambda self: self._default_note_html(),
    )
