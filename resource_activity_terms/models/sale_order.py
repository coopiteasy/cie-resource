# Copyright 2018 Coop IT Easy SC.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _default_company_note(self):
        note_id = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("resource_activity_terms.default_sale_note_html_id")
        )
        return self.env["res.company.note"].browse(int(note_id))

    @api.model
    def create(self, vals):
        order = super(SaleOrder, self).create(vals)
        # sets note CONTENT for order location and activity type
        # if none, sets default company note.
        # The note content is translated

        activity = order.activity_id

        if not activity:
            return order

        sale_note = activity.location_id.terms_ids.filtered(
            lambda r: r.note_id.active
            and r.location_id == activity.location_id
            and r.activity_type_id == activity.activity_type
        ).note_id

        if not sale_note:
            sale_note = self._default_company_note()

        content = sale_note.with_context(lang=order.partner_id.lang).content
        order.note_html = content
        return order

    note_html = fields.Html(
        string="Rich Terms and conditions",
    )
