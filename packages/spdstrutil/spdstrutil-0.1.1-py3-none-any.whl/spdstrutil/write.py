"""_summary_
write.py contains functionalities
to export some utilities data structures into
program memory

[author]    Diogo André Silvares Dias
[date]      2022-04-17
[contact]   das.dias@campus.fct.unl.pt
"""
import yaml
import os
from .data import(
    GdsTable,
)

def writeGdsTable(tab: GdsTable, filePath: str) -> None:
    path = os.path.abspath(filePath)
    if not os.path.isdir(path):
        raise ValueError("Invalid directory path provided")
    path = os.path.join(path, "gds_table.yaml")
    with open(path, "w") as yamlFile:
        yaml.dump(tab.__dict__(), yamlFile)
