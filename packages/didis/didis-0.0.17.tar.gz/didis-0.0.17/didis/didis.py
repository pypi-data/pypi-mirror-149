#!/usr/bin/python3

# DIDIS - Desy ITk Database Interaction Script -- DESY's very own framework for interacting with the ITk Production Database
# Based on itkdb: https://gitlab.cern.ch/atlas-itk/sw/db/itkdb
# Created: 2021/11/17, Updated: 2022/01/24
# Written by Maximilian Felix Caspar, DESY HH


from loguru import logger
import argh
import os
import json
import itkdb
import mimetypes
import six


def authenticate():
    "Check the DB login for this session."
    try:
        # Get the Pixel project contents to show that there is a connection
        client = itkdb.Client()
        client.get('listComponents', json={
            'project': 'P', 'pageInfo': {'pageSize': 32}})
        logger.info("Authentification successful")
    except itkdb.exceptions.ResponseException as e:
        logger.error(e)
        logger.error("Wrong or missing login credentials")
        logger.info(
            "Set environment variables ITKDB_ACCESS_CODE1 and ITKDB_ACCESS_CODE2")
    except Exception as e:
        logger.error(e)


@argh.arg('-v', '--value', nargs='+', type=str)
def lookup(project: "ATLAS Project" = 'S',
           subProject: "ATLAS Subproject" = "SE",
           lookupKey: "Key that corresponds to VALUE" = 'serialNumber',
           value: "Values to look up (can be a list)" = None,
           componentType: "Type of component" = 'BT',
           returnResults: "Return lookup results (useful if not used from CLI)" = False,
           printJSON: "PrettyPrint the component JSON" = False):
    "Look up a component or list of components in the DB."
    try:
        if value is None:
            value = []
        if isinstance(value, six.string_types):
            # Using six to get the correct string type regardless of the python version
            value = [value]
        client = itkdb.Client()
        components = client.get('listComponents', json={
                                'project': project, "componentType": componentType, "subproject": subProject})
        results = {}
        logger.info(f"Looking up {lookupKey} = {value}")
        for i, comp in enumerate(components):
            if value != []:
                # If no input is given, show all components of this type
                if comp[lookupKey] in value:
                    logger.info(
                        f"Found {lookupKey} = {comp[lookupKey]}: {comp['code']}")
                    results[comp[lookupKey]] = comp
            else:
                # Search for the ones that fit the criteria
                logger.info(
                    f"Found {lookupKey} = {comp[lookupKey]}: {comp['code']}")
                results[str(comp[lookupKey])] = comp
        if printJSON:
            for k in results:
                print(json.dumps(results[k], indent=1))
        if returnResults or __name__ != '__main__':
            return results
    except Exception as e:
        logger.error(e)
        logger.error("Error while trying to get connection to DB")
        logger.info(
            "Are environment variables ITKDB_ACCESS_CODE1 and ITKDB_ACCESS_CODE2 set?")


def attach(file: "Path of the file to upload",
           component: "Component code (NOT the ATLAS SN, use lookup for that)",
           title: "Title of the file" = "",
           description: "A file description" = "",
           filetype: "File MIME type (sript can usually guess this)" = None):
    "Attach a file to a component in the DB."
    try:
        client = itkdb.Client()
        if filetype is None:
            # If you can't be bothered to look up the MIME type,
            # we'll look it up for you :)
            filetype = mimetypes.guess_type(file)
        data = {
            'component': component,
            'title': title,
            'description': description,
            'type': 'file',
            'url': file,
        }
        # Get attachment data
        attachment = {'data': (os.path.basename(
            file), open(file, 'rb'), filetype)}

        client.post('createComponentAttachment',
                    data=data, files=attachment)
        logger.info(f"Attached file {file} to {component}")
    except Exception as e:
        logger.error(e)
        logger.error("Error while trying to get connection to DB")
        logger.info(
            "Are environment variables ITKDB_ACCESS_CODE1 and ITKDB_ACCESS_CODE2 set?")


def register(component: "Component to register (path to .json file or dict)"):
    "Register a new component"
    if isinstance(component, str) and os.path.isfile(component):
        logger.info(f"Loading component definition from file {component}")
        with open(component) as jsonFile:
            component = json.load(jsonFile)
            jsonFile.close()
    elif isinstance(component, dict):
        logger.info("Component definition was passed as a dict")
    else:
        logger.error(f"Unrecognised input {component}")
        return
    try:
        client = itkdb.Client()
        client.post('registerComponent', json=component)
        logger.info(f"Registered new component")
    except Exception as e:
        logger.error(e)
        logger.error(
            f"Unable to register component in the DB, is the format correct?")


