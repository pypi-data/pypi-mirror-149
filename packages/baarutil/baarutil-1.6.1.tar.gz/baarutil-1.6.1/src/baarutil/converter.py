import traceback
import pandas as pd
import numpy as np
from Crypto.Cipher import AES
import base64
from robot.libraries.BuiltIn import BuiltIn
from robot.libraries.BuiltIn import _Misc
import robot.api.logger as logger
from robot.api.deco import keyword
import os
import sys
import json
import random
import array
import datetime
import shutil


def get_python_path():
    path = os.path.split(sys.executable)
    return path


def read_convert(input_str: str) -> list:
    """This function reads the string format and then converts it to a dictionary of lists"""
    dict_list = []
    try:
        inputs = input_str.split("__::__")
        for lines in inputs:
            if str(lines).strip() == '':
                continue
            line_dict = {}
            line = lines.split("__$$__")
            for l in line:
                dict_value = l.split("__=__")
                key = dict_value[0]
                if len(dict_value) == 1:
                    value = ""
                else:
                    value = dict_value[1]
                if key != "":
                    line_dict[key] = value
            dict_list.append(line_dict)
    except Exception as e:
        print(traceback.format_exc(), flush=True)
    return dict_list


def write_convert(input_list: list) -> str:
    """This function reads convert the list of dictionaries(Tabular format) to a string format"""
    output_str = ""
    try:
        for dicts in input_list:
            for key, value in dicts.items():
                output_str = output_str + str(key) + "__=__" + str(value)
                output_str = output_str + "__$$__"
            output_str = output_str[:len(output_str) - 6]
            output_str = output_str + "__::__"
        output_str = output_str[:len(output_str) - 6]
    except Exception as e:
        print(traceback.format_exc(), flush=True)
    return output_str


def string_to_df(input_str: str, rename_cols: dict = {}, drop_dupes=False) -> pd.DataFrame():
    """This function converts the string format to a DataFrame"""
    final_dataframe = pd.DataFrame()
    try:
        for index, data_list in enumerate(input_str.split('__::__')):
            if str(data_list).strip() == '':
                continue
            for each_data in data_list.split('__$$__'):
                if each_data == '':
                    continue
                if '__=__' in each_data:
                    final_dataframe.at[index, str(each_data.split('__=__')[0])] = str(each_data.split('__=__')[1])
        if len(rename_cols) != 0:
            try:
                final_dataframe = final_dataframe.rename(rename_cols, axis=1)
            except Exception as e:
                print(traceback.format_exc(), flush=True)
        if drop_dupes:
            final_dataframe = final_dataframe.drop_duplicates()
        final_dataframe = final_dataframe.replace(np.nan, '', regex=True)
    except Exception as e:
        print(traceback.format_exc(), flush=True)
    return final_dataframe


def df_to_string(input_df: pd.DataFrame(), rename_cols: dict = {}, drop_dupes=False) -> str:
    """This function converts a DataFrame to the string format"""
    final_string = ''
    try:
        input_df = input_df.replace(np.nan, '', regex=True)
        if len(rename_cols) != 0:
            try:
                input_df = input_df.rename(rename_cols, axis=1)
            except Exception as e:
                print(traceback.format_exc(), flush=True)
        if drop_dupes:
            input_df = input_df.drop_duplicates()
        for data_dict in input_df.to_dict('r'):
            for key in data_dict.keys():
                final_string += str(key) + '__=__' + str(data_dict[key]) + '__$$__'
            final_string += '__::__'
    except Exception as e:
        print(traceback.format_exc(), flush=True)
    return final_string


def df_to_listdict(input_df: pd.DataFrame(), rename_cols: dict = {}, drop_dupes=False) -> list:
    """This function converts a DataFrame to the string format"""
    final_list = []
    try:
        input_df = input_df.replace(np.nan, '', regex=True)
        if len(rename_cols) != 0:
            try:
                input_df = input_df.rename(rename_cols, axis=1)
            except Exception as e:
                print(traceback.format_exc(), flush=True)
        if drop_dupes:
            input_df = input_df.drop_duplicates()
        final_list = input_df.to_dict('r')
    except Exception as e:
        print(traceback.format_exc(), flush=True)
    return final_list


