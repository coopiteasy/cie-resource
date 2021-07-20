# -*- coding: utf-8 -*-
# Copyright 2018 Coop IT Easy SCRLfs.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.model
    def _default_note_html(self):
        return self.env.user.company_id.sale_note_html_id

    note_html_id = fields.Many2one(
        comodel_name="res.company.note",
        string="Terms and conditions",
    )

    @api.model
    def create(self, vals):
        sale_order = super(SaleOrder, self).create(vals)
        sale_order._set_note_html_id()
        return sale_order

    @api.model
    def _set_note_html_id(self):
        self.ensure_one()
        if self.activity_id:
            activity = self.activity_id
            sale_note_html_id = (
                activity.location_id.terms_ids.filtered(
                    lambda r: r.note_id.active
                          and r.location_id == activity.location_id
                          and r.activity_type_id == activity.activity_type
                ).note_id
                or self._default_note_html()
            )
            self.note_html_id = sale_note_html_id

