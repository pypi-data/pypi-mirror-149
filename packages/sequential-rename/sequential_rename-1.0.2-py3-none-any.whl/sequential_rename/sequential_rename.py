import re
from typing import Union
from pathlib import Path


def seq_rename(new_directory: Union[str, Path], current_file_name: str, file_extension: str):
    search_param = re.compile(r'(\(\d+\))')
    regex_search = re.search(search_param, current_file_name)
    if Path(new_directory).joinpath(f'{current_file_name}{file_extension}').exists():
        if regex_search:
            file_num = re.sub('[()]', '', regex_search.group(0))
            file_name_no_num = re.sub(search_param, '', current_file_name).strip()
            new_num = int(file_num) + 1
            new_file_name = f'{file_name_no_num} ({new_num})'
        else:
            new_file_name = f'{current_file_name} (1)'
    else:
        return f'{current_file_name}{file_extension}'

    if new_directory.joinpath(f'{new_file_name}{file_extension}').exists():
        return seq_rename(new_directory, new_file_name, file_extension)
    else:
        return f'{new_file_name}{file_extension}'
