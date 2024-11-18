{
    "name": "The Real Estate",
    "summary": "Sample module",
    "version": "17.0.0.1.0",
    "depends": ['base'],
    "data": [
        # SECURITY
        "security/ir.model.access.csv",

        # VIEWS (actions first then menus)
        "views/estate_property_views.xml",
        "views/estate_menus_view.xml",

        # MENUS

    ],
    "demo" : [
        "demo/demo.xml"
    ]
}