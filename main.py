import re
import csv
from pathlib import Path
from datetime import datetime

# Delete the files after extracting the values
del_files = True


def main():
    csv_path = Path.cwd() / 'FreewarStatistics.csv'
    downloads_path = Path.home() / 'Downloads'
    html_path = downloads_path / 'Freewar.de.html'
    folder_path = downloads_path / 'Freewar.de_files'
    main_path = folder_path / 'main.html'
    item_path = folder_path / 'item.html'

    paths_dict = {
        'folder_path': folder_path,
        'html_path': html_path
    }

    # Check if the file exists
    assert main_path.exists(), 'The file ' + html_path.__str__() + ' doesn\'t exist!'
    assert csv_path.exists(), 'The file ' + csv_path.__str__() + ' doesn\'t exist!'

    # Read the file
    with open(main_path) as main_file:
        main_str = main_file.read().__str__()
    with open(item_path) as item_file:
        item_str = item_file.read().__str__()

    to_search = [
        'Gold in der Bank',
        'Gold in Aktien',
        'Shopwert aller Items im Inventar',
        'Shopwert aller Items auf der Bank',
        'Gesamtverm\S+gen'
    ]

    results = dict()

    for src_term in to_search:
        print('searching for "' + src_term + '"')
        re_expr = src_term + '\D*(\d+\.?\d*)'
        src_result = re.search(re_expr, main_str)
        if src_result:
            value = int(re.sub('\.', '', src_result.group(1)))
            print(value)
            results[src_term] = value
        else:
            if del_files:
                delete_files(paths_dict)
            raise Exception('Wert für "' + src_term + '" nicht gefunden!')

    src_term = 'Erfahrung'
    print('searching for "' + src_term + '"')
    re_expr = src_term + '\D*(\d+)<span.+</span>(\d+)'
    src_result = re.search(re_expr, item_str)
    if src_result:
        value = int(src_result.group(1) + src_result.group(2))
        print(value)
        results[src_term] = value
    else:
        if del_files:
            delete_files(paths_dict)
        raise Exception('Wert für "' + src_term + '" nicht gefunden!')

    # write to the csv File
    csv_cols = [
        'Gold in der Bank',
        'Gold in Aktien',
        'Shopwert aller Items im Inventar',
        'Shopwert aller Items auf der Bank',
        'Gesamtverm\S+gen',
        'Erfahrung'
    ]
    with open(csv_path, 'a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        col_list = [''] * (len(csv_cols) + 2)
        col_list[0] = datetime.now().strftime('%d.%m.%y %H:%M')
        col_list[-1] = '0'
        for i in range(len(csv_cols)):
            col_list[i + 1] = str(results[csv_cols[i]])
        csv_writer.writerow(col_list)

    if del_files:
        delete_files(paths_dict)


def delete_files(paths: dict):
    # Delete the files
    for file in paths['folder_path'].iterdir():
        file.unlink()
    paths['html_path'].unlink()
    paths['folder_path'].rmdir()
    print('###############################')
    print('# All Files have been deleted #')
    print('###############################')


if __name__ == '__main__':
    main()
