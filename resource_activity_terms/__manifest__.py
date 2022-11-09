# Copyright 2021 Coop IT Easy SC
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Resource Activity Terms",
    "version": "12.0.1.0.0",
    "depends": [
        "resource_activity",
        "sale_management",
    ],
    "author": "Coop IT Easy SC",
    "category": "Resource",
    "website": "https://github.com/coopiteasy/cie-resource",
    "license": "AGPL-3",
    "summary": """
        Manage activity terms per location.
    """,
    "data": [
        "security/ir.model.access.csv",
        "views/res_company_note_views.xml",
        "views/res_config_settings_views.xml",
        "views/res_company_terms_views.xml",
        "views/resource_location_views.xml",
        "views/sale_order_views.xml",
        "reports/sale_order_report.xml",
    ],
    "demo": [
        "demo/demo.xml",
    ],
    "installable": True,
    "application": True,
}
