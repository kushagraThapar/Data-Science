import sys
from bs4 import BeautifulSoup


class CustomSuperBowlException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


raw_html_file = "superbowl.html"
result_csv_file = "result.csv"


def main():
    cleaned_html_data = parse_raw_html_file(raw_html_file)
    process_clean_html_data(cleaned_html_data)


def parse_raw_html_file(file_name):
    soup = BeautifulSoup(open(file_name, encoding="UTF-8"), "html.parser", from_encoding="UTF-8")
    # print(soup.contains_replacement_characters)
    # print(soup.original_encoding)
    first_table = soup.find('table')
    first_table.encode("UTF-8")
    html_content = ""
    try:
        for string in first_table.contents:
            html_content += string.get_text()

        return html_content
    except TypeError:
        print(sys.exc_info()[1])
        exit_program()
    except IOError:
        print(sys.exc_info()[1])
        exit_program()


def parse_clean_html_file(file_name):
    try:
        html_content = read_file(file_name)
        return html_content
    except FileNotFoundError:
        print("File not found with name [" + file_name + "]")
        exit_program()


def process_clean_html_data(cleaned_html_data):
    try:
        soup = BeautifulSoup(cleaned_html_data, "html.parser", from_encoding="UTF-8")
        tables = soup.findAll("table", limit=2)

        # check if the table is not present in the html file
        if len(tables) < 2:
            raise CustomSuperBowlException("Desired table not found. Please check the cleaned html file.")

        second_table = tables[-1]

        result_data = "Game number,year,winning team,score,losing team,venue\n"
        # Skip the table headers
        for table_rows in second_table.contents[1:51]:
            table_rows.encode("UTF-8")
            single_row = table_rows.get_text("|")
            result_data += process_single_row(single_row) + "\n"

        result_data = result_data[:-1]
        write_file(result_csv_file, result_data)
        print("Successfully created [ " + result_csv_file + " ] file")
        print("Program will exit now... ")
    except TypeError:
        print(sys.exc_info()[1])
        exit_program()
    except CustomSuperBowlException as custom_super_bowl_exception:
        print(custom_super_bowl_exception.value)
        exit_program()
    except AttributeError:
        print(sys.exc_info()[1])
        exit_program()


def process_single_row(single_row):
    single_row_strings = single_row.split("|")
    single_row_data = single_row_strings[1].strip() + ","
    single_row_data += single_row_strings[3][-4:].strip() + ","
    single_row_data += single_row_strings[4][:-1].strip() + ","
    single_row_data += single_row_strings[9].strip() + ","
    single_row_data += single_row_strings[10][:-1].strip() + ","
    single_row_data += single_row_strings[14][:-1].strip()
    return single_row_data


def write_file(filename, text):
    f = open(filename, "w")
    f.write(text)
    f.close()
    return


def read_file(filename):
    f = open(filename, "rU")
    text = f.read()
    f.close()
    return text


def exit_program():
    print("Program will exit now... ")
    sys.exit(1)


if __name__ == '__main__':
    main()