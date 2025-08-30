import csv
import os
import sys
import pytest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pages.customs_page import CustomsFilter

def read_csv():
    """Read all rows from CSV and return a list of dicts"""
    with open('./test_data/Customs_Details_Filter.csv', mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        return list(reader)  # ✅ return all rows

# ---- Parameterize using pytest ----
@pytest.fixture(params=read_csv())
def csv_data(request):
    """Yield one row of CSV data per test run."""
    row = request.param
    return {
        "custom_house_agent": row['Customs_House_Agent_Name'],
    }

@pytest.fixture
def customs_page_and_data(browser_setup, csv_data):
    """Provides ShipperFilter instance + data from CSV."""
    page = browser_setup  # browser_setup should return a Page object
    customs_page = CustomsFilter(page)
    yield customs_page, csv_data["custom_house_agent"]
    # browser_setup handles cleanup

class TestTrademo:
    """Validating Ports Filter Functionality"""

    def test_Trademo_IndiaTC38(self, browser_setup, customs_page_and_data, Reset_Default_view, Close_modal, Reset, Check_Country):
        freight_page,custom_house_agent = customs_page_and_data
        print("🔍 Running TC38: Verify Custom Details  filter and details consistency in shipment and view details")
        Check_Country()
        Reset_Default_view()
        Reset()
        freight_page.open_customs_dropdown()
        freight_page.Click_Customs_House_Agent_Name()
        freight_page.Customs_Filter_Search(custom_house_agent)
        freight_page.Apply_Filter_Functionality()
        freight_page.Validate_ShipmentRecord_Count()
        freight_page.Validate_Total_RecordCount_In_the_Table()
        freight_page.Validate_Customs_Name_label()
        freight_page.check_customs_house_agent_inthegrid_view()
        Reset()