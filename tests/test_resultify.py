from datetime import date
import pandas as pd
import os
import pytest
from osemosys2iamc.resultify import (filter_technology_fuel,
                                     filter_emission_tech,
                                     filter_final_energy,
                                     filter_capacity,
                                     calculate_trade,
                                     read_file,
                                     iso_to_country)


class TestTrade:

    def test_trade(self):

        use = [
            ['REGION1','ID','ATBM00X00','ATBM', 2014, 5.0],
            ['REGION1','ID','ATBM00X00','ATBM', 2015, 5.0],
            ]

        production = [
            ['REGION1','ATBM00X00','ATBM', 2015, 10.0],
            ['REGION1','ATBM00X00','ATBM', 2016, 10.0],
        ]

        results = {
            'UseByTechnology': pd.DataFrame(
                data = use,
                columns = ['REGION','TIMESLICE','TECHNOLOGY','FUEL','YEAR','VALUE']
            ),
            'ProductionByTechnologyAnnual': pd.DataFrame(
                data = production,
                columns=['REGION','TECHNOLOGY','FUEL','YEAR','VALUE'])
        }

        techs = ['ATBM00X00']

        actual = calculate_trade(results, techs)

        expected_data = [
            ['REGION1',2014,  5.0],
            ['REGION1',2015, -5.0],
            ['REGION1',2016, -10.0],
        ]

        expected = pd.DataFrame(expected_data, columns=['REGION', 'YEAR', 'VALUE'])
        pd.testing.assert_frame_equal(actual, expected)


class TestEmissions:

    def test_filter_emission(self):

        folderpath = os.path.join("tests","fixtures")
        input_data = read_file(folderpath, "AnnualTechnologyEmissions", "iso2_start")

        emission = ['CO2']
        actual = filter_emission_tech(input_data, emission)

        data = [
            ["AUSTRIA", 2026, -6244.862561],
            ["AUSTRIA", 2027, -6529.532083],
            ["AUSTRIA", 2030,  3043.148835],
            ["AUSTRIA", 2031,  2189.064681],
            ["AUSTRIA", 2032,  2315.821267],
            ["BELGIUM", 2026, -2244.982800],
            ["BELGIUM", 2027, -6746.886437],
            ["BULGARIA", 2030, 11096.556931],
            ["BULGARIA", 2031, 11069.257141],
            ["BULGARIA", 2032, 11041.957354]
        ]

        expected = pd.DataFrame(
            data=data,
            columns=['REGION', 'YEAR', 'VALUE'])

        pd.testing.assert_frame_equal(actual, expected)

    def test_filter_tech_emission(self):

        folderpath = os.path.join("tests","fixtures")
        input_data = read_file(folderpath, "AnnualTechnologyEmissions", "iso2_start")

        tech = ['(?=^.{2}(BM))^.{4}(CS)']
        emission = ['CO2']
        actual = filter_emission_tech(input_data, emission, tech)

        data = [
            ['AUSTRIA', 2026, -7573.069442598169],
            ['AUSTRIA', 2027, -7766.777427515737],
            ['BELGIUM', 2026, -2244.98280006968],
            ['BELGIUM', 2027, -6746.886436926597],
        ]

        expected = pd.DataFrame(
            data=data,
            columns=['REGION', 'YEAR', 'VALUE'])
        print(actual)
        print(expected)
        pd.testing.assert_frame_equal(actual, expected)

class TestFilter:

    def test_filter_fuel(self):
        folderpath = os.path.join("tests","fixtures")
        input_data = read_file(folderpath, "UseByTechnology", "from_csv")

        technologies = ['ALUPLANT']
        fuels = ['C1_P_HCO']
        actual = filter_technology_fuel(input_data, technologies, fuels)

        data = [
            ["Globe",  2010,  0.828098],
            ["Globe",  2011,  0.825347],
            ["Globe",  2012,  0.852052]
        ]
        expected = pd.DataFrame(data=data,
            columns=['REGION', 'YEAR', 'VALUE'])

        print(actual, type(actual))
        print(expected, type(expected))

        pd.testing.assert_frame_equal(actual, expected)

