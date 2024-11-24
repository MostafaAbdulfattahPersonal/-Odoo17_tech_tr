# -*- coding: utf-8 -*-
from email.policy import default

from odoo import api,models, fields
import time


class Hobby(models.Model):
    _name = "wb.hobby"
    _description = "This is student hobbies."

    name = fields.Char(string="Hobby Name")


class School(models.Model):
    _name = "wb.school"
    _description = "This is school profile"
    _rec_name = 'school_name'

    school_name = fields.Char("School Name")
    student_ids = fields.One2many("wb.student" , "wb_school_id")
    ref_field_id = fields.Reference([
        ('wb.school','School'),
        ('wb.hobby','Hobby'),
        ('wb.student','Student'),
        ('sale.order','Sale'),
        ('purchase.order','Purchase'),
        ('account.move','Invoice')
    ],string="Reference" , default="wb.student,11")
    invoice_id = fields.Many2one("account.move")
    invoice_user_id = fields.Many2one("res.users", related="invoice_id.invoice_user_id")
    invoice_date = fields.Date(related="invoice_id.invoice_date")
    binary_field = fields.Binary("Upload File")
    binary_file_name = fields.Char("File Name")
    binary_fields = fields.Many2many("ir.attachment" ,string="Upload Multi Files")
    amount = fields.Monetary("Amount",currency_field="my_currency_id")
    # currency_id = fields.Many2one("res.currency","Currency")
    # If you want to use another name than currency you must do  as below:
    my_currency_id = fields.Many2one("res.currency", "My Currency")


class Student(models.Model):
        _name = "wb.student"
        _description = "This is student profile"
        _rec_name = 'name' # to make student name appear in the top of form view instead of student id

        name = fields.Char("Student Name")
        gender = fields.Selection([
            ('male','Male'),
            ('female','Female')
        ])

        def _get_advance_gender_list(self):
            return([
                ('male','Male'),
                ('female','Female')
            ])
        advance_gender = fields.Selection(_get_advance_gender_list)

        @api.model
        def _get_vip_gender_list(self):
            return ([
                ('a', '1'),
                ('b', '2'),
                ('c', '3')
            ])
        vip_gender = fields.Selection(_get_vip_gender_list)
        combobox = fields.Selection(selection=[('male','Male'),('female','Female')] , string="Combo Box")
        is_paid = fields.Boolean("Is Paid")
        address = fields.Text("Student Address")
        address_html = fields.Html("HTML Student Address")
        roll_number = fields.Integer("Enrollment Number" , index=True)
        student_fees = fields.Float(string="Student Total Fees" , digits=(5,3)) # OR through settings>technical... (digits="Discount")
        discount_fees = fields.Float(string="Discount", digits=(5, 3))
        final_fees_2 = fields.Float("Final Fees_2",compute="_compute_final_fees_2")
        school_data = fields.Json()
        joining_date = fields.Datetime(default=fields.Datetime.now) # .now() with brackets does not display calender
        # joining_date = fields.Datetime(default="2024-01-01 05:00:00") # actual display will be with local not global day time hours i.e 07:00:00)
        # joining_date = fields.Date(default=fields.Date.today())
        start_date = fields.Date(default=time.strftime("%Y-01-01")) #to DYNAMIC date so, we import (import time)
        end_date = fields.Date(default=time.strftime("%Y-12-31"))
        wb_school_id = fields.Many2one("wb.school")
        # wb_hobby_ids = fields.Many2many("wb.hobby",
        #                                 "student_hobby_ids_relation",
        #                                 "wb_student_id",
        #                                 "wb_hobby_id")
        wb_hobby_list_ids = fields.Many2many("wb.hobby") #أسهل بكتير من اللي فوقها

        compute_address_html = fields.Html(string="Compute Address Field")


        @api.onchange("address_html")
        def onchange_address_html_field(self):
            for record in self:
                record.compute_address_html = record.address_html

        @api.depends("student_fees","discount_fees")
        def _compute_final_fees_2(self):
            for record in self:
                record.final_fees_2 = record.student_fees - record.discount_fees


        def json_data_store(self):
            self.school_data={"name":self.name , "id":self.id , "fees":self.student_fees , "g":self.gender}