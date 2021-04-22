import os
from ..models import Session
import xlsxwriter


async def _create_session_xlsx(session_id: int):
        folder_name = "./reports"
        file_name = folder_name + '/report_' + str(session_id) + '.xlsx'
        if os.path.exists(file_name):
                return file_name

        os.makedirs(folder_name, exist_ok=True)
        session_obj = await Session.get(id=session_id)
        reports = await session_obj.reports.all()
        subject_obj = await session_obj.subject.first()
        session_info = [['Subject ID', 'Subject Name', 'Subject Element'], [subject_obj.id, subject_obj.name, "Students"], \
                        ['Student ID', 'Student Name', 'Num of warnings']]

        report_book = xlsxwriter.Workbook(file_name)
        report_sheet = report_book.add_worksheet()
        bold = report_book.add_format({"bold": True})
        unbold = report_book.add_format({"bold": False})
        row = 0
        col = 0
        
        for info in session_info:
                for element in info:
                        report_sheet.write(row, col, element, bold if row % 2 == 0 else unbold)
                        report_sheet.set_column(row, col, 40)
                        col += 1
                col = 0
                row += 1

        for report in reports:
                warning_count = await report.warnings.all().count()
                student_obj = await report.student.first()
                student_info = [student_obj.id, student_obj.email, warning_count]
                for element in student_info:
                        report_sheet.write(row, col, element)
                        col += 1
                col = 0
                row += 1
        report_book.close()
        return file_name