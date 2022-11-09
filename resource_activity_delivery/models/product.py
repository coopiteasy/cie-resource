# Copyright 2021 Coop IT Easy SC
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_delivery = fields.Boolean(string="Delivery")
