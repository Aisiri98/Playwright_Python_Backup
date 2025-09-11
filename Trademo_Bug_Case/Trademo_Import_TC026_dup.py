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
            cleaned_row["_index"] = i  # store row index for reporting
            rows.append(cleaned_row)
    print(f"📄 Loaded {len(rows)} row(s) from {file_path}")
    return rows


def merge_data(search_rows, login_rows, filter_source=None, limit_first=False):
    """
    Combine search data with login rows, ensuring Imports batch runs before Exports.
    filter_source: 'imports' | 'exports' | None (run all)
    limit_first: if True, only return first merged row (useful for debugging).
    """
    merged = []
    for source in ("imports", "exports"):
        for l_row in login_rows:
            if l_row.get("source_type", "").lower() == source:
                if filter_source and filter_source.lower() != source:
                    continue  # skip if not matching filter
                for s_row in search_rows:
                    combined = {**s_row, **l_row}
                    merged.append(combined)

    if limit_first and merged:
        merged = [merged[0]]  # only keep first row

    print(f"✅ Merged {len(merged)} rows (filter_source={filter_source}, limit_first={limit_first})")
    return merged


# --- Load CSV files ---
AUTO_FILE = "./test_data/Search_AutoSuggest.csv"
MANUAL_FILE = "./test_data/Search_ManualSuggest.csv"
LOGIN_FILE = "./test_data/login.csv"

AUTO_DATA = read_csv(AUTO_FILE)
MANUAL_DATA = read_csv(MANUAL_FILE)
LOGIN_DATA = read_csv(LOGIN_FILE)

# ✅ You can control what gets merged here:
AUTO_COMBINED = merge_data(AUTO_DATA, LOGIN_DATA, filter_source=None, limit_first=False)
MANUAL_COMBINED = merge_data(MANUAL_DATA, LOGIN_DATA, filter_source=None, limit_first=False)


@pytest.fixture(
    params=AUTO_COMBINED,
    ids=lambda row: f"AUTO-{row.get('country','NA')}-{row.get('source_type','NA')}-{row.get('hs_code','NA')}"
)
def auto_suggest_data(request, browser_setup):
    """Fixture for auto-suggest search data."""
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
        len(AUTO_COMBINED),              # total merged rows for auto-suggest
        csv_data.get("country", ""),     # from login.csv
        csv_data.get("source_type", "")  # from login.csv
    )


@pytest.fixture(
    params=MANUAL_COMBINED,
    ids=lambda row: f"MANUAL-{row.get('country','NA')}-{row.get('source_type','NA')}-{row.get('hs_code','NA')}"
)
def manual_suggest_data(request, browser_setup):
    """Fixture for manual search data."""
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
        len(MANUAL_COMBINED),            # total merged rows for manual-suggest
        csv_data.get("country", ""),     # from login.csv
        csv_data.get("source_type", "")  # from login.csv
    )

@pytest.mark.describe("AutoSelect Tests")
class TestAutoSelect:
    """Validating Search functionality"""

    def test_auto_select_options_hs_code(self, auto_suggest_data, Check_Country, Reset):
        (search_page, hs_code, product_name, shipper_name, consignee_name,
         chemical_name, port_name, row_index, total_count,
         country, source_type) = auto_suggest_data

        Reset()
        Check_Country(country, source_type)
        search_page.Close_button()
        search_page.auto_suggest_hs_code_search(hs_code)
        search_page.check_hs_code_in_shipmentgrid()
        search_page.Validate_Discover_Insights()

        print(f"✅ {row_index} ({country}-{source_type}) HS Code search test completed for: {hs_code}")

    def test_auto_select_options_product(self, auto_suggest_data, Check_Country, Reset):
        (search_page, hs_code, product_name, shipper_name, consignee_name,
         chemical_name, port_name, row_index, total_count,
         country, source_type) = auto_suggest_data

        Reset()
        Check_Country(country, source_type)
        search_page.Close_button()
        search_page.auto_suggest_product_search(product_name)
        search_page.check_product_description_in_shipment_grid()

        print(f"✅ {row_index} Product search test completed for: {product_name}")

    def test_auto_select_options_shipper(self, auto_suggest_data, Check_Country, Reset):
        (search_page, hs_code, product_name, shipper_name, consignee_name,
         chemical_name, port_name, row_index, total_count,
         country, source_type) = auto_suggest_data

        Reset()
        Check_Country(country, source_type)
        search_page.Close_button()
        search_page.auto_suggest_shipper_search(shipper_name)
        search_page.Validate_Discover_insight_link()
        search_page.check_Shipper_Name_in_theGrid_View()

        print(f"✅ {row_index} Shipper search test completed for: {shipper_name}")

    def test_auto_select_options_consignee(self, auto_suggest_data, Check_Country, Reset):
        (search_page, hs_code, product_name, shipper_name, consignee_name,
         chemical_name, port_name, row_index, total_count,
         country, source_type) = auto_suggest_data

        Reset()
        Check_Country(country, source_type)
        search_page.Close_button()
        search_page.auto_suggest_consignee_search(consignee_name)
        search_page.Validate_Discover_insight_consignee()
        search_page.check_consignee_in_shipmentgrid()
        print(f"✅ {row_index} Consignee search test completed for: {consignee_name}")

    def test_auto_select_options_chemical(self, auto_suggest_data, Check_Country, Reset):
        (search_page, hs_code, product_name, shipper_name, consignee_name,
         chemical_name, port_name, row_index, total_count,
         country, source_type) = auto_suggest_data

        Reset()
        Check_Country(country, source_type)
        search_page.Close_button()
        search_page.Chemical_Search_auto_suggest(chemical_name)
        search_page.Check_Chemical_In_shipmentGrid()

        print(f"✅ {row_index} Chemical search test completed for: {chemical_name}")

    def test_auto_select_options_port(self, browser_setup,auto_suggest_data, Check_Country, Reset):
        (search_page, hs_code, product_name, shipper_name, consignee_name,
         chemical_name, port_name, row_index, total_count,
         country, source_type) = auto_suggest_data

        Reset()
        Check_Country(country, source_type)
        search_page.Close_button()
        search_page.auto_suggest_search_port(port_name)
        search_page.Check_Port_description_Shipment_Grid()
        search_page.Validate_Discover_insight_ports()

        print(f"✅ {row_index} Port search test completed for: {port_name}")


