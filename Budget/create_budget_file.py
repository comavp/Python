import xlsxwriter
import json
import string

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
        self.showMonthlyBankInterest: bool = config_dict['showMonthlyBankInterest']
        self.showMonthlyDividends: bool = config_dict['showMonthlyDividends']
        self.balanceFromPreviousYear: int = config_dict['balanceFromPreviousYear']


def change_feb_length_if_leap_year(current_year: int) -> None:
    if current_year % 4 == 0:
        MONTHS_LENGTH['02'] += 1


def date_number_to_str_format(month_number: int) -> str:
    result: str = ''
    if month_number <= 9:
        result += '0'
    return result + str(month_number)


def read_config_file(config_name: str) -> dict:
    with open(config_name, encoding='utf-8') as config_file:
        return json.load(config_file)


def write_monthly_table(first_month_row: int, last_month_row: int, workbook, worksheet, context: dict):
    table_header_border_format = workbook.add_format({'bottom': 1, 'top': 1, 'align': 'center'})
    table_header_left_format = workbook.add_format({'bottom': 1, 'top': 1, 'align': 'center', 'left': 1})
    table_header_right_format = workbook.add_format({'bottom': 1, 'top': 1, 'align': 'center', 'right': 1})

    table_body_left_format = workbook.add_format({'left': 1})
    table_body_right_format = workbook.add_format({'right': 1})
    table_body_bottom_format = None

    curr_row = first_month_row + 3

    # Write header of monthly table
    worksheet.write_blank('P' + str(curr_row), None, table_header_left_format)
    worksheet.write_blank('Q' + str(curr_row), None, table_header_right_format)
    worksheet.write('R' + str(curr_row), 'Всего', table_header_border_format)
    worksheet.write('S' + str(curr_row), '% от р', table_header_right_format)
    worksheet.write('T' + str(curr_row), '% от д', table_header_right_format)

    # Templates of table body formulas
    total_formula_template: str = '=СУММ({col}{first_row}:{col}{last_row})'
    percentage_of_expenses_template: str = '=R{curr_row}/P{last_row}*100'
    percentage_of_income_template: str = '=R{curr_row}/O{last_row}*100'

    curr_row += 1
    cur_col: int = string.ascii_uppercase.find('G')

    # Write body of monthly table
    for item in context.expenses_list:
        total_formula = total_formula_template.format(col=string.ascii_uppercase[cur_col], first_row=first_month_row,
                                                      last_row=last_month_row)
        percentage_of_expenses = percentage_of_expenses_template.format(curr_row=curr_row, last_row=last_month_row)
        percentage_of_income = percentage_of_income_template.format(curr_row=curr_row, last_row=last_month_row)

        if curr_row == first_month_row + 3 + context.expenses_list_length:
            table_body_right_format = workbook.add_format({'right': 1, 'bottom': 1})
            table_body_left_format = workbook.add_format({'left': 1, 'bottom': 1})
            table_body_bottom_format = workbook.add_format({'bottom': 1})

        worksheet.write('P' + str(curr_row), item, table_body_left_format)
        worksheet.write_blank('Q' + str(curr_row), None, table_body_right_format)
        worksheet.write('R' + str(curr_row), total_formula, table_body_bottom_format)
        worksheet.write('S' + str(curr_row), percentage_of_expenses, table_body_right_format)
        worksheet.write('T' + str(curr_row), percentage_of_income, table_body_right_format)

        curr_row += 1
        cur_col += 1


