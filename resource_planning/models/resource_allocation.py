# Copyright 2018 Coop IT Easy SC.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class ResourceAllocation(models.Model):
    _name = "resource.allocation"
    _description = "Resource Allocation"

    @api.constrains("resource_id", "date_start", "date_end", "location")
    def _check_resource_allocations(self):
        for allocation in self:
            if allocation.state == "cancel":
                # cancelled allocations never conflict and must thus be ignored.
                continue
            other_allocations = (
                self.get_allocations(
                    allocation.date_start,
                    allocation.date_end,
                    allocation.location,
                    resource=allocation.resource_id,
                )
                - allocation
            )
            if other_allocations:
                _logger.warning(
                    "%s conflicts with %s" % (allocation, other_allocations)
                )
                raise ValidationError(
                    _("There is already an allocation for resource %s from %s to %s")
                    % (
                        allocation.serial_number,
                        allocation.date_start,
                        allocation.date_end,
                    )
                )

    name = fields.Many2one(string="Name", related="partner_id")
    resource_id = fields.Many2one("resource.resource", string="Resource", required=True)
    serial_number = fields.Char(
        related="resource_id.serial_number", string="Serial number"
    )
    resource_category_id = fields.Many2one(
        related="resource_id.category_id",
        string="Resource Category",
        store=True,
    )
    date_start = fields.Datetime(string="Date Start")
    date_end = fields.Datetime(string="Date End")
    state = fields.Selection(
        [
            ("booked", "Booked"),
            ("option", "Option"),
            ("maintenance", "Maintenance"),
            ("cancel", "Cancel"),
        ],
        string="State",
        default="option",
    )
    date_lock = fields.Date(
        string="Lock Date",
        help="If the booking type is option, it should be confirmed before "
        "the lock date expire",
    )
    partner_id = fields.Many2one(comodel_name="res.partner", string="Partner")
    location = fields.Many2one("resource.location", string="Location")

    @api.multi
    def action_confirm(self):
        self.write({"state": "booked", "date_lock": False})

    @api.multi
    def action_cancel(self):
        self.write({"state": "cancel"})

    @api.multi
    def action_option(self):
        self.write({"state": "option"})

    @api.model
    def get_allocations(
        self, date_start, date_end, location, resource=None, category=None
    ):
        """
        :param date_start: datetime
        :param date_end: datetime
        :param location: filter on allocation location
        :param resource: filter on resource allocation
        :param category: filter on resource category allocation
        :return: resource allocations intersecting with date_start to date_end
        """

        domain = [
            ("location", "=", location.id),
            ("state", "!=", "cancel"),
            "!",
            "|",
            ("date_end", "<=", date_start),
            ("date_start", ">=", date_end),
        ]

        if resource is not None:
            domain.append(("resource_id", "=", resource.id))

        if category is not None:
            domain.append(("resource_id.category_id", "=", category.id))

        return self.env["resource.allocation"].search(domain)
