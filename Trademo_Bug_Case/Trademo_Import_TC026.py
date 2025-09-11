import csv
import os
import sys
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pages.Search_page import Search


def read_csv(file_path):
    """Read all rows from CSV and return list of dicts safely, including row index."""
    rows = []
    with open(file_path, mode="r", encoding="latin1", errors="replace") as file:
        reader = csv.DictReader(file)
        for i, row in enumerate(reader, start=1):
            cleaned_row = {k.strip(): (v.strip() if v else "") for k, v in row.items()}
            cleaned_row["_index"] = i  # store row index
            rows.append(cleaned_row)
    return rows


def merge_data(search_rows, login_rows):
    """Combine search data with login rows, ensuring Imports batch runs before Exports."""
    merged = []

    # First run all Imports
    for l_row in login_rows:
        if l_row.get("source_type", "").lower() == "imports":
            for s_row in search_rows:
                combined = {**s_row, **l_row}
                merged.append(combined)

    # Then run all Exports
    for l_row in login_rows:
        if l_row.get("source_type", "").lower() == "exports":
            for s_row in search_rows:
                combined = {**s_row, **l_row}
                merged.append(combined)

    return merged


# --- Load CSV files ---
AUTO_FILE = "./test_data/Search_AutoSuggest.csv"
MANUAL_FILE = "./test_data/Search_ManualSuggest.csv"
LOGIN_FILE = "./test_data/login.csv"

AUTO_DATA = read_csv(AUTO_FILE)
MANUAL_DATA = read_csv(MANUAL_FILE)
LOGIN_DATA = read_csv(LOGIN_FILE)

AUTO_COMBINED = merge_data(AUTO_DATA, LOGIN_DATA)
MANUAL_COMBINED = merge_data(MANUAL_DATA, LOGIN_DATA)


@pytest.fixture(
    params=AUTO_COMBINED,
    ids=lambda row: f"AUTO-{row.get('country','NA')}-{row.get('source_type','NA')}-{row.get('hs_code','NA')}"
)
def auto_suggest_data(request, browser_setup):
    csv_data = request.param
    page = browser_setup
    search_page = Search(page)
    yield (
        search_page,
        csv_data.get("hs_code", ""),
        csv_data.get("product_name", ""),
        csv_data.get("shipper_name", ""),
        csv_data.get("consignee_name", ""),
        csv_data.get("chemical_name", ""),
        csv_data.get("port_name", ""),
        csv_data["_index"],              # row index from search file
        len(AUTO_DATA),                  # total rows in AutoSuggest
        csv_data.get("country", ""),     # from login.csv
        csv_data.get("source_type", "")  # from login.csv
    )


@pytest.fixture(
    params=MANUAL_COMBINED,
    ids=lambda row: f"MANUAL-{row.get('country','NA')}-{row.get('source_type','NA')}-{row.get('hs_code','NA')}"
)
def manual_suggest_data(request, browser_setup):
    csv_data = request.param
    page = browser_setup
    search_page = Search(page)
    yield (
        search_page,
        csv_data.get("hs_code", ""),
        csv_data.get("product_name", ""),
        csv_data.get("shipper_name", ""),
        csv_data.get("consignee_name", ""),
        csv_data.get("chemical_name", ""),
        csv_data.get("port_name", ""),
        csv_data["_index"],              # row index from search file
        len(MANUAL_DATA),                # total rows in ManualSuggest
        csv_data.get("country", ""),     # from login.csv
        csv_data.get("source_type", "")  # from login.csv
    )


