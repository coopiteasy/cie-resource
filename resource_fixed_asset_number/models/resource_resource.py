from odoo import fields, models


class ResourceResource(models.Model):
    _inherit = "resource.resource"

    fixed_asset_number = fields.Char()
