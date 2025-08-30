import csv
import os
import sys
import pytest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pages.Port_page import PortFilter

def read_csv():
    """Read all rows from CSV and return a list of dicts"""
    with open('./test_data/Port_Filter.csv', mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        return list(reader)  # ✅ return all rows

# ---- Parameterize using pytest ----
@pytest.fixture(params=read_csv())
def csv_data(request):
    """Yield one row of CSV data per test run."""
    row = request.param
    return {
        "port_lading": row['Port_of_lading'],
        "port_unlading": row['Port_of_unlading'],
    }

@pytest.fixture
def port_page_and_data(browser_setup, csv_data):
    """Provides ShipperFilter instance + data from CSV."""
    page = browser_setup  # browser_setup should return a Page object
    port_page = PortFilter(page)
    yield port_page, csv_data["port_lading"],csv_data["port_unlading"]
    # browser_setup handles cleanup

class TestTrademo:
    """Validating Ports Filter Functionality"""

    def test_Trademo_IndiaTC35(self, browser_setup, port_page_and_data, Reset_Default_view, Close_modal, Reset, Check_Country):
        port_page,port_lading,port_unlading = port_page_and_data  # unpack fixture
        print("🔍 Running TC35: Verify “Port of Lading” Filter Displays Relevant Data")
        Check_Country()
        Reset_Default_view()
        Reset()
        port_page.open_port_dropdown()
        port_page.Click_Port_Lading()
        port_page.Port_Filter_Search(port_lading)
        port_page.Port_Apply_Filter()
        port_page.Validate_ShipmentRecord_Count()
        port_page.Validate_Total_RecordCount_In_the_Table()
        port_page.Validate_C_S_Name_label()
        port_page.check_port_lading_inthe_grid_view()
        Reset()

    def test_Trademo_IndiaTC36(self, browser_setup, port_page_and_data, Reset_Default_view, Close_modal, Reset,
                               Check_Country):
        port_page, port_lading, port_unlading = port_page_and_data  # unpack fixture
        print("🔍 Running TC36: Verify “Port of Unlading” Filter Displays Relevant Data")
        Check_Country()
        Reset_Default_view()
        Reset()
        port_page.open_port_dropdown()
        port_page.Click_Port_UnLading()
        port_page.Port_Filter_Search(port_unlading)
        port_page.Port_Apply_Filter()
        port_page.Validate_ShipmentRecord_Count()
        port_page.Validate_Total_RecordCount_In_the_Table()
        port_page.Validate_C_S_Name_label()
        port_page.check_port_unlading_inthe_grid_view()
        Reset()