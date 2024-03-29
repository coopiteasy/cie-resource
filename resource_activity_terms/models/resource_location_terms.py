# Copyright 2018 Coop IT Easy SC.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResourceLocationTerms(models.Model):
    _name = "resource.location.terms"
    _description = "Resource Location Terms"

    _sql_constraints = [
        (
            # Constraint unique identifier
            "resource_location_terms_location_activity_terms_note_uq",
            "UNIQUE (location_id, activity_type_id)",  # Constraint SQL syntax
            "Location and Activity Type must be unique.",  # Message
        ),
    ]

    location_id = fields.Many2one(
        comodel_name="resource.location",
        string="Location",
    )
    activity_type_id = fields.Many2one(
        comodel_name="resource.activity.type",
        string="Activity Type",
        required=True,
    )
    terms_id = fields.Many2one(
        comodel_name="res.company.terms",
        string="Terms and Conditions",
        help="Terms and Conditions related to this location",
    )
    note_id = fields.Many2one(
        comodel_name="res.company.note",
        string="Sale note",
        help="Sale note related to this location",
    )
    bike_number_display = fields.Selection(
        selection=[
            ("list", "List of Bicycles"),
            ("type", "Number of Bicycles by type"),
        ],
        string="Bike Number Display",
    )