class TestEnergy:

    def test_filter_capacity(self):
        folderpath = os.path.join("tests","fixtures")
        input_data = read_file(folderpath, "ProductionByTechnologyAnnual", "iso2_start")

        technologies = ['^.{6}(I0)','^.{6}(X0)','^.{2}(HY)','^.{2}(OC)','^.{2}(SO)','^.{2}(WI)']
        actual = filter_capacity(input_data, technologies)

        data = [
            ['AUSTRIA', 2015, 26.324108350683794],
            ['AUSTRIA', 2016, 26.324108350683794],
            ['AUSTRIA', 2017, 26.324108350683794],
            ['AUSTRIA', 2018, 26.324108350683787],
            ['AUSTRIA', 2019, 26.324108350683794],
            ['BELGIUM', 2016, 141.0],
            ['BULGARIA', 2015, 1.423512],
            ['CZECHIA', 2015, 329.5950809],
            ['DENMARK', 2015, 0.0031536],
            ['ESTONIA', 2015, 28.512108],
            ['FINLAND', 2015, 0.296581102],
            ['FRANCE', 2015, 72.25974846],
            ['SPAIN', 2015, 26.75595496],
            ['SWITZERLAND', 2047, 69.9750212433476],
            ['SWITZERLAND', 2048, 91.45662886581975],
            ['SWITZERLAND', 2049, 76.86770297185006],
            ['SWITZERLAND', 2050, 70.86078033897608],
            ['SWITZERLAND', 2051, 53.88447040760964]
        ]

        expected = pd.DataFrame(data=data, columns=["REGION", "YEAR","VALUE"])

        pd.testing.assert_frame_equal(actual, expected)

    def test_filter_primary_bm(self):
        folderpath = os.path.join("tests","fixtures")
        input_data = read_file(folderpath, "ProductionByTechnologyAnnual", "iso2_start")

        technologies = ['(?=^.{2}(BM))^.{4}(00)','(?=^.{2}(WS))^.{4}(00)']
        actual = filter_capacity(input_data, technologies)

        data = [
            ['AUSTRIA',2015,26.324108350683794],
            ['AUSTRIA',2016,26.324108350683794],
            ['AUSTRIA',2017,26.324108350683794],
            ['AUSTRIA',2018,26.324108350683787],
            ['AUSTRIA',2019,26.324108350683794],
        ]

        expected = pd.DataFrame(data=data, columns=["REGION", "YEAR","VALUE"])

        pd.testing.assert_frame_equal(actual, expected)

    def test_filter_primary_co(self):
        folderpath = os.path.join("tests","fixtures")
        input_data = read_file(folderpath, "ProductionByTechnologyAnnual", "iso2_start")

        technologies = ['(?=^.{2}(CO))^.{4}(00)']
        actual = filter_capacity(input_data, technologies)

        data = [
            ['SWITZERLAND',2047,69.9750212433476],
            ['SWITZERLAND',2048,91.45662886581975],
            ['SWITZERLAND',2049,76.86770297185006],
            ['SWITZERLAND',2050,70.86078033897608],
            ['SWITZERLAND',2051,53.88447040760964],
        ]

        expected = pd.DataFrame(data=data, columns=["REGION", "YEAR","VALUE"])

        pd.testing.assert_frame_equal(actual, expected)

    def test_filter_primary_ng(self):
        folderpath = os.path.join("tests","fixtures")
        input_data = read_file(folderpath, "ProductionByTechnologyAnnual", "iso2_start")

        technologies = ['(?=^.{2}(NG))^.{4}(00)']
        actual = filter_capacity(input_data, technologies)

        data = [
            ['BELGIUM',2016,141.0],
        ]

        expected = pd.DataFrame(data=data, columns=["REGION", "YEAR","VALUE"])

        pd.testing.assert_frame_equal(actual, expected)

    def test_filter_primary_go(self):
        folderpath = os.path.join("tests","fixtures")
        input_data = read_file(folderpath, "ProductionByTechnologyAnnual", "iso2_start")

        technologies = ['(?=^.{2}(GO))^.{4}(00)']
        actual = filter_capacity(input_data, technologies)

        data = [
            ['BULGARIA',2015,1.423512],
        ]

        expected = pd.DataFrame(data=data, columns=["REGION", "YEAR","VALUE"])
        pd.testing.assert_frame_equal(actual, expected)

    def test_filter_primary_hy(self):
        folderpath = os.path.join("tests","fixtures")
        input_data = read_file(folderpath, "ProductionByTechnologyAnnual", "iso2_start")

        technologies = ['^.{2}(HY)']
        actual = filter_capacity(input_data, technologies)

        data = [
            ['CZECHIA',2015,3.3637616987287244],
        ]

        expected = pd.DataFrame(data=data, columns=["REGION", "YEAR","VALUE"])
        pd.testing.assert_frame_equal(actual, expected)

    def test_filter_primary_nu(self):
        folderpath = os.path.join("tests","fixtures")
        input_data = read_file(folderpath, "ProductionByTechnologyAnnual", "iso2_start")

        technologies = ['^.{2}(UR)']
        actual = filter_capacity(input_data, technologies)

        data = [
            ['CZECHIA',2015,326.2313192401038],
        ]

        expected = pd.DataFrame(data=data, columns=["REGION", "YEAR","VALUE"])
        pd.testing.assert_frame_equal(actual, expected)

    def test_filter_primary_oc(self):
        folderpath = os.path.join("tests","fixtures")
        input_data = read_file(folderpath, "ProductionByTechnologyAnnual", "iso2_start")

        technologies = ['^.{2}(OC)']
        actual = filter_capacity(input_data, technologies)

        data = [
            ['DENMARK',2015,0.0031536000000000003],
        ]

        expected = pd.DataFrame(data=data, columns=["REGION", "YEAR","VALUE"])

        pd.testing.assert_frame_equal(actual, expected)

    def test_filter_primary_oi(self):
        folderpath = os.path.join("tests","fixtures")
        input_data = read_file(folderpath, "ProductionByTechnologyAnnual", "iso2_start")

        technologies = ['(?=^.{2}(OI))^.{4}(00)','(?=^.{2}(HF))^.{4}(00)']
        actual = filter_capacity(input_data, technologies)

        data = [
            ['ESTONIA',2015,28.512107999999998],
        ]

        expected = pd.DataFrame(data=data, columns=["REGION", "YEAR","VALUE"])

        pd.testing.assert_frame_equal(actual, expected)

    def test_filter_primary_so(self):
        folderpath = os.path.join("tests","fixtures")
        input_data = read_file(folderpath, "ProductionByTechnologyAnnual", "iso2_start")

        technologies = ['^.{2}(SO)']
        actual = filter_capacity(input_data, technologies)

        data = [
            ['SPAIN',2015,26.75595496070811],
        ]

        expected = pd.DataFrame(data=data, columns=["REGION", "YEAR","VALUE"])

        pd.testing.assert_frame_equal(actual, expected)

    def test_filter_primary_wi(self):
        folderpath = os.path.join("tests","fixtures")
        input_data = read_file(folderpath, "ProductionByTechnologyAnnual", "iso2_start")

        technologies = ['^.{2}(WI)']
        actual = filter_capacity(input_data, technologies)

        data = [
            ['FINLAND', 2015, 0.29658110158442175],
            ['FRANCE', 2015, 72.25974845531343]
        ]

        expected = pd.DataFrame(data=data, columns=["REGION", "YEAR","VALUE"])

        pd.testing.assert_frame_equal(actual, expected)

    def test_filter_secondary_bm(self):
        folderpath = os.path.join("tests","fixtures")
        input_data = read_file(folderpath, "ProductionByTechnologyAnnual", "iso2_start")

        technologies = ['(?=^.{2}(BF))^((?!00).)*$','(?=^.{2}(BM))^((?!00).)*$', '(?=^.{2}(WS))^((?!00).)*$']
        actual = filter_capacity(input_data, technologies)

        data = [
            ['AUSTRIA', 2042, 0.6636346353894057],
            ['AUSTRIA', 2043, 1.3300518531620575],
            ['AUSTRIA', 2044, 1.9992691432067637],
            ['AUSTRIA', 2045, 2.6713041901899794],
            ['AUSTRIA', 2046, 3.4778527409137996]
        ]

        expected = pd.DataFrame(data=data, columns=["REGION", "YEAR","VALUE"])

        pd.testing.assert_frame_equal(actual, expected)

    def test_filter_final_energy(self):
        folderpath = os.path.join("tests","fixtures")
        input_data = read_file(folderpath, "Demand", "iso2_start")

        fuels = ['^.*E2$']
        actual = filter_final_energy(input_data, fuels)

        data = [
            ['AUSTRIA',2015,227.5944502],
            ['BELGIUM',2016,296.0570016],
        ]

        expected = pd.DataFrame(data=data, columns=["REGION", "YEAR", "VALUE"])

        print(actual)
        print(expected)

        pd.testing.assert_frame_equal(actual, expected)

