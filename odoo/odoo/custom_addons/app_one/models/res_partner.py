from odoo import models, fields,api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    # price = fields.Float(compute = '_compute_price', store=1)  طريقة عمل ستور باستخدام اcompute
    price = fields.Float(related='property_id.selling_price')  #باستخدام related
    property_id = fields.Many2one('property')

    # @api.depends('property_id')
    # def _compute_price (self):
    #      for rec in self:
    #          rec.price = rec.property_id.selling_price

