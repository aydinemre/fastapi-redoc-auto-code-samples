import json

BASE_URL = 'http://localhost:8000'


def get_code_samples(route, method):
    nl = '\n'  # new line character to use in f-strings.
    if method in ['POST', 'PUT', 'DELETE'] and route.body_field:
        print(f"Path:{route.path}")
        try:
            example_schema = route.body_field.type_.Config.schema_extra.get('example')
            payload = f"json.dumps({example_schema})"
            data_raw = f"\\{nl} --data-raw " + "'" + f"{json.dumps(example_schema)} " + "'"
        except Exception as e:
            print(f"Path:{route.path} Error:{e}")
            payload = '{}'
            data_raw = ''
    else:
        payload = '{}'
        data_raw = ''
    return [
        {
            'lang': 'Shell',
            'source': f"curl --location\\{nl} "
                      f"--request {method} '{BASE_URL}{route.path}'\\{nl} "
                      f"--header 'Authorization: Token 2324143'"
                      f"{data_raw}",
            'label': 'curl'
        },
        {
            'lang': 'Python',
            'source': f"import requests{nl}"
                      f"{'import json' + nl if method.lower() == 'post' else ''}{nl}"
                      f"url = \"{BASE_URL}{route.path}\"{nl}"
                      f"payload = {payload}{nl}"
                      f"headers = {{'Authorization': 'Token 2324143'}}{nl}"
                      f"response = requests.request(\"{method}\", url, headers=headers, data=payload){nl}"
                      f"print(response.text)",
            'label': 'Python3'
        },
    ]
