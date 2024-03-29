# Copyright 2018 Coop IT Easy SC.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.multi
    def _resource_activity_count(self):
        for partner in self:
            partner.activity_count = len(partner.sudo().resource_activities)

    is_partner = fields.Boolean(string="Partner")
    resource_activities = fields.One2many(
        comodel_name="resource.activity",
        inverse_name="partner_id",
        string="Resource Activities",
    )
    activity_count = fields.Integer(
        string="# of Activities", compute=_resource_activity_count
    )
