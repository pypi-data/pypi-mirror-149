from pydantic import BaseModel
from typing import (List)

"""
    These classes define the four PyBBQ dataclasses, which contain the variables to write in the PyBBQ 
    input file.
"""

class DataPyBBQ(BaseModel):
    # Cable geometry and operating values:
    width: float = None
    height: float = None
    CuSC: float = None
    non_void: float = None
    shape: str = None
    layers: int = None
    insulation_thickness: float = None
    busbar_length: float = None
    sections: int = None
    T1: float = None

    # Magnetic Field
    Calc_b_from_geometry: bool = None
    Background_Bx: float = None
    Background_By: float = None
    Background_Bz: float = None
    Self_Field: float = None
    B0_dump: bool = None

    # Load
    Current: float = None
    Inductance: float = None
    DumpR: float = None

    # Cooling
    Helium_Cooling: bool = None

    # Protection and Detection
    Detection_Voltage: float = None
    Protection_Delay: float = None

    # Solver setting:
    output: bool = None
    dt: float = None
    t0: List[float] = []

    # Materials:
    matpath: str = None
