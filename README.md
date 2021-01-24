# sclbl CLI interface.

Main usage:
```shell script
$ sclbl upload -f file.onnx -n Model name
```

The package exposes the following commands:

* `upload` : Upload an onnx file to the Scaailable Platform. Options:
* `update` : Update an existing model using its cfid
* `models` : List all models associated with the current user ID
* `devices` : List all registered devices associated with the current user ID
* `assignments` : List all assignments associated with the current user ID
* `assign` : Create a new assignment
* `delete` : Delete a model, assignment, or id.

Each of the commands above requires logging in to the Scailable platform using a valid username and
password combination. See www.scailable.net for details. Upon first login, you will be asked to store your
username and password locally. You can remove the stored local details using:

* - `sclbl reset` : Reset you user details.

See `sclbl command --help` for additional information and the required arguments/options.

Note that the sclbl CLI depends on the sclblpy package. See https://pypi.org/project/sclblpy/ for details. 
If you would like to upload fitted `sklearn` models, please use the `sclblpy` package directly from python.