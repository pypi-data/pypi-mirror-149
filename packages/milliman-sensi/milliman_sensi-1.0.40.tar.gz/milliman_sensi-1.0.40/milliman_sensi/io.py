import json
import os
import re
import shutil
import logging

import pandas as pd
import numpy as np
import milliman_sensi.syntax as syn

from pathlib import Path

pd.options.mode.chained_assignment = None  # Used to supress panda warning
SENSI_CONFIG_HEADER = ['Scenario', 'Stress name', 'Apply stress']

logger = logging.getLogger(__name__)

def setup_syntax_logger(handler, level=None):
    syn.logger.addHandler(handler)

    # To prevent setting the logger level multiple times
    if level:
        syn.logger.setLevel(level)


# Custom Exception class for sensi validation and modification
class SensiIOError(Exception):
    def __init__(self, msg):
        self.msg = str(msg)

    def __str__(self):
        return self.msg


def read_json_file(file_path):
    logger.debug(f'Reading json file in {file_path}')
    data = None
    try:
        with open(file_path) as json_file:
            data = json.load(json_file)
    except ValueError:
        logger.error(f'Error has occurred when reading json_file in {file_path}.', exc_info=True)
        raise ValueError("Failed to load the json file {}".format(file_path))
    except FileNotFoundError:
        logger.error(f'Error has occurred when reading json_file in {file_path}.', exc_info=True)
        raise FileNotFoundError("Unable to find json file {}".format(file_path))

    logger.debug(f'Returned json file from {file_path}')
    return data


def find_file_in_directory(filename, dir):
    logger.debug(f'Searching for filename: {filename} in dir: {dir}')
    for root, dirs, files in os.walk(dir):
        if filename in files:
            logger.info(f'Returned path to {filename}')
            return os.path.join(root, filename).replace("\\", "/")
    logger.debug('File was not found. ')
    return None


def validate_sensi_config(filepath):
    logger.info(f'Validating sensi config in filepath: {filepath}')
    if not os.path.exists(filepath):
        logger.error(f'{filepath} does not exist. Unable to validate sensi_config')
        return "{} does not exist".format(filepath)

    logger.debug('Reading content of sensi_config')
    sensi_config = pd.read_csv(filepath, sep=r'~', header=None).squeeze("columns")
    sensi_config = sensi_config.map(lambda x: re.sub(r'"([^"]*)"', lambda m: re.sub(r';', '_SEMI_COL', m.group()), x))
    sensi_config = pd.concat([
        sensi_config.str.split(';', expand=True),
        sensi_config.str.count(';').rename('_count_sep')
        ], axis=1)

    logger.debug(f'Verifying that number of columns is consistent.')
    if sensi_config['_count_sep'].nunique(dropna=True) != 1:
        sensi_config_rows_with_more_columns = sensi_config[
            sensi_config['_count_sep'] > sensi_config.iloc[0]['_count_sep']]['_count_sep']
        sensi_config_rows_with_less_columns = sensi_config[
            sensi_config['_count_sep'] < sensi_config.iloc[0]['_count_sep']]['_count_sep']

        message1 = "" if sensi_config_rows_with_more_columns.empty else "Rows with additional columns are {}".format(list(sensi_config_rows_with_more_columns.index.values))
        message2 = "" if sensi_config_rows_with_less_columns.empty else "Rows with fewer columns are {}".format(list(sensi_config_rows_with_less_columns.index.values))

        logger.error(f'Returned the rows with incorrect number of values in sensi_config:\n' + '\n'.join([message1, message2]))
        return '\n'.join([message1, message2])

    else:
        sensi_config = sensi_config.drop(columns=['_count_sep'])
        sensi_config.columns = sensi_config.iloc[0]
        sensi_config = sensi_config[1:]
        sensi_config.reset_index(drop=True)

    sensi_config_copy = sensi_config

    sensi_config_columns = list(sensi_config_copy.columns)
    message = []

    logger.debug(f'Validating that the required columns {SENSI_CONFIG_HEADER} exist.')
    if len(sensi_config_columns) > len(SENSI_CONFIG_HEADER):
        difference = list(set(sensi_config_columns) - set(SENSI_CONFIG_HEADER))
        for ele in sorted(difference):
            message.append("'Sensi_config.csv': '{}' is extra".format(ele))
    elif len(sensi_config_columns) < len(SENSI_CONFIG_HEADER):
        difference = list(set(SENSI_CONFIG_HEADER) - set(sensi_config_columns))
        for ele in sorted(difference):
            message.append("'Sensi_config.csv': '{}' is missing".format(ele))
    else:
        for index in range(len(sensi_config_columns)):
            if sensi_config_columns[index] != SENSI_CONFIG_HEADER[index]:
                message.append("'Sensi_config.csv': '{}' is incorrect, should be '{}'"
                               .format(sensi_config_columns[index], SENSI_CONFIG_HEADER[index]))

    if message:
        logger.error(f'Returned the list of invalid columns in sneis_config:' + '\n'.join(message))
        return '\n'.join(message)
    else:
        if sensi_config_copy['Apply stress'].dtype != bool:
            d = {'true': True, 'false': False}
            sensi_config_copy['Apply stress'] = sensi_config_copy['Apply stress'].apply(
                lambda x: x if isinstance(x, bool) or x.lower() not in ['true', 'false'] else d[x.lower()])
            incorrect_values = sensi_config_copy[(sensi_config_copy[['Apply stress']].applymap(type) != bool).any(axis=1)]
            if not incorrect_values.empty:
                return "'Sensi_config.csv': 'Apply stress' has incorrect entry at row(s) {}".format(
                    list(incorrect_values.index.values))

    logger.debug("Returned sensi_config:\n" + '\t' + sensi_config.to_string().replace('\n', '\n\t'))     
    return sensi_config


