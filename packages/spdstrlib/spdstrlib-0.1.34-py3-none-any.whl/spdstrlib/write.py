import os
import sys
from loguru import logger
import pickle
import json
from .data import *

def dump(lib: SpdstrWorkspaceLib) -> None:
    """
    Saves the workspace library (saved in .bin (binary) format)
    """
    workspaceLibPath = lib.getWorkspaceLibPath()
    #logger.info("Saving workspace library...")
    # if the workspace library path does not exist, create it
    """
    if not os.path.exists(workspaceLibPath):
        raise FileNotFoundError("The workspace library path \"{}\" does not exist".format(workspaceLibPath))
    """
    try:
        with open(workspaceLibPath, "wb") as f:
            pickle.dump(lib, f)
    except Exception as e:
        raise e
    #logger.info("Success saving workspace library")
    

def write(project: SpdstrWorkspace):
    """_summary_
    Saves a workspace (saved in .json format)
    Args:
        workspacePath (_type_): _description_
    """
    workspaceName = project.name
    workspacePath = project.workspacePath
    logger.info("Saving workspace \"{}\"".format(workspaceName))
    if workspacePath == "":
        raise ValueError("No workspace parent directory path was specified")
    
    if not os.path.exists(workspacePath):
        raise FileNotFoundError("The workspace path \"{}\" does not exist".format(workspacePath))
    # write the workspace
    filepath = os.path.join(workspacePath, "{}.json".format(workspaceName))
    with open(filepath, "w") as f:
        json.dump(project.__dict__(), f)
    logger.info("Success saving workspace \"{}\"".format(workspaceName))