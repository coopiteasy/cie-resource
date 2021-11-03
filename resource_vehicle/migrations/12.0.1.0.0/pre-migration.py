# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openupgradelib import openupgrade

_field_renames = [
    ("resource.category", "resource_category", "vehicule", "vehicle"),
    (
        "resource.category",
        "resource_category",
        "vehicule_type",
        "vehicle_type",
    ),
    (
        "resource.resource",
        "resource_resource",
        "vehicule_type",
        "vehicle_type",
    ),
]


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.rename_fields(env, _field_renames)