def write_monthly_metrics(first_month_row: int, last_month_row: int, context: dict, worksheet):
    total_monthly_income_name: str = 'Доходы:'
    total_monthly_expenses_name: str = 'Раcходы:'
    regular_expenses_name: str = 'Расходы без инвестиций и кр. трат'
    monthly_salary_name: str = 'Зарплата'
    monthly_difference_name: str = 'Остаток за м.'
    monthly_bank_interest_name: str = 'Проценты'
    monthly_dividends_name: str = 'Дивиденды'

    total_monthly_income_formula: str = '=СУММ(B{0}:E{1})'.format(first_month_row, last_month_row)
    total_monthly_expenses_formula: str = '=СУММ(G{0}:M{1})'.format(first_month_row, last_month_row)
    regular_expenses_formula: str = '=СУММ(G{0}:K{1})'.format(first_month_row, last_month_row)
    monthly_salary_formula: str = '=СУММ(B{0}:B{1})'.format(first_month_row, last_month_row)
    monthly_difference_formula: str = '=O{1}-СУММ(G{0}:L{1})'.format(first_month_row, last_month_row)
    monthly_bank_interest_formula: str = '=СУММ(C{0}:C{1})'.format(first_month_row, last_month_row)
    monthly_dividends_formula: str = '=СУММ(D{0}:D{1})'.format(first_month_row, last_month_row)

    worksheet.set_column(15, 15, len(monthly_difference_name))
    if context.showTotalMonthlyIncome:
        worksheet.write('O' + str(last_month_row - 1), total_monthly_income_name)
        worksheet.write_formula('O' + str(last_month_row), total_monthly_income_formula)
    if context.showTotalMonthlyExpenses:
        worksheet.write('P' + str(last_month_row - 1), total_monthly_expenses_name)
        worksheet.write_formula('P' + str(last_month_row), total_monthly_expenses_formula)
    if context.showRegularExpenses:
        worksheet.write('Q' + str(last_month_row - 1), regular_expenses_name)
        worksheet.write_formula('Q' + str(last_month_row), regular_expenses_formula)
    if context.showMonthlyDifference:
        worksheet.write('P' + str(last_month_row - 3), monthly_difference_name)
        worksheet.write_formula('Q' + str(last_month_row - 3), monthly_difference_formula)
    if context.showMonthlySalary:
        worksheet.write('P' + str(last_month_row - 4), monthly_salary_name)
        worksheet.write_formula('Q' + str(last_month_row - 4), monthly_salary_formula)
    if context.showMonthlyBankInterest:
        worksheet.write('P' + str(last_month_row - 5), monthly_bank_interest_name)
        worksheet.write_formula('Q' + str(last_month_row - 5), monthly_bank_interest_formula)
    if context.showMonthlyDividends:
        worksheet.write('P' + str(last_month_row - 6), monthly_dividends_name)
        worksheet.write_formula('Q' + str(last_month_row - 6), monthly_dividends_formula)


def write_row(current_row: int, current_day: int, month_with_year: str, workbook, worksheet, context) -> None:
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
    balance_formula: str = '=B{row}+C{row}+D{row}+E{row}-F{row}-G{row}-H{row}-I{row}-J{row}-K{row}-L{row}-M{row}+{balance}'
    if current_row == 2:
        balance_formula = balance_formula.format(row=current_row + 1, balance=str(context.balanceFromPreviousYear))
    else:
        balance_formula = balance_formula.format(row=current_row + 1, balance='N' + str(current_row))

    worksheet.write(current_row, col, current_date, date_format)

    income_border_ind = 'E' + str(current_row + 1)
    deficit_border_ind = 'F' + str(current_row + 1)
    expenses_border_ind = 'M' + str(current_row + 1)
    balance_border_ind = 'N' + str(current_row + 1)
    worksheet.write_blank(income_border_ind, None, right_border_format)
    worksheet.write_blank(deficit_border_ind, None, right_border_format)
    worksheet.write_blank(expenses_border_ind, None, right_border_format)
    worksheet.write_formula(balance_border_ind, balance_formula, right_border_format)


def write_month(current_month: str, current_year: str, previous_row: int, workbook, worksheet, context: dict) -> None:
    month_with_year: str = current_month + '.' + current_year
    current_row: int = previous_row + 1
    first_month_row: int = current_row
    for day in range(1, MONTHS_LENGTH[current_month] + 1):
        write_row(current_row, day, month_with_year, workbook, worksheet, context)
        current_row += 1
    write_monthly_metrics(first_month_row + 1, current_row, context, worksheet)
    if context.showMonthlyTable:
        write_monthly_table(first_month_row + 1, current_row, workbook, worksheet, context)


def write_header(workbook, worksheet, header_list, context) -> None:
    income_header = 'Доходы'
    expenses_header = 'Расходы'
    balance_header = 'Баланс'
    deficit_header = 'Недостача'

    # all values are zero indexed
    income_start_column: int = 1
    income_end_column: int = income_start_column + context.income_list_length - 1
    expenses_start_column: int = income_end_column + 1
    expenses_end_column: int = expenses_start_column + context.expenses_list_length - 1

    merge_format = workbook.add_format({'border': 1, 'align': 'center'})

    worksheet.merge_range(0, income_start_column, 0, income_end_column, income_header, merge_format)
    if context.showDeficitColumn:
        deficit_column: int = context.income_list_length + 1
        worksheet.set_column(deficit_column, deficit_column, len(deficit_header) + 3)
        worksheet.merge_range(0, income_end_column + 1, 1, income_end_column + 1, deficit_header, merge_format)
        expenses_start_column += 1
        expenses_end_column += 1
    worksheet.merge_range(0, expenses_start_column, 0, expenses_end_column, expenses_header, merge_format)
    worksheet.merge_range(0, expenses_end_column + 1, 1, expenses_end_column + 1, balance_header, merge_format)

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
        write_month(current_month, current_year, current_row, workbook, worksheet, context)
        current_row += MONTHS_LENGTH[current_month]

    workbook.close()


if __name__ == "__main__":
    print("Start")

    config_dict: dict = read_config_file(DEFAULT_CONFIG_NAME)
    change_feb_length_if_leap_year(int(config_dict['year']))
    create_file(config_dict)

    print("End")
