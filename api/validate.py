from typing import List, Dict, Callable, Tuple


# SlotValidationResult = Tuple[bool, bool, str, Dict]


def validate_finite_values_entity(values: List[Dict], supported_values: List[str] = None,
                                  invalid_trigger: str = None, key: str = None,
                                  support_multiple: bool = True, pick_first: bool = False,
                                  value_type=["id"], **kwargs):
    """
    Validate an entity on the basis of its value extracted.
    The method will check if the values extracted("values" arg) lies within the finite list of supported values(arg "supported_values").

    :param value_type: Set to 'id'
    :param pick_first: Set to true if the first value is to be picked up
    :param support_multiple: Set to true if multiple utterances of an entity are supported
    :param values: Values extracted by NLU
    :param supported_values: List of supported values for the slot
    :param invalid_trigger: Trigger to use if the extracted value is not supported
    :param key: Dict key to use in the params returned
    :return: a tuple of (filled, partially_filled, trigger, params)
    """
    if values is None or supported_values is None or invalid_trigger is None or key is None:
        return 'Missing Required Fields', 400

    result = []
    trigger = ''
    supported_values_set = set(supported_values)
    for value in values:
        if value.get('entity_type') == value_type[0] and value.get('value') in supported_values_set:
            result.append(value.get('value').upper())
        else:
            trigger = invalid_trigger

    return format_output(values, result, pick_first, invalid_trigger, trigger, key)


def validate_numeric_entity(values: List[Dict], invalid_trigger: str = None, key: str = None,
                            support_multiple: bool = True, pick_first: bool = False, constraint=None, var_name=None,
                            value_type=["number"], **kwargs):
    """
    Validate an entity on the basis of its value extracted.
    The method will check if that value satisfies the numeric constraints put on it.
    If there are no numeric constraints, it will simply assume the value is valid.

    If there are numeric constraints, then it will only consider a value valid if it satisfies the numeric constraints.
    In case of multiple values being extracted and the support_multiple flag being set to true, the extracted values
    will be filtered so that only those values are used to fill the slot which satisfy the numeric constraint.

    If multiple values are supported and even 1 value does not satisfy the numeric constraint, the slot is assumed to be
    partially filled.

    :param value_type: Set to 'number'
    :param pick_first: Set to true if the first value is to be picked up
    :param support_multiple: Set to true if multiple utterances of an entity are supported
    :param values: Values extracted by NLU
    :param invalid_trigger: Trigger to use if the extracted value is not supported
    :param key: Dict key to use in the params returned
    :param constraint: Conditional expression for constraints on the numeric values extracted
    :param var_name: Name of the var used to express the numeric constraint
    :return: a tuple of (filled, partially_filled, trigger, params)
    """

    if values is None or invalid_trigger is None or key is None or constraint is None or var_name is None:
        return 'Missing Required Fields', 400

    result = []
    trigger = ''
    _locals = locals()
    for value in values:
        if value.get('entity_type') == value_type[0]:
            try:
                exec('{}={}'.format(var_name, value.get('value')), _locals)
                exec('valid = True if ({}) else False'.format(constraint), _locals)
            except Exception as e:
                print(e)
                return "constraint not in Python format"

            valid = (_locals['valid'])
            if valid:
                result.append(value.get('value'))
            else:
                trigger = invalid_trigger

    print(result)

    return format_output(values, result, pick_first, invalid_trigger, trigger, key)


def format_output(values, result, pick_first, invalid_trigger, trigger, key):
    if values == []:
        filled_flag = False
        partially_filled_flag = False
    else:
        filled_flag = True if len(result) == len(values) else False
        partially_filled_flag = True if 0 <= len(result) < len(values) else False

    if result != []:
        if pick_first:
            result = result[0]
    else:
        trigger = invalid_trigger

    return {
        "filled": filled_flag,
        "partially_filled": partially_filled_flag,
        "trigger": trigger,
        "parameters": {
            key: result
        } if result else {}
    }