def validate_sensi_param(filepath):
    logger.info(f'Validating sensi param in filepath: {filepath}')
    if not os.path.exists(filepath):
        logger.error(f'The file at {filepath} does not exist. Unable to validate sensi_param')
        return "{} does not exist".format(filepath)

    logger.debug('Reading content of sensi_param')
    sensi_param = pd.read_csv(filepath, sep=r'~', header=None).squeeze("columns")
    sensi_param = sensi_param.map(lambda x: re.sub(r'"([^"]*)"', lambda m: re.sub(r';', '_SEMI_COL', m.group()), x))
    sensi_param = pd.concat([
        sensi_param.str.split(';', expand=True),
        sensi_param.str.count(';').rename('_count_sep')
        ], axis=1)

    logger.debug(f'Verifying that number of columns is consistent.')
    if sensi_param['_count_sep'].nunique(dropna=True) != 1:
        sensi_param_rows_with_more_columns = sensi_param[
            sensi_param['_count_sep'] > sensi_param.iloc[0]['_count_sep']]['_count_sep']
        sensi_param_rows_with_less_columns = sensi_param[
            sensi_param['_count_sep'] < sensi_param.iloc[0]['_count_sep']]['_count_sep']

        message1 = "" if sensi_param_rows_with_more_columns.empty else "Rows with additional columns are {}".format(list(sensi_param_rows_with_more_columns.index.values))
        message2 = "" if sensi_param_rows_with_less_columns.empty else "Rows with fewer columns are {}".format(list(sensi_param_rows_with_less_columns.index.values))

        logger.error('Returned the rows with incorrect number of values in sensi_param: ' + '\n'.join([message1, message2]))
        return '\n'.join([message1, message2])
    else:
        sensi_param = sensi_param.drop(columns=['_count_sep'])
        sensi_param.columns = sensi_param.iloc[0]
        sensi_param = sensi_param[1:]
        sensi_param.reset_index(drop=True)
        logger.debug('Finished setting up sensi config file')

    sensi_param_copy = sensi_param

    sensi_param_columns = list(sensi_param_copy.columns)
    message = ""

    if sensi_param_columns[0] != 'Name':
        message = "Missing column 'Name' in Sensi_param.csv"

    if message:
        logger.error(f'Returned the list of invalid columns in sensi_param: {message}')
        return message

    logger.debug(f"Returned sensi_param:\n" + '\t' + sensi_param.to_string().replace('\n', '\n\t'))   
    return sensi_param