def perform_base_decryption(encrypted_message: str, config_file: str = 'baarutil_config.json') -> str:
    """This function decrypts the Old Baar Vault Encrypted info"""
    decrypted_text = ''
    key = ''
    iv = ''
    key_name = ''
    iv_name = ''
    py_path = get_python_path()
    if len(py_path) != 0:
        config_path = os.path.join(py_path[0], 'Scripts', config_file)
        if os.path.isfile(config_path):
            try:
                config_json = open(config_path)
                config_data = json.load(config_json)
                if 'key_mapping' in config_data.keys() and 'key_value' in config_data.keys():
                    if 'key' in config_data['key_mapping'].keys() and 'iv' in config_data['key_mapping'].keys():
                        key_name = config_data['key_mapping']['key']
                        iv_name = config_data['key_mapping']['iv']
                        if key_name in config_data['key_value'].keys() and iv_name in config_data['key_value'].keys():
                            key = config_data['key_value'][key_name]
                            iv = config_data['key_value'][iv_name]
                            # ~~~~~~~~ Starting Decryption ~~~~~~~~
                            decrypted_text = base64.urlsafe_b64decode(encrypted_message)
                            decipher = AES.new(bytes(key, encoding='utf-8'), AES.MODE_CBC, bytes(iv, encoding='utf-8'))
                            decrypted_bytes = decipher.decrypt(decrypted_text)
                            decrypted_text = decrypted_bytes.decode('utf-8')
                            unpad = lambda s: s[0:-ord(s[-1])]
                            decrypted_text = unpad(decrypted_text)
                        else:
                            print('Decryption failed! Incorrect config (unknown vey value Pair):', config_path, flush=True)
                    else:
                        print('Decryption failed! Incorrect config (missing key and iv):', config_path, flush=True)
                else:
                    print('Decryption failed! Incorrect config:', config_path, flush=True)
            except Exception as e:
                print(traceback.format_exc(), flush=True)
                pass
        else:
            print('Decryption failed! Missing config file:', config_path, flush=True)
    return decrypted_text


@keyword("Decrypt Vault")
def decrypt_vault(encrypted_message: str, config_file: str = 'baarutil_config.json') -> str:
    """This function decrypts the Baar Vault Encrypted info 2.0"""
    try:
        # This will set the Log Level to NONE if it is called from a Robot Framework script
        BuiltIn.log_to_console(BuiltIn(), 'Setting Log Level from INFO to NONE!')
        old = _Misc.set_log_level(_Misc(), level='NONE')
    except:
        pass
    decrypted_string = ''
    try:
        if len(encrypted_message) != 0:
            decrypted_text = base64.b64decode(encrypted_message)
            decrypt_str = decrypted_text.decode(encoding='utf-8')
            split_num = int(decrypt_str[-1])
            decrypt_str = decrypt_str[:-1]
            split_strings = [decrypt_str[index: index + split_num] for index in range(0, len(decrypt_str), split_num)]
            extracted_string = "".join([split_strings[index] for index in range(len(split_strings)) if index == 0 or index % 2 == 0])
            extracted_string = extracted_string.rstrip('@')
            layer_num = int(extracted_string[-1])
            decrypted_string = extracted_string[:-1]
            for iiter in range(0, layer_num + 1):
                decrypted_string = perform_base_decryption(decrypted_string)
        else:
            print('Decryption failed! Encrypted data is empty', flush=True)
    except Exception as e:
        print('Decryption failed! Incorrect Encrypted data.', flush=True)
        print(traceback.format_exc(), flush=True)
    return decrypted_string


