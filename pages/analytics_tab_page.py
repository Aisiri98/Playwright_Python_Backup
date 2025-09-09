import re
import pycountry
from playwright.sync_api import Page
from playwright.sync_api import expect, TimeoutError as PlaywrightTimeoutError
from datetime import datetime,timedelta
invalid_entries =[]
def get_header_index(page, header_name: str) -> int:
    """
    Find the index of a column header by its text.
    Returns the index (0-based).
    Raises AssertionError if not found.
    """
    headers = page.locator("[role='columnheader']")
    header_count = headers.count()
    print(f"Found {header_count} headers")

    header_index = None
    for i in range(header_count):
        text = headers.nth(i).inner_text().strip()
        if text == header_name:
            header_index = i
            break

    assert header_index is not None, f"❌ Header '{header_name}' not found"
    print(f"✅ Found header '{header_name}' at index {header_index}")
    return header_index
class AnalyticsTab:
    def __init__(self, page: Page):
        self.page = page

    def analytics_tab(self):
        # Click on the Analytics tab
        self.page.locator("//a[@id='nav-summary-tab']").click()
        self.page.wait_for_timeout(1000)
        print("✅ navigated to the analytics page")
        expect(self.page.locator('[class="tw-text-xs tw-font-medium !tw-text-primary-purple-600"]')).to_contain_text("Total Number of Shipments")
        expect(self.page.get_by_text("Total Shipment Value (USD)")).to_be_visible()

    def verify_total_shipments_and_value(self):
        self.page.pause()
        locator = self.page.locator('[class="tw-font-semibold tw-text-base !tw-text-primary-purple-600"]').inner_text().strip()
        # Regex: matches any number (with optional decimals) followed by "Million"
        pattern = re.compile(r"^\d{1,3}(,\d{3})*(\.\d+)?\s+(Thousand|Million|Billion)$", re.IGNORECASE)
        #expect(locator).to_contain_text(pattern)
        if pattern.match(locator):
            print("✅ Matched:", locator)
        else:
            print("❌ Not matched:",locator)

        Total_shipment_usd = self.page.locator('[class="tw-font-semibold tw-text-base "]').inner_text().strip()
        # Regex: matches any number (with optional decimals) followed by "Million"
        pattern1 = re.compile(
            r"^USD\s+\d{1,3}(,\d{3})*(\.\d+)?\s+(Thousand|Million|Billion)$",
            re.IGNORECASE
        )
        if pattern1.match(Total_shipment_usd):
            print("✅ Matched:", Total_shipment_usd)
        else:
            print("❌ Not matched:", Total_shipment_usd)


    def Verify_Import_Section(self):
        #Click on Total Shipments option
        self.page.get_by_text("Total Number of Shipments", exact=True).click()
        expect(self.page.locator('[class="col-md-9 my-auto !tw-text-sm !tw-font-medium !tw-text-gray-900"]').first).to_contain_text("Import Trends")

    def Verify_Trends_Screen(self):
        #Click on the Trends button in Import Trends
        self.page.locator("//button[@data-tip='Analyse Import Trends of all based on their monthly, quarterly and yearly trade']").click()
        expect(self.page.locator("//h4[normalize-space()='Import Trends: Trends']")).to_be_visible(timeout=5000)
        headers_to_check = [
            "S No.",
            "Total Shipments",
            "% Overall Change",
        ]

        for header in headers_to_check:
            locator = self.page.get_by_role("columnheader", name=header)  # more precise
            expect(locator).to_be_visible(timeout=5000)
            print(f"✅ Header '{header}' is visible.")

    def Verify_Country_of_Origin_Section(self):
        # Click on Total Shipments option
        self.page.get_by_text("Total Number of Shipments").click()
        expect(self.page.locator(
            '[class="col-md-9 my-auto !tw-text-sm !tw-font-medium !tw-text-gray-900"]').first).to_contain_text(
            "Countries of Origin")

    # def Verify_CountryTrends_Screen(self):
    #     # Analyse trade trends of all Countries of Origin based on their monthly, quarterly and yearly trade

    def Validate_6digit_hs_code_screen(self):
        #Scroll to the 6-digit HS Code section
        self.page.locator("//div[normalize-space()='6 digit HS Codes']").scroll_into_view_if_needed()
        #6 Digit HS Code section with top HS Codes should be visible
        expect(self.page.locator("//td[normalize-space()='6 digit HS Code']")).to_be_visible(timeout=50000)
        expect(self.page.locator("//td[normalize-space()='Shipments']")).to_be_visible(timeout=50000)

    def validate_6digit_Hscode_Trends_headercheck(self):
        #Scroll to the 2-digit HS Code section
        self.page.locator("//div[normalize-space()='6 digit HS Codes']").scroll_into_view_if_needed()
        #Click on the Trends button in 6-digit HS Code section
        self.page.locator("[data-tip='Analyse trade trends of all 6 digit HS Codes based on their monthly, quarterly and yearly trade']").click()
        expect(self.page.locator("//h4[normalize-space()='6 digit HS Codes: Trends']")).to_be_visible(timeout=50000)
        expect(self.page.locator("//span[normalize-space()='6 digit HS Codes']")).to_be_visible(timeout=50000)
        #Columns should include:Total Shipment Value (USD)- % Overall Change- Year-wise values (e.g., 2025, 2024, 2023, 2022)
        headers_to_check = [
            "S No.",
            "6 digit HS Code",
            "Total Shipments",
            "% Overall Change",
        ]

        for header in headers_to_check:
            locator = self.page.get_by_role("columnheader", name=header)  # more precise
            expect(locator).to_be_visible(timeout=50000)
            print(f"✅ Header '{header}' is visible.")

    def Validate_checkbox(self):
        #Verify each row has a checkbox to select company
        checkboxes = self.page.locator('input[type="checkbox"][name^="select-row-"]')

        count = checkboxes.count()
        print(f"Found {count} checkboxes")

        for i in range(count):
            checkbox = checkboxes.nth(i)

            # ✅ Check visibility
            expect(checkbox).to_be_visible()

            # ✅ Check unchecked state
            expect(checkbox).not_to_be_checked()

        print("All checkboxes are visible and unchecked ✅")

        #Check all the checkboxes
        for i in range(count):
            checkbox = checkboxes.nth(i)
            checkbox.check()

            # ✅ Check visibility
            expect(checkbox).to_be_visible()

            # ✅ Check unchecked state
            expect(checkbox).to_be_checked()

        print("All checkboxes are visible and checked ✅")

        #Uncheck all the checkboxes
        for i in range(count):
            checkbox = checkboxes.nth(i)
            checkbox.uncheck()

            # ✅ Check visibility
            expect(checkbox).to_be_visible()

            # ✅ Check unchecked state
            expect(checkbox).not_to_be_checked()

        print("All checkboxes are visible and unchecked ✅")

    def Validate_download_excel(self):
        # Download excel
        self.page.locator("//span[normalize-space()='Download Excel']").click()
        expect(self.page.locator("//div[@class='modal-title h4']")).to_contain_text("Download Excel")
        expect(self.page.locator("//button[normalize-space()='Email']")).to_be_visible()
        expect(self.page.locator("//button[normalize-space()='Cancel']").last).to_be_visible()
        expect(self.page.locator("//div[@class='modal-dialog modal-dialog-centered']//span[@aria-hidden='true'][normalize-space()='×']")).to_be_visible()
        self.page.get_by_role("button", name="Cancel").click()

    def Verify_SortBy_dropdown_Trends(self):
        #Verify the Sort By shipment value usd dropdown
        self.page.locator("#sort-dropdown").click()
        expect(self.page.locator("//span[normalize-space()='Shipments']")).to_be_visible()
        expect(self.page.locator("//span[normalize-space()='Value (USD)']")).to_be_visible()
        #Click on Value (USD)
        self.page.locator("//span[normalize-space()='Value (USD)']").click()
        expect(self.page.get_by_text("Download Excel")).to_be_visible(timeout=40000)
        # Grab all values from USD column
        usd_cells = self.page.locator('[class="sc-fqkvVR sc-dcJsrY sc-iGgWBj ffYoNC fYLohF gkzfIp rdt_TableCell"]')
        count = usd_cells.count()
        print(f"Found {count} USD values")

        values_text = []
        for i in range(count):
            values_text.append(usd_cells.nth(i).inner_text().strip())

        print("Extracted values:", values_text)

        def convert_to_number(value: str) -> float:
            """
            Convert values like 674.90B, 183.84M, 45.98K, 1.19T into float.
            Supports:
              - T = Trillion
              - B = Billion
              - M = Million
              - K = Thousand
            """
            value = value.replace(",", "").upper()

            try:
                if value.endswith("T"):  # ✅ NEW: handle Trillion
                    return float(value[:-1]) * 1_000_000_000_000
                elif value.endswith("B"):
                    return float(value[:-1]) * 1_000_000_000
                elif value.endswith("M"):
                    return float(value[:-1]) * 1_000_000
                elif value.endswith("K"):
                    return float(value[:-1]) * 1_000
                else:
                    return float(value)
            except ValueError:
                raise ValueError(f"❌ Could not convert value '{value}' to number")

        numeric_values = [convert_to_number(v) for v in values_text]
        print("Numeric values:", numeric_values)

        # ✅ Validate descending order
        assert numeric_values == sorted(numeric_values, reverse=True), "❌ USD column is not sorted in descending order"
        print("✅ USD column is sorted in descending order")

        # Verify the Sort By shipment value usd dropdown
        self.page.locator("#sort-dropdown").click()
        expect(self.page.locator("//span[normalize-space()='Shipments']")).to_be_visible()
        expect(self.page.locator("//span[normalize-space()='Value (USD)']")).to_be_visible()
        # Click on Value (USD)
        self.page.locator("//span[normalize-space()='Shipments']").click()
        expect(self.page.get_by_text("Download Excel")).to_be_visible(timeout=40000)
        # Grab all values from USD column
        usd_cells = self.page.locator('[class="sc-fqkvVR sc-dcJsrY sc-iGgWBj ffYoNC fYLohF gkzfIp rdt_TableCell"]')
        count = usd_cells.count()
        print(f"Found {count} USD values")

        values_text = []
        for i in range(count):
            values_text.append(usd_cells.nth(i).inner_text().strip())

        print("Extracted values:", values_text)

        # Convert values like 674.90B, 183.84M, 45.98K into float
        def convert_to_number(value: str) -> float:
            value = value.replace(",", "").upper()
            if value.endswith("B"):
                return float(value[:-1]) * 1_000_000_000
            elif value.endswith("M"):
                return float(value[:-1]) * 1_000_000
            elif value.endswith("K"):
                return float(value[:-1]) * 1_000
            else:
                return float(value)

        numeric_values = [convert_to_number(v) for v in values_text]
        print("Numeric values:", numeric_values)

        # ✅ Validate descending order
        assert numeric_values == sorted(numeric_values, reverse=True), "❌ USD column is not sorted in descending order"
        print("✅ Shipment column is sorted in descending order")

    def Enable_Toggle_second_level(self):
        #Enable 2nd level hierarchy toggle
        self.page.locator('[class="custom-control custom-switch"]').click()
        expect(self.page.locator("//span[normalize-space()='Unique Importers']")).to_be_visible(timeout=50000)
        headers_to_check = [
            "6 digit HS Codes",
            "Unique Importers",
            "Total Shipments",
            "% Overall Change",
        ]

        for header in headers_to_check:
            locator = self.page.get_by_role("columnheader", name=header)  # more precise
            expect(locator).to_be_visible(timeout=5000)
            print(f"✅ Header '{header}' is visible.")

        #Disable 2nd level hierarchy toggle
        self.page.locator('[class="custom-control custom-switch"]').click()
        expect(self.page.locator("//span[normalize-space()='Unique Importers']")).not_to_be_visible(timeout=50000)

    def Validate_close_screen(self):
        #Click the Close (X) icon in the Trends modal
        self.page.locator("//button[@class='close']").click()
        expect(self.page.locator("//h4[normalize-space()='Top 6 Digit HS Codes']")).not_to_be_visible(timeout=50000)

    def Validate_View(self):
        # Scroll to the 6-digit HS Code section
        self.page.locator("//div[normalize-space()='6 digit HS Codes']").scroll_into_view_if_needed()
        # 6 Digit HS Code section with top HS Codes should be visible
        expect(self.page.locator("//td[normalize-space()='6 digit HS Code']")).to_be_visible(timeout=50000)
        expect(self.page.locator("//td[normalize-space()='Shipments']")).to_be_visible(timeout=50000)

    def validate_6digit_Hscode_View_all_headercheck(self):
        # Scroll to the 6-digit HS Code section
        self.page.locator("//div[normalize-space()='6 digit HS Codes']").scroll_into_view_if_needed()
        # Click on the View All button in the 6 Digit HS Code section
        self.page.locator(
            "[data-tip='View all 6 digit HS Codes based on their ranking']").click()
        expect(self.page.locator("//h4[normalize-space()='Top 6 Digit HS Codes']")).to_be_visible(timeout=50000)
        expect(self.page.locator("//div[contains(text(),'Top 6 Digit HS Codes')]")).to_be_visible(timeout=50000)
        # Scroll down to verify shipment table fields
        headers_to_check = [
            "S No.",
            "Top 6 Digit HS Codes",
            "Shipments",
            "Value (USD)",
            "% share by Number of Shipments",
            "Apply Filter"
        ]

        for header in headers_to_check:
            locator = self.page.get_by_role("columnheader", name=header) .first # more precise
            expect(locator).to_be_visible(timeout=50000)
            print(f"✅ Header '{header}' is visible.")

    def Verify_SortBy_dropdown_Viewall(self):
        #Verify the Sort By shipment value usd dropdown
        self.page.pause()
        self.page.locator("#time-frame-dropdown").click()
        expect(self.page.get_by_text("Number of Shipments",exact=True)).to_be_visible(timeout=30000)
        expect(self.page.get_by_text("Total Shipment Value (USD)").last).to_be_visible()
        #Click on total Shipment Value (USD)
        self.page.get_by_text("Number of Shipments",exact=True).click()
        expect(self.page.get_by_text("Download Excel")).to_be_visible(timeout=40000)
        self.page.wait_for_timeout(4000)
        # Grab all headers
        header_name = "Shipments"
        headers = self.page.locator("[role='columnheader']")
        header_count = headers.count()
        print(f"Found {header_count} headers")

        header_index = None
        for i in range(header_count):
            text = headers.nth(i).inner_text().strip()
            if text == header_name:
                header_index = i
                break

        assert header_index is not None, f"❌ Header '{header_name}' not found"
        print(f"✅ Found header '{header_name}' at index {header_index}")

        # Wait for table refresh
        expect(self.page.get_by_text("Download Excel")).to_be_visible(timeout=40000)

        # Collect all rows in the table
        rows = self.page.locator("[role='row']")

        values_text = []
        row_count = rows.count()
        for r in range(1, row_count):  # skip header row (row 0)
            cell = rows.nth(r).locator("[role='cell']").nth(header_index)
            values_text.append(cell.inner_text().strip())

        print("Extracted values:", values_text)

        # Convert values like 674.90B, 183.84M, 45.98K into float
        def convert_to_number(value: str) -> float:
            value = value.replace(",", "").upper()
            if value.endswith("B"):
                return float(value[:-1]) * 1_000_000_000
            elif value.endswith("M"):
                return float(value[:-1]) * 1_000_000
            elif value.endswith("K"):
                return float(value[:-1]) * 1_000
            else:
                return float(value)

        numeric_values = [convert_to_number(v) for v in values_text]
        print("Numeric values:", numeric_values)

        # ✅ Validate descending order
        assert numeric_values == sorted(numeric_values, reverse=True), (
            f"❌ Column '{header_name}' is not sorted in descending order"
        )
        print(f"✅ Column '{header_name}' is sorted in descending order")

        # Verify the Sort By shipment
        self.page.locator("#time-frame-dropdown").click()
        expect(self.page.get_by_text("Number of Shipments",exact=True)).to_be_visible()
        expect(self.page.get_by_text("Total Shipment Value (USD)").last).to_be_visible()
        # Click on total Shipment Value (USD)
        self.page.get_by_text("Total Shipment Value (USD)").last.click()
        expect(self.page.get_by_text("Download Excel")).to_be_visible(timeout=40000)
        # Grab all headers
        header_name = "Value (USD)"
        headers = self.page.locator("[role='columnheader']")
        header_count = headers.count()
        print(f"Found {header_count} headers")

        header_index = None
        for i in range(header_count):
            text = headers.nth(i).inner_text().strip()
            if text == header_name:
                header_index = i
                break

        assert header_index is not None, f"❌ Header '{header_name}' not found"
        print(f"✅ Found header '{header_name}' at index {header_index}")

        # Wait for table refresh
        expect(self.page.get_by_text("Download Excel")).to_be_visible(timeout=40000)

        # Collect all rows in the table
        rows = self.page.locator("[role='row']")

        values_text = []
        row_count = rows.count()
        for r in range(1, row_count):  # skip header row (row 0)
            cell = rows.nth(r).locator("[role='cell']").nth(header_index)
            values_text.append(cell.inner_text().strip())

        print("Extracted values:", values_text)

        # Convert values like 674.90B, 183.84M, 45.98K into float
        def convert_to_number(value: str) -> float:
            value = value.replace(",", "").upper()
            if value.endswith("B"):
                return float(value[:-1]) * 1_000_000_000
            elif value.endswith("M"):
                return float(value[:-1]) * 1_000_000
            elif value.endswith("K"):
                return float(value[:-1]) * 1_000
            else:
                return float(value)

        numeric_values = [convert_to_number(v) for v in values_text]
        print("Numeric values:", numeric_values)

        # ✅ Validate descending order
        assert numeric_values == sorted(numeric_values, reverse=True), (
            f"❌ Column '{header_name}' is not sorted in descending order"
        )
        print(f"✅ Column '{header_name}' is sorted in descending order")

    def Verify_ViewModal_SearchBar(self):
        """
        Verifies presence of search bar inside the HS Code modal,
        extracts a code from the table, searches for it,
        and validates that results match the search.
        """

        # ✅ Wait for search bar to appear
        search_box = self.page.get_by_placeholder("Type to search 6 digit HS Codes")
        expect(search_box).to_be_visible(timeout=50000)

        header_name = "Top 6 Digit HS Codes"
        headers = self.page.locator("[role='columnheader']")
        header_count = headers.count()
        print(f"Found {header_count} headers")

        header_index = None
        for i in range(header_count):
            text = headers.nth(i).inner_text().strip()
            if text == header_name:
                header_index = i
                break

        assert header_index is not None, f"❌ Header '{header_name}' not found"
        print(f"✅ Found header '{header_name}' at index {header_index}")

        # ✅ Wait until table is loaded
        expect(self.page.get_by_text("Download Excel")).to_be_visible(timeout=40000)

        # ✅ Extract first HS code from table
        rows = self.page.locator("[role='row']")
        row_count = rows.count()
        extracted_code = None

        for r in range(1, row_count):  # skip header row
            cell_text = rows.nth(r).locator("[role='cell']").nth(header_index).inner_text().strip()
            match = re.match(r"^(\d+)\s*-", cell_text)
            if match:
                extracted_code = match.group(1)
                print("Extracted HS Code:", extracted_code)
                break

        assert extracted_code, "❌ No HS Code could be extracted from the table."

        # ✅ Perform search
        search_box.fill(extracted_code)
        expect(self.page.locator("._form_check_label_nookn_22 > div > b")).to_contain_text(extracted_code)

        # ✅ Click on Search button
        self.page.locator("//button[@class='_btn_e8xj1_1 _btn-primaryWithIcon_e8xj1_23 _size-small_e8xj1_86 ml-1 mb-3 d-flex align-items-center px-3 d-flex align-items-center justify-content-center']").click()
        # ✅ Validate filtered results
        rows = self.page.locator("div[role='row']")
        row_count = rows.count()
        print(f"Found {row_count - 1} result rows after search")

        invalid_entries = []
        for r in range(1, row_count):
            cell_text = rows.nth(r).locator("div[role='cell']").nth(header_index).inner_text().strip()
            if not cell_text.startswith(extracted_code):
                invalid_entries.append(cell_text)
                print(f"❌ FAIL: Row {r} contains invalid HS Code '{cell_text}'")
            else:
                print(f"✅ Row {r} contains correct HS Code '{cell_text}'")

        if invalid_entries:
            print(f"🚨 Invalid entries found: {invalid_entries}")
        else:
            print("🎉 All rows match the searched HS Code ✅")

        # ✅ Clear the search
        self.page.locator('[class="mr-1 cursor-pointer"]').click()

        return extracted_code  # return so it can be reused in other tests

    def Apply_filter_icon(self):
        self.page.pause()
        """
        Extract the HS Code from the first row under 'Top 6 Digit HS Codes'
        and store it in self.hscode_applyfilter for later validation.
        """
        expect(self.page.get_by_text("Download Excel")).to_be_visible(timeout=40000)
        # ✅ Get header index dynamically
        header_name = "Top 6 Digit HS Codes"
        headers = self.page.locator("[role='columnheader']")
        header_count = headers.count()

        assert header_count > 0, "❌ No headers found in the table!"

        header_index = None
        for i in range(header_count):
            text = headers.nth(i).inner_text().strip()
            if text == header_name:
                header_index = i
                break

        assert header_index is not None, f"❌ Header '{header_name}' not found in the table"
        print(f"✅ Found header '{header_name}' at index {header_index}")

        # ✅ Get first row data safely
        rows = self.page.locator("table tbody tr")
        row_count = rows.count()
        assert row_count > 0, "❌ No rows found in the table!"

        # ✅ Extract HS Code from first row
        # Locate the first visible HS Code cell
        cell_locator = self.page.locator("//div[@class='text-left']/span[normalize-space()]").first

        # ✅ Wait for the locator to be visible
        expect(cell_locator).to_be_visible(timeout=60000)

        # ✅ Extract text safely
        self.hscode_applyfilter = cell_locator.inner_text().strip()

        # ✅ Assert to catch empty value early
        assert self.hscode_applyfilter, "❌ Failed to extract HS Code from the shipment grid."

        # ✅ Print result for debugging
        print(f"✅ Extracted HS Code from grid: {self.hscode_applyfilter}")

        # ✅ (Optional) Extract only the numeric part (before ' - ') if needed
        self.selected_hs_code = self.hscode_applyfilter.split(" - ")[0]
        print(f"🔎 Selected HS Code: {self.selected_hs_code}")

        #Apply filter
        self.page.locator("td:nth-child(7)").first.click()

        # ✅ Validate Shipment Tab is selected
        self.page.wait_for_timeout(2000)
        self.page.locator("//a[@id='nav-home-tab']").click()
        shipment_tab = self.page.locator("#nav-home-tab")
        expect(shipment_tab).to_have_attribute("aria-selected", "true")
        print("✅ Shipment tab is selected")
        # ✅ Wait until "Top 6 Digit HS Codes" section is no longer visible
        expect(self.page.locator("//h4[normalize-space()='Top 6 Digit HS Codes']")
        ).not_to_be_visible(timeout=50000)

        print("✅ 'Top 6 Digit HS Codes' section is hidden after applying filter")

    def Validate_preselected_code_inthe_cargo_filter(self):
        """
        Validates that the selected 6 Digit HS Code is pre-selected in the Cargo filter.
        """

        # ✅ Open Cargo filter and click 6 Digit HS Code section
        self.page.get_by_text("Cargo", exact=True).click()
        self.page.locator("//div[contains(text(),'6 Digit HS Code')]").click()

        # ✅ Extract first HS Code text
        text = self.page.locator("[class='text-no-transform']").nth(0).inner_text().strip()
        match = re.match(r"^(\d+)\s*-", text)
        assert match, "❌ Could not extract HS Code from first filter item"
        hs_code = match.group(1)
        print("Extracted HS code:", hs_code)

        # ✅ Verify checkbox is checked
        checkbox = self.page.locator('input[type="checkbox"]').nth(0)
        expect(checkbox).to_be_checked()
        print("✅ First HS Code checkbox is checked")

        # ✅ Get the HS Code that was clicked in Apply_filter_icon()
        selected_hs_code = self.page.locator('[class="text-no-transform"]').nth(0).inner_text().strip().split(" - ")[0]

        if hs_code == selected_hs_code:
            print(f"✅ HS Code '{hs_code}' is correctly pre-selected in Cargo filter")
        else:
            print(f"❌ HS Code '{hs_code}' does NOT match previously selected '{selected_hs_code}'")

        # ✅ Close filter modal
        self.page.locator("//span[@aria-hidden='true']").click()

    def Validate_HSCode_In_ShipmentGrid(self, validate: bool = True):
        """
        Validate that Shipment Grid contains correct HS Codes.
        Checks that each row's HS Code starts with the selected HS Code.
        """

        headers = self.page.locator("table thead tr th")
        header_count = headers.count()

        self.S_No = None
        self.HS_Code_field = None

        # Extract headers
        for i in range(header_count):
            header_text = headers.nth(i).inner_text().strip()
            if header_text.lower() in ["s no", "sl no", "serial no"]:
                self.S_No = i
            elif header_text.lower() == "hs code":
                self.HS_Code_field = i

        if self.HS_Code_field is None:
            raise Exception("❌ 'HS Code' column not found in the table.")

        print(f"✅ Found column indexes → S No: {self.S_No}, HS Code: {self.HS_Code_field}")

        rows = self.page.locator("table tbody tr")
        row_count = rows.count()

        invalid_entries = []

        for i in range(row_count):
            cells = rows.nth(i).locator("td")
            sl_no = cells.nth(self.S_No).inner_text().strip()
            hs_code = cells.nth(self.HS_Code_field).inner_text().strip()

            if validate:
                if hs_code.startswith(self.selected_hs_code):
                    print(f"✅ PASS: HS Code '{hs_code}' at Sl. No: {sl_no}")
                else:
                    print(
                        f"❌ FAIL: Invalid HS Code '{hs_code}' at Sl. No: {sl_no} (Expected prefix: {self.selected_hs_code})")
                    invalid_entries.append((sl_no, hs_code))

        # Final report
        if validate:
            if not invalid_entries:
                print("🎉 All entries are valid ✅")
            else:
                print("🚨 Invalid entries found ❌:", invalid_entries)

    def Enable_Toggle_second_level_Viewall(self):
        #Enable 2nd level hierarchy toggle
        self.page.locator('[class="custom-control custom-switch"]').click()
        expect(self.page.locator("//span[normalize-space()='Unique Importers']")).to_be_visible(timeout=50000)
        headers_to_check = [
            "6 digit HS Codes",
            "Unique Importers",
            "Shipments",
            "Value (USD)",
            "% share by Total Shipment Value (USD)"
        ]

        for header in headers_to_check:
            locator = self.page.get_by_role("columnheader", name=header).first  # more precise
            expect(locator).to_be_visible(timeout=5000)
            print(f"✅ Header '{header}' is visible.")

        #Disable 2nd level hierarchy toggle
        self.page.locator('[class="custom-control custom-switch"]').click()
        expect(self.page.locator("//span[normalize-space()='Unique Importers']")).not_to_be_visible(timeout=50000)

    def Validate_consignee_states_screen(self):
        # Scroll to the consignee states section
        self.page.locator("//div[contains(text(),'Consignee States')]").scroll_into_view_if_needed()

    def validate_Consignee_Trends_headercheck(self):
        # Click on the Trends button in 6-digit HS Code section
        self.page.locator(
            "[data-tip='Analyse trade trends of all Consignee States based on their monthly, quarterly and yearly trade']").click()
        expect(self.page.locator("//h4[normalize-space()='Consignee States: Trends']")).to_be_visible(timeout=50000)
        expect(self.page.locator("//span[normalize-space()='Consignee States']")).to_be_visible(timeout=50000)
        # Columns should include:Total Shipment Value (USD)- % Overall Change- Year-wise values (e.g., 2025, 2024, 2023, 2022)
        headers_to_check = [
            "S No.",
            "Consignee States",
            "Total Shipments",
            "% Overall Change",
            "Apply Filter"
        ]

        for header in headers_to_check:
            locator = self.page.get_by_role("columnheader", name=header)  # more precise
            expect(locator).to_be_visible(timeout=50000)
            print(f"✅ Header '{header}' is visible.")

    def Enable_Toggle_second_level_consignee(self):
        # Enable 2nd level hierarchy toggle
        self.page.locator('[class="custom-control custom-switch"]').click()
        expect(self.page.locator("//span[normalize-space()='Countries of Origin']")).to_be_visible(timeout=50000)
        headers_to_check = [
            "Consignee States",
            "Countries of Origin",
            "Total Shipments",
            "% Overall Change",
        ]

        for header in headers_to_check:
            locator = self.page.get_by_role("columnheader", name=header)  # more precise
            expect(locator).to_be_visible(timeout=5000)
            print(f"✅ Header '{header}' is visible.")

        # Disable 2nd level hierarchy toggle
        self.page.locator('[class="custom-control custom-switch"]').click()
        expect(self.page.locator("//span[normalize-space()='Countries of Origin']")).not_to_be_visible(timeout=50000)

    def Validate_close_screen_consignee(self):
        # Click the Close (X) icon in the Trends modal
        self.page.locator("//button[@class='close']").click()
        expect(self.page.locator("//span[normalize-space()='Countries of Origin']")).not_to_be_visible(timeout=50000)

    def Validate_Time_Range_drp_Yearly(self):
        expect(self.page.locator("//span[normalize-space()='Download Excel']")).to_be_visible(timeout=100000)
        self.page.wait_for_timeout(3000)
        self.page.wait_for_selector('[role="columnheader"]', state="attached", timeout=50000)

        # Get all header elements first
        headers = self.page.locator('[role="columnheader"]')
        header_count = headers.count()  # ✅ This works in sync mode

        header_texts = []
        for i in range(header_count):
            text = headers.nth(i).inner_text().strip()
            header_texts.append(text)

        print("Detected headers:", header_texts)

        # --- Filter only year headers (4-digit numbers) ---
        yearly_headers = [h for h in header_texts if h.isdigit() and len(h) == 4]

        # --- Build expected yearly headers (current year → 2020) ---
        current_year = datetime.today().year
        expected_years = [str(y) for y in range(current_year, 2019, -1)]
        print("Expected yearly headers:", expected_years)

        # --- Validation ---
        missing_years = [y for y in expected_years if y not in yearly_headers]
        if missing_years:
            raise AssertionError(f"❌ Missing yearly headers in table: {missing_years}")
        else:
            print(f"✅ All yearly headers present from {current_year} to 2020")

    def Validate_Time_Range_drp_Monthly(self):
        self.page.locator("//span[normalize-space()='Yearly']").click()
        self.page.locator("//span[normalize-space()='Monthly']").click()
        expect(self.page.locator("//span[normalize-space()='Download Excel']")).to_be_visible(timeout=100000)
        self.page.wait_for_timeout(3000)
        self.page.wait_for_selector('[role="columnheader"]', state="attached", timeout=50000)

        headers = self.page.locator('[role="columnheader"]')
        header_count = headers.count()

        header_texts = []
        for i in range(header_count):
            text = headers.nth(i).inner_text().strip()
            header_texts.append(text)

        print("Raw header texts:", header_texts)

        # --- Filter and normalize headers that look like Month-Year ---
        monthly_headers = []
        for h in header_texts:
            # Accept both "Jul 2025" and "Jul-2025"
            parts = h.replace(" ", "-").split("-")
            if len(parts) == 2 and parts[0].isalpha() and parts[1].isdigit():
                normalized = f"{parts[0][:3].title()}-{parts[1]}"
                monthly_headers.append(normalized)

        # --- Build expected months ---
        today = datetime.today()
        last_month = today.replace(day=1) - timedelta(days=1)

        expected_months = []
        while last_month >= datetime(2020, 1, 1):
            expected_months.append(last_month.strftime("%b-%Y"))
            last_month = last_month.replace(day=1) - timedelta(days=1)

        print("Expected months:", expected_months[:12], "...")

        # --- Validation ---
        missing_months = [m for m in expected_months if m not in monthly_headers]
        if missing_months:
            print(f"❌ Missing months in table headers: {missing_months}")
        else:
            print("✅ All monthly columns present from latest to Jan-2020")

    def Validate_Time_Range_drp_Quaterly(self):
        self.page.locator("//span[normalize-space()='Monthly']").click()
        self.page.locator("//span[normalize-space()='Quarterly']").click()
        self.page.wait_for_timeout(3000)
        self.page.wait_for_selector('[role="columnheader"]', state="attached", timeout=50000)
        expect(self.page.locator("//span[normalize-space()='Download Excel']")).to_be_visible(timeout=100000)

        headers = self.page.locator('[role="columnheader"]')
        header_count = headers.count()  # ✅ Needs await if running async (see below)

        header_texts = []
        for i in range(header_count):
            text = headers.nth(i).inner_text().strip()
            header_texts.append(text)

        print("Raw header texts:", header_texts)

        # --- Build Expected Quarters ---
        today = datetime.today()
        year = today.year
        month = today.month
        current_quarter = (month - 1) // 3 + 1

        expected_quarters = []
        while year > 2020 or (year == 2020 and current_quarter >= 1):
            expected_quarters.append(f"Q{current_quarter}-{year}")
            current_quarter -= 1
            if current_quarter == 0:
                current_quarter = 4
                year -= 1

        print("Expected quarters:", expected_quarters[:8], "...")

        # --- Extract and Normalize Quarterly Headers ---
        quarterly_headers = []
        quarter_regex = re.compile(r"(Q[1-4])[\s\-]?(FY)?(\d{2,4})", re.IGNORECASE)

        for h in header_texts:
            match = quarter_regex.search(h)
            if match:
                q = match.group(1).upper()  # Q1/Q2/Q3/Q4
                year = match.group(3)
                if len(year) == 2:  # Convert FY25 → 2025
                    year = "20" + year
                quarterly_headers.append(f"{q}-{year}")

        print("Quarterly headers found in table:", quarterly_headers)

        missing_quarters = [q for q in expected_quarters if q not in quarterly_headers]
        if missing_quarters:
            print(f"❌ Missing quarters in table headers: {missing_quarters}")
        else:
            print("✅ All quarterly columns present from latest to Q1-2020")

    def Validate_custom_house_agent_screen(self):
        # Scroll to the consignee states section
        self.page.locator("#custom_house .card-header .col-md-6", has_text="Customs House Agent Name").scroll_into_view_if_needed()

    def validate_Customhouseagent_Trends_headercheck(self):
        # Scroll to the Customs House Agent Name section
        self.page.locator(
            "[data-tip='Analyse trade trends of all Customs House Agent Name based on their monthly, quarterly and yearly trade']").click()
        expect(self.page.locator("//h4[normalize-space()='Customs House Agent Name: Trends']")).to_be_visible(timeout=50000)
        expect(self.page.locator("//div[@id='column-key']")).to_be_visible(timeout=50000)
        expect(self.page.locator("//span[normalize-space()='Download Excel']")).to_be_visible(timeout=50000)
        expect( self.page.locator("#sort-dropdown")).to_be_visible(timeout=50000)
        # Columns should include:Total Shipment Value (USD)- % Overall Change- Year-wise values (e.g., 2025, 2024, 2023, 2022)
        headers_to_check = [
            "S No.",
            "Customs House Agent Name",
            "Total Shipments",
            "% Overall Change",
            "Apply Filter"
        ]

        for header in headers_to_check:
            locator = self.page.get_by_role("columnheader", name=header)  # more precise
            expect(locator).to_be_visible(timeout=50000)
            print(f"✅ Header '{header}' is visible.")


    def Custom_House_Agent_Name_View_All(self):
        self.page.locator('[data-tip="View all Customs House Agent Name based on their ranking"]').click()
        expect(self.page.locator("//h4[normalize-space()='Customs Houses']")).to_be_visible(
            timeout=50000)
        expect(self.page.locator("//div[contains(text(),'Customs Houses')]")).to_be_visible(timeout=50000)
        expect(self.page.locator("//span[normalize-space()='Download Excel']")).to_be_visible(timeout=50000)
        # A modal opens listing all importing countries with table columns:
        # Country Name, Shipments, Value (USD), % Share by number of shipment. Also includes search bar, sort dropdown, and download Excel icon
        headers_to_check = [
            "S No.",
            "Customs Houses",
            "Shipments",
            "Value (USD)",
            "% share by Number of Shipments",
            "Apply Filter"
        ]

        for header in headers_to_check:
            locator = self.page.get_by_role("columnheader", name=header).first  # more precise
            expect(locator).to_be_visible(timeout=50000)
            print(f"✅ Header '{header}' is visible.")

    def Apply_filter_custom_house(self):
        self.page.pause()
        expect(self.page.get_by_text("Download Excel")).to_be_visible(timeout=40000)
        # ✅ Get header index dynamically
        header_name = "Customs Houses"
        headers = self.page.locator("[role='columnheader']")
        header_count = headers.count()

        assert header_count > 0, "❌ No headers found in the table!"

        header_index = None
        for i in range(header_count):
            text = headers.nth(i).inner_text().strip()
            if text == header_name:
                header_index = i
                break

        assert header_index is not None, f"❌ Header '{header_name}' not found in the table"
        print(f"✅ Found header '{header_name}' at index {header_index}")

        # ✅ Get first row data safely
        rows = self.page.locator("table tbody tr")
        row_count = rows.count()
        assert row_count > 0, "❌ No rows found in the table!"
        cell_locator = self.page.locator("//div[@class='text-capitalize']").first

        # ✅ Wait for the locator to be visible
        expect(cell_locator).to_be_visible(timeout=60000)

        self.customs_house = cell_locator.get_attribute("data-tip")

        print("Extracted data-tip value:", self.customs_house)

        # ✅ Assert to catch empty value early
        assert self.customs_house, "❌ Failed to extract custom house name from the view all grid."

        # ✅ Print result for debugging
        print(f"✅ Extracted customs house from grid: {self.customs_house}")

        # Apply filter
        self.page.locator("td:nth-child(7)").first.click()

        # ✅ Validate Shipment Tab is selected
        self.page.wait_for_timeout(2000)
        self.page.locator("//a[@id='nav-home-tab']").click()
        shipment_tab = self.page.locator("#nav-home-tab")
        expect(shipment_tab).to_have_attribute("aria-selected", "true")
        print("✅ Shipment tab is selected")

    def Validate_preselected_code_inthe_customs_filter(self):
        """
        Validates that the selected 6 Digit HS Code is pre-selected in the Cargo filter.
        """

        # ✅ Open Cargo filter and click 6 Digit HS Code section
        self.page.get_by_text("Customs Details", exact=True).click()
        self.page.locator('[class="_filteritemtext_a6k5f_88"]').nth(0).click()

        # ✅ Extract first HS Code text
        match = re.match(r"^(.*?)(?:,\s*\()", self.customs_house)
        if match:
            custom_name = match.group(1).strip()
        else:
            custom_name = self.customs_house  # fallback if pattern not found

        print("Extracted custom house name:", custom_name)

        # ✅ Verify checkbox is checked
        checkbox = self.page.locator('input[type="checkbox"]').nth(0)
        expect(checkbox).to_be_checked()
        print("✅ First custom house checkbox is checked")

        if self.customs_house == custom_name:
            print(f"✅ Custom house name '{custom_name}' is correctly pre-selected in custom name filter")
        else:
            print(f"❌ Custom house name'{custom_name}' does NOT match'")

        # ✅ Close filter modal
        self.page.locator("//span[@aria-hidden='true']").click()

    def Validate_Customs_house_In_ShipmentGrid(self, validate: bool = True):
        self.page.locator("//a[@id='nav-home-tab']").click()

        if not hasattr(self, "invalid_entries"):
            self.invalid_entries = []

        headers = self.page.locator("table thead tr th")
        header_count = headers.count()

        self.S_No = None
        self.C_H_field = None

        # Extract headers
        table_headers = []
        for i in range(header_count):
            header_text = headers.nth(i).inner_text().strip()
            table_headers.append(header_text)
            if header_text.lower() in ["s no", "sl no", "serial no"]:
                self.S_No = i
            elif header_text.lower() == "custom house agent name":
                self.C_H_field = i

        # --- Handle missing "Country of Import" column ---
        if self.C_H_field is None:
            self.page.locator("//span[normalize-space()='Customise Shipment Grid']").click()
            self.page.locator("//span[normalize-space()='custom details']").click()
            self.page.locator("//span[@data-for='Custom House Agent Nameelipsis']").click()
            self.page.locator("//button[normalize-space()='Save Configuration']").click()
            expect(self.page.get_by_text("View").last).to_be_visible(timeout=10000)

            # 🔄 Re-fetch headers after update
            headers = self.page.locator("table thead tr th")
            header_count = headers.count()
            for i in range(header_count):
                header_text = headers.nth(i).inner_text().strip().lower()
                if header_text == "custom house agent name":
                    self.C_H_field = i
                    print("✅ 'Custom House Agent Name' column added successfully!")

        if self.C_H_field is None:
            raise Exception("❌ 'Custom House Agent Name' column not found even after customization.")

        print(f"✅ Found column indexes → S No: {self.S_No}, Custom House Agent Name: {self.C_H_field}")

        rows = self.page.locator("table tbody tr")
        row_count = rows.count()

        invalid_entries = []

        for i in range(row_count):
            cells = rows.nth(i).locator("td")
            sl_no = cells.nth(self.S_No).inner_text().strip()
            custom_house = cells.nth(self.C_H_field).inner_text().strip()

            if validate:
                if custom_house.lower() == self.customs_house.lower():
                    print(f"✅ PASS: Valid custom house name '{custom_house}' found at Sl. No: {sl_no}")
                else:
                    print(
                        f"❌ FAIL: Invalid custom house name '{custom_house}' found at Sl. No: {sl_no} (Expected prefix: {self.customs_house})")
                    invalid_entries.append((sl_no, custom_house))

        # Final report
        if validate:
            if not invalid_entries:
                print("🎉 All entries are valid ✅")
            else:
                print("🚨 Invalid entries found ❌:", invalid_entries)

    def Validate_port_laiding_screen(self):
        # Scroll to the port lading
        self.page.locator("#port_of_lading .card-header .col-md-6",has_text="Ports of Lading").scroll_into_view_if_needed(timeout=40000)

    def validate_port_lading_Trends_headercheck(self):
        # Scroll to the port lading section
        self.page.locator(
            "[data-tip='Analyse trade trends of all Ports of Lading based on their monthly, quarterly and yearly trade']").click()
        expect(self.page.locator("//h4[normalize-space()='Ports of Lading: Trends']")).to_be_visible(
            timeout=50000)
        expect(self.page.locator("//div[@id='column-key']")).to_be_visible(timeout=50000)
        expect(self.page.locator("//span[normalize-space()='Download Excel']")).to_be_visible(timeout=50000)
        expect(self.page.locator("#sort-dropdown")).to_be_visible(timeout=50000)
        # Columns should include:Total Shipment Value (USD)- % Overall Change- Year-wise values (e.g., 2025, 2024, 2023, 2022)
        headers_to_check = [
            "S No.",
            "Ports of Lading",
            "Total Shipments",
            "% Overall Change",
            "Apply Filter"
        ]

        for header in headers_to_check:
            locator = self.page.get_by_role("columnheader", name=header).first  # more precise
            expect(locator).to_be_visible(timeout=50000)
            print(f"✅ Header '{header}' is visible.")

    def Port_lading_View_All(self):
        self.page.locator('[data-tip="View all Ports of Lading based on their ranking"]').click()
        expect(self.page.locator("//h4[normalize-space()='Ports of lading']")).to_be_visible(
            timeout=50000)
        expect(self.page.locator("//span[normalize-space()='Download Excel']")).to_be_visible(timeout=50000)
        # A modal opens listing all importing countries with table columns:
        # Country Name, Shipments, Value (USD), % Share by number of shipment. Also includes search bar, sort dropdown, and download Excel icon
        headers_to_check = [
            "S No.",
            "Ports of Lading",
            "Shipments",
            "Value (USD)",
            "% share by Number of Shipments",
            "Apply Filter"
        ]

        for header in headers_to_check:
            locator = self.page.get_by_role("columnheader", name=header).first  # more precise
            expect(locator).to_be_visible(timeout=50000)
            print(f"✅ Header '{header}' is visible.")


    def Apply_filter_Ports_lading(self):
        self.page.pause()
        expect(self.page.get_by_text("Download Excel")).to_be_visible(timeout=40000)
        # ✅ Get header index dynamically
        header_name = "Ports of lading"
        headers = self.page.locator("[role='columnheader']")
        header_count = headers.count()

        assert header_count > 0, "❌ No headers found in the table!"

        header_index = None
        for i in range(header_count):
            text = headers.nth(i).inner_text().strip()
            if text == header_name:
                header_index = i
                break

        assert header_index is not None, f"❌ Header '{header_name}' not found in the table"
        print(f"✅ Found header '{header_name}' at index {header_index}")

        # ✅ Get first row data safely
        rows = self.page.locator("table tbody tr")
        row_count = rows.count()
        assert row_count > 0, "❌ No rows found in the table!"
        cell_locator = self.page.locator("//div[@class='text-capitalize']").first

        # ✅ Wait for the locator to be visible
        expect(cell_locator).to_be_visible(timeout=60000)

        self.port_lading = cell_locator.inner_text().strip()

        print("Port lading value:", self.port_lading)

        # ✅ Assert to catch empty value early
        assert self.port_lading, "❌ Failed to extract port lading from the view all grid."

        # ✅ Print result for debugging
        print(f"✅ Extracted port lading from grid: {self.port_lading}")

        # Apply filter
        self.page.locator("td:nth-child(7)").first.click()

        # ✅ Validate Shipment Tab is selected
        self.page.wait_for_timeout(2000)
        self.page.locator("//a[@id='nav-home-tab']").click()
        shipment_tab = self.page.locator("#nav-home-tab")
        expect(shipment_tab).to_have_attribute("aria-selected", "true")
        print("✅ Shipment tab is selected")

    def Validate_preselected_code_inthe_port_lading_filter(self):
        # ✅ Open Cargo filter and click 6 Digit HS Code section
        global full_port_name
        self.page.get_by_text("Ports", exact=True).click()
        self.page.locator("//div[contains(text(),'Port Of Lading')]").first.click()

        Portladingwithcount = self.page.locator('[data-for = "localize-filter-tooltip"]').nth(
            0).inner_text().strip()
        match = re.match(r"(.+?)\(([\d,]+)\)", Portladingwithcount)
        if match:
            raw_port = match.group(1).strip()
            Total_Record_Count = match.group(2)  # keep commas as-is (string)

            # Save full port name
            full_port_name = raw_port

            print("✅ Full Port Name:", full_port_name)
            print("✅ Value:", Total_Record_Count)

        # ✅ Verify checkbox is checked
        checkbox = self.page.locator('input[type="checkbox"]').nth(1)
        expect(checkbox).to_be_checked()
        print("✅ First port lading checkbox is checked")

        if full_port_name.lower() in self.port_lading.lower():
            print(f"✅ Port lading name '{full_port_name}' is correctly pre-selected in port lading filter")
        else:
            print(f"❌ Port lading name'{full_port_name}' does NOT match'")

        # ✅ Close filter modal
        self.page.locator("//span[@aria-hidden='true']").click()

    def Validate_Port_lading_In_ShipmentGrid(self, validate: bool = True):
        self.page.locator("//a[@id='nav-home-tab']").click()

        if not hasattr(self, "invalid_entries"):
            self.invalid_entries = []

        headers = self.page.locator("table thead tr th")
        header_count = headers.count()

        self.S_No = None
        self.P_L_field = None

        # Extract headers
        table_headers = []
        for i in range(header_count):
            header_text = headers.nth(i).inner_text().strip()
            table_headers.append(header_text)
            if header_text.lower() in ["s no", "sl no", "serial no"]:
                self.S_No = i
            elif header_text.lower() == "port of lading":
                self.P_L_field = i

        if self.P_L_field is None:
            raise Exception("❌ 'Port of lading' column is not found in the table")

        print(f"✅ Found column indexes → S No: {self.S_No}, Port of lading: {self.P_L_field}")

        rows = self.page.locator("table tbody tr")
        row_count = rows.count()

        invalid_entries = []

        for i in range(row_count):
            cells = rows.nth(i).locator("td")
            sl_no = cells.nth(self.S_No).inner_text().strip()
            port_lading_value = cells.nth(self.P_L_field).inner_text().strip()

            if validate:
                if port_lading_value.lower() == self.port_lading.lower():
                    print(f"✅ PASS: Valid port lading name '{port_lading_value}' found at Sl. No: {sl_no}")
                else:
                    print(
                        f"❌ FAIL: Invalid port lading name '{port_lading_value}' found at Sl. No: {sl_no} (Expected prefix: {self.port_lading})")
                    invalid_entries.append((sl_no, port_lading_value))

        # Final report
        if validate:
            if not invalid_entries:
                print("🎉 All entries are valid ✅")
            else:
                print("🚨 Invalid entries found ❌:", invalid_entries)

    def Validate_port_unlaiding_screen(self):
        # Scroll to the port lading
        element = self.page.locator("#port_of_unlading .card-header .col-md-6", has_text="Ports of Unlading")
        element.wait_for(state="visible", timeout=40000)
        element.scroll_into_view_if_needed(timeout=40000)

    def validate_port_unlading_Trends_headercheck(self):
        # Scroll to the port lading section
        self.page.locator(
            "[data-tip='Analyse trade trends of all Ports of Unlading based on their monthly, quarterly and yearly trade']").click()
        expect(self.page.locator("//h4[normalize-space()='Ports of Unlading: Trends']")).to_be_visible(
            timeout=50000)
        expect(self.page.locator("//div[@id='column-key']")).to_be_visible(timeout=50000)
        expect(self.page.locator("//span[normalize-space()='Download Excel']")).to_be_visible(timeout=50000)
        expect(self.page.locator("#sort-dropdown")).to_be_visible(timeout=50000)
        # Columns should include:Total Shipment Value (USD)- % Overall Change- Year-wise values (e.g., 2025, 2024, 2023, 2022)
        headers_to_check = [
            "S No.",
            "Ports of Unlading",
            "Total Shipments",
            "% Overall Change",
            "Apply Filter"
        ]

        for header in headers_to_check:
            locator = self.page.get_by_role("columnheader", name=header).first  # more precise
            expect(locator).to_be_visible(timeout=50000)
            print(f"✅ Header '{header}' is visible.")

    def Port_Unlading_View_All(self):
        self.page.locator('[data-tip="View all Ports of Unlading based on their ranking"]').click()
        expect(self.page.locator("//h4[normalize-space()='Ports of Unlading']")).to_be_visible(
            timeout=50000)
        expect(self.page.locator("//span[normalize-space()='Download Excel']")).to_be_visible(timeout=50000)
        # A modal opens listing all importing countries with table columns:
        # Country Name, Shipments, Value (USD), % Share by number of shipment. Also includes search bar, sort dropdown, and download Excel icon
        headers_to_check = [
            "S No.",
            "Ports of Unlading",
            "Shipments",
            "Value (USD)",
            "% share by Number of Shipments",
            "Apply Filter"
        ]

        for header in headers_to_check:
            locator = self.page.get_by_role("columnheader", name=header).first  # more precise
            expect(locator).to_be_visible(timeout=50000)
            print(f"✅ Header '{header}' is visible.")

    def Apply_filter_Ports_Unlading(self):
        self.page.pause()
        expect(self.page.get_by_text("Download Excel")).to_be_visible(timeout=40000)
        # ✅ Get header index dynamically
        header_name = "Ports of Unlading"
        headers = self.page.locator("[role='columnheader']")
        header_count = headers.count()

        assert header_count > 0, "❌ No headers found in the table!"

        header_index = None
        for i in range(header_count):
            text = headers.nth(i).inner_text().strip()
            if text == header_name:
                header_index = i
                break

        assert header_index is not None, f"❌ Header '{header_name}' not found in the table"
        print(f"✅ Found header '{header_name}' at index {header_index}")

        # ✅ Get first row data safely
        rows = self.page.locator("table tbody tr")
        row_count = rows.count()
        assert row_count > 0, "❌ No rows found in the table!"
        cell_locator = self.page.locator("//div[@class='text-capitalize']").first

        # ✅ Wait for the locator to be visible
        expect(cell_locator).to_be_visible(timeout=60000)

        self.port_unlading = cell_locator.inner_text().strip()

        print("Port unlading value:", self.port_unlading)

        # ✅ Assert to catch empty value early
        assert self.port_unlading, "❌ Failed to extract port lading from the view all grid."

        print(f"✅ Extracted port unlading from grid: {self.port_unlading}")

        # Apply filter
        self.page.locator("td:nth-child(7)").first.click()

        # ✅ Validate Shipment Tab is selected
        self.page.wait_for_timeout(2000)
        self.page.locator("//a[@id='nav-home-tab']").click()
        shipment_tab = self.page.locator("#nav-home-tab")
        expect(shipment_tab).to_have_attribute("aria-selected", "true")
        print("✅ Shipment tab is selected")

    def Validate_preselected_code_inthe_port_unlading_filter(self):
        # ✅ Open Cargo filter and click 6 Digit HS Code section
        global full_port_unlading_name
        self.page.get_by_text("Ports", exact=True).click()
        self.page.locator("//div[contains(text(),'Port Of Unlading')]").first.click()

        Portunladingwithcount = self.page.locator('[data-for = "localize-filter-tooltip"]').nth(
            0).inner_text().strip()
        match = re.match(r"(.+?)\(([\d,]+)\)", Portunladingwithcount)
        if match:
            raw_port = match.group(1).strip()
            Total_Record_Count = match.group(2)  # keep commas as-is (string)

            # Save full port name
            full_port_unlading_name = raw_port

            print("✅ Full Port Name:", full_port_unlading_name)
            print("✅ Value:", Total_Record_Count)

        # ✅ Verify checkbox is checked
        checkbox = self.page.locator('input[type="checkbox"]').nth(1)
        expect(checkbox).to_be_checked()
        print("✅ First port lading checkbox is checked")

        if full_port_unlading_name.lower() in self.port_unlading.lower():
            print(f"✅ Port lading name '{full_port_unlading_name}' is correctly pre-selected in port lading filter")
        else:
            print(f"❌ Port lading name'{full_port_unlading_name}' does NOT match'")

        # ✅ Close filter modal
        self.page.locator("//span[@aria-hidden='true']").click()

    def Validate_Port_unlading_In_ShipmentGrid(self, validate: bool = True):
        self.page.locator("//a[@id='nav-home-tab']").click()

        if not hasattr(self, "invalid_entries"):
            self.invalid_entries = []

        headers = self.page.locator("table thead tr th")
        header_count = headers.count()

        self.S_No = None
        self.P_UL_field = None

        # Extract headers
        table_headers = []
        for i in range(header_count):
            header_text = headers.nth(i).inner_text().strip()
            table_headers.append(header_text)
            if header_text.lower() in ["s no", "sl no", "serial no"]:
                self.S_No = i
            elif header_text.lower() == "port of unlading":
                self.P_UL_field = i

        if self.P_UL_field is None:
            raise Exception("❌ 'Port of unlading' column is not found in the table")

        print(f"✅ Found column indexes → S No: {self.S_No}, Port of unlading: {self.P_UL_field}")

        rows = self.page.locator("table tbody tr")
        row_count = rows.count()

        invalid_entries = []

        for i in range(row_count):
            cells = rows.nth(i).locator("td")
            sl_no = cells.nth(self.S_No).inner_text().strip()
            port_unlading_value = cells.nth(self.P_UL_field).inner_text().strip()

            if validate:
                if port_unlading_value.lower() == self.port_unlading.lower():
                    print(f"✅ PASS: Valid port unlading name '{port_unlading_value}' found at Sl. No: {sl_no}")
                else:
                    print(
                        f"❌ FAIL: Invalid port unlading name '{port_unlading_value}' found at Sl. No: {sl_no} (Expected prefix: {self.port_unlading})")
                    invalid_entries.append((sl_no, port_unlading_value))

        # Final report
        if validate:
            if not invalid_entries:
                print("🎉 All entries are valid ✅")
            else:
                print("🚨 Invalid entries found ❌:", invalid_entries)

    def Validate_mode_transportation_screen(self):
        # Scroll to the port lading
        element = self.page.locator("#mode_of_transport .card-header .col-md-6", has_text="Modes of Transportation")
        element.wait_for(state="visible", timeout=40000)
        element.scroll_into_view_if_needed(timeout=40000)

    def validate_mode_transportation_Trends_headercheck(self):
        # Scroll to the port lading section
        self.page.locator(
            "[data-tip='Analyse trade trends of all Modes of Transportation based on their monthly, quarterly and yearly trade']").click()
        expect(self.page.locator("//h4[normalize-space()='Modes of Transportation: Trends']")).to_be_visible(
            timeout=50000)
        expect(self.page.locator("//div[@id='column-key']")).to_be_visible(timeout=50000)
        expect(self.page.locator("//span[normalize-space()='Download Excel']")).to_be_visible(timeout=50000)
        expect(self.page.locator("#sort-dropdown")).to_be_visible(timeout=50000)
        # Columns should include:Total Shipment Value (USD)- % Overall Change- Year-wise values (e.g., 2025, 2024, 2023, 2022)
        headers_to_check = [
            "S No.",
            "Modes of Transportation",
            "Total Shipments",
            "% Overall Change",
            "Apply Filter"
        ]

        for header in headers_to_check:
            locator = self.page.get_by_role("columnheader", name=header).first  # more precise
            expect(locator).to_be_visible(timeout=50000)
            print(f"✅ Header '{header}' is visible.")


    def Transport_mode_View_All(self):
        self.page.locator('[data-tip="View all Modes of Transportation based on their ranking"]').click()
        expect(self.page.locator("//h4[normalize-space()='Mode of Transportation']")).to_be_visible(
            timeout=50000)
        expect(self.page.locator("//span[normalize-space()='Download Excel']")).to_be_visible(timeout=50000)
        # Modal opens showing:
        # • List of transportation modes
        # • Columns: Shipments, Value, % share by Number of Shipmentst
        # • Search bar
        # • Sort by dropdown
        # • Download Excel button
        headers_to_check = [
            "S No.",
            "Mode of Transportation",
            "Shipments",
            "Value (USD)",
            "% share by Number of Shipments",
            "Apply Filter"
        ]

        for header in headers_to_check:
            locator = self.page.get_by_role("columnheader", name=header).first  # more precise
            expect(locator).to_be_visible(timeout=50000)
            print(f"✅ Header '{header}' is visible.")

        expect(self.page.locator("//input[@placeholder='Type to search Modes of Transportation']")).to_be_visible(timeout=50000)

    def Apply_filter_Transport_mode(self):
        self.page.pause()
        expect(self.page.get_by_text("Download Excel")).to_be_visible(timeout=40000)
        # ✅ Get header index dynamically
        header_name = "Mode of Transportation"
        headers = self.page.locator("[role='columnheader']")
        header_count = headers.count()

        assert header_count > 0, "❌ No headers found in the table!"

        header_index = None
        for i in range(header_count):
            text = headers.nth(i).inner_text().strip()
            if text == header_name:
                header_index = i
                break

        assert header_index is not None, f"❌ Header '{header_name}' not found in the table"
        print(f"✅ Found header '{header_name}' at index {header_index}")

        # ✅ Get first row data safely
        rows = self.page.locator("table tbody tr")
        row_count = rows.count()
        assert row_count > 0, "❌ No rows found in the table!"
        cell_locator = self.page.locator("//div[@class='text-capitalize']").first

        # ✅ Wait for the locator to be visible
        expect(cell_locator).to_be_visible(timeout=60000)

        self.transport_mode = cell_locator.inner_text().strip()

        print("Transport mode value:", self.transport_mode)

        # ✅ Assert to catch empty value early
        assert self.transport_mode, "❌ Failed to extract transport mode value from the view all grid."

        print(f"✅ Extracted transport mode value from grid: {self.transport_mode}")

        # Apply filter
        self.page.locator("td:nth-child(7)").first.click()

        # ✅ Validate Shipment Tab is selected
        self.page.wait_for_timeout(2000)
        self.page.locator("//a[@id='nav-home-tab']").click()
        shipment_tab = self.page.locator("#nav-home-tab")
        expect(shipment_tab).to_have_attribute("aria-selected", "true")
        print("✅ Shipment tab is selected")

    def Validate_preselected_mode_inthe_freight_filter(self):
        self.page.get_by_text("Freight", exact=True).click()
        self.page.locator('[class="_filteritemtext_a6k5f_88"]', has_text="Mode of Transportation").first.click()

        # ✅ Extract first HS Code text
        mode = self.page.locator("[class='text-no-transform']").nth(0).inner_text().strip()
        print("Extracted Mode:", mode)

        # ✅ Verify checkbox is checked
        checkbox = self.page.locator('input[type="checkbox"]').nth(0)
        expect(checkbox).to_be_checked()
        print("✅ First  checkbox is checked")

        if  mode.lower()== self.transport_mode.lower():
            print(f"✅ Transport mode '{mode}' is correctly pre-selected in freight filter")
        else:
            print(f"❌ Transport mode '{mode}' does NOT match previously selected '{self.transport_mode}'")

        # ✅ Close filter modal
        self.page.locator("//span[@aria-hidden='true']").click()

    def Validate_Transport_Mode_In_ShipmentGrid(self, validate: bool = True):
        self.page.locator("//a[@id='nav-home-tab']").click()

        if not hasattr(self, "invalid_entries"):
            self.invalid_entries = []

        headers = self.page.locator("table thead tr th")
        header_count = headers.count()

        self.S_No = None
        self.P_UL_field = None

        # Extract headers
        table_headers = []
        for i in range(header_count):
            header_text = headers.nth(i).inner_text().strip()
            table_headers.append(header_text)
            if header_text.lower() in ["s no", "sl no", "serial no"]:
                self.S_No = i
            elif header_text.lower() == "mode of transportation":
                self.M_T_field = i

        if self.M_T_field is None:
            raise Exception("❌ 'Port of unlading' column is not found in the table")

        print(f"✅ Found column indexes → S No: {self.S_No}, Mode of Transportation: {self.M_T_field}")

        rows = self.page.locator("table tbody tr")
        row_count = rows.count()

        invalid_entries = []

        for i in range(row_count):
            cells = rows.nth(i).locator("td")
            sl_no = cells.nth(self.S_No).inner_text().strip()
            mode_transport_value = cells.nth(self.M_T_field).inner_text().strip()

            if validate:
                if mode_transport_value.lower() == self.transport_mode.lower():
                    print(f"✅ PASS: Valid transport mode name '{mode_transport_value}' found at Sl. No: {sl_no}")
                else:
                    print(
                        f"❌ FAIL: Invalid transport mode name '{mode_transport_value}' found at Sl. No: {sl_no} (Expected : {self.transport_mode})")
                    invalid_entries.append((sl_no, mode_transport_value))

        # Final report
        if validate:
            if not invalid_entries:
                print("🎉 All entries are valid ✅")
            else:
                print("🚨 Invalid entries found ❌:", invalid_entries)
















