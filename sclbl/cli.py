import click
import sclbl._globals as glob
from sclblpy import _set_taskmanager_URL, _set_toolchain_URL, _set_usermanager_URL, stop_print, \
    upload_onnx, update_onnx, \
    models as spmodels, \
    assignments as spassignments, \
    devices as spdevices, \
    remove_credentials


# Todo(McK): After all tests etc. Check if silent mode it is fully silent.


@click.group()
def main():
    """ Scailable CLI interface

    This package provides a CLI interface to the Scailable Platform.

    """
    init()


# init initializes the package; this is called by main (which is called whenever the package is used).
def init():
    if not glob.DEBUG:  # If package not in debug mode, suppress printing from sclblpy.
        stop_print()

    # Set the correct target servers (see _globals.py)
    _set_toolchain_URL(glob.TOOLCHAIN_URL)
    _set_usermanager_URL(glob.USER_MANAGER_URL)
    _set_taskmanager_URL(glob.TASK_MANAGER_URL)


# upload uploads an ONNX file to the toolchain.
@main.command()
@click.option('--file', '-f', type=str, required=True, help="Path for the input ONNX file.")
@click.option('--name', '-n', type=str, required=True, help="Name of the model.")
@click.option('--docs', '-d', type=str, required=False, default="...", help="Model documentation.")
@click.option('--example', '-e', type=str, required=False, default="...", help="Example model input string.")
@click.option('--email', '-m', type=bool, required=False, default=True, help="Send confirmation email.")
@click.option('--verbose', '-v', type=bool, required=True, default=True, help="Provide user feedback.")
def upload(file, name, docs, example, email, verbose):

    # upload onnx
    docs = {'name': name, 'docs': docs}
    result = upload_onnx(file, example, docs, email)
    if verbose:
        if result:
            print("Your model is uploaded to the Scailable toolchain.")
        else:
            print("We were unable to upload your model.")


# update updates an existing model using its cfid
@click.command()
@click.option('--cfid', '-id', type=str, required=True, help="The computed function ID (cfid).")
@click.option('--file', '-f', type=str, required=True, help="Path for the input ONNX file.")
@click.option('--name', '-n', type=str, required=True, help="Name of the model.")
@click.option('--docs', '-d', type=str, required=False, default="...", help="Model documentation.")
@click.option('--example', '-e', type=str, required=False, default="...", help="Example model input string.")
@click.option('--email', '-m', type=bool, required=False, default=True, help="Send confirmation email.")
@click.option('--verbose', '-v', type=bool, required=True, default=True, help="Provide user feedback.")
def update(file, name, docs, example, email, verbose):

    # upload onnx
    docs = {'name': name, 'docs': docs}
    result = update_onnx(file, example, docs, email)
    if verbose:
        if result:
            print("Your model has been updated.")
        else:
            print("We were unable to update your model.")


# `models` : List all models associated with the current user ID
@click.command()
@click.option('--offset', '-o', type=int, required=False, default=0, help="Offset for DB query.")
@click.option('--limit', '-l', type=int, required=False, default=20, help="Limit for DB query.")
@click.option('--verbose', '-v', type=bool, required=True, default=True, help="Provide user feedback.")
def models(offset, limit, verbose):

    # get models
    result = spmodels(offset=offset, limit=limit, _verbose=glob.DEBUG, _return=True)
    if isinstance(result, list):
        if len(result) == 0:
            if verbose:
                print("You have not yet registered any models.")
        else:
            # print table
            print("-----------------------------------------------------------------------")
            print("Model name:                     | CFID:")
            print("-----------------------------------------------------------------------")
            for key in result:
                print(cutfill(key['name'], 30), " | ", key['cfid'])
            print("-----------------------------------------------------------------------")
    else:
        if verbose:
            print("Unable to retrieve your models.")


# `devices` : List all registered devices associated with the current user ID
@click.command()
@click.option('--offset', '-o', type=int, required=False, default=0, help="Offset for DB query.")
@click.option('--limit', '-l', type=int, required=False, default=20, help="Limit for DB query.")
@click.option('--verbose', '-v', type=bool, required=True, default=True, help="Provide user feedback.")
def devices(offset, limit, verbose):

    # get models
    result = spdevices(offset=offset, limit=limit, _verbose=glob.DEBUG, _return=True)
    if isinstance(result, list):
        if len(result) == 0:
            if verbose:
                print("You have not yet registered any devices.")
        else:
            # print table
            print("---------------------------------------------------------------------------------------")
            print("Model name:                     | DID:          | RID: ")
            print("---------------------------------------------------------------------------------------")
            for key in result:
                print(cutfill(key['name'], 30), " | ", key['did'], " | ", key['rid'])
            print("---------------------------------------------------------------------------------------")
    else:
        if verbose:
            print("Unable to retrieve your devices.")


# `assignments` : List all assignments associated with the current user ID
@click.command()
@click.option('--offset', '-o', type=int, required=False, default=0, help="Offset for DB query.")
@click.option('--limit', '-l', type=int, required=False, default=20, help="Limit for DB query.")
@click.option('--verbose', '-v', type=bool, required=True, default=True, help="Provide user feedback.")
def assignments(offset, limit, verbose):

    # get models
    result = spassignments(offset=offset, limit=limit, _verbose=glob.DEBUG, _return=True)
    if isinstance(result, list):
        if len(result) == 0:
            if verbose:
                print("You have not yet assigned any models.")
        else:
            # print table
            print("-------------------------------------------------------------------------------------------")
            print("Model name:              |  Device name:             | AID:")
            print("-------------------------------------------------------------------------------------------")
            for key in result:
                print(cutfill(key['model_name'], 23), " | ", cutfill(key['device_name'], 23), " |",key['aid'])
            print("-------------------------------------------------------------------------------------------")
    else:
        if verbose:
            print("Unable to retrieve your assignments.")


# `assign` : Create a new assignment
# `delete` : Delete a model, assignment, or id.

# reset resets a user's details
@click.command()
@click.option('--verbose', '-v', type=bool, required=True, default=True, help="Provide user feedback.")
def reset(verbose):

    # reset
    result = remove_credentials(glob.DEBUG)
    if verbose:
        if result:
            print("Your user details have been removed.")
        else:
            print("Unable to remove your user detials.")


# cutfull is a utility to print string of the right lengt
def cutfill(string, length):
    out = (string[:(length-2)] + '..') if len(string) > length else string
    return out.ljust(length)


if __name__ == '__main__':
    print("Make sure to...")