class TestCapacity:

    def test_filter_inst_capacity(self):
        folderpath = os.path.join("tests","fixtures")
        input_data = read_file(folderpath, "TotalCapacityAnnual", "iso2_start")
        technologies = ['^((?!(EL)|(00)).)*$']
        actual = filter_capacity(input_data, technologies)

        data = [
            ['AUSTRIA',2015,0.446776],
            ['BELGIUM',2016,0.184866],
            ['BULGARIA',2015,4.141],
            ['CYPRUS',2015,0.3904880555817921],
            ['CZECHIA',2015,0.299709],
            ['DENMARK',2015,0.0005],
            ['ESTONIA',2015,0.006],
            ['FINLAND',2015,0.0263],
            ['FRANCE',2015,0.47835],
            ['GERMANY',2015,9.62143],
            ['SPAIN',2015,7.7308],
            ['SWITZERLAND',2026,0.004563975391582646]
            
        ]

        expected = pd.DataFrame(data=data, columns=["REGION", "YEAR", "VALUE"])

        print(actual)

        print(expected)

        pd.testing.assert_frame_equal(actual, expected)

    def test_filter_inst_capacity_bio(self):
        folderpath = os.path.join("tests","fixtures")
        input_data = read_file(folderpath, "TotalCapacityAnnual", "iso2_start")
        technologies = ['(?=^.{2}(BF))^((?!00).)*$','(?=^.{2}(BM))^((?!00).)*$', '(?=^.{2}(WS))^((?!00).)*$']
        actual = filter_capacity(input_data, technologies)

        data = [
            ['AUSTRIA',2015,0.446776],
            ['BELGIUM',2016,0.184866],
            ['FRANCE', 2015, 0.47835],
        ]

        expected = pd.DataFrame(data=data, columns=["REGION", "YEAR", "VALUE"])

        pd.testing.assert_frame_equal(actual, expected)

    def test_filter_inst_capacity_coal(self):
        folderpath = os.path.join("tests","fixtures")
        input_data = read_file(folderpath, "TotalCapacityAnnual", "iso2_start")
        technologies = ['(?=^.{2}(CO))^((?!00).)*$']
        actual = filter_capacity(input_data, technologies)

        data = [
            ['BULGARIA',2015,4.141],
        ]

        expected = pd.DataFrame(data=data, columns=["REGION", "YEAR", "VALUE"])

        pd.testing.assert_frame_equal(actual, expected)

    def test_filter_inst_capacity_gas(self):
        folderpath = os.path.join("tests","fixtures")
        input_data = read_file(folderpath, "TotalCapacityAnnual", "iso2_start")
        technologies = ['(?=^.{2}(NG))^((?!00).)*$']
        actual = filter_capacity(input_data, technologies)

        data = [
            ['GERMANY',2015,9.62143],
        ]

        expected = pd.DataFrame(data=data, columns=["REGION", "YEAR", "VALUE"])

        pd.testing.assert_frame_equal(actual, expected)

    def test_filter_inst_capacity_geo(self):
        folderpath = os.path.join("tests","fixtures")
        input_data = read_file(folderpath, "TotalCapacityAnnual", "iso2_start")
        technologies = ['(?=^.{2}(GO))^((?!00).)*$']
        actual = filter_capacity(input_data, technologies)

        data = [
            ['SWITZERLAND',2026,0.004563975391582646],
        ]

        expected = pd.DataFrame(data=data, columns=["REGION", "YEAR", "VALUE"])

        pd.testing.assert_frame_equal(actual, expected)

    def test_filter_inst_capacity_hydro(self):
        folderpath = os.path.join("tests","fixtures")
        input_data = read_file(folderpath, "TotalCapacityAnnual", "iso2_start")
        technologies = ['^.{2}(HY)']
        actual = filter_capacity(input_data, technologies)

        data = [
            ['CZECHIA',2015,0.299709],
        ]

        expected = pd.DataFrame(data=data, columns=["REGION", "YEAR", "VALUE"])

        pd.testing.assert_frame_equal(actual, expected)

    def test_filter_inst_capacity_nuclear(self):
        folderpath = os.path.join("tests","fixtures")
        input_data = read_file(folderpath, "TotalCapacityAnnual", "iso2_start")
        technologies = ['^.{2}(NU)']
        actual = filter_capacity(input_data, technologies)

        data = [
            ['SPAIN',2015,7.7308],
        ]

        expected = pd.DataFrame(data=data, columns=["REGION", "YEAR", "VALUE"])

        pd.testing.assert_frame_equal(actual, expected)

    def test_filter_inst_capacity_ocean(self):
        folderpath = os.path.join("tests","fixtures")
        input_data = read_file(folderpath, "TotalCapacityAnnual", "iso2_start")
        technologies = ['^.{2}(OC)']
        actual = filter_capacity(input_data, technologies)

        data = [
            ['DENMARK',2015,0.0005],
        ]

        expected = pd.DataFrame(data=data, columns=["REGION", "YEAR", "VALUE"])

        pd.testing.assert_frame_equal(actual, expected)

    def test_filter_inst_capacity_oil(self):
        folderpath = os.path.join("tests","fixtures")
        input_data = read_file(folderpath, "TotalCapacityAnnual", "iso2_start")
        technologies = ['(?=^.{2}(HF))^((?!00).)*$']
        actual = filter_capacity(input_data, technologies)

        data = [
            ['CYPRUS',2015,0.3904880555817921],
        ]

        expected = pd.DataFrame(data=data, columns=["REGION", "YEAR", "VALUE"])

        pd.testing.assert_frame_equal(actual, expected)

    def test_filter_inst_capacity_solar(self):
        folderpath = os.path.join("tests","fixtures")
        input_data = read_file(folderpath, "TotalCapacityAnnual", "iso2_start")
        technologies = ['^.{2}(SO)']
        actual = filter_capacity(input_data, technologies)

        data = [
            ['ESTONIA',2015,0.006],
        ]

        expected = pd.DataFrame(data=data, columns=["REGION", "YEAR", "VALUE"])

        pd.testing.assert_frame_equal(actual, expected)

    def test_filter_inst_capacity_wi_offshore(self):
        folderpath = os.path.join("tests","fixtures")
        input_data = read_file(folderpath, "TotalCapacityAnnual", "iso2_start")
        technologies = ['(?=^.{2}(WI))^.{4}(OF)']
        actual = filter_capacity(input_data, technologies)

        data = [
            ['FINLAND',2015,0.0263],
        ]

        expected = pd.DataFrame(data=data, columns=["REGION", "YEAR", "VALUE"])

        pd.testing.assert_frame_equal(actual, expected)

