import csv
import os
import sys
import pytest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pages.Shipment_page import ShipmentFilter

@pytest.fixture(scope="session")
def csv_data():
    """Read CSV data once per test session."""
    with open('./test_data/Shipment.csv', mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        first_row = next(reader)
        return {
            "To_range1": first_row['To_Range1'],
            "To_range2": first_row['To_Range2'],
            "note": first_row['Note']
        }

@pytest.fixture
def shipment_page_and_data(browser_setup, csv_data):
    """Provides CargoFilter instance + product & HS code from CSV."""
    page = browser_setup  # browser_setup should return a Page object
    shipment_page = ShipmentFilter(page)

    yield shipment_page,csv_data["To_range1"],csv_data["To_range2"], csv_data["note"]
    # browser_setup handles cleanup


class TestTrademo:
    """Test class for Trademo platform functionality"""

    def test_Trademo_IndiaTC45(self, browser_setup):
        page = browser_setup
        shipment_page = ShipmentFilter(page)

        print("🔍 Running TC45: Verify All Shipment Tabs: Shipments, Importers, Exporters, Analytics")
        shipment_page.check_India_import()
        shipment_page.Verify_Reset_button()
        shipment_page.Verify_Shipment_Tab()

    def test_Trademo_IndiaTC46(self, browser_setup):
        page = browser_setup
        shipment_page = ShipmentFilter(page)
        print("🔍 Running TC46: Verify sorting functionality in the Bill of Entry Date and CIF Value (USD) header.")
        shipment_page.check_India_import()
        shipment_page.Sort_Billing_Entry_Column()
        shipment_page.Sort_CIF_Column()

    def test_Trademo_IndiaTC47(self, browser_setup ,shipment_page_and_data ):
        page = browser_setup
        shipment_page, To_range1, To_range2 , note = shipment_page_and_data
        print("🔍 Running TC47: Verify Download Functionality in Shipment Grid")
        shipment_page.check_India_import()
        shipment_page.Validate_Download_Screen()
        shipment_page.Validate_Cancel_Close_button()
        shipment_page.Validate_Download_Screen()
        shipment_page.Validate_Download_All_Column_Shipment(To_range1, To_range2)
        shipment_page.Validate_All_Columns_Download()
        shipment_page.Validate_Download_Screen()
        shipment_page.Validate_Download_GridColumn_Shipment(To_range1, To_range2)
        shipment_page.Validate_Colmn_Shown_In_the_Grid_Download()


    def test_Trademo_IndiaTC48(self, browser_setup):
        page = browser_setup
        shipment_page = ShipmentFilter(page)
        print("🔍 Running TC48: Verify the functionality after selecting checkboxes in the shipment grid")
        shipment_page.check_India_import()
        shipment_page.Validate_Checkbox()

    def test_Trademo_IndiaTC50(self, shipment_page_and_data):
        shipment_page,_, _, note = shipment_page_and_data
        print("🔍 Running TC50: Verify that the shipment detail view displays Bookmark, Download, Close icon, and Take Note section with Add New Note functionality")
        shipment_page.Validate_Bookmark()
        shipment_page.Validate_take_note(note)
        shipment_page.Validate_Download()

    def test_Trademo_IndiaTC51(self, shipment_page_and_data):
        shipment_page,_, _, note = shipment_page_and_data
        print(
            "🔍 Running TC51: Verify ‘Customise Shipment Grid’ Functionality")
        shipment_page.Validate_Customise_Shipment_Grid()
        shipment_page.Validate_Customise_Shipment_Grid_checkbox()
        shipment_page.Validate_Uncheck_check_checkbox()
        shipment_page.Validate_Drag_and_Drop()
        shipment_page.Validate_Reset_default_view()

    def test_Trademo_IndiaTC52(self, shipment_page_and_data):
        shipment_page, *_ = shipment_page_and_data
        print("🔍 Running TC52: Verify that clicking the HS Code hyperlink in the shipment grid navigates to the correct HS Code details page and displays related shipment data")
        #In the shipment grid, click on the HS Code hyperlink
        shipment_page.Validate_HSCode_Hyperlink()

    def test_Trademo_IndiaTC53(self, shipment_page_and_data):
        shipment_page, *_ = shipment_page_and_data
        print(
            "🔍 Running TC53: Verify that clicking the Shipper Name opens the company profile page with detailed tabs, trade overview, and shipment list")
        # In the shipment grid, click on the HS Code hyperlink
        shipment_page.Validate_Shippername_Hyperlink()

    def test_Trademo_IndiaTC54(self, shipment_page_and_data):
        shipment_page, *_ = shipment_page_and_data
        print(
            "🔍 Running TC54: Verify that clicking the Shipper Name opens the company profile page with detailed tabs, trade overview, and shipment list")
        # In the shipment grid, click on the consignee hyperlink
        shipment_page.Validate_Consigneename_Hyperlink()

    def test_Trademo_IndiaTC55(self, shipment_page_and_data):
        shipment_page, *_ = shipment_page_and_data
        print("🔍 Running TC55: Verify that clicking the Port of Lading / Port of Unlading  hyperlink redirects to the Port Profile page with detailed tabs, trade overview, and shipment list")
        # In the shipment grid, click on the port of laiding and unlaiding hyperlink
        shipment_page.Validate_Port_Laiding_Hyperlink()
        shipment_page.Validate_Port_Unlaiding_Hyperlink()

    def test_Trademo_IndiaTC56_49(self, shipment_page_and_data):
        shipment_page, *_ = shipment_page_and_data
        print("🔍 Running TC56: Verify that the Bill of Entry Date is displayed in the correct MMM DD, YYYY format and matches the actual shipment data")
        print("🔍 Running TC49: Verify ‘View Details’ Functionality for a Shipment")
        shipment_page.Validate_Bill_Entry_Data_Column()

    def test_Trademo_IndiaTC57(self, shipment_page_and_data):
        shipment_page, *_ = shipment_page_and_data
        print("🔍 Running TC57: Verify that the Country of Origin, Port of Lading, Shipper Name,Shipper Type, Country of Export, and Shipper Jurisdiction Country in the shipment grid match exactly with the values shown in the “Shipment Origin Details” section of the detailed view")
        labels = ["Country of Origin", "port of lading", "Shipper name","Shipper Type","Country of Export", "Shipper Jurisdiction Coun..."]
        shipment_page.validate_shipment_fields_Shipment_Origin_Details(labels)

    def test_Trademo_IndiaTC58(self, shipment_page_and_data,Reset_Default_view):
        shipment_page, *_ = shipment_page_and_data
        print("🔍 Running TC58: Verify that the Port of Unlading, Consignee Name, Country of Import, Consignee State, Consignee City, Consignee Pincode, and Consignee Jurisdiction Country shown in the shipment grid match exactly with the values displayed in the “Shipment Destination Details” section of the detail view")
        Reset_Default_view()
        labels = ["Port of Unlading", "Consignee Name", "Country of Import", "Consignee State", "Consignee City", "Consignee Pincode",
                  "Consignee Jurisdiction Co..."]
        shipment_page.validate_shipment_fields_Shipment_Destination_Details(labels)

    def test_Trademo_IndiaTC59(self, shipment_page_and_data,Reset_Default_view):
        shipment_page, *_ = shipment_page_and_data
        print("🔍 Running TC59: Verify that the Product Description is present for each shipment and is relevant to the associated HS Code category")
        Reset_Default_view()
        labels = ["Product Description", "HS Code"]
        shipment_page.validate_shipment_fields_HS_Product_Details(labels)

    def test_Trademo_IndiaTC60(self, shipment_page_and_data,Reset_Default_view):
        shipment_page, *_ = shipment_page_and_data
        print("🔍 Running TC60: Verify that the CIF Value, Per unit value, and Quantity value are correctly displayed in the shipment grid and the Cargo section of the shipment details view")
        Reset_Default_view()
        labels = ["Quantity", "CIF Value (USD)", "Per Unit Value (USD)"]
        shipment_page.validate_shipment_fields_Cargo_Details(labels)



































