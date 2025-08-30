import allure
import pytest
from playwright.sync_api import sync_playwright, expect
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pages.page1 import TrademoPlatform


def load_CSV_data(file_path='./test_data/data.csv'):
    import csv
    with open(file_path, mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        first_row = next(reader)
        print("Loaded row:", first_row)
        return first_row['email'], first_row['password']

@pytest.fixture(scope="class")
def browser_setup(request):
    """Setup browser and page for all tests in the class"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            record_video_dir="videos/",
            viewport={"width": 1280, "height": 720}
        )
        page = context.new_page()
        trademo_page = TrademoPlatform(page)

        # Attach to the test class
        request.cls.page = page
        request.cls.context = context
        request.cls.trademo_page = trademo_page

        # Login once here
        email, password = load_CSV_data()
        trademo_page.Launch_Application()
        trademo_page.fill_email(email)
        trademo_page.fill_password(password)
        trademo_page.click_sign_in()
        trademo_page.wait_for_page_load()
        if trademo_page.is_saved_searches_visible():
            user_avatar = trademo_page.get_user_avatar()
            expect(user_avatar).to_be_visible()
        else:
            trademo_page.handle_password_refill(password)
            if trademo_page.handle_session_confirmation():
                user_avatar = trademo_page.get_user_avatar()
                expect(user_avatar).to_be_visible()
                trademo_page.wait_for_page_load()
            else:
                print('No active session found')
                trademo_page.click_submit_sign_in()

        yield trademo_page

        video_path = page.video.path()
        page.close()
        context.close()
        browser.close()
        if os.path.exists(video_path):
            allure.attach.file(video_path, name="Test Video", attachment_type=allure.attachment_type.MP4)

@pytest.mark.usefixtures("browser_setup")
class TestTrademo:
    """Test class for Trademo platform functionality"""

    def test_01_verify_autosuggest_search_functionality(self):
        """Test Case 1: Verify autosuggest search functionality with pagination"""
        print("🔍 Running TC01: Verify autosuggest search functionality")
        trademo_page = self.trademo_page

        # Search valid HS Code
        trademo_page.click_search_all()
        trademo_page.select_hs_code_search()
        trademo_page.fill_hs_code_search("392330")
        trademo_page.select_hs_code_suggestion()
        trademo_page.press_enter_on_search()
        trademo_page.verify_hs_code_visible()
        trademo_page.click_discover_insights()

        # Click on Shipment
        trademo_page.click_shipment_tab()

        expected_prefix = "392330"

        # Check if HS Code is visible on all the records in the page
        trademo_page.Record_Count()
        trademo_page.check_hs_codes_on_page(expected_prefix)
        # Print invalid entries
        trademo_page.print_invalid_entries()

    def test_03_verify_shipper_name(self):
        """Test Case 3: Verify shipper name consistency"""
        print("🚢 Running TC03: Verify shipper name")
        trademo_page = self.trademo_page
        # Click on Shipment tab
        shipment_tab = trademo_page.wait_for_shipment_tab_visible()
        shipment_tab.click()

        # Extract the shipper name from the Shipment tab
        shipper_link = trademo_page.get_shipper_link()
        shipper_name_page1 = shipper_link.inner_text()
        print(" Shipper Name on Page 1:", shipper_name_page1)

        # Click on the shipper name
        shipper_link.click()
        trademo_page.wait_for_page_load(10000)

        # Wait for shipper detail page
        shipper_detail_header = trademo_page.get_shipper_detail_header()
        expect(shipper_detail_header).to_be_visible()

        # Get inner text
        shipper_name_page2 = shipper_detail_header.inner_text().strip()
        print("Shipper on page 2:", shipper_name_page2)

        # Compare Shipper names on the two pages
        assert shipper_name_page1 == shipper_name_page2, "❌ Shipper names do not match"
        print("✅ Shipper names matched.")
        trademo_page.click_back_button()

    def test_02_verify_consignee_standardized_name_filter(self):
        """Test Case 2: Verify consignee standardized name filter with pagination"""
        print("👥 Running TC02: Verify consignee standardized name filter")
        trademo_page = self.trademo_page

        # Click on Consignee dropdown
        trademo_page.click_consignee_dropdown()

        # Click on Consignee Standardized Name
        trademo_page.click_consignee_standardized_name()

        # Check any checkbox
        trademo_page.select_first_checkbox()

        # Get any consignee name from the 'Filter by Consignee Standardized Name' filter
        consignee_text = trademo_page.get_consignee_text()
        consignee_record_clean = trademo_page.get_consignee_record_count()

        # Click Apply Filter
        trademo_page.click_apply_filter()

        # Wait for Shipment tab to be visible and click it
        shipment_tab = trademo_page.wait_for_shipment_tab_visible()
        shipment_tab.click()

        # Validate the total shipment record count from 1-10 of X
        total_from_summary = trademo_page.get_total_records_from_table()

        print(f"Total shipment Record count: {total_from_summary}")
        assert total_from_summary == consignee_record_clean, "Record count mismatch!"

        # Check if the consignee name is showing correct in all the records
        trademo_page.Record_Count()
        trademo_page.check_consignee(consignee_text)
        trademo_page.click_back_button()

    def test_04_validate_commas_in_shipment_value(self):
        """Test Case 4: Validate commas in shipment value with pagination"""
        print("💰 Running TC04: Validate commas in shipment value")
        trademo_page = self.trademo_page
        # Click on Shipment tab
        shipment_tab = trademo_page.wait_for_shipment_tab_visible()
        shipment_tab.click()
        # Check for the commas in all the shipment records
        trademo_page.Record_Count()
        trademo_page.Validate_Commas_In_shipment_value()

    def test_05_validate_shipment_value_zero(self):
        """Test Case 5: Validate shipment value is zero with pagination"""
        print("🔍 Running TC05: Validate shipment value is zero")
        trademo_page = self.trademo_page

        # Wait for and click Shipment tab
        shipment_tab = trademo_page.wait_for_shipment_tab_visible(10000)
        shipment_tab.click()

        # Click Cargo dropdown
        trademo_page.click_cargo_dropdown()

        # Click on "Shipment Value (USD)"
        trademo_page.click_shipment_value_usd()

        # Ensure Filter modal title appears
        trademo_page.verify_filter_title()

        # Clear Maximum Range field and type 0
        trademo_page.set_max_range_to_zero()

        # Click Apply Filter button
        trademo_page.click_apply_filter()

        # Verify that shipment value is showing zero for all the records
        trademo_page.Record_Count()
        trademo_page.check_zero_shipment()
        print("\n🎉 All test cases completed successfully!")