@keyword("Generate Password")
def generate_password(password_size: int=10, upper: bool=True, lower: bool=True, digits: bool=True, symbols: bool=True, exclude_chars: list=[]) -> str:
    """This function generates random Passwords"""
    try:
        # This will set the Log Level to NONE if it is called from a Robot Framework script
        BuiltIn.log_to_console(BuiltIn(), 'Setting Log Level from INFO to NONE!')
        old = _Misc.set_log_level(_Misc(), level='NONE')
    except:
        pass

    def apply_exclusion_list(char_list, exclusion_list):
        final_list = []
        try:
            final_list = [char for char in char_list if char not in exclusion_list]
        except Exception as e:
            print(traceback.format_exc(), flush=True)
        return final_list

    # ~~~~ Variable Initialization ~~~~
    password = ''
    MAX_LEN = password_size
    DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    LOCASE_CHARACTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    UPCASE_CHARACTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'M', 'N', 'O', 'p', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    SYMBOLS = ['@', '#', '$', '%', '=', ':', '?', '.', '/', '|', '~', '>', '*', '(', ')', '<']
    rand_digit = rand_upper = rand_lower = rand_symbol = ''
    final_combined_list = []
    default_count = 0

    # ~~~~ Applying exclusion list ~~~~
    DIGITS = apply_exclusion_list(DIGITS, exclude_chars)
    LOCASE_CHARACTERS = apply_exclusion_list(LOCASE_CHARACTERS, exclude_chars)
    UPCASE_CHARACTERS = apply_exclusion_list(UPCASE_CHARACTERS, exclude_chars)
    SYMBOLS = apply_exclusion_list(SYMBOLS, exclude_chars)

    # ~~~~ Main Operation ~~~~
    try:
        if not password_size < 4:
            if upper:
                final_combined_list += UPCASE_CHARACTERS
                rand_upper = random.choice(UPCASE_CHARACTERS)
                default_count += 1
            if lower:
                final_combined_list += LOCASE_CHARACTERS
                rand_lower = random.choice(LOCASE_CHARACTERS)
                default_count += 1
            if digits:
                final_combined_list += DIGITS
                rand_digit = random.choice(DIGITS)
                default_count += 1
            if symbols:
                final_combined_list += SYMBOLS
                rand_symbol = random.choice(SYMBOLS)
                default_count += 1

            if upper or lower or digits or symbols:
                COMBINED_LIST = final_combined_list
                temp_pass = rand_digit + rand_upper + rand_lower + rand_symbol
                temp_pass_list = []
                for count in range(MAX_LEN - default_count):
                    temp_pass = temp_pass + random.choice(COMBINED_LIST)
                    temp_pass_list = array.array('u', temp_pass)
                    random.shuffle(temp_pass_list)
                for char in temp_pass_list:
                    password = password + char
            else:
                print('All character types must not be False.', flush=True)
        else:
            print('Password length must be more than 4.', flush=True)
    except Exception as e:
        print(traceback.format_exc(), flush=True)

    return password


