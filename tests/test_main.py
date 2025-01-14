from osemosys2iamc.resultify import main
import os
from yaml import load, SafeLoader
from pyam import IamDataFrame
from pyam.testing import assert_iamframe_equal
import pandas as pd

def test_main_input():

    config = os.path.join("tests", "fixtures", "config_input.yaml")
    inputs = os.path.join("tests", "fixtures")
    results = os.path.join("tests", "fixtures")

    with open(config, 'r') as config_file:
        config = load(config_file, Loader=SafeLoader)

    actual = main(config, inputs, results)

    data = pd.DataFrame([
        ['AUSTRIA', 'Price|Primary Energy|Biomass', 2015, 3.15],
        ['AUSTRIA', 'Price|Primary Energy|Biomass', 2016, 4.2],
        ['BELGIUM', 'Price|Primary Energy|Biomass', 2015, 1.785],
        ['BELGIUM', 'Price|Primary Energy|Biomass', 2016, 1.890],
    ], columns=['region', 'variable', 'year', 'value'])

    expected = IamDataFrame(data, model='OSeMBE v1.0.0', scenario= 'DIAG-C400-lin-ResidualFossil', unit='EUR_2020/GJ')

    assert_iamframe_equal(actual, expected)

def test_main_result():

    config = os.path.join("tests", "fixtures", "config_result.yaml")
    inputs = os.path.join("tests", "fixtures")
    results = os.path.join("tests", "fixtures")

    with open(config, 'r') as config_file:
        config = load(config_file, Loader=SafeLoader)

    actual = main(config, inputs, results)

    data = pd.DataFrame([
        ['AUSTRIA','Capacity|Electricity',2015,0.446776],
        ['BELGIUM','Capacity|Electricity',2016,0.184866],
        ['BULGARIA','Capacity|Electricity',2015,4.141],
        ['CYPRUS','Capacity|Electricity',2015,0.3904880555817921],
        ['CZECHIA','Capacity|Electricity',2015,0.299709],
        ['DENMARK','Capacity|Electricity',2015,0.0005],
        ['ESTONIA','Capacity|Electricity',2015,0.006],
        ['FINLAND','Capacity|Electricity',2015,0.0263],
        ['FRANCE','Capacity|Electricity',2015,0.47835],
        ['GERMANY','Capacity|Electricity',2015,9.62143],
        ['SPAIN','Capacity|Electricity',2015,7.7308],
        ['SWITZERLAND','Capacity|Electricity',2026,0.004563975391582646],
        
    ], columns=['region', 'variable', 'year', 'value'])

    expected = IamDataFrame(data, model='OSeMBE v1.0.0', scenario= 'DIAG-C400-lin-ResidualFossil', unit='GW')

    assert_iamframe_equal(actual, expected)

def test_main_result_capture():
    """
    REGION1,ATBMCSPN2,CO2,2026,-7573.069442598169
    REGION1,ATBMCSPN2,CO2,2027,-7766.777427515737
    REGION1,BEBMCSPN2,CO2,2026,-2244.98280006968
    REGION1,BEBMCSPN2,CO2,2027,-6746.886436926597
    """

    config = os.path.join("tests", "fixtures", "config_result_capture.yaml")
    inputs = os.path.join("tests", "fixtures")
    results = os.path.join("tests", "fixtures")

    with open(config, 'r') as config_file:
        config = load(config_file, Loader=SafeLoader)

    actual = main(config, inputs, results)

    data = pd.DataFrame([
        ['AUSTRIA', 'Carbon Capture|Biomass', 2026, 7.573069442598169],
        ['AUSTRIA', 'Carbon Capture|Biomass', 2027, 7.766777427515737],
        ['BELGIUM', 'Carbon Capture|Biomass', 2026, 2.24498280006968],
        ['BELGIUM', 'Carbon Capture|Biomass', 2027, 6.746886436926597],
    ], columns=['region', 'variable', 'year', 'value'])

    expected = IamDataFrame(data, model='OSeMBE v1.0.0', scenario= 'DIAG-C400-lin-ResidualFossil', unit='Mt CO2/yr')

    assert_iamframe_equal(actual, expected)
