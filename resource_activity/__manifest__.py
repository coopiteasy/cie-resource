# Copyright 2021 Coop IT Easy SCRL fs
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Resource Activity",
    "version": "12.0.1.0.0",
    "depends": [
        "base",
        "mail",
        "resource_planning",
        "product",
        "sale",
        "web_tree_many2one_clickable",
        "web_tree_dynamic_colored_field",
    ],
    "author": "Coop IT Easy SCRLfs",
    "category": "Resource",
    "website": "https://github.com/OCA/sale-workflow",
    "license": "AGPL-3",
    "summary": """
        Manage activities, book resources and generate sale orders.
    """,
    "data": [
        "security/ir.model.access.csv",
        "data/resource_activity_data.xml",
        "data/cron.xml",
        "views/partner_views.xml",
        "views/product_views.xml",
        "views/resource_activity_lang_views.xml",
        "views/resource_activity_registration_views.xml",
        "views/resource_activity_theme_views.xml",
        "views/resource_activity_type_views.xml",
        "views/resource_activity_views.xml",
        "views/resource_allocation_views.xml",
        "views/resource_category_views.xml",
        "views/sale_order_views.xml",
        "wizard/activity_draft_to_done.xml",
        "wizard/cancel_sale_order_wizard.xml",
        "reports/resource_activity_report.xml",
        "reports/d_day_report.xml",
        "reports/sale_order_report.xml",
        "reports/layouts.xml",
        "views/menus.xml",
    ],
    "demo": [
        "demo/demo.xml",
    ],
    "installable": True,
    "application": True,
}