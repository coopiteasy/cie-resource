# Copyright 2021 Coop IT Easy SCRL fs
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Resource Vehicle",
    "version": "12.0.1.0.0",
    "depends": [
        "resource_planning",
    ],
    "author": "Coop IT Easy SCRLfs",
    "category": "Resource",
    "website": "https://coopiteasy.be",
    "license": "AGPL-3",
    "summary": """
        Manage vehicles attribute on your resources.
    """,
    "data": [
        "security/ir.model.access.csv",
        "views/resource_vehicle_views.xml",
        "views/menus.xml",
    ],
    "demo": [
        "demo/demo.xml",
    ],
    "installable": True,
    "application": True,
}
