# Copyright 2021 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Resource Stock Information",
    "version": "12.0.1.0.0",
    "depends": [
        "resource_planning",
    ],
    "author": "Coop IT Easy SCRLfs",
    "category": "Resource",
    "website": "https://coopiteasy.be",
    "license": "AGPL-3",
    "summary": """
        Track resources movement in and out of stock.
    """,
    "data": [
        "views/resource_views.xml",
        "wizards/resource_stock_removal_wizard.xml",
    ],
    "installable": True,
    "application": True,
}
