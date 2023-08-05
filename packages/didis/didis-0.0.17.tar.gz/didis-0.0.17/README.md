# DIDIS - Desy ITk Database Interaction Script
DIDIS is a Python script meant to ease interaction with the ATLAS ITk Production Database (DB) for the detector (pre-)production efforts at DESY-HH.

## Installation
Pip users can get the package by issuing
```bash
pip install didis
```
On some systems, use *pip3* instead of *pip*.

## Requirements
DIDIS is based on *python3*. You can install all requirements at once by issuing
```
pip install --user requests argh loguru itkdb
```
When you install via pip, it will be done for you during the intalltion.

## Authentication
The DB required two user specific access codes to authenticate the user. For security reasons, these should not be stored on the disk. They are stored in the environment variables *ITKDB_ACCESS_CODE1* and *ITKDB_ACCESS_CODE2*. In linux, they can be set for the current terminal session like this:
```bash
export ITKDB_ACCESS_CODE1=YourFirstPassword
export ITKDB_ACCESS_CODE2=YourSecondPassword
```
or for Windows
```bash
set ITKDB_ACCESS_CODE1=YourFirstPassword
set ITKDB_ACCESS_CODE2=YourSecondPassword
```
Check whether the authentication is working by calling
```
didis authenticate
```

## Looking up components in the DB
With DIDIS, the ITk DB can be searched for all sorts of keys, not only for serial numbers. The tool "lookup" does exactly this and outputs the DB codes.  
```bash
didis lookup -v 20USEBT1098765 --printJSON
```
looks up a Bus Tape with the ATLAS SN  20USEBT1098765 and prints the component info in human readable JSON. The subproject, component type and lookup key can also be changed using the optional arguments. Call the script with *--help* for more info.
By passing the option *--returnResults*, the function returns a dictionary that either appears as the CLI output or can be used by the calling function.

## Attaching a file to a component
To attach a file from your local file system to a component with ID CID, use
```bash
didis attach results.zip CID
```
The ID can be found using the *lookup* command.

## Setting the production stage
Setting the production stage of a component with ATLAS serial number SN to STAGE is done via
```bash
didis stage SN -s STAGE
```
Leaving the *-s* argument just prints the current production stage without changing anything.

## Get all available tests for a component type
Get all available tests for type "BT":
```bash
didis tets --componentType BT
```

## Get a test skeleton JSON
Get a bare test JSON for a given test type:
```bash
didis skeleton --test BTELECTRICAL --componentType BT
```
Using *--returnResults* makes the skeleton available as a dict via the function return.

## Upload a test result to the DB
> The *content* field requires to be set to the ATLAS serial number, not to the component ID
To upload a JSON test result to the DB, use
```bash
didis upload FILE.json
```
When not using the CLI, the function can also convert a dict directly.

## Get all test results associated with a component
To get a dict with all test results for a given component id, use
```bash
didis testruns DB_COMPONENT_ID
```
You can find the component id using the *lookup* command.

## Attaching a file to a test run
To attach a file from your local file system to a test run with ID TID, use
```bash
didis testfile results.zip TID
```
The ID can be found using the *testruns* command.

## Usage in another Python script
To use the functions in the *didis.py* script, use the import
```python
import didis.didis as dd
```

## Registering new Components
Make an Excel file with all the properties and serial numbers and register them all via
```bash
didis-batch register YOUREXCELFILE
```
Start batch identifiers with *B_*.

## Assembling Components
Assemble a child component to a parent using
```bash
didis assemble PARENT_SERIAL_NUMBER CHILD_SERIAL_NUMBER
```
If the component has no ATLAS serial number, use the alternative identifier instead. Specify this using the *--parentAID* and *--childAID* flags. Optionally, a *.json* file or dict can be passed to the *properties* input.

## Changing Component properties
To change a component property, use
```bash
didis property COMPONENT_ID PROPERTY_ID VALUE
```
The component ID can also be a ATLAS serial number.

## Adding a comment to a component / test
To add a comment to a component, use
```bash
didis comment COMPONENT_SERIAL_OR_ID "COMMENT_STRING"
```
To add a comment to a test run, use
```bash
didis comment TEST_ID "COMMENT_STRING" --isTest
```
TODO: When only adding one comment, the DB throws an error. An additional empty comment is created as a workaround as of now