# -*- coding: utf-8 -*-
{
    'name': "Student",

    'summary': "Short (1 phrase/line) summary of the module's purpose",
    'license': 'LGPL-3',

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '17.0.0.1.0',

    # any module necessary for this one to work correctly
    'depends': ['base','account'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/student_views.xml',
        'views/wb_school_views.xml',
        'views/wb_hobby_views.xml'
    ],

}

