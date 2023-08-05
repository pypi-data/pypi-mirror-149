import os
import re
import logging

from objectpath import *

from mpmath import mp

mp.dps = 13
mp.pretty = False

import pandas as pd

logger = logging.getLogger(__name__)


MODEL_DIR_NAMES = {'IR': 'Nominal_rates',
                   'RIR': 'Real_rates',
                   'EQ': 'Equity',
                   'RE': 'Real_estate',
                   'CRED': 'Credit',
                   'FX': 'FX_rate'}
FILE_MARK = "file::"


# Custom Exception class for sensi validation
class SensiSyntaxError(Exception):
    def __init__(self, msg):
        self.msg = str(msg)

    def __str__(self):
        return self.msg
        

class Syntax:
    def __init__(self, expression, col, condition, value):
        self.expression = expression
        self.col = col
        self.condition = condition
        self.value = value

    def __str__ (self):
        return f'Syntax(expression={self.expression}, col={self.col}, condition={self.condition}, value={self.value})'


def extract_value_from_equal(param_string):
    logger.debug(f'Extracting syntax and value from "param_string": {param_string}.')
    
    if "=" not in param_string:
        logger.error('Unable to find equal in expression.')
        raise SensiSyntaxError("Incorrect syntax in param. Unable to find equal.")

    last_equal_position = param_string.rindex("=")
    syntax = param_string[:last_equal_position].strip('"')
    value = param_string[last_equal_position+1:]
    logger.debug(f'Returned {syntax} and {value}.')
    return syntax, value


def extract_target_column(param_string):
    logger.debug(f'Extracting column from "param_string": {param_string} if exists.')
    param_string = param_string.strip('"')

    if ("[" in param_string) and (param_string.endswith("]")):
        right_quote_position = param_string.rindex("]")
        left_quote_position = param_string.rindex("[")
        syntax = param_string[:left_quote_position].strip('"')
        value = param_string[left_quote_position+1:right_quote_position]
        logger.debug(f'Returned {syntax} and {value}.')
        return syntax, value
    else:
        logger.error('Unable to find a column inside square brackets.')
        raise SensiSyntaxError("Incorrect syntax in param. Unable to find square quote at the end of syntax.")


def parse_param(input_syntax):
    logger.debug(f'Parsing parametres from "input_syntax": {input_syntax}')

    syntax = None
    param_expression = ""
    param_col = ''
    param_condition = ''
    param_value = ''
    param_string = str(input_syntax).strip()

    if FILE_MARK not in input_syntax:
        logger.debug(f'Expression {input_syntax} does not start with {FILE_MARK}.')
        param_string, param_value = extract_value_from_equal(input_syntax)
        logger.debug(f'Created Syntax object with expression: {param_string} | value: {param_value}.')
        return Syntax(param_string, param_col, param_condition, param_value)

    logger.debug(f'Expression {input_syntax} starts with {FILE_MARK}.')
    param_string, param_value = extract_value_from_equal(input_syntax)
    param_string = param_string[len(FILE_MARK):]

    # Checks if '.where' exists in param_string
    if ".where" in param_string:
        logger.debug(f'Expression {param_string} contains a condition.')
        param_expression, param_condition = param_string.split(".where")
        logger.debug(f'Condition is {param_condition}')
    else:
        param_expression = param_string
    logger.debug(f'Expression is {param_expression}')

    # Gets the column in the para_expressions
    param_expression, param_col = extract_target_column(param_expression)

    param_names = re.findall(r'\[.+?\]', param_expression)
    result = "$"
    
    logger.debug(f'Constructing query for input file extraction from sensi in {param_names}.')
    for name in param_names:
        logger.debug(f'Inserting expression for parametre name: {name}')
        result = "".join([result, "..*[@.name is '{}']".format(name.strip('[]'))])

    result = "".join([result, re.split(r'\[.+?\]', param_expression)[-1].strip('[]'), '.filename'])
    param_expression = result

    syntax = Syntax(param_expression, param_col, param_condition, param_value)
    logger.debug(f'Created Syntax object with expression: {param_string} | column: {param_col} | condition: {param_condition} | value: {param_value}.')
    return syntax


