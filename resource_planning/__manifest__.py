# Copyright 2018 Coop IT Easy SCRLfs.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Resource Planning",
    "version": "11.0.1.0.0",
    "depends": [
        "base",
        "mail",
        "resource",
        "web_gantt8",
    ],
    "author": "Houssine BAKKALI <houssine@coopiteasy.be>",
    "category": "Resource",
    "website": "www.coopiteasy.be",
    "license": "AGPL-3",
    "description": """
    This module manages the planning of the resources. It aims to provide an api in
    in order to be able to tie a resource with any other model.
    """,
    "data": [
        "data/resource_planning_data.xml",
        "security/resource_planning_security.xml",
        "security/ir.model.access.csv",
        "wizard/allocate_resource_wizard.xml",
        "wizard/check_resource_availabilities_wizard.xml",
        "views/partner_views.xml",
        "views/res_config_views.xml",
        "views/resource_allocation_views.xml",
        "views/resource_category_views.xml",
        "views/resource_location_views.xml",
        "views/resource_resource_views.xml",
        "views/actions.xml",
        "views/menus.xml",
    ],
    "demo": [
        "demo/demo.xml",
    ],
    "installable": True,
    "application": True,
}
