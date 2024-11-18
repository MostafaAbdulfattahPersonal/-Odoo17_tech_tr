from email.policy import default

from odoo import fields,models,api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError

from odoo.tools.populate import compute


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Test Model'

    def default_date_availability(self):
        return fields.Date.today() + relativedelta(months=3)
    name = fields.Char(default='House')
    price = fields.Float()
    date = fields.Date()
    state = fields.Selection([
        ('new', 'New'),
        ('received', 'Offer Received'),
        ('accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('canceled', 'Canceled'),
    ], default='new')
    date_availability = fields.Date(default= default_date_availability, copy=False, string="Availability Date")
    expected_price = fields.Float( string="Expected Price")
    best_offer = fields.Float(string="Best Offer")
    selling_price = fields.Float(readonly=True, copy=False, string="Selling Price")
    description = fields.Text(string="Description")
    bedrooms = fields.Integer(default=2, string="Bedrooms")
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection([
        ('north', "North"),
        ('south', "South"),
        ('east', "East"),
        ('west', "West")],string="Garden Orientation")

    estate_property_type_id = fields.Many2one("estate.property.type")
    estate_property_tag_ids = fields.Many2many("estate.property.tag")
    estate_property_offer_ids = fields.One2many("estate.property.offer","estate_property_id")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesperson_id = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user)
    total_area = fields.Integer(compute="_compute_total_area", string="Total Area")
    best_offer = fields.Float(compute = "_compute_best_offer")
    line_ids = fields.One2many('estate.property.line', 'estate_property_id')

    @api.depends('estate_property_offer_ids.price')
    def _compute_best_offer(self):
        for rec in self:
            rec.best_offer = max(rec.estate_property_offer_ids.mapped('price')) if rec.estate_property_offer_ids else 0


    @api.depends('garden_area','living_area')
    def _compute_total_area(self):
        for rec in self :
            rec.total_area = rec.garden_area + rec.living_area

    validity = fields.Integer(default = 7)
    date_deadline = fields.Date(compute = "_compute_date_deadline ",inverse = "_inverse_date_deadline")

    @api.depends('validity')
    def _compute_date_deadline(self):
        for rec in self :
            rec.date_deadline = fields.Date.today() + relativedelta(days = rec.validity)

    @api.depends('date_deadline')
    def _inverse_date_deadline(self):
        for rec in self :
            rec.validity = (rec.date_deadline - fields.Date.today).days

    @api.constrains('living_area','garden_area')
    def action_areas_error(self):
        for rec in self:
            if rec.living_area > rec.garden_area :
                raise ValidationError("Gareden Area Should be Greater ")



class EstatePropertyLine(models.Model):
        _name = "estate.property.line"
        estate_property_id = fields.Many2one('estate.property')
        area = fields.Float()
        description = fields.Char()
        living_area = fields.Integer(string="Living Area (sqm)")
        garden_area = fields.Integer(string="Garden Area (sqm)")
        total_area = fields.Integer(compute="_compute_total_area", string="Total Area")

        @api.depends('garden_area', 'living_area')
        def _compute_total_area(self):
            for rec in self:
                rec.total_area = rec.garden_area + rec.living_area




