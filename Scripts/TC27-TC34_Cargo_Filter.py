import csv
import os
import sys
import pytest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pages.Cargo_page import CargoFilter


def read_csv():
    """Read all rows from CSV and return list of dicts"""
    with open('./test_data/Cargo_filter.csv', mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        return list(reader)   # ✅ return all rows

# ---- Parameterize using pytest ----
@pytest.fixture(params=read_csv())
def csv_data(request):
    """Yield one row of CSV data per test run."""
    row = request.param
    return {
        "product_name": row['Product_Name'],
        "hs_code": row['HS_Code'],
        "hs_code_6": row['HS_Code_6'],
        "min_range": row['Min_range'],
        "max_range": row['Max_range'],
        "unit": row['Quantity_Unit'],
        "quantity": row['Select_Quantity']
    }

@pytest.fixture
def cargo_page_and_data(browser_setup, csv_data):
    """Provides CargoFilter instance + product & HS code from CSV."""
    page = browser_setup  # browser_setup should return a Page object
    cargo_page = CargoFilter(page)
    yield cargo_page, csv_data["product_name"], csv_data["hs_code"] , csv_data["hs_code_6"], csv_data["min_range"], csv_data["max_range"] , csv_data["unit"] ,csv_data['quantity']
    # browser_setup handles cleanup


class TestTrademo:
    """Validating Cargo filter functionality"""

    def test_Trademo_IndiaTC27(self, browser_setup, csv_data,Reset_Default_view,Close_modal,Reset,Check_Country):
        page = browser_setup
        cargo_page = CargoFilter(page)

        print("🔍 Running TC27: Verify the Cargo filter option displays correct data")
        Check_Country()
        cargo_page.verify_Cargo_Filter_Option()

    def test_Trademo_IndiaTC28(self, cargo_page_and_data,browser_setup,Reset_Default_view,Close_modal,Reset,Check_Country):
        cargo_page, product_name, _, _, _, _, _, _= cargo_page_and_data  # ignore HS code here

        print("🔍 Running TC28: Verify Product Category Filter Displays Relevant Data")
        Close_modal()
        Reset()
        Reset_Default_view()
        cargo_page.ProductCategory_Filter()
        cargo_page.Cargo_Filter_Search(product_name)
        cargo_page.Cargo_Apply_Filter()
        cargo_page.Verify_Shipment_Record_count()
        cargo_page.Verify_Product_Label()

    # def test_Trademo_IndiaTC29(self, cargo_page_and_data,browser_setup,Reset_Default_view,Close_modal,Reset,Check_Country):
    #     cargo_page, _, hs_code , _ , _,_,_,_= cargo_page_and_data  # ignore product name here
    #
    #     print("🔍 Running TC29: Verify “HS Code” Filter Displays Relevant Data")
    #     Close_modal()
    #     Check_Country()
    #     Reset()
    #     cargo_page.Verify_HSCode_Filter()
    #     cargo_page.HSCode_Filter_Search(hs_code)
    #     cargo_page.HSCode_Apply_Filter()
    #     cargo_page.Verify_Shipment_Record_count()
    #     cargo_page.Check_CargoFilter_By_HSCode()
    #
    # def test_Trademo_IndiaTC31(self, cargo_page_and_data,browser_setup,Reset_Default_view,Close_modal,Reset,Check_Country):
    #     cargo_page, _, _, hs_code_6, _, _,_,_ = cargo_page_and_data  # ignore product name here
    #
    #     print("🔍 Running TC31: Verify “6 Digit HS Code” Filter Displays Relevant Data")
    #     Close_modal()
    #     Check_Country()
    #     Reset()
    #     cargo_page.Verify_HSCode_6_Filter()
    #     cargo_page.HSCode_6_Filter_Search(hs_code_6)
    #     cargo_page.HSCode_6_Apply_Filter()
    #     cargo_page.Verify_Shipment_Record_count()
    #     cargo_page.Verify_Product_Label()
    #     cargo_page.Check_CargoFilter_By_HSCode()
    #
    # def test_Trademo_IndiaTC32(self, cargo_page_and_data,browser_setup,Reset_Default_view,Close_modal,Reset,Check_Country):
    #     cargo_page, _, _, _, min_range, max_range,_,_ = cargo_page_and_data  # ignore product name here
    #
    #     print("🔍 Running TC32: Verify that the Shipment Value(USD) filters accept a numeric range in the cargo filter")
    #     Close_modal()
    #     Check_Country()
    #     Reset()
    #     cargo_page.Verify_Shipment_Value_Filter()
    #     cargo_page.Shipment_Value_Apply(min_range , max_range)
    #     cargo_page.Validate_Shipment_Value_in_the_grid()
    #
    # def test_Trademo_IndiaTC33(self, cargo_page_and_data,browser_setup,Reset_Default_view,Close_modal,Reset,Check_Country):
    #     cargo_page, _, _, _, min_range, max_range,unit,quantity = cargo_page_and_data  # ignore product name here
    #     print("🔍 Running TC33: Verify Quantity Filter Functionality  in Cargo Filter")
    #     Close_modal()
    #     Check_Country()
    #     Reset()
    #     # cargo_page.Open_Quanity_Filter()
    #     # cargo_page.Verify_Quanity_Units_Search_Filter(unit)
    #     # cargo_page.Quantity_Unit_Apply_Filter()
    #     # cargo_page.Open_Quanity_Filter()
    #     # cargo_page.Verify_Quantity_Unit_Filter_After_Reopen()
    #     # cargo_page.Verify_Shipment_Record_count()
    #     # cargo_page.Verify_Product_Label()
    #     # cargo_page.Validate_Quantity_in_the_grid()
    #     #Qunity Value
    #     cargo_page.Verify_Reset_button()
    #     cargo_page.Open_Quanity_Filter()
    #     cargo_page.Quantity_Value_Apply_Filter(quantity,min_range , max_range)
    #     cargo_page.Verify_Product_Label()
    #     cargo_page.Validate_Quantity_Value_in_the_grid()
    # #
    # def test_Trademo_IndiaTC34(self, cargo_page_and_data,browser_setup,Reset_Default_view,Close_modal,Reset,Check_Country):
    #     cargo_page, _, _, _, min_range, max_range,unit,quantity = cargo_page_and_data  # ignore product name here
    #     print("🔍 Running TC34: Verify the Per Unit Value (USD) filter under the cargo filter funtionality and reflects accurate data in the shipment grid and details view")
    #     Close_modal()
    #     Check_Country()
    #     Reset()
    #     cargo_page.Open_PerUnitUSD_Filter()
    #     cargo_page.PerUnitUSD_Apply_Filter(min_range, max_range, quantity)
    #     cargo_page.Verify_Product_Label()
    #     cargo_page.Validate_Quantity_Per_Unit_in_the_grid()































