class Table(object):
    name = ""
    table_content = [[]]

    def add_row(self, new_content):
        self.table_content.append(new_content)

    def add_col(self, col_name):
        self.table_content[0].append(col_name)

    def edit_row(self, row_num, col_name, new_value):
        self.table_content[row_num][self.table_content[0].index(col_name)] = new_value

    def filter(self, col_name, value, type="exact", search_start=1, search_end="END", add_headers_to_result=True):
        if search_end == "END":
            search_end = int(len(self.table_content))

        result_list = []
        for i in self.table_content[search_start:search_end]:

            if type == "exact":
                if i[self.table_content[0].index(col_name)] == value:
                    result_list.append(i)
            elif type == "iexact":
                if i[self.table_content[0].index(col_name)].lower() == value.lower():
                    result_list.append(i)

            elif type == "greaterthan":
                if int(i[self.table_content[0].index(col_name)]) > int(value):
                    result_list.append(i)

            elif type == "lessthan":
                if int(i[self.table_content[0].index(col_name)]) < int(value):
                    result_list.append(i)

            else:
                raise Exception(f'Could not find filter method "{type}"')

        if add_headers_to_result:
            result_list.insert(0, self.table_content[0])

        return result_list


class CsvTable(Table):
    def __init__(self, csv_path):
        self.csv_path = csv_path

        with open(csv_path) as csv_file:
            csv_content = csv_file.read()

        csv_content = csv_content.split("\n")

        csv_content_list = []
        for row in csv_content:
            csv_content_list.append(row.split(","))

        self.table_content = csv_content_list
