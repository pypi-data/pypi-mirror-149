#!/usr/bin/python3

# DIDIS - Desy ITk Database Interaction Script -- DESY's very own framework for interacting with the ITk Production Database
# Based on itkdb: https://gitlab.cern.ch/atlas-itk/sw/db/itkdb
# Created: 2021/11/17, Updated: 2022/02/15
# Written by Maximilian Felix Caspar, DESY HH


from loguru import logger
import argh

import pandas as pd
import didis.didis as dd


def register(excelFile: "Excel file containing the component data",
             componentType: "Type of component" = "THERMALFOAMSET",
             project: "ATLAS Project" = "S",
             subProject: "ATLAS Subproject" = "SE",
             institution: "Institute doing the registration" = "DESYHH",
             subType: "Component Subtype" = "THERMALFOAMSET_PETAL",
             lambdaFunction: "Function that modifies the df (takes the df as argument, returns the modified df)" = None,
             sheetName: "Name or number of the excel sheet to process" = 0
             ):
    "Registering components from an excel file."
    df = pd.read_excel(excelFile, header=1, sheet_name=sheetName)
    print(df)
    if lambdaFunction is not None:
        df = lambdaFunction(df)
        logger.info("Modified the dataframe")
        assert isinstance(df, pd.DataFrame)
        print(df)
    # Loop over the rows
    for i, r in df.iterrows():
        JSON = {}
        JSON['institution'] = institution
        JSON['componentType'] = componentType
        JSON['project'] = project
        JSON['subproject'] = subProject
        JSON['type'] = subType

        Properties = {}
        Batches = {}
        # Loop over the columns in the row
        for i, k in enumerate(r.keys()):
            if k == "serialNumber":
                JSON["serialNumber"] = r[k]
            elif k == "alternativeIdentifier":
                JSON["alternativeIdentifier"] = r[k]
                JSON["serialNumber"] = None
            elif k.startswith("B_"):
                Batches[k[2:]] = r[k]
            else:
                Properties[k] = r[k]
        JSON['properties'] = Properties
        if Batches != {}:
            JSON["batches"] = Batches
        dd.register(JSON)


def main():
    parser = argh.ArghParser()
    parser.add_commands([register])
    parser.dispatch()


if __name__ == '__main__':
    main()
