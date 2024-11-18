from odoo import models, fields


class Building(models.Model):
    _name = 'building'
    _description ='New Building Record'          #  The display name in chatter and any place
    _inherit = ['mail.thread' ,'mail.activity.mixin']
    _rec_name = 'code'  # when removed the reserved field (name) will take its place(dominant)

    no = fields.Integer()
    code = fields.Char()
    description = fields.Text()
    name = fields.Char()       # one of reserved fields
    active = fields.Boolean(default=1)   # one of reserved fields