def query(data, expression):
    logger.debug(f'Querying for a value using objectpath "expression": {expression} in data:\n {data}')
    result = []
    if data and expression:
        if expression.startswith("$"):
            try:
                logger.debug("Creating objectPath Tree object.")
                tree = Tree(data)
                result = tree.execute(expression)
                # If result is not a string (i.e. generator)
                # convert results to a list
                # In general: generators are returned when using an expression that contains ..* operator
                #             itertools can also be returned with just using .. operator
                if not isinstance(result, str):
                    logger.debug(f'Result of objectpath query execution {result} is not a string.')
                    result = list(result)

            except AttributeError as err:
                logger.error(f'An AttributeError occurred in Tree(data)', exc_info=True)
                raise SensiSyntaxError("In Tree(data): ", err.message)

            except StopIteration:
                logger.error('An StopIteration occurred in tree.execute(expression)', exc_info=True)
                raise SensiSyntaxError("In tree.execute(expression): StopIteration")

            except SyntaxError:
                logger.error(f'An SyntaxError occurred in tree.execute(expression)', exc_info=True)
                raise SensiSyntaxError("In tree.execute(expression): SyntaxError")

    elif data is None:
        logger.error("Empty data parametre passed to the query function.")
        raise SensiSyntaxError("Empty Data in query function")

    else:
        logger.error("Empty expression parametre passed to the query function.")
        raise SensiSyntaxError("Empty Expression in query function")

    logger.debug(f"Returned result: {result}.")
    return result


def get_input_file_path(data, expression, env_dir):
    logger.debug(f'Getting path to input_file in "env_dir": {env_dir} from "data" using "expression": {expression}.')
    filename = query(data, expression)
    eco_name, driver_name = re.findall(r"(?<=')\w+(?=')", expression)
    driver_name = MODEL_DIR_NAMES[driver_name]

    if filename:
        eco_folder_id = query(data, "$.framework..*[@.name is '{}']".format(eco_name))
        if eco_folder_id:
            local_filepath = "/".join([eco_folder_id[0]['folder_id'], driver_name, filename[0]])
            logger.debug(f'local_filepath is {local_filepath}')

            # fetch root and input_root names from settings.json
            folder_id = query(data, "$.framework.sensi_1.folder_id")
            input_root_name = "RN_inputs" if query(data, "$.framework.name") == "RN" else "RW_inputs"
            file_path = os.path.join(env_dir, 'resources', folder_id, input_root_name, local_filepath).replace('\\', '/')
            if not os.path.exists(file_path):
                logger.debug(f'File_path {file_path} does not exist.')
                folder_name = query(data, "$.framework.sensi_1.name")
                file_path = os.path.join(env_dir, 'resources', folder_name, input_root_name, local_filepath).replace('\\', '/')
                logger.debug(f'file_path is {file_path}.')

                if not os.path.exists(file_path):
                    logger.error(f'Input file does not exist in {file_path}')
                    raise SensiSyntaxError("Unable to find input file {}".format(file_path))

            logger.debug(f"Returned file_path: {file_path}")
            return file_path

        else:
            logger.error(f'Unable to find folder_id in "data"')
            raise SensiSyntaxError("Unable to find {} folder_id in settings.json".format(eco_name))
    else:
        logger.error(f'Unable to find filename in "data"')
        raise SensiSyntaxError(f"Unable to find input file from expression {expression} in {env_dir}")


