from rich.console import Console
from rich.table import Table
from rich import box

def display_table(console:Console, title: str, headers: list, data: list):
    if len(data) == 0:
        console.print("No data!")
        return
    table = Table(show_header=True)
    table.title = title
    table.box = box.ROUNDED

    for header in headers:
        cell_justify = header.get("justify", "center")
        table.add_column(header["text"], justify=cell_justify)

    for item in data:
        row_data = dict_to_str_array(headers, item)
        table.add_row(*row_data)

    console.print(table)

def dict_to_str_array(headers: list, data: dict) -> list:
        keys = data.keys()
        result_list = []
        if len(keys) == 0:
            return result_list
        for header in headers:
            key = header["value"]
            if key not in data:
                result_list.append("-")
                continue
            if type(data[key]) is dict:
                result_list.append(dict_to_string(data[key]))
            elif type(data[key]) is list:
                result_list.append(list_to_string(data[key]))
            else:
                result_list.append(f'{data[key]}')
        return result_list

def dict_to_string(data: dict) -> str:
    if data.keys() == 0:
        return "-"
    result = ""
    for key in data:
        if type(data[key]) in (int, str, bool, float):
            result += f'{key}: {data[key]}\n'
        elif type(data[key]) is list:
            result += list_to_string(data[key])
    return result

def list_to_string(item_list: list) -> str:
    if len(item_list) == 0:
        return ""
    if type(item_list[0]) == str:
       return  ", ".join(item_list)
    result = ""
    for item in item_list:
        item_str = dict_to_string(item)
        result += item_str
    return result
    