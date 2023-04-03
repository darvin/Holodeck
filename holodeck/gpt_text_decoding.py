import json
import yaml


def deyaml(chain_response):
    text = chain_response['text']
    yaml_start = text.find('```')
    yaml_end = text.rfind('```')
    if yaml_start != -1 and yaml_end == -1:
        yaml_end = len(text)-1
    if yaml_start != -1 and yaml_end != -1 and yaml_start < yaml_end:
        text = text[yaml_start+3:yaml_end].strip()

    while True:
        try:
            return yaml.safe_load(text)
        except yaml.scanner.ScannerError as e:
            lines = text.split('\n')
            if len(lines) == 1:
                raise e
            text = '\n'.join(lines[:-1])
            if len(lines) <= 2:
                break



def dejson(chain_response):
    text = chain_response['text']
    json_start = text.find('```json')
    json_end = text.rfind('```')
    if json_start != -1 and json_end == -1:
        json_end = len(text) - 1
    if json_start != -1 and json_end != -1 and json_start < json_end:
        text = text[json_start + 7:json_end].strip()

    while True:
        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            lines = text.split('\n')
            if len(lines) == 1:
                raise e
            text = '\n'.join(lines[:-1])
            if len(lines) <= 2:
                break
