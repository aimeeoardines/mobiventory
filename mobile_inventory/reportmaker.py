import xlwt
import os
from django.http import HttpResponse

from .models import Device, Transaction, TransactionBorrow


class Report:
    def __init__(self):
        self.REPORT_FILE_PATH = './mobile_inventory/report/report.xls'
        self.header_style = xlwt.easyxf('font: name Times New Roman, color-index red, bold on')
        self.devices = Device.objects.all().order_by('-service_tag')

        self.generate

    @property
    def generate(self):
        wb = xlwt.Workbook()
        ws = wb.add_sheet('Transaction Report')

        # Writing has params: row, col, label, style
        ws.write(0, 0, 'Service Tag', self.header_style)
        ws.write(0, 1, 'Model', self.header_style)
        ws.write(0, 2, 'Category', self.header_style)
        ws.write(0, 3, 'Serial Number', self.header_style)
        ws.write(0, 4, 'Location', self.header_style)
        ws.write(0, 5, 'Notes', self.header_style)
        ws.write(0, 6, 'Person', self.header_style)
        ws.write(0, 7, 'Status', self.header_style)
        ws.write(0, 8, 'Date Checked', self.header_style)

        row = 1
        for device in self.devices:
            borrower = self.get_borrower(device.id)
            ws.write(row, 0, device.service_tag)
            ws.write(row, 1, device.model)
            ws.write(row, 2, device.category.category)
            ws.write(row, 3, device.serial_no)
            ws.write(row, 4, device.status.location.location)
            ws.write(row, 5, device.status.notes)
            ws.write(row, 6, borrower)
            ws.write(row, 7, device.status.health)
            row += 1

        wb.save(self.REPORT_FILE_PATH)

    @property
    def download(self):
        if os.path.exists(self.REPORT_FILE_PATH):
            with open(self.REPORT_FILE_PATH, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(self.REPORT_FILE_PATH)
                return response
            raise Http404

    def get_borrower(self, device_id):
        borrow_trans = TransactionBorrow.objects.filter(
            transaction__device__id=device_id,
            transaction__status__is_available=False,
        ).order_by('-transaction__transaction_date')

        if not borrow_trans:
            return ''

        return borrow_trans.first().borrower.name
