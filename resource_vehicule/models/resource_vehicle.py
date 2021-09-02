# Copyright 2018 Coop IT Easy SCRLfs.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResourceCategory(models.Model):
    _inherit = "resource.category"

    # fixme typo vehicule => vehicle
    vehicule = fields.Boolean(string="Vehicule")
    vehicule_type = fields.Selection(
        [("bike", "Bike"), ("car", "Car")], string="Vehicle type"
    )


class ResourceResource(models.Model):
    _inherit = "resource.resource"

    purchase_price = fields.Float(string="Purchase price")
    catalog_price = fields.Float(string="Catalog price")
    insurance = fields.Char(string="Insurance")
    brand_id = fields.Many2one(comodel_name="resource.brand", string="Brand")
    color = fields.Many2one(comodel_name="resource.color", string="Color")
    model_id = fields.Many2one(comodel_name="resource.model", string="Model")
    gearbox = fields.Many2one(comodel_name="resource.gearbox", string="Gearbox")
    vehicule_type = fields.Selection(related="category_id.vehicule_type")


class ResourceBrand(models.Model):
    _name = "resource.brand"
    _description = "Resource Brand"

    name = fields.Char(string="Brand")
    code = fields.Char(string="Code")
    active = fields.Boolean("Active", default=True)


class ResourceModel(models.Model):
    _name = "resource.model"
    _description = "Resource Model"

    name = fields.Char(string="Model")
    code = fields.Char(string="Code")
    active = fields.Boolean("Active", default=True)


class ResourceColor(models.Model):
    _name = "resource.color"
    _description = "Resource Color"

    name = fields.Char(string="Color")
    code = fields.Char(string="code")
    active = fields.Boolean("Active", default=True)


class ResourceGearbox(models.Model):
    _name = "resource.gearbox"
    _description = "Resource Gearbox"

    name = fields.Char(string="Gearbox")
    code = fields.Char(string="code")
    active = fields.Boolean("Active", default=True)