def get_selection_from_dataframe(selection, dataframe):
    logger.debug(f'Selecting data using "selection": {selection} from dataframe (head(10)):\n' + '\t' + dataframe.head(10).to_string().replace('\n', '\n\t'))
    if not dataframe.empty and selection.strip():
        col = selection.strip('[]')
        if col.count(',') == 1:
            column, row = col.split(',')
        elif col.count(',') == 0:
            column, row = col, None
        else:
            column, row = None, None
        logger.debug(f'Found that column: {column} and row: {row}')

        if column:
            try:
                column = column.strip()
                if column.startswith("'") and column.endswith("'"):
                    dataframe = dataframe[[column.strip("'")]]
                elif column.count("'") == 0:
                    if column == "*":
                        pass
                    elif column.isnumeric():
                        if int(column) >= 1:
                            dataframe = dataframe[[dataframe.columns[int(column)-1]]]
                        else:
                            logger.error('Selection failed because the column is less than 1')
                            raise SensiSyntaxError("Unable to select because the {} column is less than 1".format(column))
                    else:
                        logger.error('Selection failed because the column is not and int or *')
                        raise SensiSyntaxError("Unable to select because the {} column is not an int or *".format(column))
                else:
                    logger.error('Selection failed because the column is not defined correctly')
                    raise SensiSyntaxError("Unable to select because the {} column is not defined correctly".format(column))

            except KeyError:
                logger.error('Selection failed because the column is not a valid column', exc_info=True)
                raise SensiSyntaxError("Unable to select because the {} column is not a valid column".format(column))

            except IndexError:
                logger.error('Selection failed because the column is out of bounds', exc_info=True)
                raise SensiSyntaxError("Unable to select because the {} column is out of bounds".format(column))

            logger.debug(f'Column was {column}')
            
        if row:
            try:
                row = row.strip()
                if row.startswith("'") and row.endswith("'"):
                    dataframe = dataframe.loc[[row.strip("'")]]
                elif row.count("'") == 0:
                    if row == "*":
                        pass
                    elif row.isnumeric():
                        if int(row) >= 1:
                            dataframe = dataframe.iloc[[int(row)-1], :]
                        else:
                            logger.error('Selection failed because the row is less than 1')
                            raise SensiSyntaxError("Unable to select because the {} row is less than 1".format(row))
                    else:
                        logger.error('Selection failed because the row is not and int or *')
                        raise SensiSyntaxError("Unable to select because the {} row is not an int or *".format(row))
                else:
                    logger.error('Selection failed because the row is not defined correctly')
                    raise SensiSyntaxError("Unable to select because the {} row is not defined correctly".format(row))

            except KeyError:
                logger.error('Selection failed because the row is not a valid column', exc_info=True)
                raise SensiSyntaxError("Unable to select because {} is not a valid row".format(row))

            except IndexError:
                logger.error('Selection failed because the row is out of bounds', exc_info=True)
                raise SensiSyntaxError("Unable to select because the row {} is out of bounds".format(row))

            logger.debug(f'Row was {row}')
    
    logger.debug(f'Returned dataframe:\n' + '\t' + dataframe.to_string().replace('\n', '\n\t'))
    return dataframe


def select_from_dataframe(condition, operation, dataframe):
    logger.debug(f'Selecting data using condition: {condition} and operation: {operation} from dataframe (head(10)):\n' + '\t' + dataframe.head(10).to_string().replace('\n', '\n\t'))
    lvalue, rvalue = condition.split(operation)
    logger.debug(f"Seperated assignment operator values lvalue: {lvalue} and rvalue: {rvalue} .")
    if lvalue:
        lvalue = lvalue.strip()
        selected = get_selection_from_dataframe(lvalue, dataframe)
        logger.debug(f'Converting values in {selected} to numeric')
        selected = selected.apply(pd.to_numeric, errors='ignore')
        if not selected.empty:
            if rvalue:
                values = rvalue.strip().split(',')
                for index in range(len(values)):                    
                    values[index] = values[index].strip()
                    logger.debug(f'Converting value[{index}]: {values[index]}')
                    if values[index]:
                        if values[index].lower() in ["true", "false"]:
                            logger.debug(f'Converted value: {values[index]} to bool.')
                            values[index] = values[index].lower() == "true"
                        else:
                            try:
                                values[index] = int(values[index])
                                logger.debug(f'Converted value: {values[index]} to int.')
                            except ValueError:
                                try:
                                    values[index] = float(values[index])
                                    logger.debug(f'Converted value: {values[index]} to float.')
                                except ValueError:
                                    logger.debug(f"Using value {values[index]} as string.")
                                    pass

                logger.debug(f'Selecting values from dataframe using "operation": {operation}')

                try:
                    if operation == "==":
                        dataframe = dataframe[selected.T.iloc[0].isin(values)]
                    elif operation == "!=":
                        dataframe = dataframe[~selected.T.iloc[0].isin(values)]
                    elif operation == ">=":
                        dataframe = dataframe[selected.T.iloc[0] >= values[0]]
                    elif operation == ">":
                        dataframe = dataframe[selected.T.iloc[0] > values[0]]
                    elif operation == "<=":
                        dataframe = dataframe[selected.T.iloc[0] <= values[0]]
                    elif operation == "<":
                        dataframe = dataframe[selected.T.iloc[0] < values[0]]
                    else:
                        logger.error(f"{operation} is unsupported by this tool.")
                        raise SensiSyntaxError("{} is an unsupported Operation!".format(operation))
                except Exception:
                    logger.error(f"Selection failed using {operation}.", exc_info=True)
                    raise SensiSyntaxError(f"Failed to execute selection with {operation}")

                logger.debug(f"Returned dataframe:\n" + '\t' + dataframe.to_string().replace('\n', '\n\t'))
                return dataframe

            else:
                logger.error('rvalue was not extracted successfully.')
                raise SensiSyntaxError('No rvalue found in {}'.format(condition))
    else:
        logger.error('lvalue was not extracted successfully.')
        raise SensiSyntaxError('No lvalue found in {}'.format(condition))