class TestPrice:

    def test_price_bm(self):
        folderpath = os.path.join("tests","fixtures")
        input_data = read_file(folderpath, "VariableCost", "iso2_start")
        commodity = ['(?=^.{2}(BM))^.{6}(X0)']
        actual = filter_capacity(input_data, commodity)

        data = [
            ['AUSTRIA',2015,3.0],
            ['AUSTRIA',2016,4.0],
            ['BELGIUM',2015,1.7],
            ['BELGIUM',2016,1.8],
        ]

        expected = pd.DataFrame(data=data, columns=["REGION", "YEAR", "VALUE"])

        print(actual)
        print(expected)

        pd.testing.assert_frame_equal(actual, expected)

class TestCountryConversion:

    def test_iso_to_country_iso2start(self):
        techs = ['NGNGA2', 'DENGA2', 'NGKENGX', 'ZXNGA']

        actual = iso_to_country('iso2_start', techs, 'TotalCapacityAnnual')

        expected = ['NIGERIA', 'GERMANY', 'NIGERIA', '']

        assert actual == expected

    def test_iso_to_country_iso3start(self):
        techs = ['NGANGA', 'BHSHYA', 'TCASOA', 'ZXNGA']

        actual = iso_to_country('iso3_start', techs, 'TotalCapacityAnnual')

        expected = ['NIGERIA', 'BAHAMAS', 'TURKS AND CAICOS ISLANDS', '']

        assert actual == expected

    def test_iso_to_country_iso2end(self):
        techs = ['NGA2NG', 'NGA2DE', 'KENGXNG', 'NGAZX']

        actual = iso_to_country('iso2_end', techs, 'TotalCapacityAnnual')

        expected = ['NIGERIA', 'GERMANY', 'NIGERIA', '']

        assert actual == expected

    def test_iso_to_country_iso3end(self):
        techs = ['NGANGA', 'HYABHS', 'SOATCA', 'NGAZX']

        actual = iso_to_country('iso3_end', techs, 'TotalCapacityAnnual')

        expected = ['NIGERIA', 'BAHAMAS', 'TURKS AND CAICOS ISLANDS', '']

        assert actual == expected

    def test_iso_to_country_iso2middle(self):
        techs = ['NGA2NGZZ', 'NGA2DEVV', 'NGAZXVV', 'CZF']

        actual = iso_to_country('iso2_5', techs, 'TotalCapacityAnnual')

        expected = ['NIGERIA', 'GERMANY', '', '']

        assert actual == expected

    def test_iso_to_country_iso3middle(self):
        techs = ['NGANGAGHAPP', 'HYABHSLCA', 'ABWBMUABC', 'NGAZX']

        actual = iso_to_country('iso3_7', techs, 'TotalCapacityAnnual')

        expected = ['GHANA', 'SAINT LUCIA', '', '']

        assert actual == expected