@keyword("Generate Report")
def generate_report(data_df: pd.DataFrame(), file_name: str, path: str = os.getcwd(), file_type: str = 'csv', detailed_report: bool = False, replace_old_file: bool = False, final_file_name_case: str = 'unchanged', time_stamp: bool = False, encoding: str = 'utf-8', index: bool = False, engine: str = 'openpyxl', max_new_files_count: int = 100, sheet_name: str = 'Sheet1'):
    start_time = str(datetime.datetime.now())
    alt_file_type = file_type = str(file_type).lower().strip().replace(' ', '')
    final_file_name_case = str(final_file_name_case).lower().strip().replace(' ', '')
    supported_extension_list = ['csv', 'xlsx']
    supported_final_file_name_case = ['upper', 'lower', 'unchanged']
    # ~~~~~~~~~~ Initializing Return variables ~~~~~~~~~~
    status_dict = {}
    status_dict['file_path'] = file_path = ''
    status_dict['file_generation_status'] = file_generation_status = False
    status_dict['message'] = message = 'EORROR: File generation failed! Please check the inputs.'
    status_dict['start_time'] = start_time
    status_dict['end_time'] = start_time
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    try:
        if file_type in supported_extension_list:
            if final_file_name_case in supported_final_file_name_case:
                if os.path.isdir(path):
                    if final_file_name_case == 'upper':
                        file_name = file_name.upper()
                        file_type = file_type.upper()
                        file_type = file_type.upper() if file_type.lower().strip() != 'xlsx' else file_type.lower()
                        alt_file_type = file_type.lower()
                    elif final_file_name_case == 'lower':
                        file_name = file_name.lower()
                        alt_file_type = file_type = file_type.lower()
                    if not replace_old_file:
                        temp_file_name = file_name
                        for file_count in range(1, max_new_files_count+1):
                            if temp_file_name + '.' + file_type in os.listdir(path):
                                temp_file_name = file_name + '(' + str(file_count) + ')'
                        file_name = temp_file_name
                    else:
                        for file in os.listdir(path):
                            if file.lower() == file_name.lower() + '.' + file_type.lower():
                                os.remove(os.path.join(path, file))
                    if time_stamp:
                        curr_time_stamp = str(int(datetime.datetime.now().replace(microsecond=0).timestamp()))
                        file_name += '-' + curr_time_stamp
                    file_path = os.path.join(path, file_name + '.' + file_type)
                    try:
                        if file_type.lower() == 'csv':
                            data_df.to_csv(file_path, encoding=encoding, index=index)
                            file_generation_status = True
                            message = 'SUCCESS: File Generation Successful!'
                        elif file_type.lower() == 'xlsx':
                            try:
                                data_df.to_excel(file_path, encoding=encoding, index=index, engine=engine, sheet_name=sheet_name)
                                message = 'SUCCESS: File Generation Successful!'
                                file_generation_status = True
                            except:
                                data_df.to_excel(file_path, encoding=encoding, index=index, sheet_name=sheet_name)
                                message = f'SUCCESS: File Generation Successful! However, excel writer engine {engine} is not supported in this system.'
                                file_generation_status = True
                        else:
                            message = f"""EORROR: File generation failed! File type "{file_type}" not supported. Only supported formats are - {','.join(supported_extension_list)}"""
                    except Exception as e:
                        print(traceback.format_exc(), flush=True)
                        message = 'EORROR: File generation failed! Incorrect file write configurations (pandas to_csv/ to_excel).'
                else:
                    message = f"""EORROR: File generation failed! Path - "{path}" doesn't exists"""
            else:
                message = f"""EORROR: File generation failed! File name case "{final_file_name_case}" not supported. Only supported cases are - {','.join(supported_final_file_name_case)}"""
        else:
            message = f"""EORROR: File generation failed! File type "{file_type}" not supported. Only supported formats are - {','.join(supported_extension_list)}"""
    except Exception as e:
        print(traceback.format_exc(), flush=True)
    status_dict['file_path'] = file_path
    status_dict['file_generation_status'] = file_generation_status
    status_dict['message'] = message
    status_dict['start_time'] = start_time
    status_dict['end_time'] = str(datetime.datetime.now())
    print(message, flush=True)
    if detailed_report:
        return status_dict
    else:
        return file_generation_status


@keyword("String To Report")
def string_to_report(data: str, file_name: str, path: str = os.getcwd(), file_type: str = 'csv', detailed_report: bool = False, replace_old_file: bool = False, final_file_name_case: str = 'unchanged', time_stamp: bool = False, encoding: str = 'utf-8', index: bool = False, engine: str = 'openpyxl', max_new_files_count: int = 100, sheet_name: str = 'Sheet1', rename_cols: dict = {}, drop_dupes: bool = False):
    data_df = string_to_df(data, rename_cols, drop_dupes)
    status = generate_report(data_df, file_name, path, file_type, detailed_report, replace_old_file, final_file_name_case, time_stamp, encoding, index, engine, max_new_files_count, sheet_name)
    return status


@keyword("Clean Directory")
def clean_directory(path: str, remove_directory: bool=False) -> bool:
    status = False
    iter_count = 0
    unique_path_list = list(set(path.split('|')))
    for individual_path in unique_path_list:
        iter_count += 1
        status = False
        if os.path.isdir(individual_path):
            if len(os.listdir(individual_path)) != 0:
                for file in os.listdir(individual_path):
                    if os.path.isfile(os.path.join(individual_path, file)):
                        try:
                            os.remove(os.path.join(individual_path, file))
                            status = True
                        except Exception as e:
                            print(traceback.format_exc(), flush=True)
                    elif os.path.isdir(os.path.join(individual_path, file)) and remove_directory:
                        try:
                            shutil.rmtree(os.path.join(individual_path, file), ignore_errors=True)
                            status = True
                        except Exception as e:
                            print(traceback.format_exc(), flush=True)
    return status


