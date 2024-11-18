from odoo import models, fields
from odoo.addons.base.tests.test_uninstall import MODEL


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "test"

    name= fields.Char(string="Name")

