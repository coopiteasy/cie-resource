# Copyright 2018 Coop IT Easy SC.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class Resource(models.Model):
    _inherit = "resource.resource"

    purchase_date = fields.Date(string="Purchase Date")
    purchase_invoice_ref = fields.Char(string="Purchase Invoice Ref")

    removed_from_stock = fields.Boolean(
        string="Removed From Stock", default=False, track_visibility=True
    )
    stock_removal_date = fields.Date(string="Stock Removal Date", track_visibility=True)
    stock_removal_reason = fields.Selection(
        string="Stock Removal Reason",
        selection=[
            ("sold", "Sold"),
            ("stolen", "Stolen"),
            ("given", "Given"),
            ("broken", "Broken"),
            ("other", "Other"),
        ],
        track_visibility=True,
    )
    selling_price = fields.Float(string="Selling Price", track_visibility=True)
    sale_invoice_ref = fields.Char(string="Sale Invoice Ref", track_visibility=True)

    @api.multi
    def action_remove_from_stock(self):
        self.ensure_one()
        wiz = self.env["resource.stock.removal.wizard"].create(
            {
                "resource_id": self.id,
            }
        )
        return {
            "type": "ir.actions.act_window",
            "name": "Remove %s from Stock" % self.name,
            "view_type": "form",
            "view_mode": "form",
            "res_model": wiz._name,
            "res_id": wiz.id,
            "target": "new",
        }

    @api.multi
    def action_available(self):
        res = super().action_available()
        self.write(
            {
                "removed_from_stock": False,
                "stock_removal_date": False,
                "stock_removal_reason": False,
                "selling_price": False,
                "sale_invoice_ref": False,
            }
        )
        return res