@pytest.mark.describe("Manual Search Tests")
class TestManual:
    """Validating Manual Search functionality"""

    def test_manual_search_product(self, manual_suggest_data, Reset,Check_Country):
        (search_page, hs_code, product_name, shipper_name, consignee_name,
         chemical_name, port_name, row_index, total_count, country, source_type) = manual_suggest_data

        print(f"🔍 {row_index} Verify manual search functionality")

        # Product search
        Reset()
        Check_Country(country, source_type)
        search_page.Close_button()
        search_page.Search_product_manualsuggest(product_name)
        search_page.Verify_Shipment_tab_Manual_suggest(product_name)
        print(f"✅ {row_index} Manual Product search test completed for: {product_name}")

    def test_manual_search_hscode(self, manual_suggest_data, Reset, Check_Country):
        (search_page, hs_code, product_name, shipper_name, consignee_name,
         chemical_name, port_name, row_index, total_count, country, source_type) = manual_suggest_data

        # HS Code search
        Reset()
        Check_Country(country, source_type)
        search_page.Close_button()
        search_page.Manual_suggest_hs_code(hs_code)
        search_page.Verify_Shipment_tab_Manual_suggest(hs_code)
        print(f"✅ {row_index} Manual HS Code search test completed for: {hs_code}")

    def test_manual_search_shipper(self, manual_suggest_data, Reset, Check_Country):
        (search_page, hs_code, product_name, shipper_name, consignee_name,
         chemical_name, port_name, row_index, total_count, country, source_type) = manual_suggest_data

        # Shipper search
        Reset()
        Check_Country(country, source_type)
        search_page.Close_button()
        search_page.Manual_suggest_shipper(shipper_name)
        search_page.Verify_Shipment_tab_Manual_suggest(shipper_name)
        print(f"✅ {row_index} Manual shipper name search test completed for: {shipper_name}")

    def test_manual_search_consignee(self, manual_suggest_data, Reset, Check_Country):
        (search_page, hs_code, product_name, shipper_name, consignee_name,
         chemical_name, port_name, row_index, total_count, country, source_type) = manual_suggest_data
        # Consignee search
        Reset()
        Check_Country(country, source_type)
        search_page.Close_button()
        search_page.Manual_suggest_consignee(consignee_name)
        search_page.Verify_Shipment_tab_Manual_suggest(consignee_name)
        print(f"✅ {row_index} Manual consignee search test completed for: {consignee_name}")

    def test_manual_search_chemical(self, manual_suggest_data, Reset, Check_Country):
        (search_page, hs_code, product_name, shipper_name, consignee_name,
         chemical_name, port_name, row_index, total_count, country, source_type) = manual_suggest_data
        # Chemical search
        Reset()
        Check_Country(country, source_type)
        search_page.Close_button()
        search_page.Manual_suggest_chemical(chemical_name)
        search_page.Verify_Shipment_tab_Manual_suggest(chemical_name)
        print(f"✅ {row_index} Manual chemical search test completed for: {chemical_name}")

    def test_manual_search_port(self, manual_suggest_data, Reset, Check_Country):
        (search_page, hs_code, product_name, shipper_name, consignee_name,
         chemical_name, port_name, row_index, total_count, country, source_type) = manual_suggest_data
        # Port search
        Reset()
        Check_Country(country, source_type)
        search_page.Close_button()
        search_page.Manual_suggest_port(port_name)
        search_page.Verify_Shipment_tab_Manual_suggest(port_name)
        print(f"✅ {row_index} Manual port search test completed for: {port_name}")