class TestTrademo:
    """Validating Search functionality"""

    def test_Auto_select_options(self, auto_suggest_data, Check_Country, Reset):
        (search_page, hs_code, product_name, shipper_name, consignee_name,
         chemical_name, port_name, row_index, total_count,
         country, source_type) = auto_suggest_data

        Reset()
        Check_Country(country, source_type)   # ✅ pass values from login.csv
        search_page.Close_button()
        search_page.auto_suggest_hs_code_search(hs_code)
        search_page.check_hs_code_in_shipmentgrid()
        search_page.Validate_Discover_Insights()

        print(f"✅ [{row_index}/{total_count}] ({country}-{source_type}) HS Code search test completed for: {hs_code}")




        # Reset()
        # search_page.Close_button()
        # search_page.auto_suggest_product_search(product_name)
        # search_page.check_product_description_in_shipment_grid()
        # print(f"✅ [{row_index}/{total_count}] Product search test completed for: {product_name}")

        # Reset()
        # search_page.Close_button()
        # search_page.auto_suggest_shipper_search(shipper_name)
        # search_page.Validate_Discover_insight_link()
        # search_page.check_Shipper_Name_in_theGrid_View()
        # print(f"✅ [{row_index}/{total_count}] Shipper search test completed for: {shipper_name}")

        # Reset()
        # search_page.Close_button()
        # search_page.auto_suggest_consignee_search(consignee_name)
        # search_page.Validate_Discover_insight_consignee()
        # search_page.check_consignee_in_shipmentgrid()
        # print(f"✅ [{row_index}/{total_count}] Consignee search test completed for: {consignee_name}")

        # Reset()
        # search_page.Close_button()
        # search_page.Chemical_Search_auto_suggest(chemical_name)
        # search_page.Check_Chemical_In_shipmentGrid()
        # print(f"✅ [{row_index}/{total_count}] Chemical search test completed for: {chemical_name}")
        #
        # Reset()
        # search_page.Close_button()
        # search_page.auto_suggest_search_port(port_name)
        # search_page.Check_Port_description_Shipment_Grid()
        # search_page.Validate_Discover_insight_ports()
        # print(f"✅ [{row_index}/{total_count}] Port search test completed for: {port_name}")
    #
    # def test_Manual_select_option(self, manual_suggest_data, Reset):
    #     (search_page, hs_code, product_name, shipper_name, consignee_name,
    #      chemical_name, port_name, row_index, total_count) = manual_suggest_data
    #
    #     print(f"🔍 [{row_index}/{total_count}] Verify manual search functionality")
    #
    #     Reset()
    #     search_page.Close_button()
    #     search_page.Search_product_manualsuggest(product_name)
    #     search_page.Verify_Shipment_tab_Manual_suggest(product_name)
    #     print(f"✅ [{row_index}/{total_count}] Manual Product search test completed for: {product_name}")
    #
    #     Reset()
    #     search_page.Close_button()
    #     search_page.Manual_suggest_hs_code(hs_code)
    #     search_page.Verify_Shipment_tab_Manual_suggest(hs_code)
    #     print(f"✅ [{row_index}/{total_count}] Manual HS Code search test completed for: {hs_code}")
    #
    #     Reset()
    #     search_page.Close_button()
    #     search_page.Manual_suggest_shipper(shipper_name)
    #     search_page.Verify_Shipment_tab_Manual_suggest(shipper_name)
    #     print(f"✅ [{row_index}/{total_count}] Manual shipper name search test completed for: {shipper_name}")
    #
    #     Reset()
    #     search_page.Close_button()
    #     search_page.Manual_suggest_consignee(consignee_name)
    #     search_page.Verify_Shipment_tab_Manual_suggest(consignee_name)
    #     print(f"✅ [{row_index}/{total_count}] Manual consignee search test completed for: {consignee_name}")
    #
    #     Reset()
    #     search_page.Close_button()
    #     search_page.Manual_suggest_chemical(chemical_name)
    #     search_page.Verify_Shipment_tab_Manual_suggest(chemical_name)
    #     print(f"✅ [{row_index}/{total_count}] Manual chemical search test completed for: {chemical_name}")
    #
    #     Reset()
    #     search_page.Close_button()
    #     search_page.Manual_suggest_port(port_name)
    #     search_page.Verify_Shipment_tab_Manual_suggest(port_name)
    #     print(f"✅ [{row_index}/{total_count}] Manual port search test completed for: {port_name}")