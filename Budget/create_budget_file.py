import xlsxwriter
from datetime import datetime
import typing
import json

DEFAULT_CONFIG_NAME: str = 'config.json'
MONTHS_LENGTH: dict = {'01': 31, '02': 28, '03': 31, '04': 30, '05': 31, '06': 30, '07': 31, '08': 31, '09': 30,
                       '10': 31, '11': 30, '12': 31}


class WorkBookInformation:
    def __init__(self, config_dict: dict):
        self.year: str = config_dict['year']
        self.income_list: list = config_dict['income']
        self.income_list_length: int = len(self.income_list)
        self.expenses_list: list = config_dict['expenses']
        self.expenses_list_length: int = len(self.expenses_list)
        self.showDeficitColumn: bool = config_dict['showDeficitColumn']
        self.showMonthlyTable: bool = config_dict['showMonthlyTable']
        self.showMonthlySalary: bool = config_dict['showMonthlySalary']
        self.showTotalMonthlyIncome: bool = config_dict['showTotalMonthlyIncome']
        self.showTotalMonthlyExpenses: bool = config_dict['showTotalMonthlyExpenses']
        # Expenses without investments and large expenses
        self.showRegularExpenses: bool = config_dict['showRegularExpenses']
        # Difference between total income and total expenses without investments
        self.showMonthlyDifference: bool = config_dict['showMonthlyDifference']
        self.balanceFromPreviousYear: int = config_dict['balanceFromPreviousYear']


def change_feb_length_if_leap_year(current_year: int) -> None:
    if current_year % 4 == 0:
        MONTHS_LENGTH['feb'] += 1


def date_number_to_str_format(month_number: int) -> str:
    result: str = ''
    if month_number <= 9:
        result += '0'
    return result + str(month_number)


def read_config_file(config_name: str) -> dict:
    with open(config_name, encoding='utf-8') as config_file:
        return json.load(config_file)


def write_row(current_row: int, current_day: int, month_with_year: str, workbook, worksheet) -> None:
    date_format = workbook.add_format({'right': 1, 'align': 'center'})
    right_border_format = workbook.add_format({'right': 1})
    bottom_border_format = workbook.add_format({'bottom': 1})

    col: int = 0
    if current_day == MONTHS_LENGTH[month_with_year[0:2]]:
        date_format.set_bottom(1)
        right_border_format.set_bottom(1)
        col += 1
        while col < 13:
            worksheet.write_blank(current_row, col, None, bottom_border_format)
            col += 1
        col = 0

    current_date = date_number_to_str_format(current_day) + '.' + month_with_year

    worksheet.write(current_row, col, current_date, date_format)

    income_border_ind = 'E' + str(current_row + 1)
    deficit_border_ind = 'F' + str(current_row + 1)
    expenses_border_ind = 'M' + str(current_row + 1)
    balance_border_ind = 'N' + str(current_row + 1)
    worksheet.write_blank(income_border_ind, None, right_border_format)
    worksheet.write_blank(deficit_border_ind, None, right_border_format)
    worksheet.write_blank(expenses_border_ind, None, right_border_format)
    worksheet.write_blank(balance_border_ind, None, right_border_format)


def write_month(current_month: str, current_year: str, previous_row: int, workbook, worksheet) -> None:
    month_with_year: str = current_month + '.' + current_year
    current_row: int = previous_row + 1
    for day in range(1, MONTHS_LENGTH[current_month] + 1):
        write_row(current_row, day, month_with_year, workbook, worksheet)
        current_row += 1


def write_header(workbook, worksheet, header_list, context) -> None:
    income_header = 'Доходы'
    expenses_header = 'Расходы'
    balance_header = 'Баланс'
    deficit_header = 'Недостача'

    merge_format = workbook.add_format({'border': 1, 'align': 'center'})

    worksheet.merge_range('B1:E1', income_header, merge_format)
    if context.showDeficitColumn:
        deficit_column: int = context.income_list_length + 1
        worksheet.set_column(deficit_column, deficit_column, len(deficit_header) + 3)
        worksheet.merge_range('F1:F2', deficit_header, merge_format)
    worksheet.merge_range('G1:M1', expenses_header, merge_format)
    worksheet.merge_range('N1:N2', balance_header, merge_format)

    border_format = workbook.add_format({'bottom': 1, 'top': 1, 'align': 'center'})

    row: int = 1
    col: int = 1

    for item in header_list:
        worksheet.set_column(col, col, len(item) + 3)
        worksheet.write(row, col, item, border_format)
        col += 1
        if col == context.income_list_length + 1 and context.showDeficitColumn:
            col += 1


def create_file(config_dict: dict) -> None:
    context = WorkBookInformation(config_dict)
    current_year: str = config_dict['year']
    income_list: list = config_dict['income']
    expenses_list: list = config_dict['expenses']
    main_worksheet_name: str = 'Бюджет'

    workbook = xlsxwriter.Workbook(current_year + '.xlsx')
    worksheet = workbook.add_worksheet(main_worksheet_name)

    write_header(workbook, worksheet, income_list + expenses_list, context)
    worksheet.set_column(0, 0, 11)
    worksheet.write_blank(1, 0, None, workbook.add_format({'right': 1}))

    current_row: int = 1
    for month_number in range(1, 13):
        current_month: str = date_number_to_str_format(month_number)
        write_month(current_month, current_year, current_row, workbook, worksheet)
        current_row += MONTHS_LENGTH[current_month]

    workbook.close()


if __name__ == "__main__":
    print("Start")

    config_dict: dict = read_config_file(DEFAULT_CONFIG_NAME)
    change_feb_length_if_leap_year(int(config_dict['year']))
    create_file(config_dict)

    print("End")
