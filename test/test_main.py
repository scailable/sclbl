from click.testing import CliRunner
from sclbl.cli import init
from sclbl.cli import upload
from sclbl.cli import update
from sclbl.cli import models
from sclbl.cli import devices
from sclbl.cli import assignments
from sclbl.cli import assign
from sclbl.cli import reset
from sclbl.cli import delete
from sclblpy import models as spmodels
from sclblpy import devices as spdevices
from sclblpy import assignments as spassignments

RUN_TESTS = True  # Prevent unintended testing
DEBUG = True  # Set debugging / verbose feedback
USER = "..."
PASS = "..."


# test_upload tests the upload() function:
def test_upload():
    runner = CliRunner()
    result = runner.invoke(upload,
                           ['-f', '../test/files/model.onnx', '-n', 'Model name from CLI', '-v', DEBUG],
                           input=USER + "\n" + PASS + "\ny")
    assert result.exit_code == 0, "Test upload failed."
    if DEBUG:
        assert 'Your model is uploaded' in result.output, "Response from upload not correct"
    print(result.output)


# test_update tests the update function:
def test_update():
    try:
        result = spmodels(_return=True, _verbose=DEBUG)
        cfid = result[0]['cfid']
    except Exception as e:
        print("No model found to test update.")

    runner = CliRunner()
    result = runner.invoke(update,
                           ['-id', cfid, '-f', '../test/files/model.onnx', '-n', 'Update model name CLI', '-v', DEBUG],
                           input=USER + "\n" + PASS + "\ny")
    assert result.exit_code == 0, "Test update failed."
    if DEBUG:
        assert 'update' in result.output, "Response from update not correct"
    print(result.output)


# test_models test the models() function
def test_models():
    runner = CliRunner()
    result = runner.invoke(models, ['-v', DEBUG], input=USER + "\n" + PASS + "\ny")
    assert result.exit_code == 0, "Test models failed."
    # Only if at least one model is available.
    # assert 'CFID' in result.output, "models() failed OR no model has been uploaded yet."
    print(result.output)


# test_devices test the devices() function
def test_devices():
    runner = CliRunner()
    result = runner.invoke(devices, ['-v', DEBUG], input=USER + "\n" + PASS + "\ny")
    assert result.exit_code == 0, "Test devices failed."
    # Only if at least one device is registered
    # assert 'DID' in result.output, "devices() failed OR no device has been uploaded yet."
    print(result.output)


# test_assignments test the devices() function
def test_assignments():
    runner = CliRunner()
    result = runner.invoke(assignments, ['-v', DEBUG], input=USER + "\n" + PASS + "\ny")
    assert result.exit_code == 0, "Test assignments failed."
    # Only if at least one device is registered
    # assert 'AID' in result.output, "assignments() failed OR no assignment has been done yet."
    print(result.output)


# test assign tests creating an assignment
def test_assign():
    cfid = ""
    try:
        result = spmodels(_return=True, _verbose=DEBUG)
        cfid = result[0]['cfid']
    except Exception as e:
        print("No model found to test assign.")

    did = ""
    rid = ""
    try:
        result = spdevices(_return=True, _verbose=DEBUG)
        did = result[0]['did']
        rid = result[0]['rid']
    except Exception as e:
        print("No device found to test assign.")

    runner = CliRunner()
    result = runner.invoke(assign, ['-v', DEBUG, '-cfid', cfid, '-did', did, '-rid', rid],
                           input=USER + "\n" + PASS + "\ny")
    assert result.exit_code == 0, "Test assign failed."
    # assert 'success' in result.output, "Unable to test assign; is there a device AND model registered?"
    print(result.output)


# test delete funtion
def test_delete():
    runner = CliRunner()
    result = runner.invoke(delete, ['-v', DEBUG],
                           input=USER + "\n" + PASS + "\ny")
    assert result.exit_code == 0, "Test delete empty failed."
    if DEBUG:
        assert 'failed' in result.output, "Should not be able to delete an empty record."

    # model:
    cfid = ""
    try:
        result = spmodels(_return=True, _verbose=False)
        cfid = result[0]['cfid']
    except Exception as e:
        if DEBUG:
            print("No model found to test delete.")

    result = runner.invoke(delete, ['-v', DEBUG, '-cfid', cfid],
                           input=USER + "\n" + PASS + "\ny")
    assert result.exit_code == 0, "Test delete compute function failed (model)."
    if DEBUG and cfid:
        assert 'success' in result.output, "Error in deleting model."

    # device:
    did = ""
    try:
        result = spdevices(_return=True, _verbose=False)
        did = result[0]['did']
    except Exception as e:
        if DEBUG:
            print("No device found to test delete.")

    result = runner.invoke(delete, ['-v', DEBUG, '-did', did],
                           input=USER + "\n" + PASS + "\ny")
    assert result.exit_code == 0, "Test delete compute function failed (device)."
    if DEBUG and did:
        assert 'success' in result.output, "Error in deleting device."

    # assignment:
    aid = ""
    try:
        result = spassignments(_return=True, _verbose=False)
        aid = result[0]['aid']
    except Exception as e:
        if DEBUG:
            print("No assignment found to test delete.")

    result = runner.invoke(delete, ['-v', DEBUG, '-aid', aid],
                           input=USER + "\n" + PASS + "\ny")
    assert result.exit_code == 0, "Test delete compute function failed (assignment)."
    if DEBUG and aid:
        assert 'success' in result.output, "Error in deleting assignment."


# test_reset tests removing user details:
def test_reset():
    runner = CliRunner()
    result = runner.invoke(reset, ['-v', DEBUG], input="maurits@mauritskaptein.com\ntest\ny")
    assert result.exit_code == 0, "Test reset failed."
    if DEBUG:
        assert 'user details have been removed' in result.output, "reset() failed."
    print(result.output)


if RUN_TESTS:

    print("Running tests...")
    init(DEBUG)  # Initialize to make sure the correct servers are set
    test_upload()
    test_update()
    test_models()
    test_devices()
    test_assignments()
    test_assign()
    test_delete()
    test_reset()
    print("All test passed.")

else:
    print("Test not run; toggle RUN_TEST at the top of the fail test_main.py")
