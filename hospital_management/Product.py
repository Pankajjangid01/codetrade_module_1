<!-- my_module/views/product_template_kanban_button.xml -->
<odoo>
    <record id="product_template_kanban_view_custom" model="ir.ui.view">
        <field name="name">product.template.kanban.custom</field>
        <field name="model">product.template</field>
        <field name="inherit_id" ref="product.product_template_kanban_view"/>
        <field name="arch" type="xml">
            <xpath expr="//kanban" position="attributes">
                <attribute name="create">true</attribute>
            </xpath>
            <xpath expr="//kanban/templates" position="before">
                <header>
                    <button type="action"
                            name="%(action_product_excel_upload_wizard)d"
                            string="Upload Products (Excel)"
                            class="btn btn-primary"
                            context="{}"/>
                </header>
            </xpath>
        </field>
    </record>
</odoo>
# my_module/models/product_excel_upload_wizard.py

from odoo import models, fields, api
import base64
import tempfile
import openpyxl

class ProductExcelUploadWizard(models.TransientModel):
    _name = 'product.excel.upload.wizard'
    _description = 'Product Excel Upload Wizard'

    upload_file = fields.Binary("Upload Excel File", required=True)
    file_name = fields.Char("File Name")

    def action_upload_excel(self):
        if self.upload_file:
            file_data = base64.b64decode(self.upload_file)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as f:
                f.write(file_data)
                f.seek(0)
                workbook = openpyxl.load_workbook(f.name)
                sheet = workbook.active

                for row in sheet.iter_rows(min_row=2, values_only=True):
                    name = row[0]
                    price = row[1] if len(row) > 1 else 0.0
                    self.env['product.template'].create({
                        'name': name,
                        'list_price': price,
                    })

        return {'type': 'ir.actions.act_window_close'}

<!-- my_module/views/product_excel_upload_wizard_view.xml -->
<odoo>
    <record id="view_product_excel_upload_wizard_form" model="ir.ui.view">
        <field name="name">product.excel.upload.wizard.form</field>
        <field name="model">product.excel.upload.wizard</field>
        <field name="arch" type="xml">
            <form string="Upload Excel Sheet">
                <group>
                    <field name="upload_file" filename="file_name"/>
                    <field name="file_name"/>
                </group>
                <footer>
                    <button name="action_upload_excel" string="Upload" type="object" class="btn-primary"/>
                    <button string="Cancel" special="cancel"/>
                </footer>
            </form>
        </field>
    </record>

    <record id="action_product_excel_upload_wizard" model="ir.actions.act_window">
        <field name="name">Upload Product Excel</field>
        <field name="res_model">product.excel.upload.wizard</field>
        <field name="view_mode">form</field>
        <field name="target">new</field>
    </record>
</odoo>