def read_sensitivities(env_dir):
    """
    1. Read Sensi_config.csv & Sensi_param.csv in the /sensitivities directory (throw error if column does not match)
    2. Sanitary check for columns in both csv files
    3. Return two dict: sensi_list, param_map
       sensi_list: Name_in_Sensi_config -> [List_of_Stress_name_in_Sensi_config_in_order]
         eg: "Sensi_1" -> ["Stress_vol_1", "Stress_eq_vol_1"]
       param_map: Stress_name_in_Sensi_param -> [List_of_Parameters_syntax_in_Sensi_param]
         eg: "Stress_vol_1" -> ["param.H=(+100)","file::eco[GBP].driver[IR].data.swaptions.mkt[*,1]=(+100)"]
    """
    logger.info(f"Reading sensi files in {env_dir}")
    sensi_list = {}
    param_map = {}
    result = validate_sensi_config(find_file_in_directory('Sensi_config.csv', env_dir))
    if isinstance(result, str):
        logger.error(f'Sensi_config validation was unsuccessful')
        raise SensiIOError(result)

    sensi_config = result

    result = validate_sensi_param(find_file_in_directory('Sensi_param.csv', env_dir))
    if isinstance(result, str):
        logger.error(f'Sensi_param validation was unsuccessful')
        raise SensiIOError(result)

    sensi_param = result
    sensi_names = sensi_config['Scenario'].unique()
    logger.info(f'Fetched sensi_names : {sensi_names}')

    # Add all sensi to sensi_names and fill the ones with a stress to Apply
    sensi_list = {sensi: [] for sensi in sensi_names}
    for sensi in sensi_names:
        sensi_list[sensi] = list(sensi_config["Stress name"][ (sensi_config["Scenario"] == sensi) & (sensi_config["Apply stress"] == True) ])
        logger.debug(f'{sensi} added to sensi_list')

    sensi_param_stresses = set(sensi_param.columns)
    sensi_param_stresses.remove("Name")

    # Checks if colmuns of sensi_config['Stress name'] values all are columns in sensi_param by
    # verifying that sensi_config['Stress name'] are contained in sensi_param.columns
    logger.debug(f'Verifying that all sensi_config columns exist in sensi_param.')
    if sensi_param_stresses is None :
        logger.error(f'Sensi_config do not contain any stresses from Sensi_param')
        raise SensiIOError("Sensi_config do not contain any stresses from Sensi_param")

    if not set(sensi_config['Stress name']).issubset(sensi_param_stresses):
        logger.error(f'Columns {set(sensi_config["Stress name"]) - sensi_param_stresses} in Sensi_param do not match the stresses in sensi_config')
        raise SensiIOError("Columns {} in Sensi_param do not match the stresses in sensi_config".format(set(sensi_config['Stress name']) - sensi_param_stresses))

    param_map_unsorted = {}

    logger.debug(f'Cleaning up the list of sensi_param')
    for stress_name in list(sensi_param.columns)[1:]:
        # Drop all rows with empty values for that stress_name
        sensi_param_cleaned = sensi_param[['Name', stress_name]]
        sensi_param_cleaned.replace('', np.nan, inplace=True)
        sensi_param_cleaned.dropna(inplace=True)
        # Concatenate values
        sensi_param_cleaned[stress_name] = sensi_param_cleaned['Name'] + '=' + sensi_param_cleaned[stress_name].astype(str)
        param_map_unsorted[stress_name] = sensi_param_cleaned.to_dict('list')[stress_name]

    # Ordering Stress names in param_map following the values in sensi_config.csv
    logger.debug(f'Orderding the list of sensi in sensi_param')
    param_map = {key: param_map_unsorted[key] for key in sensi_config[sensi_config['Apply stress'] == True]['Stress name']}

    # Pop the list of sensi without stress to be applied from sensi_list
    sensi_list_without_stress = [sensi for sensi in sensi_list.keys() if len(sensi_list[sensi]) == 0]
    sensi_list = {k: v for k, v in sensi_list.items() if v}

    logger.debug(f'Returned sensi_list:\n {sensi_list}\n sensi_list_without_stress:\n {sensi_list_without_stress}\n and param_map:\n {param_map}')

    return sensi_list, sensi_list_without_stress, param_map


