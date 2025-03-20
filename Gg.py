def action_generate_sale_order(self):
    """Generate Sale Order from Lab Test"""
    sale_order_obj = self.env['sale.order']
    sale_order_line_obj = self.env['sale.order.line']

    for lab in self:
        if not lab.test_type_name or not lab.patient_id:
            raise UserError("Test Type and Patient must be selected to generate a Sale Order.")

        # Create Sale Order
        order = sale_order_obj.create({
            'partner_id': lab.patient_id.partner_id.id,  # Assuming patient has related partner
            'origin': lab.request_id,
            'note': f'Lab Test: {lab.test_type_name.name}',
        })

        # Create Sale Order Line
        sale_order_line_obj.create({
            'order_id': order.id,
            'name': lab.test_type_name.name,
            'product_id': lab.test_type_name.product_id.id,  # Assuming test_type is linked with product
            'product_uom_qty': 1,
            'price_unit': lab.test_type_name.product_id.lst_price,
        })

        lab.state = 'tested'  # Mark lab as tested or update state if needed

    return {
        'name': 'Sale Order',
        'type': 'ir.actions.act_window',
        'res_model': 'sale.order',
        'view_mode': 'form',
        'res_id': order.id,
        'target': 'current',
    }
