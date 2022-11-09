# Copyright 2021 Coop IT Easy SC
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Resource Activity Opening Hours",
    "version": "12.0.1.0.0",
    "depends": [
        "resource_activity",
        "web_tree_dynamic_colored_field",
    ],
    "author": "Coop IT Easy SC",
    "category": "Resource",
    "website": "https://github.com/coopiteasy/cie-resource",
    "license": "AGPL-3",
    "summary": """
        Set opening hours for the locations and warn the use if
        activity is outside those.
    """,
    "data": [
        "security/ir.model.access.csv",
        "data/opening_hours.xml",
        "views/opening_hours.xml",
        "views/resource_activity_views.xml",
        "views/resource_location_views.xml",
        "reports/activity_reports.xml",
    ],
    "demo": [
        "demo/opening_hours.xml",
    ],
    "installable": True,
    "application": True,
}