def create_dir_for_one_sensi_from_base(sensi_name, base_dir, sensi_path=None):
    logger.info(f'Creating "{sensi_name}" directory from {base_dir}')
    if sensi_path is not None:
        logger.debug(f'Creating the directory in {sensi_path}')
        sensi_path = sensi_path.replace("\\", '/')
        try:
            # Re-copy all files
            logger.info(f"Copying files to {sensi_path}")
            sensi_rsrc_dir = os.path.join(sensi_path, "resources").replace("\\", "/")
            sensi_rsrc_admin_dir = os.path.join(sensi_path, "resources_admin").replace("\\", "/")
            base_rsrc_dir = os.path.join(base_dir, "resources").replace("\\", "/")
            base_rsrc_admin_dir = os.path.join(base_dir, "resources_admin").replace("\\", "/")
            if os.path.exists(sensi_rsrc_dir):
                shutil.rmtree(sensi_rsrc_dir)

            if os.path.exists(base_rsrc_dir):
                shutil.copytree(base_rsrc_dir, sensi_rsrc_dir)

            if os.path.exists(sensi_rsrc_admin_dir):
                shutil.rmtree(sensi_rsrc_admin_dir)

            if os.path.exists(base_rsrc_admin_dir):
                shutil.copytree(base_rsrc_admin_dir, sensi_rsrc_admin_dir)
            logger.debug('Copy completed')

            logger.info('Cleaning up calibration_settings.json and simulation_settings.json')
            try:
                os.remove(os.path.join(sensi_rsrc_dir, 'settings_calibration.json'))
                logger.debug(f'{os.path.join(sensi_rsrc_dir, "settings_calibration.json")} was deleted!')
            except OSError:
                logger.warning(f'Settings_calibration.json does not exist in {sensi_rsrc_dir}')

            try:
                os.remove(os.path.join(sensi_rsrc_dir, 'settings_simulation.json'))
                logger.debug(f'{os.path.join(sensi_rsrc_dir, "settings_simulation.json")} was deleted!')
            except OSError:
                logger.warning(f'settings_simulation.json does not exist in {sensi_rsrc_dir}')

            logger.debug('Clean up completed.')

        except Exception as exc:
            logger.error(f'Copy from {base_dir} to {sensi_path} failed', exc_info=True)
            return SensiIOError(f"Unable to copy files to {sensi_name}: {exc}")

        try:
            logger.debug('Writing values for sensi in settings.json')
            settings_json_path = f"{sensi_path}/resources/settings.json"
            settings_json_sensi = read_json_file(settings_json_path)
            settings_json_sensi['gen_param']['name'] = '{}_{}'.format(settings_json_sensi['gen_param']['name'], sensi_name)
            settings_json_sensi['gen_param']['path'] = sensi_path
            settings_json_sensi['framework']['sensi_1']['name'] = sensi_name
            with open(settings_json_path, 'w') as f:
                f.write(json.dumps(settings_json_sensi, indent=4))
        except Exception as err:
            logger.error(f'Writing settings_json to {settings_json_path} failed', exc_info=True)
            return SensiIOError("Unable to read/write settings.json to {}".format(sensi_name))

    logger.debug(f'Returned sensi_path: {sensi_path}')
    return sensi_path