def tests(componentType: "Type of component" = "BT",
          project: "ATLAS Subproject" = 'S',
          returnResults: "Return available tests (useful if not used from CLI)" = False):
    "Get a list of available tests for a component."
    logger.info(f"Polling for test types for {componentType}")
    try:
        client = itkdb.Client()
        out = client.get("listTestTypes", json={
            'project': project, "componentType": componentType})
        logger.info("Test type and required results:")
        result = {}
        for i, test in enumerate(out):
            result[test['code']] = test
            if not returnResults:
                print(test['code'], ":", test['name'])
                for p in test['parameters']:
                    print("  ", p['code'], ":", p['name'])
        if returnResults or __name__ != '__main__':
            return result
    except Exception as e:
        logger.error(e)
        logger.error("Error while trying to get connection to DB")
        logger.info(
            "Are environment variables ITKDB_ACCESS_CODE1 and ITKDB_ACCESS_CODE2 set?")


def stage(lookupValue: "Value to look up (must be unique in the DB!)",
          stage: "Production stage to set",
          project: "ATLAS Project" = 'S',
          subProject: "ATLAS Subproject" = "SE",
          lookupKey: "Key that corresponds to VALUE" = 'serialNumber',
          componentType: "Type of component" = 'BT',
          comment: "Reason for production stage change" = ""):
    "Set or look up production stage for a component."
    logger.info(f"Getting component from the DB")
    component = lookup(project=project, subProject=subProject, lookupKey=lookupKey, value=[
                       lookupValue], componentType=componentType, returnResults=True)
    if len(component) == 0:
        logger.error(
            "No components that match the criteria were found in the DB")
        raise LookupError
    elif len(component) > 1:
        logger.error(
            "More than 1 component that match the criteria was found")
        raise LookupError
    component = component[lookupValue]
    if stage == "":
        logger.info(
            f"Current production stage: {component['currentStage']['code']}")
        if __name__ != '__main__':
            return component['currentStage']['code']
        else:
            return
    client = itkdb.Client()
    data = {
        'component': component['code'],
        'stage': stage,
    }
    if comment != "":
        data['comment'] = comment
    try:
        client.post('setComponentStage', data=data)
        logger.info(f"Set stage to {stage}")
    except Exception as e:
        logger.error(e)
        logger.error(
            f"DB error, is {stage} a valid stage for {componentType}?")


def skeleton(test: "Type of test",
             componentType: "Type of component" = "BT",
             project: "ATLAS Project" = 'S',
             returnResults: "Return available tests (useful if not used from CLI)" = False):
    "Genereate a test skeleton for a given test. Otput is either as JSON to the CLI or as a dict as a return value."
    allTests = tests(componentType=componentType,
                     project=project, returnResults=True)
    if not test in allTests:
        logger.error(f"Unable to find {test} for {componentType}")
    skeleton = {
        'runNumber': '0-0',
        'component': None,
        'results':
        {
        },
        'properties':
        {
        },
        'passed': False,
        'problems': False,
        'testType': test,
        'institution': None
    }

    for v in allTests[test]["properties"]:
        skeleton["properties"][v["code"]] = None
    for v in allTests[test]["parameters"]:
        skeleton["results"][v["code"]] = None

    if returnResults or __name__ != '__main__':
        return skeleton
    else:
        print(json.dumps(allTests[test], indent=1))


def upload(result: "Results from the test (path to .json file or dict)"):
    "Upload a test result to the DB."
    if isinstance(result, str) and os.path.isfile(result):
        logger.info(f"Loading test result from file {result}")
        with open(result) as jsonFile:
            result = json.load(jsonFile)
            jsonFile.close()
    elif isinstance(result, dict):
        logger.info("Test result was passed as a dict")
    else:
        logger.error(f"Unrecognised input {result}")
        return
    try:
        client = itkdb.Client()
        client.post('uploadTestRunResults', json=result)
        logger.info(
            f"Uploaded {result['testType']} results for {result['component']} to the DB")
    except Exception as e:
        logger.error(e)
        logger.error(f"Unable to upload result to DB, is the format correct?")


def testruns(cid: "Component ID",
             returnResults: "Return lookup results (useful if not used from CLI)" = False,
             printJSON: "PrettyPrint the component JSON" = False):
    "Look up all test results associated with a component ID."
    try:
        logger.info(f"Looking up tests in CID = {cid}")
        client = itkdb.Client()
        runs = client.get('listTestRunsByComponent', json={'component': cid})
        results = {}
        for i, testres in enumerate(runs):
            logger.info(
                f"Found {testres['testType']['name']} with ID = {testres['id']}")
            results[testres['id']] = testres
        if printJSON:
            for k in results:
                print(json.dumps(results[k], indent=1))
        if returnResults or __name__ != '__main__':
            return results
    except Exception as e:
        logger.error(e)
        logger.error("Error while trying to get connection to DB")
        logger.info(
            "Are environment variables ITKDB_ACCESS_CODE1 and ITKDB_ACCESS_CODE2 set?")


