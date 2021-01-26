import click
import sys
import sclbl._globals as glob

# simple check for the correct version of sclblpy
from sclblpy import __version__ as version
if version == "0.1.5":
    print("Please update your version of sclblpy to 0.1.6 or higher to use the sclbl CLI tools.")
    sys.exit(1)

# import others:
from sclblpy import _set_taskmanager_URL, _set_toolchain_URL, _set_usermanager_URL, stop_print, \
    upload_onnx, update_onnx, \
    models as spmodels, delete_model, \
    assignments as spassignments, assign as spassign, delete_assignment, \
    devices as spdevices, delete_device, \
    remove_credentials


@click.group()
def main():
    """ Scailable CLI interface

    This package provides a CLI interface to the Scailable Platform. Check the package readme
    or runs sclbl command --help for usage details.
    """
    init()  # is called whenever CLI interface is used, but not when testing click.


# init initializes the package; this is called by main (which is called whenever the package is used).
def init(debug=glob.DEBUG):
    """ Initalize the package.

    Called every time and used to set the correct target servers.
    """
    if not debug:  # If package not in debug mode, suppress printing from sclblpy.
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
@click.option('--verbose', '-v', type=bool, required=False, default=True, help="Provide user feedback.")
def upload(file, name, docs, example, email, verbose):
    """ ** Upload an ONNX file to the Scaialble platform.

    Use the path of an ONNX file and (at minimum) its name to upload the model for automatic
    conversion to WebAssembly.
    """

    # upload onnx
    docs = {'name': name, 'docs': docs}
    result = upload_onnx(file, example, docs, email)
    if verbose:
        if result:
            print("Your model is uploaded to the Scailable toolchain.")
        else:
            print("We were unable to upload your model; are you sure the path is correct?")


# update updates an existing model using its cfid
@main.command()
@click.option('--cfid', '-id', type=str, required=True, help="The computed function ID (cfid).")
@click.option('--file', '-f', type=str, required=True, help="Path for the input ONNX file.")
@click.option('--name', '-n', type=str, required=True, help="Name of the model.")
@click.option('--docs', '-d', type=str, required=False, default="...", help="Model documentation.")
@click.option('--example', '-e', type=str, required=False, default="...", help="Example model input string.")
@click.option('--email', '-m', type=bool, required=False, default=True, help="Send confirmation email.")
@click.option('--verbose', '-v', type=bool, required=False, default=True, help="Provide user feedback.")
def update(file, cfid, name, docs, example, email, verbose):
    """ Update an existing model on the Scaialble platform.

    Use the model id (cfid), the path of an ONNX file and (at minimum) its name to upload the model for automatic
    conversion to WebAssembly and overwrite the existing model.
    """

    # update onnx
    docs = {'name': name, 'docs': docs}
    result = update_onnx(file, cfid, example, docs, email)
    if verbose:
        if result:
            print("Your model has been submitted for an update.")
        else:
            print("We were unable to update your model.")


# `models` : List all models associated with the current user ID
@main.command()
@click.option('--offset', '-o', type=int, required=False, default=0, help="Offset for DB query.")
@click.option('--limit', '-l', type=int, required=False, default=20, help="Limit for DB query.")
@click.option('--verbose', '-v', type=bool, required=False, default=True, help="Provide user feedback.")
def models(offset, limit, verbose):
    """ Models lists all the registered models.

    Generate a printed table of models including their name and ID. More info regarding the models
    is available at https://admin.sclbl.net.
    """

    # get models
    result = spmodels(offset=offset, limit=limit, _verbose=glob.DEBUG, _return=True)
    if isinstance(result, list):
        if len(result) == 0:
            if verbose:
                print("You have not yet uploaded any models.")
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
@main.command()
@click.option('--offset', '-o', type=int, required=False, default=0, help="Offset for DB query.")
@click.option('--limit', '-l', type=int, required=False, default=20, help="Limit for DB query.")
@click.option('--verbose', '-v', type=bool, required=False, default=True, help="Provide user feedback.")
def devices(offset, limit, verbose):
    """ Devices lists all the registered devices.

    Generate a printed table of devices including their name, Device-ID, and Registration-ID.
    More info regarding the registered devices is available at https://admin.sclbl.net.
    """

    # get models
    result = spdevices(offset=offset, limit=limit, _verbose=glob.DEBUG, _return=True)
    if isinstance(result, list):
        if len(result) == 0:
            if verbose:
                print("You have not yet registered any devices.")
        else:
            # print table
            print("---------------------------------------------------------------------------------------")
            print("Device name:                    | DID:          | RID: ")
            print("---------------------------------------------------------------------------------------")
            for key in result:
                print(cutfill(key['name'], 30), " | ", key['did'], " | ", key['rid'])
            print("---------------------------------------------------------------------------------------")
    else:
        if verbose:
            print("Unable to retrieve your devices.")


