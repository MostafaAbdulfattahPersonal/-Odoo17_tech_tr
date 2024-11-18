from email.policy import default

from odoo import fields,models,api


class SchoolProfile(models.Model):
    _name = "school.profile"

    def default_open_date(self):  # extra, look dow to now the easier method in (open_date) field
        return fields.Datetime.now()

    name = fields.Char(string="School Name")
    email = fields.Char(string="Email")
    phone = fields.Char("Phone")
    is_virtual_class = fields.Boolean(string="Virtual Class Support ?")
    school_rank = fields.Integer(string="School Rank")
    result = fields.Float(string="Result" , digits=(2,3))
    address = fields.Text(string = "Address" , trim = False)# trim to leave or remove spaces in the beginning of text
    establish_date = fields.Date(default= fields.Datetime.today())
    open_date = fields.Datetime(default= lambda lm:lm.default_open_date()) #we can use (default = fields.Datetime.now()) .
    school_type = fields.Selection([
        ('public','Public School'),
        ('private','Private School')], string = "Type of School"
    )
    documents = fields.Binary(string="Documents" )
    document_name = fields.Char(string="File Name")
    school_image = fields.Image(string="Upload School Image", max_width=100,max_height=100)
    school_description = fields.Html(string="Description")
