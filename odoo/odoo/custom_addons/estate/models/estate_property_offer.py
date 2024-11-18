from odoo import fields, models

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offers made for real estates"

    price = fields.Float(string="Price")
    status = fields.Selection([
            ('accepted', "Accepted"),
            ('refused', "Refused")
        ],copy=False,string="Status"
    )
    partner_id = fields.Many2one("res.partner", string="Partner")
    estate_property_id = fields.Many2one("estate.property")
    estate_property_offer_type_id = fields.Many2one(related = "estate_property_id.estate_property_type_id",store = True)

