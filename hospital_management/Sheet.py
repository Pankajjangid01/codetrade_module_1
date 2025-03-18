import base64
import io
import tempfile
from PIL import Image
import xlsxwriter
from odoo import models

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def action_export_selected_products_excel(self):
        # Create an in-memory output file
        output = io.BytesIO()

        # Create a workbook and worksheet
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet("Product Data")

        # Define header format
        header_format = workbook.add_format({'bold': True, 'bg_color': '#D3D3D3'})

        # Write headers
        worksheet.write('A1', 'Product Name', header_format)
        worksheet.write('B1', 'Price', header_format)
        worksheet.write('C1', 'Image', header_format)

        # Set column widths
        worksheet.set_column('A:A', 30)
        worksheet.set_column('B:B', 15)
        worksheet.set_column('C:C', 20)

        row = 1  # Start from second row

        for product in self:  # 'self' contains all selected records
            # Write product data
            worksheet.write(row, 0, product.name or '')
            worksheet.write(row, 1, product.list_price or 0.0)

            # Insert product image (if exists)
            if product.image_1920:
                try:
                    image_data = base64.b64decode(product.image_1920)
                    temp_img = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
                    img = Image.open(io.BytesIO(image_data))
                    img.save(temp_img.name, format='PNG')

                    worksheet.set_row(row, 80)  # Adjust row height
                    worksheet.insert_image(row, 2, temp_img.name, {
                        'x_offset': 5,
                        'y_offset': 5,
                        'x_scale': 0.5,
                        'y_scale': 0.5,
                    })
                except Exception:
                    pass  # You can log error if needed

            row += 1

        # Close workbook and prepare output
        workbook.close()
        output.seek(0)

        # Create attachment for download
        attachment = self.env['ir.attachment'].create({
            'name': 'product_export.xlsx',
            'type': 'binary',
            'datas': base64.b64encode(output.read()),
            'res_model': 'product.template',
            'res_id': self.ids[0] if self else False,
            'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        })

        url = f'/web/content/{attachment.id}?download=true'
        return {
            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'new',
        }