def interpret_condition(condition, dataframe):
    logger.debug(f"Filtering data using condition: {condition} in dataframe(head(10)):\n" + '\t' + dataframe.head(10).to_string().replace('\n', '\n\t'))
    if condition.strip() and not dataframe.empty:
        condition = condition.strip()
        logger.debug(f"Choosing selection methode using correct operator in condition")
        if condition.count('==') == 1:
            dataframe = select_from_dataframe(condition, "==", dataframe)
        elif condition.count('!=') == 1:
            dataframe = select_from_dataframe(condition, "!=", dataframe)
        elif condition.count('>=') == 1:
            dataframe = select_from_dataframe(condition, ">=", dataframe)
        elif condition.count('>') == 1:
            dataframe = select_from_dataframe(condition, ">", dataframe)
        elif condition.count('<=') == 1:
            dataframe = select_from_dataframe(condition, "<=", dataframe)
        elif condition.count('<') == 1:
            dataframe = select_from_dataframe(condition, "<", dataframe)
        else:
            logger.error(f'Incorrect condition used.')
            raise SensiSyntaxError("{} is not a correct condition".format(condition))

    logger.debug(f"Returned dataframe:\n" + '\t' + dataframe.to_string().replace('\n', '\n\t'))
    return dataframe


def apply_value_to_selection(value, selected_dict):
    logger.debug(f"Applying value: {value} to selection:\n {selected_dict} .")
    applying_operation = False
    operation = None

    value = value.replace(' ', '')
    value = value.strip('"')

    if value.startswith("(") and value.endswith(")"):
        logger.debug(f"Operation {value} is inclosed in parantheses.")
        applying_operation = True
        value = value.strip("()")
        
    logger.debug(f'Extracted value was {value}')

    if value:
        operation = ""

        if applying_operation:
            if value[0] in ('+', '-', '*', '/'):
                operation, value = value[0], value[1:]
        logger.debug(f'Operation: {operation} and value: {value}')

        if str(value).lower() in ["true", "false"]:
            value = (value.lower() == "true")
            logger.debug(f'Converted value {value} to bool')
        else:
            try:
                value = mp.mpf(value.replace(",", "."))
                logger.debug(f'Converted value to {type(value)} .')
            except (ValueError):
                logger.warning(f'The value to be applied {value} is not numerical.')
                logger.debug(f"Using value {value} as string.")
                pass
            
        if applying_operation:
            try:
                logger.debug(f"Applying operation: {operation}")
                # We use the mpmath module to execute operations with maximum of precision (currently 13)
                if operation == '+':
                    for column in selected_dict.keys():
                        selected_dict[column] = {k: mp.nstr(mp.mpf(v) + value, 13) for k, v in selected_dict[column].items()}
                elif operation == '-':
                    for column in selected_dict.keys():
                        selected_dict[column] = {k: mp.nstr(mp.mpf(v) - value, 13) for k, v in selected_dict[column].items()}
                elif operation == '*':
                    for column in selected_dict.keys():
                        selected_dict[column] = {k: mp.nstr(mp.mpf(v) * value, 13) for k, v in selected_dict[column].items()}
                elif operation == '/':
                    for column in selected_dict.keys():
                        selected_dict[column] = {k: mp.nstr(mp.mpf(v) / value, 13) for k, v in selected_dict[column].items()}
                else:
                    logger.debug('Applying a + as the default operation')
                    for column in selected_dict.keys():
                        selected_dict[column] = {k: mp.nstr(mp.mpf(v) + value, 13) for k, v in selected_dict[column].items()}

            except Exception as exc:
                logger.error(f'Failed to execute operation: {operation} between {selected_dict} and {value}.', exc_info=True)
                raise SensiSyntaxError("Could not execute operation '{}' between '{}' and '{}'".format(operation, selected_dict ,value))
    
        else:
            logger.debug(f'No operation was given, replacing data in {selected_dict} with {value}.')
            for column in selected_dict.keys():
                selected_dict[column] = {k: mp.nstr(value, 18) if isinstance(value, mp.mpf) else value for k, v in selected_dict[column].items()}

    logger.debug(f'Returned dict:\n {selected_dict}')
    return selected_dict