@keyword("Archive")
def archive(source: str, destination: str, operation_type: str = 'cut', dynamic_folder: bool = True, dynamic_filename: bool = False, custom_folder_name_prefix: str = 'Archive', timestamp_format: str = '''%d-%m-%Y_%H.%M.%S'''):
    try:
        completion_flag = False
        supported_op_types = ['cut', 'copy']
        folder_name = ''
        failed_items = []
        final_destination = ''
        curr_raw_timestamp = int(datetime.datetime.now().replace(microsecond=0).timestamp())
        curr_timestamp = datetime.datetime.now().strftime(timestamp_format)
        if str(timestamp_format).strip().lower() == 'timestamp':
            folder_name = custom_folder_name_prefix + '_' + curr_raw_timestamp
            curr_timestamp = curr_raw_timestamp
        else:
            folder_name = custom_folder_name_prefix + '_' + curr_timestamp
        if dynamic_folder:
            destination = os.path.join(destination, folder_name)
        final_destination = destination
        if str(operation_type).strip().lower() in supported_op_types:
            if not dynamic_filename:
                if os.path.isdir(source):
                    if os.path.isdir(destination):
                        try:
                            shutil.copytree(source, destination)
                            if str(operation_type).strip().lower() == 'cut':
                                clean_directory(source, remove_directory=True)
                                completion_flag = True
                            elif str(operation_type).strip().lower() == 'copy':
                                completion_flag = True
                        except Exception as e:
                            print(traceback.format_exc(), flush=True)
                            completion_flag = False
                    else:
                        try:
                            shutil.copytree(source, destination)
                            if str(operation_type).strip().lower() == 'cut':
                                clean_directory(source, remove_directory=True)
                                completion_flag = True
                            elif str(operation_type).strip().lower() == 'copy':
                                completion_flag = True
                        except Exception as e:
                            print(traceback.format_exc(), flush=True)
                            completion_flag = False
                else:
                    print(f'''Source folder "{source}" is not a valid path. Please re-check!''', flush=True)
            else:
                if os.path.isdir(source):
                    if os.path.isdir(destination):
                        for file in os.listdir(source):
                            try:
                                if os.path.isfile(os.path.join(source, file)):
                                    modified_file_name = ''.join(str(file).split('.')[:-1]) + '_' + str(curr_timestamp) + '.' + str(str(file).split('.')[-1])
                                    shutil.copy2(os.path.join(source, file), os.path.join(destination, file))
                                    os.rename(os.path.join(destination, file), os.path.join(destination, modified_file_name))
                                elif os.path.isdir(os.path.join(source, file)):
                                    modified_folder_name = str(file) + '_' + str(curr_timestamp)
                                    shutil.copytree(os.path.join(source, file), destination)
                                    os.rename(os.path.join(destination, file), os.path.join(destination, modified_folder_name))
                            except Exception as e:
                                print(traceback.format_exc(), flush=True)
                                failed_items.append(file)
                                completion_flag = False
                        if str(operation_type).strip().lower() == 'cut':
                            clean_directory(source, remove_directory=True)
                            completion_flag = True
                        elif str(operation_type).strip().lower() == 'copy':
                            completion_flag = True
                    else:
                        os.makedirs(destination)
                        for file in os.listdir(source):
                            try:
                                if os.path.isfile(os.path.join(source, file)):
                                    modified_file_name = ''.join(str(file).split('.')[:-1]) + '_' + str(curr_timestamp) + '.' + str(str(file).split('.')[-1])
                                    shutil.copy2(os.path.join(source, file), os.path.join(destination, file))
                                    os.rename(os.path.join(destination, file), os.path.join(destination, modified_file_name))
                                elif os.path.isdir(os.path.join(source, file)):
                                    modified_folder_name = str(file) + '_' + str(curr_timestamp)
                                    shutil.copytree(os.path.join(source, file), destination)
                                    os.rename(os.path.join(destination, file), os.path.join(destination, modified_folder_name))
                            except Exception as e:
                                print(traceback.format_exc(), flush=True)
                                failed_items.append(file)
                                completion_flag = False
                        if str(operation_type).strip().lower() == 'cut':
                            clean_directory(source, remove_directory=True)
                            completion_flag = True
                        elif str(operation_type).strip().lower() == 'copy':
                            completion_flag = True
                else:
                    print(f'''Source folder "{source}" is not a valid path. Please re-check!''', flush=True)
        else:
            print(f'''Selected operation type {operation_type} is not supported. Only supported operation types are - {",".join(operation_type)}''', flush=True)
    except Exception as e:
        print(traceback.format_exc(), flush=True)
        completion_flag = False
    if not completion_flag and len(failed_items) != 0:
        print(f'''Failed Items:\n{",".join(failed_items)}''')
        final_destination = ''
    return completion_flag, final_destination
