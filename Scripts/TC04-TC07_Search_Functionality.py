import csv
import os
import sys
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pages.Search_page import Search


def read_csv():
    """Read all rows from CSV and return list of dicts"""
    with open('./test_data/Search.csv', mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        return list(reader)   # ✅ return all rows


# ---- Parameterize using pytest ----
@pytest.fixture(params=read_csv())
def csv_data(request):
    """Yield one row of CSV data per test run."""
    row = request.param
    return {
        "hs_code": row['HS_Code'],
        "product_name": row['Product_name'],
        "shipper_name": row['Shipper_name'],
        "consignee_name": row['Consignee_name'],
        "chemical_name": row['Chemical_name'],
        "port_name": row['Port_name'],
        "file_name1": row['file_name1'],
        "file_name2": row['file_name2'],
        "file_name3": row['file_name3'],
        "file_name4": row['file_name4'],
        "file_name5": row['file_name5'],
        "file_name6": row['file_name6'],
        "file_name7": row['file_name7'],
        "file_name8": row['file_name8'],
        "file_name9": row['file_name9'],
        "file_name10": row['file_name10'],
        "file_name11": row['file_name11'],
        "file_name12": row['file_name12'],
    }


@pytest.fixture
def Search_page_and_data(browser_setup, csv_data):
    """Provides Search instance + data from CSV row."""
    page = browser_setup
    search_page = Search(page)
    yield (
        search_page,
        csv_data["hs_code"],
        csv_data["product_name"],
        csv_data["shipper_name"],
        csv_data["consignee_name"],
        csv_data["chemical_name"],
        csv_data["port_name"],
        csv_data["file_name1"],
        csv_data["file_name2"],
        csv_data["file_name3"],
        csv_data["file_name4"],
        csv_data["file_name5"],
        csv_data["file_name6"],
        csv_data["file_name7"],
        csv_data["file_name8"],
        csv_data["file_name9"],
        csv_data["file_name10"],
        csv_data["file_name11"],
        csv_data["file_name12"],
    )

class TestTrademo:
    """Validating Search functionality"""
    # def test_Trademo_IndiaTC04(self, browser_setup, Search_page_and_data, Check_Country, Reset):
    #     (search_page, hs_code, product_name, shipper_name, consignee_name,
    #      chemical_name, port_name, file_name1, file_name2, file_name3,
    #      file_name4, file_name5, file_name6, *_) = Search_page_and_data
    #
    #     Reset()
    #     Check_Country()

        # search_page.auto_suggest_hs_code_search(hs_code)
        # search_page.check_hs_code_in_shipmentgrid()
        # search_page.Validate_Discover_Insights()
        # print(f"✅ HS Code search test completed for: {hs_code}")

        # Reset()
        # search_page.auto_suggest_product_search(product_name)
        # search_page.check_product_description_in_shipment_grid()
        # print(f"✅ Product search test completed for: {product_name}")
        #
        # Reset()
        # search_page.auto_suggest_shipper_search(shipper_name)
        # search_page.Validate_exporter_tab()
        # search_page.check_shipper_name_export_tab()
        # search_page.Validate_Discover_insight_link()
        # search_page.validate_duplicate_country_names()
        # search_page.check_Shipper_Name_in_theGrid_View()
        # print(f"✅ Shipper search test completed for: {shipper_name}")

        # Reset()
        # search_page.auto_suggest_consignee_search(consignee_name)
        # search_page.Validate_importer_tab()
        # search_page.check_consignee_Name_Import_tab()
        # search_page.Validate_Discover_insight_consignee()
        # search_page.validate_duplicate_country_names()
        # search_page.check_Consignee_Name_in_theGrid_View()
        # print(f"✅ Consignee search test completed for: {consignee_name}")

        # Reset()
        # search_page.Chemical_Search_auto_suggest(chemical_name)
        # search_page.Check_Chemical_In_shipmentGrid()
        # print(f"✅ Chemical search test completed for: {chemical_name}")

        # Reset()
        # search_page.auto_suggest_search_port(port_name)
        # search_page.Check_Port_description_Shipment_Grid()
        # search_page.Validate_Discover_insight_ports()
        # print(f"✅ Port search test completed for: {port_name}")

    def test_Trademo_IndiaTC05(self, browser_setup, Search_page_and_data, Reset):
        (search_page, hs_code, product_name, shipper_name, consignee_name,
         chemical_name, port_name, *_) = Search_page_and_data

        # print("🔍 Running TC05: Verify manual search functionality")
        # Reset()
        # search_page.Search_product_manualsuggest(product_name)
        # search_page.Verify_Shipment_tab_Manual_suggest(product_name)
        # print(f"✅ Manual Product search test completed for: {product_name}")
        #
        # Reset()
        # search_page.Manual_suggest_hs_code(hs_code)
        # search_page.Verify_Shipment_tab_Manual_suggest(hs_code)
        # print(f"✅ Manual HS Code search test completed for: {hs_code}")
        #
        # Reset()
        # search_page.Manual_suggest_shipper(shipper_name)
        # search_page.Verify_Shipment_tab_Manual_suggest(shipper_name)
        # print(f"✅ Manual shipper name search test completed for: {shipper_name}")
        #
        # Reset()
        # search_page.Manual_suggest_consignee(consignee_name)
        # search_page.Verify_Shipment_tab_Manual_suggest(consignee_name)
        # print(f"✅ Manual consignee search test completed for: {consignee_name}")

        # Reset()
        # search_page.Manual_suggest_chemical(chemical_name)
        # search_page.Verify_Shipment_tab_Manual_suggest(chemical_name)
        # print(f"✅ Manual consignee search test completed for: {chemical_name}")
        #
        # Reset()
        # search_page.Manual_suggest_port(port_name)
        # search_page.Verify_Shipment_tab_Manual_suggest(port_name)
        # print(f"✅ Manual port search test completed for: {port_name}")

    def test_Trademo_IndiaTC06(self, browser_setup, Search_page_and_data, Reset):
        (search_page, hs_code, product_name, shipper_name, consignee_name,
         chemical_name, port_name,file_name1, file_name2, file_name3,
         file_name4, file_name5, file_name6, file_name7, file_name8, file_name9,
         file_name10, file_name11, file_name12) = Search_page_and_data

        # print("🔍 Running TC06: Verify autosuggest functionality with manual entry")
        # Reset()
        # search_page.auto_suggest_manual_hs_code(hs_code)
        # search_page.check_hs_code_in_shipmentgrid()
        #
        # Reset()
        # search_page.auto_suggest_manual_product(product_name)
        # search_page.check_product_description_in_shipment_grid()
        #
        # Reset()
        # search_page.auto_suggest_manual_shipper(shipper_name)
        # search_page.Validate_exporter_tab()
        # search_page.check_Shipper_Name_in_theGrid_View()
        #
        # Reset()
        # search_page.auto_suggest_manual_consignee(consignee_name)
        # search_page.Validate_importer_tab()
        # search_page.check_Consignee_Name_in_theGrid_View()

        # Reset()
        # search_page.auto_suggest_manual_chemical(chemical_name)
        # search_page.Check_Chemical_In_shipmentGrid()

        Reset()
        search_page.auto_suggest_manual_port(port_name)
        search_page.Check_Port_description_Shipment_Grid()

    # def test_Trademo_IndiaTC07(self, browser_setup, Search_page_and_data, Reset):
    #     search_page, hs_code, *_ = Search_page_and_data
    #     print("🔍 Running TC07: Validate Save Search modal functionality")
    #
    #     Reset()
    #     search_page.auto_suggest_hs_code_search_save_search(hs_code)
    #     search_page.Verify_Save_Search_screen(hs_code)
    #     search_page.Verify_SaveSearch_Cancel_Close()
    #     search_page.Verify_SaveSearch_button()
