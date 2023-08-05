def lookupModelDataToPyBBQ(key: str, mode='data2PyBBQ'):
    """
        Retrieves the correct PyBBQ parameter name for a DataModelMagnet input
        The argument mode is used to define the direction, either "data2PyBBQ" or "PyBBQ2data"
    """
    lookup = {
    'GeneralParameters.material_database_path': 'matpath',
    'Power_Supply.I_initial': 'Current',
    'Quench_Protection.Energy_Extraction.R_EE': 'DumpR',
    'Options_PyBBQ.geometry.thInsul' : 'insulation_thickness',
    'Options_PyBBQ.geometry.lenBusbar': 'busbar_length',
    'Options_PyBBQ.magnetic_field.Calc_b_from_geometry' : 'Calc_b_from_geometry',
    'Options_PyBBQ.magnetic_field.Background_Bx' : 'Background_Bx',
    'Options_PyBBQ.magnetic_field.Background_By' : 'Background_By',
    'Options_PyBBQ.magnetic_field.Background_Bz' : 'Background_Bz',
    'Options_PyBBQ.magnetic_field.Self_Field' : 'Self_Field',
    'Options_PyBBQ.magnetic_field.B0_dump': 'B0_dump',
    'Options_PyBBQ.simulation.meshSize': 'sections',
    'Options_PyBBQ.simulation.layers': 'layers',
    'Options_PyBBQ.simulation.output': 'output',
    'Options_PyBBQ.simulation.dt': 'dt',
    'Options_PyBBQ.simulation.t0': 't0',
    'Circuit.L_circuit': 'Inductance',
    'GeneralParameters.T_initial': 'T1',
    'Options_PyBBQ.physics.VThreshold': 'Detection_Voltage',
    'Options_PyBBQ.physics.tValidation': 'Protection_Delay',
    'Options_PyBBQ.physics.withCoolingToBath': 'Helium_Cooling',
     }

    if mode == 'data2PyBBQ':
        returned_key = lookup[key] if key in lookup else None
    elif mode == 'PyBBQ2data':
        # Generate an inverted dictionary
        lookup_inverted = {v: k for k, v in lookup.items()}
        returned_key = lookup_inverted[key] if key in lookup_inverted else None

    return returned_key
