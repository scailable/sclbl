from click.testing import CliRunner
from sclbl.cli import init
from sclbl.cli import upload
from sclbl.cli import update
from sclbl.cli import models
from sclbl.cli import devices
from sclbl.cli import assignments
from sclbl.cli import reset


# test_upload tests the upload() function:
def test_upload():

    runner = CliRunner()
    result = runner.invoke(upload,
                           ['-f','../test/files/model.onnx', '-n', 'Model name from CLI'],
                           input="maurits@mauritskaptein.com\ntest\ny")
    assert result.exit_code == 0, "Test upload failed."
    print(result.output)


# test_models test the models() function
def test_models():

    runner = CliRunner()
    result = runner.invoke(models, ['-v', True], input="maurits@mauritskaptein.com\ntest\ny")
    #assert result.exit_code == 0, "Test models failed."
    #assert 'Debug mode is on' in result.output
    print(result.output)


# test_devices test the devices() function
def test_devices():

    runner = CliRunner()
    result = runner.invoke(devices, ['-v', True], input="maurits@mauritskaptein.com\ntest\ny")
    #assert result.exit_code == 0, "Test models failed."
    #assert 'Debug mode is on' in result.output
    print(result.output)


# test_assignments test the devices() function
def test_assignments():

    runner = CliRunner()
    result = runner.invoke(assignments, ['-v', True], input="maurits@mauritskaptein.com\ntest\ny")
    #assert result.exit_code == 0, "Test models failed."
    #assert 'Debug mode is on' in result.output
    print(result.output)


# test_reset tests removing user details:
def test_reset():

    runner = CliRunner()
    result = runner.invoke(reset, ['-v', True], input="maurits@mauritskaptein.com\ntest\ny")
    #assert result.exit_code == 0, "Test models failed."
    #assert 'Debug mode is on' in result.output
    print(result.output)


init()  # Initialize to make sure the correct servers are set
# test_upload()
# test_models()
# test_devices()
# test_assignments()
test_reset()