def testfile(file: "Path of the file to upload",
             testrun: "Test run code",
             title: "Title of the file" = "",
             description: "A file description" = "",
             filetype: "File MIME type (script can usually guess this)" = None):
    "Attach a file to a testrun in the DB."
    try:
        client = itkdb.Client()
        if filetype is None:
            # If you can't be bothered to look up the MIME type,
            # we'll look it up for you :)
            filetype = mimetypes.guess_type(file)
        data = {
            'testRun': testrun,
            'title': title,
            'description': description,
            'type': 'file',
            'url': file,
        }
        # Get attachment data
        attachment = {'data': (os.path.basename(
            file), open(file, 'rb'), filetype)}

        client.post('createTestRunAttachment',
                    data=data, files=attachment)
        logger.info(f"Attached file {file} to {testrun}")
    except Exception as e:
        logger.error(e)
        logger.error("Error while trying to get connection to DB")
        logger.info(
            "Are environment variables ITKDB_ACCESS_CODE1 and ITKDB_ACCESS_CODE2 set?")


def assemble(parent:     "Parent component identifier (ATLAS SN or alternative ID)",
             child:      "Child component identifier (ATLAS SN or alternative ID)",
             parentAID:  "Parent identifier is an alternative ID" = False,
             childAID:   "Child identifier is an alternative ID" = False,
             properties: "Properties collection (dict or .json file)" = None):
    "Assemble a component"
    if isinstance(properties, str) and os.path.isfile(properties):
        logger.info(f"Loading properties from file {properties}")
        with open(properties) as jsonFile:
            properties = json.load(jsonFile)
            jsonFile.close()
    elif isinstance(properties, dict):
        logger.info("Properties where passed as a dict")
    elif properties is None:
        logger.info("No properties given")
    else:
        logger.error(f"Unrecognised input {properties}")
        return
    try:
        data = {
            "parent": parent,
            "child": child,
            "alternativeIdentifierParent": parentAID,
            "alternativeIdentifierChild": childAID,
            "properties": properties
        }
        client = itkdb.Client()
        client.post('assembleComponent', json=data)
        logger.info(f"Assembled components {parent} and {child}")
    except Exception as e:
        logger.error(e)
        logger.error(
            f"Unable to assemble component in the DB, is the format correct?")


def property(componentID: "Component identifier or ATLAS serial number",
             property: "Property code",
             value: "Target value "):
    "Change a component property"
    try:
        client = itkdb.Client()
        data = {
            'component': componentID,
            'code': property,
            'value': value
        }

        client.post('setComponentProperty', data=data)
        logger.info(f"Changed property {property} of {componentID} to {value}")
    except Exception as e:
        logger.error(e)
        logger.error("Error while trying to get connection to DB")
        logger.info(
            "Are environment variables ITKDB_ACCESS_CODE1 and ITKDB_ACCESS_CODE2 set?")


def comment(identifier: "ID for the comment to be attached to (can be a ATLAS serial number in case of a component)",
            comment: "Comment to attach (can also be an array)",
            isTest: "If you want to attach to test instead of component" = False):
    "Attach a comment to a component or test"
    try:
        if isinstance(comment, str):
            comment = [comment]
        assert isinstance(comment, list)

        # Workaround for a very annoying bug in the db
        if len(comment) == 1:
            comment += [""]

        if isTest:
            data = {
                "testRun": identifier,
                "comments": comment
            }
            client = itkdb.Client()
            client.post('createTestRunComment', data=data)
        else:
            data = {
                "component": identifier,
                "comments": comment
            }
            client = itkdb.Client()
            client.post('createComponentComment', data=data)

        logger.info(f"Attached comment(s) to {identifier}")
    except Exception as e:
        logger.error(e)
        logger.error("Error while trying to get connection to DB")
        logger.info(
            "Are environment variables ITKDB_ACCESS_CODE1 and ITKDB_ACCESS_CODE2 set?")


def main():
    parser = argh.ArghParser()
    parser.add_commands([authenticate, register, lookup,
                        attach, tests, stage,
                        skeleton, upload, testruns,
                        testfile, assemble, property,
                        comment])
    parser.dispatch()


if __name__ == '__main__':
    main()
