# models/product_import_wizard.py

from odoo import models, fields, api
import base64
import io
import xlrd  # For .xls
import openpyxl  # For .xlsx

class ProductImportWizard(models.TransientModel):
    _name = 'product.import.wizard'
    _description = 'Import Products from Excel'

    file = fields.Binary(string='Excel File', required=True)
    file_name = fields.Char(string='File Name')

    def import_products(self):
        if not self.file_name.endswith('.xlsx'):
            raise UserError("Please upload a .xlsx file")

        file_data = base64.b64decode(self.file)
        workbook = openpyxl.load_workbook(io.BytesIO(file_data))
        sheet = workbook.active

        for row in sheet.iter_rows(min_row=2, values_only=True):  # Skipping header row
            name, default_code, price, qty, uom_name = row[:5]

            # Find existing product
            product = self.env['product.template'].search([('default_code', '=', default_code)], limit=1)

            # Find UoM
            uom = self.env['uom.uom'].search([('name', '=', uom_name)], limit=1)

            vals = {
                'name': name,
                'default_code': default_code,
                'list_price': price or 0.0,
                'uom_id': uom.id if uom else False,
                'uom_po_id': uom.id if uom else False,
            }

            if product:
                product.write(vals)
            else:
                self.env['product.template'].create(vals)
<!-- views/product_import_wizard_view.xml -->
<odoo>
  <record id="view_product_import_wizard" model="ir.ui.view">
    <field name="name">product.import.wizard.form</field>
    <field name="model">product.import.wizard</field>
    <field name="arch" type="xml">
      <form string="Import Products">
        <group>
          <field name="file" filename="file_name"/>
        </group>
        <footer>
          <button string="Upload" type="object" name="import_products" class="btn-primary"/>
          <button string="Cancel" class="btn-secondary" special="cancel"/>
        </footer>
      </form>
    </field>
  </record>
</odoo>

<!-- server_action.xml -->
<odoo>
  <record id="action_import_product_wizard" model="ir.actions.act_window">
    <field name="name">Import Products</field>
    <field name="res_model">product.import.wizard</field>
    <field name="view_mode">form</field>
    <field name="target">new</field>
  </record>

  <record id="server_action_import_product" model="ir.actions.server">
    <field name="name">Import Products from Excel</field>
    <field name="model_id" ref="product.model_product_template"/>
    <field name="binding_model_id" ref="product.model_product_template"/>
    <field name="state">code</field>
    <field name="code">
      action = env.ref('your_module_name.action_import_product_wizard').read()[0]
    </field>
  </record>
</odoo>

<!-- add_button_product_template_view.xml -->
<odoo>
  <record id="product_template_tree_view_inherit" model="ir.ui.view">
    <field name="name">product.template.tree.inherit</field>
    <field name="model">product.template</field>
    <field name="inherit_id" ref="product.product_template_tree_view"/>
    <field name="arch" type="xml">
      <xpath expr="//tree" position="before">
        <header>
          <button name="%(your_module_name.server_action_import_product)d"
                  string="Import Products"
                  type="action"
                  class="btn-primary"/>
        </header>
      </xpath>
    </field>
  </record>
</odoo>
