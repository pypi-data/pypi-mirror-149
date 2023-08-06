import re

def camel_to_snake(name):
    """
    Pasa de notacion CamelCase a Snake
    Ejemplos:
    print(camel_to_snake('camel2_camel2_case'))  # camel2_camel2_case
    print(camel_to_snake('getHTTPResponseCode'))  # get_http_response_code
    print(camel_to_snake('HTTPResponseCodeXYZ'))  # http_response_code_xyz
    :param name:
    :return:
    """
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()

def snake_to_camel(name):
    """
    Pasa de notacion Snake a CamelCase
    :param name:
    :return:
    """
    name = ''.join(word.title() for word in name.split('_'))
    return name