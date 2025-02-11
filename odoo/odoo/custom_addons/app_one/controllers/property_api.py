import json
import math
from logging import error
from urllib.parse import parse_qs
from PIL.ImageChops import offset
from odoo import http
from odoo.http import request

def invalid_response(error, status):
    response_body = {
        'error': error,
    }
    return request.make_json_response(response_body, status=status)

def valid_response(data,pagination_info, status):
    response_body = {
        'message': "Successful",
        'data': data,
    }
    if pagination_info:
        response_body['pagination_info'] = pagination_info
    return request.make_json_response(response_body, status=status)

class PropertyApi(http.Controller):

    # @http.route("/v1/property",methods=["POST"],type="http",auth="none",csrf=False)
    # def post_property(self):
    #     args = request.httprequest.data.decode()
    #     vals = json.loads(args) #to return values in form of table not json
    #     if not vals.get('name') :
    #         return request.make_json_response({
    #             "error": "name is required ya ba",
    #
    #         }, status=400)
    #
    #     try:
    #         res = request.env['property'].sudo().create(vals)  # walkaround to authenticate...use superuser sudo
    #         if res:
    #            return request.make_json_response({
    #                "message": "Property has been created successfully in http type",
    #                "name": res.name,
    #                "id": res.id,
    #
    #            }, status=201)  # 200 in case of success , 201 for creation success
    #     except Exception as error :
    #         return request.make_json_response({
    #             "error": error,
    #         }, status=400) # 400 for error

    @http.route("/v1/property",methods=["POST"],type="http",auth="none",csrf=False)
    def post_property(self):
        args = request.httprequest.data.decode()
        vals = json.loads(args) #to return values in form of table not json
        if not  vals.get('name') :
            return request.make_json_response({
                "error": "name is required ya ba",
            }, status=400)

        try:
            # res = request.env['property'].sudo().create(vals)  # walkaround to authenticate...use superuser sudo
            cr = request.env.cr
            columns= ','.join(vals.keys())
            values= ','.join(['%s'] * len(vals))
            query = f"""INSERT INTO property ({columns}) VALUES ({values}) RETURNING id,name,postcode"""
            cr.execute(query , tuple(vals.values()))
            res= cr.fetchone()
            print(res)
            if res:
               return request.make_json_response({
                   "message": "Property has been created successfully in http type",
                   "name": res[1],
                   "id": res[0],
                   "postcode": res[2],
               }, status=201)  # 200 in case of success , 201 for creation success
        except Exception as error :
            return request.make_json_response({
                "error": error,
            }, status=400) # 400 for error

    # @http.route("/v1/property/json", methods=["POST"], type="json", auth="none", csrf=False)
    # def post_property_json(self):
    #      args = request.httprequest.data.decode()
    #      vals = json.loads(args)
    #      res = request.env['property'].sudo().create(vals)
    #      if res:
    #          return {
    #              "message":"Property has been created successfully in json"
    #         }



    @http.route("/v1/property/<int:property_id>", methods=["GET"], type="http", auth="none", csrf=False)
    def get_property(self,property_id):
        try:
            property_id = request.env['property'].sudo().search([('id', '=', property_id)])
            if not property_id:
                return invalid_response("ID is not exist ", status=400)
            return valid_response({
                "name": property_id.name,
                "id": property_id.id,
                "ref": property_id.ref,
                "description": property_id.description,
                "bedrooms": property_id.bedrooms,
            }, status=200)

        except Exception as error:
            return request.make_json_response({
                "error": error
            }, status=400)

    @http.route("/v1/property/<int:property_id>", methods=["DELETE"], type="http", auth="none", csrf=False)
    def delete_property(self, property_id):
        try:
            property_id = request.env['property'].sudo().search([('id', '=', property_id)])
            if not property_id:
                return request.make_json_response({
                    "error": "ID is not exist ",
                }, status=400)

            property_id.unlink()
            return request.make_json_response({
                "message": "Property has been Deleted successfully"
            }, status=200)

        except Exception as error:
            return request.make_json_response({
                "error": error,
            }, status=400)

    @http.route("/v1/properties", methods=["GET"], type="http", auth="none", csrf=False)
    def get_property_list(self):
        try:
            params = parse_qs(request.httprequest.query_string.decode('utf-8'))
            property_domain = []
            page = offset = None
            limit = 5
            if params:
               if params.get('limit'):
                  limit = int(params.get('limit')[0])
               if params.get('page'):
                  page = int(params.get('page')[0])
            if page:
               offset = (page * limit) - limit
            if params.get('state'):
                property_domain += [('state','=',params.get('state')[0])]
            property_ids = request.env['property'].sudo().search(property_domain, offset=offset ,limit=limit ,order = 'id desc') #offset means pass this number of records then retrive the other
            property_count = request.env['property'].sudo().search_count(property_domain)

            if not property_ids:
                return request.make_json_response({
                    "error": " There are not records to get",
                }, status=400)
            return valid_response([{
                "name": property_id.name,
                "id": property_id.id,
                "ref": property_id.ref,
                "description": property_id.description,
                "bedrooms": property_id.bedrooms,
            } for property_id in property_ids],pagination_info={
                'page' : page if page else 1 ,
                'limit' : limit,
                'pages' : math.ceil(property_count/limit) if limit else 1,
                'count' : property_count
                }, status=200)

        except Exception as error:
            return (request.make_json_response({
                "error": error,
            }, status=400))


    # <int:property_id> to make URL dynamic
    @http.route("/v1/property/<int:property_id>", methods=["PUT"], type="http", auth="none", csrf=False )
    def update_property(self,property_id):
        try:
            property_id = request.env['property'].sudo().search([('id', '=', property_id)])
            if not property_id :
                return request.make_json_response({
                    "error": "ID is not exist ",
                }, status=400)
            args = request.httprequest.data.decode()
            vals = json.loads(args)
            property_id.write(vals)
            return request.make_json_response({
            "message": "Property has been updated successfully in http type",
            "name": property_id.name,
            "id": property_id.id,
            }, status=200)
        except Exception as error:
            return request.make_json_response({
                "error": error,
            }, status=400)




