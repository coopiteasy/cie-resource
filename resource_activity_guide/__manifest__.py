# Copyright 2021 Coop IT Easy SC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Resource Activity Guide",
    "version": "12.0.1.1.0",
    "depends": ["resource_activity"],
    "author": "Coop IT Easy SC",
    "category": "Resource",
    "website": "https://github.com/coopiteasy/cie-resource",
    "license": "AGPL-3",
    "summary": """
        Add guides to you activities
    """,
    "data": [
        "views/partner_views.xml",
        "views/product_views.xml",
        "views/resource_activity_views.xml",
        "views/resource_location_views.xml",
        "reports/activity_reports.xml",
    ],
    "demo": [
        "demo/demo.xml",
    ],
    "installable": True,
    "application": True,
}
