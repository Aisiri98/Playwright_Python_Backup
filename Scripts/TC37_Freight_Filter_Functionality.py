import csv
import os
import sys
import pytest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pages.Freight_page import FrieghtFilter

def read_csv():
    """Read all rows from CSV and return a list of dicts"""
    with open('./test_data/Freight_Filter.csv', mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        return list(reader)  # ✅ return all rows

# ---- Parameterize using pytest ----
@pytest.fixture(params=read_csv())
def csv_data(request):
    """Yield one row of CSV data per test run."""
    row = request.param
    return {
        "mode_transportation": row['Mode_of_Transportation'],
    }

@pytest.fixture
def freight_page_and_data(browser_setup, csv_data):
    """Provides ShipperFilter instance + data from CSV."""
    page = browser_setup  # browser_setup should return a Page object
    freight_page = FrieghtFilter(page)
    yield freight_page, csv_data["mode_transportation"]
    # browser_setup handles cleanup

class TestTrademo:
    """Validating Ports Filter Functionality"""

    def test_Trademo_IndiaTC37(self, browser_setup, freight_page_and_data, Reset_Default_view, Close_modal, Reset, Check_Country):
        freight_page,mode_transportation = freight_page_and_data  # unpack fixture
        print("🔍 Running TC37: Verify that the Freight filter allows users to filter shipments based on freight-related options")
        Check_Country()
        Reset_Default_view()
        Reset()
        freight_page.open_freight_dropdown()
        freight_page.Click_Mode_of_Transportation()
        freight_page.validate_freight_type_checkboxes()
        freight_page.Freight_Filter_Search(mode_transportation)
        freight_page.Apply_Filter_Functionality()
        freight_page.Validate_ShipmentRecord_Count()
        freight_page.Validate_Total_RecordCount_In_the_Table()
        freight_page.Validate_Freight_Name_label()
        freight_page.check_mode_of_transport_inthe_grid_view()
        freight_page.open_freight_dropdown()
        freight_page.Click_Mode_of_Transportation()
        freight_page.Apply_filter_Exclude()
        freight_page.check_mode_of_transport_exclude_inthe_grid_view()
        Reset()