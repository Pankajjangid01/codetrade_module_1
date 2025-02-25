from odoo import http
from odoo.http import request

class CustomerController(http.Controller):

    @http.route('/api/hr-details',type="http", auth='user', methods=['GET','POST'])
    def get_customers(self, **kw):
        """Function to get all hr's through api"""
        try:
            hr_list = request.env['company.hr'].search([])
            if hr_list:
                hr_data = {hr.name for hr in hr_list}
                return request.make_json_response({'HR': hr_data},status=200) 
            else:
                return request.make_json_response({"No HR registered, Please go and Register"},status=404)

        except Exception as exe:
            return request.make_json_response({f"Error:Failed To fetch the Data:{exe}"},status=500)
        
    @http.route('/api/create-hr',type="http", auth='user', methods=['GET','POST'],csrf=False)
    def create_hr(self,**kwargs):
        """Function to get New hr through api"""
        try:
            new_hr = request.env['company.hr'].create(kwargs)
            return request.make_json_response(kwargs,status=200)
        except Exception as exe:
            return request.make_json_response({f"Error:Failed To Create HR:{exe}"},status=500)