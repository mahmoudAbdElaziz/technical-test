from odoo import models, fields


class FleetOrdersXlsx(models.AbstractModel):
    _name = "report.report_xlsx.fleet_orders_xlsx"
    _inherit = "report.report_xlsx.abstract"
    _description = "Fleet Orders XLSX Report"

    def generate_xlsx_report(self, workbook, data, records):
        sheet = workbook.add_worksheet("Report")

        heading = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': '10px',
             'bg_color': '#c0c1c0',
             'border': 1,
             'border_color': 'black'})

        txt = workbook.add_format({'font_size': '10px', 'border': 1, 'align': 'center', })

        row = 0

        sheet.write(row, 0, "Reference", heading)
        sheet.write(row, 1, "Form", heading)
        sheet.write(row, 2, "To", heading)
        sheet.write(row, 3, "Contact", heading)
        sheet.write(row, 4, "Scheduled Date", heading)
        sheet.write(row, 5, "Status", heading)
        col = 7

        row += 1
        for rec in records:
            sheet.write(row, 0, rec.name, txt)
            sheet.write(row, 1, rec.location_id.name, txt)
            sheet.write(row, 2, rec.location_dest_id.name, txt)
            sheet.write(row, 3, rec.partner_id.name, txt)
            sheet.write(row, 4, fields.Datetime.to_string(rec.scheduled_date), txt)
            sheet.write(row, 5, rec.state, txt)

        sheet.set_column(0, 0, 20)
        sheet.set_column(0, 1, 15)
        sheet.set_column(0, 2, 15)
        sheet.set_column(0, 3, 15)
        sheet.set_column(0, 4, 15)
        sheet.set_column(0, 5, 15)
