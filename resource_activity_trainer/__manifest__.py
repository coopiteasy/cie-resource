# Copyright 2021 Coop IT Easy SC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Resource Activity Trainer",
    "version": "12.0.1.1.0",
    "depends": [
        "resource_activity",
    ],
    "author": "Coop IT Easy SC",
    "category": "Resource",
    "website": "https://github.com/coopiteasy/cie-resource",
    "license": "AGPL-3",
    "summary": """
        Add trainers to your activities.
    """,
    "data": [
        "views/res_partner_views.xml",
        "views/resource_activity_views.xml",
        "views/resource_location_views.xml",
    ],
    "installable": True,
    "application": True,
}
