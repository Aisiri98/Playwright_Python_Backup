import csv
import os
import sys
import pytest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pages.consignee_page import ConsigneeFilter

def read_csv():
    """Read all rows from CSV and return a list of dicts"""
    with open('./test_data/Consignee_filter.csv', mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        return list(reader)  # ✅ return all rows

# ---- Parameterize using pytest ----
@pytest.fixture(params=read_csv())
def csv_data(request):
    """Yield one row of CSV data per test run."""
    row = request.param
    return {
        "C_S_Name": row['Consignee_Standardized_Name_Search'],
        "Partial_C_S_Name": row['Search_partial_ShipperName'],
        "C_Name": row['Consignee_Name'],
        "country": row['Country'],
        "consignee_type":row["Consignee_Type"],
        "consignee_state":row["Consignee_State"],
        "consignee_city":row["Consignee_City"],
        "consignee_pincode": row["Consignee_Pincode"]
    }

@pytest.fixture
def consignee_page_and_data(browser_setup, csv_data):
    """Provides ShipperFilter instance + data from CSV."""
    page = browser_setup  # browser_setup should return a Page object
    consignee_page = ConsigneeFilter(page)
    yield consignee_page, csv_data["C_S_Name"],csv_data["Partial_C_S_Name"],csv_data["C_Name"],csv_data["country"],csv_data["consignee_type"],csv_data["consignee_state"],csv_data["consignee_city"],csv_data["consignee_pincode"]
    # browser_setup handles cleanup

class TestTrademo:
    """Validating Consignee Filter Functionality"""

    def test_Trademo_IndiaTC09(self, browser_setup, consignee_page_and_data, Reset_Default_view, Close_modal, Reset, Check_Country):
        consignee_page, _,_,_,_,_,consignee_state,consignee_city,consignee_pincode = consignee_page_and_data  # unpack fixture
        print("🔍 Running TC09: Verify the Consignee filter option displays correct data")
        Check_Country()
        Reset_Default_view()
        Reset()
        consignee_page.open_consignee_dropdown()
        consignee_page.check_consignee_filter()

    def test_Trademo_IndiaTC10(self, browser_setup, consignee_page_and_data, Reset_Default_view, Close_modal, Reset,
                               Check_Country):
        consignee_page,C_S_Name,Partial_C_S_Name , _, _, _ ,consignee_state,consignee_city,consignee_pincode= consignee_page_and_data  # unpack fixture

        print("🔍 Running TC10: Verify “Consignee Standardized Name” Filter Displays Relevant Data")
        Close_modal()
        Check_Country()
        Reset()
        consignee_page.open_consignee_dropdown()
        consignee_page.Click_C_SName()
        consignee_page.Consignee_Filter_Search_Company(C_S_Name)
        consignee_page.Apply_Filter_Functionality()
        consignee_page.Validate_ShipmentRecord_Count()
        consignee_page.Validate_Total_RecordCount_In_the_Table()
        consignee_page.Validate_C_S_Name_label()
        consignee_page.Validate_Importer_Tab_Count()
        consignee_page.validate_duplicate_country_names()
        consignee_page.validate_company_names()
        consignee_page.check_Consignee_Standardized_Name_Filter()
        Reset()
        consignee_page.Manual_Search(C_S_Name, Partial_C_S_Name)
        Reset()

    def test_Trademo_IndiaTC11(self, browser_setup, consignee_page_and_data, Reset_Default_view, Close_modal, Reset,
                               Check_Country):
        consignee_page, C_S_Name, Partial_C_S_Name, C_Name, country, consignee_type, consignee_state, consignee_city, consignee_pincode = consignee_page_and_data  # unpack fixture

        print("🔍 Running TC11: Verify “Consignee Name” Filter Displays Relevant Data")
        Close_modal()
        Check_Country()
        Reset()
        consignee_page.open_consignee_dropdown()
        consignee_page.Click_ConsigneeName_Option()
        consignee_page.Consignee_Filter_Search_Company(C_Name)
        consignee_page.Apply_Filter_Functionality()
        consignee_page.Validate_ShipmentRecord_Count()
        consignee_page.Validate_Total_RecordCount_In_the_Table()
        consignee_page.Validate_C_S_Name_label()
        consignee_page.Validate_Importer_Tab_Count()
        consignee_page.validate_duplicate_country_names()
        consignee_page.validate_company_names()
        consignee_page.check_Consignee_Name_intheGrid_View()
        Reset()

    def test_Trademo_IndiaTC12(self, browser_setup, consignee_page_and_data, Reset_Default_view, Close_modal, Reset,
                               Check_Country):
        consignee_page, C_S_Name, Partial_C_S_Name, C_Name,country,consignee_type,consignee_state,consignee_city,consignee_pincode = consignee_page_and_data  # unpack fixture

        print("🔍 Running TC12: Verify “Consignee Jurisdiction Country” Filter Displays Relevant Data")
        Close_modal()
        Check_Country()
        Reset()
        consignee_page.open_consignee_dropdown()
        consignee_page.Consignee_Juridiction_option()
        consignee_page.Consignee_Country_Filter_Search(country)
        consignee_page.Consignee_Country_Apply_Filter()
        consignee_page.Validate_ShipmentRecord_Count()
        consignee_page.Validate_Total_RecordCount_In_the_Table()
        consignee_page.Validate_C_S_Name_label()
        consignee_page.Validate_Importer_Tab_Count()
        consignee_page.validate_duplicate_company_names()
        consignee_page.validate_country_names()
        consignee_page.check_Consignee_Juridiction_Filter()
        Reset()

    def test_Trademo_IndiaTC13(self, browser_setup, consignee_page_and_data, Reset_Default_view, Close_modal, Reset,
                               Check_Country):
        consignee_page, C_S_Name, Partial_C_S_Name, C_Name,country,consignee_type,consignee_state,consignee_city,consignee_pincode = consignee_page_and_data  # unpack fixture

        print("🔍 Running TC13: Verify “Consignee Type” Filter Displays Relevant Data")
        Close_modal()
        Check_Country()
        Reset()
        consignee_page.open_consignee_dropdown()
        consignee_page.Click_ConsigneeType_Option()
        consignee_page.Consignee_Filter_Search_Company(consignee_type)
        consignee_page.Apply_Filter_Functionality()
        consignee_page.Validate_ShipmentRecord_Count()
        consignee_page.Validate_Total_RecordCount_In_the_Table()
        consignee_page.Validate_C_S_Name_label()
        consignee_page.Validate_Importer_Tab_Count()
        consignee_page.check_Consignee_Type_inthegrid_view()
        Reset()

    def test_Trademo_IndiaTC14(self, browser_setup, consignee_page_and_data, Reset_Default_view, Close_modal, Reset,
                               Check_Country):
        consignee_page, C_S_Name, Partial_C_S_Name, C_Name,country,consignee_type,consignee_state,consignee_city,consignee_pincode = consignee_page_and_data  # unpack fixture

        print("🔍 Running TC14: Verify “Country of Import” Filter Displays Relevant Data")
        Close_modal()
        Check_Country()
        Reset()
        Reset_Default_view()
        consignee_page.open_consignee_dropdown()
        consignee_page.Country_of_Import_Option()
        consignee_page.Consignee_Country_Import_Filter_Search(country)
        consignee_page.Consignee_Country_Apply_Filter()
        consignee_page.Validate_ShipmentRecord_Count()
        consignee_page.Validate_Total_RecordCount_In_the_Table()
        consignee_page.Validate_C_S_Name_label()
        consignee_page.Validate_Importer_Tab_Count()
        consignee_page.validate_duplicate_company_names()
        consignee_page.validate_country_names()
        consignee_page.check_country_of_import_inthegrid_view()
        Reset()

    def test_Trademo_IndiaTC15(self, browser_setup, consignee_page_and_data, Reset_Default_view, Close_modal, Reset,
                               Check_Country):
        consignee_page, C_S_Name, Partial_C_S_Name, C_Name,country,consignee_type,consignee_state,consignee_city,consignee_pincode = consignee_page_and_data  # unpack fixture

        print("🔍 Running TC15: Verify “Consignee State” Filter Displays Relevant Data")
        Check_Country()
        Reset()
        Reset_Default_view()
        consignee_page.open_consignee_dropdown()
        consignee_page.Consignee_State_Option()
        consignee_page.Consignee_Country_Filter_Search(consignee_state)
        consignee_page.Consignee_Country_Apply_Filter()
        consignee_page.Validate_ShipmentRecord_Count()
        consignee_page.Validate_Total_RecordCount_In_the_Table()
        consignee_page.Validate_C_S_Name_label()
        consignee_page.check_consignee_state_inthegrid_view()
        Reset()

    def test_Trademo_IndiaTC16(self, browser_setup, consignee_page_and_data, Reset_Default_view, Close_modal, Reset,
                               Check_Country):
        consignee_page, C_S_Name, Partial_C_S_Name, C_Name, country, consignee_type, consignee_state,consignee_city,consignee_pincode = consignee_page_and_data  # unpack fixture

        print("🔍 Running TC16: Verify “Consignee City” Filter Displays Relevant Data")
        Check_Country()
        Reset()
        Reset_Default_view()
        consignee_page.open_consignee_dropdown()
        consignee_page.Consignee_City_Option()
        consignee_page.Consignee_Country_Filter_Search(consignee_city)
        consignee_page.Consignee_Country_Apply_Filter()
        consignee_page.Validate_ShipmentRecord_Count()
        consignee_page.Validate_Total_RecordCount_In_the_Table()
        consignee_page.Validate_C_S_Name_label()
        consignee_page.check_consignee_city_inthegrid_view()
        Reset()

    def test_Trademo_IndiaTC17(self, browser_setup, consignee_page_and_data, Reset_Default_view, Close_modal, Reset,
                               Check_Country):
        consignee_page, C_S_Name, Partial_C_S_Name, C_Name, country, consignee_type, consignee_state,consignee_city,consignee_pincode = consignee_page_and_data  # unpack fixture

        print("🔍 Running TC17: Verify “Consignee Pincode” Filter Displays Relevant Data")
        Check_Country()
        Reset()
        Reset_Default_view()
        consignee_page.open_consignee_dropdown()
        consignee_page.Consignee_Pincode_Option()
        consignee_page.Consignee_Filter_Search_Company(consignee_pincode)
        consignee_page.Apply_Filter_Functionality()
        consignee_page.Validate_ShipmentRecord_Count()
        consignee_page.Validate_Total_RecordCount_In_the_Table()
        consignee_page.Validate_C_S_Name_label()
        consignee_page.check_consignee_pincode_inthegrid_view()
        Reset()
