class SensiConfig:
    def __init__(self, env_dir):
        logger.info(f'Creating SensiConfig object with env_dir: {env_dir}')
        if not os.path.exists(env_dir):
            logger.error(f'Failed to find Base table {env_dir}')
            raise SensiIOError("Base table {} does not exist".format(env_dir))
        self.base_dir = env_dir
        self.settings_json = read_json_file(f'{env_dir}/resources/settings.json')
        self.sensi_list, self.sensi_list_without_any_stress, self.param_map = read_sensitivities(self.base_dir)

    def get_stress_desc(self, sensi_name):
        logger.info(f'Get stress description for sensi in {sensi_name}')
        param_list = self.sensi_list.get(sensi_name, [])
        return "".join([">>".join(self.param_map.get(p, [""])) for p in param_list])

    def create_tables(self, sensi_dirs={}):
        logger.info(f'Creating tables for sensi_list: {self.sensi_list}')
        # For Seni_config.csv
        # To new create directory from the name of the Scenario
        # Copy env_dir to each directory of the name of the Scenario
        # Replace gen_param.name = name of the Scenario in the settings.json of the newly copied directory
        # Replace gen_param.path = newly created path
        # Input sensi_dirs can be provided by the API as dict { "<SENSI_NAME>":"<TABLE_ENV_PATH>" }
        # If sensi_dirs is provided, only the tables for the Sensi there are created
        # Else all the tables are created for every sensi in sensi_list
        # Dict that contains the list of sensi and their dirs

        processed_sensi_dirs = {}
        if len(self.sensi_list) > 0:
            logger.debug(f'Creating list of sensi_dirs to be processed')
            if len(sensi_dirs) > 0:
                logger.debug(f'Modifying list using: {sensi_dirs}')
                for sensi in self.sensi_list.keys():
                    # Checks that it is a sensi in the specified sensi lists (i.e. sensi_dirs) 
                    # or that there is at least one stress name to apply for it.
                    if sensi in sensi_dirs.keys() and len(self.sensi_list[sensi]) > 0:
                        res = create_dir_for_one_sensi_from_base(sensi, self.base_dir, sensi_dirs[sensi])
                        if res is not None:
                            processed_sensi_dirs[sensi] = res
                            logger.debug(f'Added {sensi} to processed_sensi_dirs')
            else:
                path = Path(self.base_dir)
                parent_dir = path.parent
                for sensi in self.sensi_list.keys():
                    if len(self.sensi_list[sensi]) > 0:
                        res = create_dir_for_one_sensi_from_base(sensi, self.base_dir, os.path.join(parent_dir, sensi))
                        if res is not None:
                            processed_sensi_dirs[sensi] = res
                            logger.debug(f'Added {sensi} to processed_sensi_dirs')

        logger.debug(f'Returned processed_sensi_dirs:\n {processed_sensi_dirs}')
        return processed_sensi_dirs

    def apply(self, sensi_dirs={}):
        logger.info(f'Applying stress for sensi in {self.sensi_list}')
        # For Sensi_param.csv
        # Iterate over sensi_list and apply the stress in the param_map
        # When interate param_map:
        # Build the good correct path from the json query
        # Call syntax.apply_sentax_to_file(path, syntax) in the syntax.py
        # Input sensi_dirs can be provided by the API as dict { "<SENSI_NAME>":"<TABLE_ENV_PATH>" }
        # If sensi_dirs is provided, only Sensi in sensi_dirs are stress applied
        # Else all the sensis are stress applied
        # Dict that contains the list of sensi and their dirs
        sensi_dirs_to_process = {}
        processed_sensi_messages = {}
        if len(self.sensi_list)>0:
            logger.debug(f'Creating list of sensi_dirs to be processed')
            if len(sensi_dirs)>0:
                logger.debug(f'Inserting sensi_dirs in {sensi_dirs} to sensi_dirs_to_process')
                for sensi in self.sensi_list.keys():
                    if sensi in sensi_dirs.keys():
                        sensi_dirs_to_process[sensi] = sensi_dirs[sensi].replace('\\', '/')
                        logger.debug(f'Added {sensi} to sensi_dirs_to_process')
            else:
                path = Path(self.base_dir)
                parent_dir = path.parent
                for sensi in self.sensi_list.keys():
                    sensi_dirs_to_process[sensi] = os.path.join(parent_dir, sensi).replace('\\', '/')
                    logger.debug(f'Added {sensi} to sensi_dirs_to_process')
        else:
            logger.debug(f'Returned sensi_dirs_to_process:\n {sensi_dirs_to_process}')
            return sensi_dirs_to_process

        if len(self.param_map)>0:
            # Read settings.json from each sensi dir and apply changes
            for sensi_name, sensi_dirpath in sensi_dirs_to_process.items():
                logger.debug(f"Applying {sensi_name} stresses in {sensi_dirpath}")
                if os.path.exists(sensi_dirpath):
                    try:
                        settings_json_sensi = read_json_file(os.path.join(sensi_dirpath, 'resources/settings.json').replace("\\", "/"))
                    except Exception as err:
                        processed_sensi_messages[sensi_name] = SensiIOError("Unable to read the settings.json in {}".format(sensi_name))
                        logger.error(processed_sensi_messages[sensi_name].msg, exc_info=True)
                        continue

                    if settings_json_sensi is not None:
                        settings_modif_express = list()
                        settings_modif_values = list()
                        total_applied = 0
                        processed_sensi_messages[sensi_name] = ""
                        for stress_name in self.sensi_list[sensi_name]:
                            logger.debug(f"Applying stress {stress_name} to {sensi_name}")
                            counter = 0
                            for command in self.param_map[stress_name]:
                                logger.debug(f'Processing command: {command}')
                                try:
                                    syntax = syn.parse_param(command)
                                    if syntax.expression.startswith("$"):
                                        path_to_file = syn.get_input_file_path(settings_json_sensi, syntax.expression, sensi_dirpath)
                                        # Apply the changes to the input file using the syntax
                                        applied = syn.apply_syntax_to_file(path_to_file, syntax, settings_json_sensi)
                                        if applied:
                                            counter += 1
                                            processed_sensi_messages[sensi_name] = 'Applied "{}" modification(s) on input files of {}'.format(counter, sensi_name)
                                            logger.debug('Applied "{}" with col: "{}", condition: "{}" and value: "{}" on input file {}'.format(syntax.expression, syntax.col, syntax.condition, syntax.value, path_to_file))
                                        else:
                                            # print("Failed to apply a syntax to {}".format(path_to_file))
                                            processed_sensi_messages[sensi_name] = SensiIOError("Failed to apply {} stress on {}".format(sensi_name, Path(path_to_file).name))
                                            logger.error('Failed to apply "{}" with col: "{}", condition: "{}" and value: "{}" on {}'.format(syntax.expression, syntax.col, syntax.condition, syntax.value, path_to_file))
                                            break
                                    else:
                                        try:
                                            table_name = syn.query(settings_json_sensi, "$.framework.sensi_1.name")
                                            expression = syntax.expression
                                            if not syntax.expression.startswith("framework"):
                                                expression = "framework.sensi[{}].{}".format(table_name, syntax.expression)
                                            settings_modif_express.append(expression)
                                            settings_modif_values.append(syntax.value)
                                            
                                            processed_sensi_messages[sensi_name] = f"Added settings modification to settings_modif of {sensi_name}"
                                            logger.info("Added {} to settings_modif".format(expression))
                                        except syn.SensiSyntaxError:
                                            processed_sensi_messages[sensi_name] = SensiIOError("Unable to add {} to settings_modif because no table name is found in settings_json".format(syntax.expression))
                                            logger.error("Unable to add {} to settings_modif because no table name is found in settings_json".format(syntax.expression), exc_info=True)
                                        continue

                                except syn.SensiSyntaxError as err:
                                    processed_sensi_messages[sensi_name] = SensiIOError(f"An error occurred while applying {stress_name} stresses")
                                    logger.error(f"Failed to apply Command: {command} for sensi: {stress_name}", exc_info=True)
                                    break
                            
                            logger.debug(f'Increased number of applied stress to {total_applied}')
                            total_applied = total_applied+counter
                        
                        # Saving settings_modif commands to settings_modif.csv
                        if len(settings_modif_express)>0 and len(settings_modif_values)>0:
                            total_applied = total_applied + len(settings_modif_express)
                            settings_modif_pd = pd.DataFrame({"id": settings_modif_express, "value": settings_modif_values})
                            settings_modif_pd.to_csv(os.path.join(sensi_dirpath, 'resources/settings_modif.csv'), sep=";", index=False)
                            logger.info(f"settings_modif.csv of {sensi_name} saved in {sensi_dirpath}")

                        if not isinstance(processed_sensi_messages[sensi_name], SensiIOError):
                            processed_sensi_messages[sensi_name] = "Applied {} modification(s) on {}".format(total_applied, sensi_name)
                            logger.debug(processed_sensi_messages[sensi_name])
                else:
                    processed_sensi_messages[sensi_name] = SensiIOError("Sensitivity path does not exist")
                    logger.error(processed_sensi_messages[sensi_name].msg)

        logger.debug(f'Returned processed_sensi_messages:\n {processed_sensi_messages}')
        return processed_sensi_messages