def apply_syntax_to_file(input_path, syntax, settings_json):
    logger.debug(f'Applying syntax: {syntax} to file: {input_path}')
    # read path to dataframe
    # apply syntax
    if input_path and syntax and settings_json:
        logger.debug(f'Getting separators from settings.json:\n {settings_json}')
        seps = settings_json.get('gen_param').get('input_format')
        if seps:            
            dec_sep = seps['dec_sep']
            col_sep = seps['col_sep']
            logger.debug(f'Found dec_sep: {dec_sep} and col_sep: {col_sep}')

            if os.path.exists(input_path):
                input_df = pd.read_csv(input_path, sep=col_sep, converters={i: str for i in range(100)})
                logger.debug(f'Input file in {input_path} read.')
                if syntax.condition:
                    condition = syntax.condition.strip('()')
                    or_conditions = condition.split('||')
                    logger.debug(f'Applying conditions seperated by ||: {or_conditions}')
                    df_indexes_list_or = []
                    for or_cond in or_conditions:
                        logger.debug(f'Applying {or_cond}')
                        if or_cond.strip():
                            and_conditions = or_cond.split('&&')
                            logger.debug(f'Applying conditions seperated by &&: {and_conditions}')
                            df_indexes_list_and = []
                            for and_cond in and_conditions:
                                logger.debug(f'\tApplying {and_cond}')
                                selected_df = interpret_condition(and_cond, input_df)
                                df_indexes_list_and.append(set(selected_df.index))

                                logger.debug(f'Appended result of and_condition to the list.')

                            df_common_indexes = set.intersection(*df_indexes_list_and)
                            df_indexes_list_or.append(df_common_indexes)
                            logger.debug(f'Appended result of or_condition to the list.')

                    df_total_indexes = set().union(*df_indexes_list_or)
                    df_concat = input_df.iloc[list(df_total_indexes)]

                if syntax.col:
                    logger.debug(f'Selecting data using {syntax.col} .')
                    try:
                        if syntax.condition:
                            logger.debug(f'Using condition {condition}')
                            selected_df = get_selection_from_dataframe(syntax.col, df_concat)
                        else:
                            selected_df = get_selection_from_dataframe(syntax.col, input_df)
                    except SensiSyntaxError as err:
                        index = err.msg.find("because")
                        final_msg = err.msg[:index] + 'from ' + input_path + ' ' + err.msg[index:]
                        logger.error('Failed', exc_info=True)
                        raise SensiSyntaxError(final_msg)

                    selected_dict = selected_df.to_dict() # {"Nom_column": {"Num de ligne": "valeur associé"}}
                    logger.debug(f'Converted selected_df to dict:\n {selected_dict}')

                    if syntax.value:
                        applied_dict = apply_value_to_selection(syntax.value, selected_dict)
    
                    for column, indexes in applied_dict.items():
                        for index in indexes:
                            logger.debug(f'Replacing value at [{index},{column}] with {indexes[index]}')
                            input_df.loc[index, column] = indexes[index]

                    logger.debug(f'Dataframe types are:\n {input_df.dtypes}')
                    os.remove(input_path)
                    input_df.to_csv(input_path, sep=col_sep, index=False, float_format='%.18g')
                    logger.debug(f'Saved to {input_path}:\n' + '\t' + input_df.to_string().replace('\n', '\n\t'))

                    logger.debug('Returned True')
                    return True

                else:
                    logger.error("No col found for selection")
                    raise SensiSyntaxError("No col found for selection")
            else:
                logger.error(f'Unable to find the input file {input_path}')
                raise SensiSyntaxError("Unable to find the input file {}".format(input_path))
        else:
            logger.error(f'Unable to find the input_format in settings.json')
            raise SensiSyntaxError("Unable to find the input_format in settings.json")
    else:
        msg = []
        if input_path is None:
            logger.error("Unable to find input file to apply syntax")
            raise SensiSyntaxError("Unable to find input file to apply syntax")
        if syntax is None:
            logger.error("No syntax to apply to file")
            raise SensiSyntaxError("No syntax to apply to file")
        if settings_json is None:
            logger.error("Unable to read settings.json")
            raise SensiSyntaxError("Unable to read settings.json")

    logger.debug('Returned False')
    return False

