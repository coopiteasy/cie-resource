# Copyright 2021 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class ActivityDraftToDoneWizard(models.TransientModel):
    _name = "resource.activity.draft.done.wizard"
    _description = "Resource Activity Draft to Done Wizard"

    @api.multi
    def draft_to_done(self):
        activity = self.env["resource.activity"].browse(
            self._context.get("active_ids")
        )[0]
        activity.set_activity_as_done()
        return {"type": "ir.actions.act_window_close"}
