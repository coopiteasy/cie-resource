# Copyright 2018 Coop IT Easy SCRLfs.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class CheckResourceWizard(models.TransientModel):
    _name = "check.resource.availabilities.wizard"
    _description = "Check Resource Availabilities Wizard"

    date_start = fields.Datetime(string="Date Start", required=True)
    date_end = fields.Datetime(string="Date End", required=True)
    multi_resource_category_id = fields.Many2many(
        "resource.category", string="Resource Category"
    )
    location = fields.Many2one(
        comodel_name="resource.location", string="Location", required=True
    )

    @api.multi
    def check_resource_availabilities(self):
        res = []
        if not self.multi_resource_category_id:
            raise ValidationError(_("Please choose at least one category"))

        self.env["resource.resource"].check_dates(self.date_start, self.date_end)

        for category in self.multi_resource_category_id:
            res.extend(
                category.resources.check_availabilities(
                    self.date_start, self.date_end, self.location
                )
            )

        action = self.env.ref("resource.action_resource_resource_tree")

        return {
            "name": action.name,
            "help": action.help,
            "type": action.type,
            "view_type": action.view_type,
            "view_mode": action.view_mode,
            "target": action.target,
            "context": "{'search_default_resource_category': 1}",
            "res_model": action.res_model,
            "domain": [("id", "in", res)],
        }
