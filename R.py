from odoo import models, fields, api
import razorpay
import logging

_logger = logging.getLogger(__name__)

class RazorpayPayment(models.Model):
    _name = 'razorpay.payment'
    _description = 'Razorpay Payment'

    name = fields.Char(string='Order ID')
    amount = fields.Float(string='Amount')
    currency = fields.Char(default='INR')

    @api.model
    def create_razorpay_order(self, amount):
        client = razorpay.Client(auth=("RAZORPAY_API_KEY", "RAZORPAY_API_SECRET"))

        data = {
            "amount": int(amount * 100),  # Razorpay expects paise
            "currency": "INR",
            "receipt": "order_rcptid_11",
            "payment_capture": 1
        }
        order = client.order.create(data=data)
        _logger.info("Razorpay Order Created: %s", order)

        # Save order ID in Odoo
        record = self.create({
            'name': order.get('id'),
            'amount': amount
        })
        return order

  <record id="view_razorpay_payment_form" model="ir.ui.view">
    <field name="name">razorpay.payment.form</field>
    <field name="model">razorpay.payment</field>
    <field name="arch" type="xml">
        <form string="Razorpay Payment">
            <sheet>
                <group>
                    <field name="name"/>
                    <field name="amount"/>
                    <field name="currency"/>
                </group>
                <footer>
                    <button name="action_create_order"
                            type="object"
                            string="Pay with Razorpay"
                            class="btn-primary"/>
                </footer>
            </sheet>
        </form>
    </field>
</record>


def action_create_order(self):
        self.ensure_one()
        order = self.create_razorpay_order(self.amount)
        # You can redirect user to Razorpay checkout here or open in JS popup
        return {
            'type': 'ir.actions.act_url',
            'url': f"https://checkout.razorpay.com/v1/checkout.js?order_id={order['id']}",
            'target': 'new',
        }


        