# `assignments` : List all assignments associated with the current user ID
@main.command()
@click.option('--offset', '-o', type=int, required=False, default=0, help="Offset for DB query.")
@click.option('--limit', '-l', type=int, required=False, default=20, help="Limit for DB query.")
@click.option('--verbose', '-v', type=bool, required=False, default=True, help="Provide user feedback.")
def assignments(offset, limit, verbose):
    """ Assignments lists all the current assignments.

    Generate a printed table of assignments including the model name, device name, and assignment ID.
    More info regarding the assignments is available at https://admin.sclbl.net.
    """

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


# assign creates a new assignment
@main.command()
@click.option('--cfid', '-cfid', type=str, required=True, help="The computed function / model ID (cfid).")
@click.option('--did', '-did', type=str, required=True, help="The device ID.")
@click.option('--rid', '-rid', type=str, required=True, help="The registration ID (see devices).")
@click.option('--verbose', '-v', type=bool, required=False, default=True, help="Provide user feedback.")
def assign(cfid, did, rid, verbose):
    """ Assign a model to a device.

    Assign a model to a device. Note that using 'sclbl devices' and 'sclbl models' you can find the
    required IDs to create the assignment.

    More info is available at https://admin.sclbl.net.
    """
    # assign
    result = spassign(cfid, did, rid, glob.DEBUG)
    if verbose:
        if result:
            print("Assignment successfully created.")
        else:
            print("We were unable to create your assignment.")


# delete deletes a model, device, or assignment.
@main.command()
@click.option('--cfid', '-cfid', type=str, default="", required=False, help="The computed function / model ID (cfid).")
@click.option('--did', '-did', type=str, default="", required=False, help="The device ID.")
@click.option('--aid', '-aid', type=str, default="", required=False, help="The assignment ID (see assignments).")
@click.option('--verbose', '-v', type=bool, required=False, default=True, help="Provide user feedback.")
def delete(cfid, did, aid, verbose):
    """ Delete a model, device, or assignment.

    Delete a model, device, or assignment by providing its cfid, did, or aid respectively.
    """

    result = False
    if cfid:
        if verbose:
            print("Deleting model with id: " + cfid)
        result = delete_model(cfid)
    elif did:
        if verbose:
            print("Deleting device with id: " + did)
        result = delete_device(did)
    elif aid:
        if verbose:
            print("Deleting assignment with id: " + aid)
        result = delete_assignment(aid)
    else:
        if verbose:
            print("Please provide a cfid, did, or aid.")

    if verbose:
        if result:
            print("Delete action successful.")
        else:
            print("The delete action failed.")


# reset resets a user's details
@main.command()
@click.option('--verbose', '-v', type=bool, required=False, default=True, help="Provide user feedback.")
def reset(verbose):
    """ Reset user details.

    Remove the currently stored user details. After running reset you will be asked for you login again
    when calling a command in the sclbl CLI.
    """
    # reset
    result = remove_credentials(glob.DEBUG)
    if verbose:
        if result:
            print("Your user details have been removed.")
        else:
            print("Unable to remove your user detials.")


# cutfill is a utility to print string of the right length
def cutfill(string, length):
    """ Cutfill formats strings

    If the input string is longer than length, it is trimmed to length-2 adding "..".
    If the input string is shorter than length, it will be padded.

    Args:
        string: String to operate on
        length: Desired length of the output
    Returns:
        The shortened/padded string
    """
    out = (string[:(length-2)] + '..') if len(string) > length else string
    return out.ljust(length)


# Run if ran as main
if __name__ == '__main__':
    print("No options running as main.")