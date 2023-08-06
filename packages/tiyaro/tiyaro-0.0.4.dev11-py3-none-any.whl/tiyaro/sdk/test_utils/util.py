import json
import os
import shutil

import requests
import validators
import yaml

from ...common.constants import KEYWORD_FROM_CONFIG, HANDLER_MODEL_MANIFEST_FILE, C_PRETRAINED_FILE_OR_URL
from ...handler.tiyaro_test_state import save_input, save_output

from ..base_handler import TiyaroBase

KEYWORD_FROM_CONFIG = 'from-config'
HANDLER_MODEL_MANIFEST_FILE = './tiyaro_handler/model_manifest.yml'
C_PRETRAINED_FILE_OR_URL = 'pretrained_model_url'


def get_pretrained_file_path(x):
    def local_file(x, err_msg):
        if os.path.isfile(x):
            return x
        else:
            raise ValueError(err_msg)

    if x == KEYWORD_FROM_CONFIG:
        # read from yaml
        # if url, download to /tmp and return path
        # if local path, return path
        with open(HANDLER_MODEL_MANIFEST_FILE, 'r') as file:
            contents = yaml.safe_load(file)
            value = contents[C_PRETRAINED_FILE_OR_URL]
            if (
                (value is None)
                or (not isinstance(value, str))
                or (not value.strip())
            ):
                raise ValueError(
                    f'Please set a valid model {C_PRETRAINED_FILE_OR_URL} in {HANDLER_MODEL_MANIFEST_FILE}')
            if validators.url(value):
                r = requests.get(value, stream=True)
                file_path = '/tmp/pre_trained.pth'
                print(
                    f'DOWNLOADING - pretrained file to {file_path} from URL: {value}')
                if r.status_code == 200:
                    with open(file_path, 'wb') as f:
                        r.raw.decode_content = True
                        shutil.copyfileobj(r.raw, f)
                    print('DOWNLOAD - Done')
                    return file_path
                else:
                    raise RuntimeError(
                        f'Unable to download pretrained file from: {value}')
            else:
                return local_file(value, 'Expected valid local file path')

    return local_file(x, 'Expected valid local file path')


def get_input_json(x):
    if os.path.isfile(x):
        with open(x, 'r') as f:
            return json.load(f)
    if isinstance(x, str):
        return json.loads(x)

    raise ValueError('Expected Valid JSON input string or file path')


def save_test_input_if_schema(handler: TiyaroBase, input_json):
    if handler.input_schema:
        handler.input_schema().load(input_json)
        save_input(input_json)
        print(f'INPUT - Validation Done')
    else:
        print('WARN - Input schema not defined')


def save_test_output_if_schema(handler: TiyaroBase, output_json):
    if handler.output_schema:
        handler.output_schema().load(output_json)
        save_output(output_json)
        print(f'OUTPUT - Validation Done')
    else:
        print('WARN - Output schema not defined')
