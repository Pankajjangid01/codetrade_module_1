from odoo import http, fields
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)

class CodetradeController(http.Controller):

    @http.route('/', type='http', auth='public', website=True, methods=['GET', 'POST'])
    def home_page(self, **post):
        """Render the home page of the website"""
        try:
            return request.render('codetrade_module.home_page')
        except Exception as e:
            _logger.error(f"Error: {str(e)}")
            return "Error: Something went wrong."

    @http.route('/contactus', type='http', auth='public', website=True, methods=['GET', 'POST'])
    def hr_detail(self, **post):
        """Handles GET (renders page) and POST (submits form data)"""
        try:
            if request.httprequest.method == 'POST':
                _logger.info(f"Form Data Received: {post}")  

                request.env['company.employee'].sudo().create({
                    'name': post.get('name'),
                    'email': post.get('email_from'),
                })
                return request.redirect('/employee-details')

            return request.render('codetrade_module.custom_field')

        except Exception as e:
            _logger.error(f"Error in form submission: {str(e)}")
            return "Error: The form could not be submitted. Check server logs."
