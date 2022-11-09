# Copyright 2021 Coop IT Easy SC
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class CancelSaleOrderWizard(models.TransientModel):
    _name = "cancel.sale.order.wizard"
    _description = "Cancel Sale Order Wizard"

    @api.multi
    def cancel_sale_order(self):
        activity = self.env["resource.activity"].browse(
            self._context.get("active_ids")
        )[0]
        for sale_order in activity.sale_orders:
            sale_order.with_context(activity_action=True).action_cancel()

        return {"type": "ir.actions.act_window_close"}
