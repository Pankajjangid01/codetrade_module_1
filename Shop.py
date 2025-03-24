<template id="custom_shop_template" name="Custom Shop Page">
    <t t-call="website.layout">
        <div class="container mt-5">
            <h2 class="text-center mb-4">Shop Products</h2>
            <div class="row">
                <t t-foreach="products" t-as="product">
                    <div class="col-md-4 mb-4">
                        <div class="card shadow-sm">
                            <div class="card-body">
                                <h5 class="card-title"><t t-esc="product.name"/></h5>
                                <p class="card-text">
                                    <strong>Price:</strong> ₹ <t t-esc="product.list_price"/>
                                </p>
                                <!-- Optionally add add-to-cart or details button -->
                            </div>
                        </div>
                    </div>
                </t>
            </div>
        </div>
    </t>
</template>

from odoo import http
from odoo.http import request

class WebsiteShop(http.Controller):
    @http.route('/custom-shop', type='http', auth='public', website=True)
    def custom_shop(self, **kwargs):
        products = request.env['product.template'].sudo().search([('sale_ok', '=', True)])
        return request.render('your_module.custom_shop_template', {
            'products': products
        })
