import csv
import os
import sys
import pytest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pages.Shipper_Page import ShipperFilter

def read_csv():
    """Read all rows from CSV and return a list of dicts"""
    with open('./test_data/Shipper_filter.csv', mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        return list(reader)  # ✅ return all rows

# ---- Parameterize using pytest ----
@pytest.fixture(params=read_csv())
def csv_data(request):
    """Yield one row of CSV data per test run."""
    row = request.param
    return {
        "S_S_Name": row['Shipper_Standardized_Name_Search'],
        "Partial_S_S_Name": row['Search_partial_ShipperName'],
        "S_Name": row['Shipper_Name'],
        "country": row['Country'],
        "shipper_type":row["Shipper_Type"]
    }

@pytest.fixture
def shipper_page_and_data(browser_setup, csv_data):
    """Provides ShipperFilter instance + data from CSV."""
    page = browser_setup  # browser_setup should return a Page object
    shipper_page = ShipperFilter(page)
    yield shipper_page, csv_data["S_S_Name"],csv_data["Partial_S_S_Name"],csv_data["S_Name"],csv_data["country"],csv_data["shipper_type"]
    # browser_setup handles cleanup

# ---- Test Class ----
class TestTrademo:
    """Validating Shipper Filter Functionality"""

    def test_Trademo_IndiaTC19(self, browser_setup, shipper_page_and_data, Reset_Default_view, Close_modal, Reset, Check_Country):
        page = browser_setup
        shipper_page, _,_,_,_,_ = shipper_page_and_data  # unpack fixture

        print("🔍 Running TC19: Verify the Cargo filter option displays correct data")
        Check_Country()
        Reset_Default_view()
        Reset()
        shipper_page.open_shipper_dropdown()
        shipper_page.Shipment_Filter_Option()

    def test_Trademo_IndiaTC20(self, browser_setup, shipper_page_and_data, Reset_Default_view, Close_modal, Reset, Check_Country):
        shipper_page, S_S_Name,Partial_S_S_Name,S_Name,_,_= shipper_page_and_data  # fixed unpacking

        Check_Country()
        Reset()
        print("🔍 Running TC20: Verify 'Shipper Standardized Name' Filter Displays Relevant Data")
        shipper_page.open_shipper_dropdown()
        shipper_page.Click_S_SName()
        shipper_page.Shipper_Filter_Search(S_S_Name)
        shipper_page.Apply_Filter_Functionality()
        shipper_page.Validate_ShipmentRecord_Count()
        shipper_page.Validate_Total_RecordCount_In_the_Table()
        shipper_page.Validate_S_S_Name_label()
        shipper_page.Validate_Exporter_Tab()
        shipper_page.check_Shipper_Standardized_Name_Filter()
        Reset()
        shipper_page.Manual_Search(S_S_Name,Partial_S_S_Name)

    def test_Trademo_IndiaTC21(self, browser_setup, shipper_page_and_data, Reset_Default_view, Close_modal, Reset,Check_Country):
        shipper_page, S_S_Name, Partial_S_S_Name,S_Name,_,_ = shipper_page_and_data  # fixed unpacking
        Check_Country()
        Reset()
        """Test Case 21: Verify “Shipper Name” Filter Displays Relevant Data"""
        print("🔍 Running TC21: Verify “Shipper Name” Filter Displays Relevant Data")
        shipper_page.open_shipper_dropdown()
        shipper_page.Click_ShipperName_Option()
        shipper_page.Shipper_Filter_Search(S_Name)
        shipper_page.Apply_Filter_Functionality()
        shipper_page.Validate_ShipmentRecord_Count()
        shipper_page.Validate_Total_RecordCount_In_the_Table()
        shipper_page.Validate_S_S_Name_label()
        shipper_page.Validate_Exporter_Tab()
        shipper_page.check_Shipper_Name_intheGrid_View()
        Reset()

    def test_Trademo_IndiaTC22(self, browser_setup, shipper_page_and_data, Reset_Default_view, Close_modal, Reset,Check_Country):
        shipper_page, S_S_Name, Partial_S_S_Name, S_Name,country,shipper_type = shipper_page_and_data  # fixed unpacking
        Check_Country()
        Reset()
        """Test Case 22: Verify “Shipper Jurisdiction Country” Filter Displays Relevant Data"""
        print("🔍 Running TC22: Verify “Shipper Jurisdiction Country” Filter Displays Relevant Data")
        shipper_page.open_shipper_dropdown()
        shipper_page.Shipper_Juridiction_option()
        shipper_page.Shipper_Country_Filter_Search(country)
        shipper_page.Shipper_Country_Apply_Filter()
        shipper_page.Validate_ShipmentRecord_Count()
        shipper_page.Validate_Total_RecordCount_In_the_Table()
        shipper_page.Validate_S_S_Name_label()
        shipper_page.Validate_Exporter_Tab()
        shipper_page.validate_duplicate_company_names()
        shipper_page.check_Shipper_Juridiction_Filter()
        Reset()

    def test_Trademo_IndiaTC23(self, browser_setup, shipper_page_and_data, Reset_Default_view, Close_modal, Reset,Check_Country):
        shipper_page, S_S_Name, Partial_S_S_Name, S_Name, country,shipper_type = shipper_page_and_data  # fixed unpacking
        Check_Country()
        Reset()
        """Test Case 23: Verify “Shipper Type” Filter Displays Relevant Data"""
        print("🔍 Running TC23: Verify “Shipper Type” Filter Displays Relevant Data")
        shipper_page.open_shipper_dropdown()
        shipper_page.Click_ShipperType_Option()
        shipper_page.Shipper_Filter_Search(shipper_type)
        shipper_page.Apply_Filter_Functionality()
        shipper_page.Validate_ShipmentRecord_Count()
        shipper_page.Validate_Total_RecordCount_In_the_Table()
        shipper_page.Validate_S_S_Name_label()
        shipper_page.Validate_Exporter_Tab()
        shipper_page.check_Shipper_Type_inthgrid_view()
        Reset()

    def test_Trademo_IndiaTC24(self, browser_setup, shipper_page_and_data, Reset_Default_view, Close_modal, Reset,Check_Country):
        shipper_page, S_S_Name, Partial_S_S_Name, S_Name,country,shipper_type = shipper_page_and_data  # fixed unpacking
        Check_Country()
        Reset()
        """Test Case 24: Verify “Country of Export” Filter Displays Relevant Data"""
        print("🔍 Running TC24: Verify “Country of Export” Filter Displays Relevant Data")
        shipper_page.open_shipper_dropdown()
        shipper_page.Country_of_Export_Option()
        shipper_page.Shipper_Country_Filter_Search(country)
        shipper_page.Shipper_Country_Apply_Filter()
        shipper_page.Validate_ShipmentRecord_Count()
        shipper_page.Validate_Total_RecordCount_In_the_Table()
        shipper_page.Validate_S_S_Name_label()
        shipper_page.Validate_Exporter_Tab()
        shipper_page.check_country_of_export_inthegrid_view()
        Reset()

    def test_Trademo_IndiaTC25(self, browser_setup, shipper_page_and_data, Reset_Default_view, Close_modal, Reset,Check_Country):
        shipper_page, S_S_Name, Partial_S_S_Name, S_Name,country,shipper_type = shipper_page_and_data  # fixed unpacking
        Check_Country()
        Reset()
        """Test Case 25: Verify “Country of Origin” Filter Displays Relevant Data"""
        print("🔍 Running TC25: Verify “Country of Origin” Filter Displays Relevant Data")
        shipper_page.open_shipper_dropdown()
        shipper_page.Country_of_Export_Option()
        shipper_page.Shipper_Country_Filter_Search(country)
        shipper_page.Shipper_Country_Apply_Filter()
        shipper_page.Validate_ShipmentRecord_Count()
        shipper_page.Validate_Total_RecordCount_In_the_Table()
        shipper_page.Validate_S_S_Name_label()
        shipper_page.Validate_Exporter_Tab()
        shipper_page.check_country_of_origin_inthegrid_view()
        Reset()













