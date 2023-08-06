import os
import shutil
import subprocess
import tarfile

import click
import requests

from ..api.status_update import update_status_init
from ..common.constants import *
from ..common.utils import failed, get_tiyaro_token, success, warn
from ..handler.cli_state import get_model_name_with_suffix, save_model_metadata, get_model_framework


@click.command()
@click.option('-f', '--force', is_flag=True, default=False, help=INIT_HELP)
@click.option('-v', '--verbose', is_flag=True, default=False, help=VERBOSE_HELP)
def init(force, verbose):
    """
    - Initializes model repo for Tiyaro Push
    """
    get_tiyaro_token()
    validate_ok_to_init(force, verbose)

    name = click.prompt('Please enter the name of your model', type=str)
    framework = get_framework(verbose)
    save_model_metadata(name, framework, verbose)
    update_status_init(get_model_name_with_suffix(), get_model_framework())

    if framework == 'pytorch':
        get_pytorch_templates(verbose)
        success(f'Created {TIYARO_HANDLER_DIR}, {HANDLER_MODEL_MODEL_TEST_FILE} templates successfully !')
    else:
        warn('Thank you for your interest in trying Tiyaro Cli !  Currently, only pytorch framework is supported.  Kindly reachout to Tiyaro Team.')
        subprocess.run(f'tiyaro clear -f', shell=True)

def get_framework(is_verbose):
    while True:
        framework_opt = '\n 1\t Pytorch\n 2\t Tensorflow\n 3\t JAX\n 4\t Other -specify\n'
        option = click.prompt(f'Please enter the framework of your model {framework_opt} \t\t\t', type=str)
        option = option.casefold()

        if option in ['1', 'pytorch']:
            option = 'pytorch'
            break
        elif option in ['2', 'tensorflow']:
            option = 'tensorflow'
            break
        elif option in ['3', 'jax']:
            option = 'jax'
            break
        elif option == '4':
            failed(f'For option 4, please specify the framework name')
        else:
            break

        success(f'DEBUG - user selected option is: {option}', is_verbose)
    return option


def validate_ok_to_init(is_overwrite, is_verbose):
    __init_validate(is_overwrite, HANDLER_MODEL_MANIFEST_FILE)
    __init_validate(is_overwrite, HANDLER_MODEL_MODEL_HANDLER_FILE)
    __init_validate(is_overwrite, HANDLER_MODEL_MODEL_TEST_FILE)


def __init_validate(is_overwrite, file):
    if (os.path.isfile(file)):
        if not is_overwrite:
            warn(f"{file} already exists.  To force init kindly use 'tiyaro init -f' ")
            exit(-1)
        else:
            subprocess.run(f'tiyaro clear -f', shell=True)


def get_pytorch_templates(is_verbose):
    success('Fetching tiyaro pytorch handler templates...')
    token = get_tiyaro_token()
    resp = requests.get(
        f'{PUSH_SUPPORT_FILES_ENDPOINT}/{ARTIFACTS_FILE_NAME}',
        headers={
            'Authorization': token
        })
    if resp.status_code == 200:
        template_url = resp.content
    else:
        failed(resp.status_code)
        failed(resp.content)
        failed(
            f'Unable to get templates URL.  Is your {TIYARO_TOKEN} still valid ?')
        exit(-1)

    os.makedirs(ARTIFACTS_DOWNLOAD_DIR)
    downloaded_artifact = f'{ARTIFACTS_DOWNLOAD_DIR}/ARTIFACTS_FILE_NAME'

    resp = requests.get(template_url, stream=True)
    if resp.status_code == 200:
        with open(downloaded_artifact, 'wb') as f:
            f.write(resp.raw.read())
    else:
        failed(
            f'Unable to get templates.  Is your {TIYARO_TOKEN} still valid ?')
        exit(-1)

    def members(tf, sub_folder):
        l = len(sub_folder)
        for member in tf.getmembers():
            if member.path.startswith(sub_folder):
                member.path = member.path[l:]
                yield member

    tar = tarfile.open(downloaded_artifact)
    tar.extractall(path=TIYARO_HANDLER_DIR,
                   members=members(tar, ARTIFACTS_FILES_DIR))
    # move test file to project root for tiyaro test
    shutil.move(f'{TIYARO_HANDLER_DIR}/{HANDLER_MODEL_MODEL_TEST_FILE}',
                f'{HANDLER_MODEL_MODEL_TEST_FILE}')
    shutil.rmtree(ARTIFACTS_DOWNLOAD_DIR)
