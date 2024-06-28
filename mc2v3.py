import csv
import chardet
import argparse
from datetime import datetime

def detect_encoding(file_path):
    """Detect the encoding of a given file."""
    with open(file_path, 'rb') as file:
        result = chardet.detect(file.read())
    return result['encoding'] or 'utf-8'

def escape_vcard_value(value):
    """ Escape special characters for vCard format """
    return value.replace(';', '\\;').replace(',', '\\,')

# 映射CSV列名到vCard字段
# csv_to_vcard_mapping = {
#     'First Name': 'FN',
#     'Last Name': 'N',
#     'Cell Phone': 'TEL;TYPE=CELL',
#     'Home Phone': 'TEL;TYPE=HOME',
#     'Work Phone': 'TEL;TYPE=WORK',
#     'Home Email': 'EMAIL;TYPE=HOME',
#     'Work Email': 'EMAIL;TYPE=WORK',
#     # 注意：地址需要特殊处理，因为它包含多个分段
#     'Home Address': ('ADR;TYPE=HOME', ['street', 'city', 'state', 'pcode', 'country']), 
#     'Work Address': ('ADR;TYPE=WORK', ['street', 'city', 'state', 'pcode', 'country']),
#     'Company': 'ORG',
#     'Title': 'TITLE',
#     'Notes': 'NOTE',
#     'Website': 'URL'
# }
csv_to_vcard_mapping = {
    'FN': 'FN',
    'N': 'N',
    'TEL;TYPE=CELL': 'TEL;TYPE=CELL',
    'TEL;TYPE=HOME': 'TEL;TYPE=HOME',
    'TEL;TYPE=WORK': 'TEL;TYPE=WORK',
    'EMAIL;TYPE=HOME': 'EMAIL;TYPE=HOME',
    'EMAIL;TYPE=WORK': 'EMAIL;TYPE=WORK',
    # 注意：地址需要特殊处理，因为它包含多个分段
    'ADR;TYPE=HOME;CHARSET=UTF-8': 'ADR;TYPE=HOME;CHARSET=UTF-8', 
    'ADR;TYPE=WORK;CHARSET=UTF-8': 'ADR;TYPE=WORK;CHARSET=UTF-8',
    'ORG;CHARSET=UTF-8': 'ORG;CHARSET=UTF-8',
    #'Title': 'TITLE',
    'NOTE;CHARSET=UTF-8': 'NOTE;CHARSET=UTF-8',
    'URL': 'URL'
}

def create_vcard(row):
    """ Create a single vCard entry from a CSV row with a configurable header """
    vcard = ["BEGIN:VCARD", "VERSION:3.0"]
    
    for csv_key, vcard_field in csv_to_vcard_mapping.items():
        # if isinstance(vcard_field, tuple):  # 特殊处理地址字段
        #     if row[csv_key]:
        #         parts = row[csv_key].split(';')
        #         vcard.append(f"{vcard_field[0]}:;;;;{escape_vcard_value(parts[0])};;;;{escape_vcard_value(parts[1])}")
        # elif row[csv_key]:  # 处理其他普通字段
            vcard_value = row[csv_key]
            if csv_key.startswith('TEL') or csv_key.startswith('EMAIL'):
                vcard_value = f"{vcard_field}:{escape_vcard_value(vcard_value)}"
            else:
                vcard_value = f"{vcard_field}:{escape_vcard_value(vcard_value)}"
            vcard.append(vcard_value)
    
    vcard.append("END:VCARD")
    return "\n".join(vcard) + "\n"


def main(input_csv='contact.csv'):
    # 获取当前时间戳，格式化为字符串
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    output_vcf = f'output_{timestamp}.vcf'
    
    with open(output_vcf, 'w', encoding='utf-8') as vcf_file:
        with open(input_csv, newline='', encoding=detect_encoding(input_csv)) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                vcf_file.write(create_vcard(row))

    print(f"vCards have been successfully written to {output_vcf}.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert a CSV file to vCard format.")
    parser.add_argument('--csv', metavar='CSV_FILE', type=str, help="Input CSV file name. Defaults to 'contact.csv'.")
    args = parser.parse_args()
    
    input_csv = args.csv if args.csv else 'contact.csv'
    main(input_csv)