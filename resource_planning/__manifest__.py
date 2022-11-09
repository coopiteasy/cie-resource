# Copyright 2018 Coop IT Easy SC.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Resource Planning",
    "version": "12.0.1.0.0",
    "depends": [
        "base",
        "mail",
        "resource",
    ],
    "author": "Coop IT Easy SC",
    "category": "Resource",
    "website": "https://github.com/coopiteasy/cie-resource",
    "license": "AGPL-3",
    "summary": """
    This module manages the planning of the resources (reservation, booking, ...).
    It provides an api in order to tie a resource with any other model.
    """,
    "data": [
        "data/resource_planning_data.xml",
        "security/resource_planning_security.xml",
        "security/ir.model.access.csv",
        "wizard/allocate_resource_wizard.xml",
        "views/res_config_views.xml",
        "views/res_partner_views.xml",
        "views/res_users_views.xml",
        "views/resource_allocation_views.xml",
        "views/resource_category_views.xml",
        "views/resource_location_views.xml",
        "views/resource_resource_views.xml",
        "wizard/check_resource_availabilities_wizard.xml",
        "views/actions.xml",
        "views/menus.xml",
    ],
    "demo": [
        "demo/demo.xml",
    ],
    "installable": True,
    "application": True,
}
