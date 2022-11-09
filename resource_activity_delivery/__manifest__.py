# Copyright 2021 Coop IT Easy SC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Resource Activity Deliveries",
    "version": "12.0.1.0.1",
    "depends": [
        "resource_activity",
    ],
    "author": "Coop IT Easy SC",
    "category": "Resource",
    "website": "https://github.com/coopiteasy/cie-resource",
    "license": "AGPL-3",
    "summary": """
        Manage resource deliveries for your activities.
    """,
    "data": [
        "security/ir.model.access.csv",
        "views/product_views.xml",
        "views/resource_activity_delivery_views.xml",
        "views/resource_activity_views.xml",
        "views/sale_order_views.xml",
        "reports/activity_reports.xml",
        "reports/invoice_report.xml",
        "reports/saleorder_report.xml",
    ],
    "demo": [
        "demo/demo.xml",
    ],
    "installable": True,
    "application": True,
}
