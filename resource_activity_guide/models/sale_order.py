# Copyright 2021 Coop IT Easy SC
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    resource_guide = fields.Boolean(string="Resource Guide")
