import os
import re

from openpyxl import Workbook
from openpyxl.styles import PatternFill
from playwright.sync_api import Page, expect
from playwright.sync_api import expect, TimeoutError as PlaywrightTimeoutError
invalid_entries =[]
import pytest

def split_location(text: str):
    # Remove commas and extra spaces
    clean_text = text.replace(",", " ").strip()

    # Split into words
    parts = clean_text.split()

    return parts
class Search:
    def __init__(self, page: Page):
        self.port_name_hyperlink = None
        self.page = page
        self.invalid_consignee_entries = []

    def Close_button(self):
        close_locator = self.page.locator('[class="tw-mt-6 tw-cursor-pointer"]').first
        self.page.wait_for_timeout(5000)
        if close_locator.is_visible(timeout=40000):
            print("🔍 'close' is visible, clicking...")
            close_locator.click()
            expect(self.page.get_by_placeholder(
                "Type to search in all categories or choose from the category below")).to_be_visible()
        else:
            print("ℹ️ 'Close' button is not visible.")

    def auto_suggest_hs_code_search(self, hs_code: str):
        """Test HS Code search functionality"""
        print(f"Testing autosuggest HS Code search for: {hs_code}")
        self.page.pause()
        #Select category HS Code, enter keyword, and select from autosuggest
        self.page.get_by_role("textbox", name="Type to search in all").click()
        expect(self.page.get_by_placeholder("Type to search in all categories or choose from the category below")).to_be_visible()
        self.page.wait_for_timeout(3000)
        self.page.get_by_text("HS Code", exact=True).first.click()
        self.page.get_by_role("textbox", name="Search upto 20 Harmonised").fill(hs_code)
        #select value from autosuggest
        #store hs code in a variable
        self.selected_hs_code = self.page.locator('[class="tw-font-medium tw-bg-transparent tw-p-0"]').nth(0).inner_text().strip()
        self.page.locator('[class="tw-font-medium tw-bg-transparent tw-p-0"]').nth(0).click()
        print(f"Selected HS Code is: {self.selected_hs_code}")


        # Ensure Exact Phrase match type is selected
        exact_phrase_text = self.page.locator(".tw-text-nowrap > span").text_content()
        if "Exact Phrase" not in exact_phrase_text:
            self.page.locator("div").filter(has_text=re.compile(r"^Contains$")).nth(2).click()
            #self.page.get_by_text("Exact Phrase").first.click()
            self.page.locator('[class=" css-10xa8g5-option"]').first.click()

        self.page.locator(".tw-bg-primary-purple-500").click()

        # Verify results
        expect(self.page.locator("a.btn-link.trademo-link").first).to_have_text(f"HS: {hs_code}")

    def auto_suggest_hs_code_search_save_search(self, hs_code: str):
        """Test HS Code search functionality"""
        print(f"Testing autosuggest HS Code search for: {hs_code}")

        # Select category HS Code, enter keyword, and select from autosuggest
        self.page.get_by_role("textbox", name="Type to search in all").click()
        expect(self.page.get_by_placeholder(
            "Type to search in all categories or choose from the category below")).to_be_visible()
        self.page.wait_for_timeout(3000)
        self.page.get_by_text("HS Code", exact=True).first.click()
        self.page.get_by_role("textbox", name="Search upto 20 Harmonised").fill(hs_code)
        # select value from autosuggest
        # store hs code in a variable
        self.selected_hs_code = self.page.locator('[class="tw-font-medium tw-bg-transparent tw-p-0"]').nth(
            0).inner_text().strip()
        self.page.locator('[class="tw-font-medium tw-bg-transparent tw-p-0"]').nth(0).click()
        print(f"Selected HS Code is: {self.selected_hs_code}")

        self.page.locator(".tw-bg-primary-purple-500").click()

    def check_hs_code_in_shipmentgrid(self, validate: bool = True, use_pagination: bool = False):
        shipment_tab = self.page.locator("//a[@id='nav-home-tab']")
        if not shipment_tab.is_visible(timeout=10000):  # wait max 5s for results
            print("❌ No search results found in Shipment Grid.")
            return []
        self.page.locator("//a[@id='nav-home-tab']").click(timeout=40000)

        if not hasattr(self, "invalid_entries"):
            self.invalid_entries = []

        headers = self.page.locator("table thead tr th")
        header_count = headers.count()

        self.S_No = None
        self.HS_Code_field = None
        self.Matching_Field = None

        # --- Extract headers dynamically ---
        table_headers = []
        for i in range(header_count):
            header_text = headers.nth(i).inner_text().strip()
            table_headers.append(header_text)

            if header_text.lower() in ["s no", "sl no", "serial no"]:
                self.S_No = i
            elif header_text.lower() == "hs code":
                self.HS_Code_field = i
            elif header_text.lower() in ["matching fields", "matching field"]:
                self.Matching_Field = i

        if self.S_No is None:
            raise Exception("❌ 'S No' column not found in table headers")
        if self.HS_Code_field is None:
            raise Exception("❌ 'HS Code' column not found in table headers")
        if self.Matching_Field is None:
            raise Exception("❌ 'Matching Field' column not found in table headers")

        print(
            f"✅ Found column indexes → S No: {self.S_No}, HS Code: {self.HS_Code_field}, Matching Field: {self.Matching_Field}")

        all_rows_data = []

        # --- function to process a page ---
        def process_current_page():
            rows = self.page.locator("table tbody tr")
            row_count = rows.count()

            for i in range(row_count):
                row_data = []
                cells = rows.nth(i).locator("td")
                cell_count = cells.count()

                for j in range(cell_count):
                    row_data.append(cells.nth(j).inner_text().strip())

                validation_note = ""  # extra Excel column

                if validate:
                    sl_no = row_data[self.S_No]
                    hs_code = row_data[self.HS_Code_field]
                    matching_field = row_data[self.Matching_Field]

                    # ✅ Validate HS Code
                    if hs_code.startswith(self.selected_hs_code):
                        print(f"✅ PASS: HS Code '{hs_code}' at Sl. No: {sl_no}")
                    else:
                        print(
                            f"❌ FAIL: Invalid HS Code '{hs_code}' at Sl. No: {sl_no} (Expected prefix: {self.selected_hs_code})")
                        self.invalid_entries.append({"slNo": sl_no, "HS Code": hs_code, "Matching": matching_field})
                        validation_note = "❌ Invalid HS Code"

                    # ✅ Validate Matching Field
                    if matching_field.lower() == "hs code":
                        print(f"✅ PASS: Matching field '{matching_field}' at Sl. No: {sl_no}")
                    else:
                        print(f"❌ FAIL: Invalid Matching field '{matching_field}' at Sl. No: {sl_no}")
                        self.invalid_entries.append({"slNo": sl_no, "HS Code": hs_code, "Matching": matching_field})
                        validation_note = (
                                              validation_note + " | " if validation_note else "") + "❌ Invalid Matching Field"

                row_data.append(validation_note)
                all_rows_data.append(row_data)

        # --- Pagination ---
        if use_pagination:
            while True:
                process_current_page()
                next_button = self.page.locator('[class="trademo-table-arrow-button"]').nth(1)
                if next_button.is_enabled():
                    next_button.click()
                    self.page.locator("table tbody tr td:nth-child(1)").first.wait_for(
                        state="visible", timeout=100000
                    )
                else:
                    break
        else:
            process_current_page()

        # --- Save to Excel only if invalid entries exist ---
        if self.invalid_entries:
            os.makedirs("results", exist_ok=True)
            workbook = Workbook()
            sheet = workbook.active
            sheet.title = "HS Code Data"

            # Add "Validation" column
            sheet.append(table_headers + ["Validation"])

            red_fill = PatternFill(start_color="FF0000", end_color="FF0000", fill_type="solid")

            for row_data in all_rows_data:
                sheet.append(row_data)
                if row_data and "Invalid" in row_data[-1]:
                    # Highlight HS Code + Matching Field columns
                    hs_col_index = self.HS_Code_field + 1
                    match_col_index = self.Matching_Field + 1
                    sheet.cell(row=sheet.max_row, column=hs_col_index).fill = red_fill
                    sheet.cell(row=sheet.max_row, column=match_col_index).fill = red_fill

            file_path = f"results/search_page_{self.selected_hs_code}.xlsx"
            workbook.save(file_path)
            print(f"📁 All rows saved to {file_path} (invalid HS Codes highlighted in red)")
        else:
            print("📘 No invalid HS Codes found. Excel not generated.")

        return self.invalid_entries

    def Validate_Discover_Insights(self):
        shipment_tab = self.page.locator("//a[@id='nav-home-tab']")
        if not shipment_tab.is_visible(timeout=10000):  # wait max 5s for results
            print("❌ No search results found in Shipment Grid.")
            return []
        with self.page.expect_popup() as page1_info:
            self.page.get_by_text("HS:").click()
        page1 = page1_info.value
        expect(page1.get_by_role("heading")).to_contain_text(f"HS Code - {self.selected_hs_code}")
        page1.close()

    def auto_suggest_product_search(self , product_name:str):
        """Test Product search functionality"""
        #Select category Product, enter keyword, and select from autosuggest
        print(f"Testing Product search for: {product_name}")
        self.page.get_by_role("textbox", name="Type to search in all").click()
        self.page.get_by_text("Product", exact=True).click()
        self.page.get_by_role("textbox", name="Search for 20 commodities such as Apple, Laptops").fill(product_name)
        self.selected_product = self.page.locator('[class="tw-font-medium tw-bg-transparent tw-p-0"]').nth(
            0).inner_text().strip()
        self.page.locator('[class="tw-font-medium tw-bg-transparent tw-p-0"]').nth(0).click()
        print(f"Selected product is: {self.selected_product}")
        #Click on Apply button
        self.page.locator(".tw-bg-primary-purple-500").click()

        self.page.locator("//a[@id='nav-home-tab']").click()
        self.page.wait_for_timeout(2000)
        self.page.locator("table tbody tr td:nth-child(4)").first.wait_for(state="visible", timeout=100000)

    def check_product_description_in_shipment_grid(self, validate: bool = True, use_pagination: bool = False):
        """Check product descriptions across shipment grid pages"""
        self.page.pause()
        shipment_tab = self.page.locator("//a[@id='nav-home-tab']")
        if not shipment_tab.is_visible(timeout=10000):  # wait max 5s for results
            print("❌ No search results found in Shipment Grid.")
            return []
        self.page.locator("//a[@id='nav-home-tab']").click(timeout=40000)
        if not hasattr(self, "invalid_entries"):
            self.invalid_entries = []

        headers = self.page.locator("table thead tr th")
        header_count = headers.count()

        self.S_No = None
        self.Matching_field = None
        self.Product_field = None

        # --- Extract headers ---
        table_headers = []
        for i in range(header_count):
            header_text = headers.nth(i).inner_text().strip()
            table_headers.append(header_text)

            if header_text.lower() in ["s no", "sl no", "serial no"]:
                self.S_No = i
            elif "matching" in header_text.lower():
                self.Matching_field = i
            elif header_text.lower() in ["product description", "description"]:
                self.Product_field = i

        if self.S_No is None:
            raise Exception("❌ 'S No' column not found in table headers")
        if self.Matching_field is None:
            raise Exception("❌ 'Matching Field' column not found in table headers")
        if self.Product_field is None:
            raise Exception("❌ 'Product Description' column not found in table headers")

        print(
            f"✅ Found column indexes → S No: {self.S_No}, Matching: {self.Matching_field}, Product: {self.Product_field}")

        all_rows_data = []  # store all rows with full column values
        keywords = self.selected_product.lower().split()  # e.g. "lab coat" -> ["lab", "coat"]

        # --- function to extract and validate current page ---
        def process_current_page():
            rows = self.page.locator("table tbody tr")
            row_count = rows.count()

            for i in range(row_count):
                row_data = []
                cells = rows.nth(i).locator("td")
                cell_count = cells.count()

                for j in range(cell_count):
                    cell_text = cells.nth(j).inner_text().strip()
                    row_data.append(cell_text)

                validation_note = ""  # extra column for Excel

                if validate:
                    sl_no = row_data[self.S_No]
                    matching_field = row_data[self.Matching_field]

                    # Handle tooltip product description if present
                    product_span = rows.nth(i).locator("td").nth(self.Product_field).locator("[data-tip]").first
                    product_tip = product_span.get_attribute("data-tip") if product_span.count() > 0 else None
                    product = product_tip.strip() if product_tip else rows.nth(i).locator("td").nth(
                        self.Product_field).inner_text().strip()

                    print(f"🔎 Checking product: {product}")

                    row_data[self.Product_field] = product  # overwrite with tooltip if found

                    # ✅ Keyword validation
                    if any(k in product.lower() for k in keywords):
                        print(f"✅ PASS: Product matches → {product} at sl.No: {sl_no}")
                    else:
                        print(f"❌ FAIL: Invalid product → {product} at sl.No: {sl_no}")
                        self.invalid_entries.append({"slNo": sl_no, "Product": product})
                        validation_note = "❌ Invalid Product"

                    # ✅ Matching field validation
                    if matching_field.lower() == "product description":
                        print(f"✅ Shows Matching field as {matching_field} at sl.No: {sl_no}")
                    else:
                        print(f"❌ FAIL: Invalid matching field → {matching_field} at sl.No: {sl_no}")
                        self.invalid_entries.append({"slNo": sl_no, "MatchingField": matching_field})
                        validation_note = "❌ Invalid Matching Field"

                row_data.append(validation_note)
                all_rows_data.append(row_data)

        # --- handle pagination if enabled ---
        if use_pagination:
            while True:
                process_current_page()
                next_button = self.page.locator('[class="trademo-table-arrow-button"]').nth(1)
                if next_button.is_enabled():
                    next_button.click()
                    self.page.locator("table tbody tr td:nth-child(1)").first.wait_for(
                        state="visible", timeout=100000
                    )
                else:
                    break
        else:
            process_current_page()

        # --- save to Excel only if failures ---
        if self.invalid_entries:
            os.makedirs("results", exist_ok=True)
            workbook = Workbook()
            sheet = workbook.active
            sheet.title = "Product Data"

            # Write headers (+ extra validation column)
            sheet.append(table_headers + ["Validation"])

            red_fill = PatternFill(start_color="FF0000", end_color="FF0000", fill_type="solid")

            for row_data in all_rows_data:
                sheet.append(row_data)
                if row_data and "Invalid" in row_data[-1]:
                    prod_col_index = self.Product_field + 1
                    sheet.cell(row=sheet.max_row, column=prod_col_index).fill = red_fill

            file_path = f"results/product_data_{self.selected_product}.xlsx"
            workbook.save(file_path)
            print(f"📁 All rows saved to {file_path} (invalid products highlighted in red)")
        else:
            print("📘 No invalid product description found. Excel not generated.")

        return self.invalid_entries

    def auto_suggest_shipper_search(self, shipper_name: str):
        """Test Shipper search functionality"""
        print(f"Testing Shipper search for: {shipper_name}")
        self.page.get_by_role("textbox", name="Type to search in all").click()
        self.page.locator("(//div[contains(text(),'Shipper')])[1]").click()
        self.page.get_by_role("textbox", name="Search upto 20 Shipper's name or address").fill(shipper_name)
        self.page.wait_for_timeout(3000)
        self.selected_shipper = self.page.locator('[class="tw-font-medium tw-bg-transparent tw-p-0"]').nth(
            0).inner_text().strip()
        self.page.locator('[class="tw-font-medium tw-bg-transparent tw-p-0"]').nth(0).click()
        print(f"Selected shipper name is: {self.selected_shipper}")
        #click on search button
        self.page.locator(".tw-bg-primary-purple-500").click()

    def Validate_exporter_tab(self):
        shipment_tab = self.page.locator("//a[@id='nav-home-tab']")
        if not shipment_tab.is_visible(timeout=10000):  # wait max 5s for results
            print("❌ No search results found in Shipment Grid.")
            return []
        # Navigate to exporter tab
        self.page.locator("//a[@id='nav-contact-tab']").click()

        # Verify The Exporters tab label should update to Exporters (1) and display the selected Shipper name under the Company Name section
        total_record = self.page.locator(".trademo-table-count-text").inner_text().strip()
        total_count = total_record.split("of")[-1].strip()
        expect(self.page.locator(
            '[class=" tw-text-xs tw-p-1 tw-rounded tw-bg-primary-purple-100 tw-text-primary-purple-600 tw-font-medium"]')).to_have_text(
            total_count)

    def check_shipper_name_export_tab(self, validate: bool = True):
        """Check shipper names across all pages and collect invalid entries"""
        export_tab =  self.page.locator("//a[@id='nav-contact-tab']")
        if not export_tab.is_visible(timeout=10000):  # wait max 5s for results
            print("❌ No search results found in Shipment Grid.")
            return []
        rows = self.page.locator("table tbody tr")
        row_count = rows.count()

        if validate:
            for i in range(row_count):
                sl_no = rows.nth(i).locator("td").nth(1).inner_text().strip()

                # Get company name from data-tip or fallback to visible text
                company_cell = rows.nth(i).locator("td").nth(2)
                company_name_locator = company_cell.locator("[data-tip]").first
                company_tip = (
                    company_name_locator.get_attribute("data-tip")
                    if company_name_locator.count() > 0 else None
                )

                company = (
                    company_tip.strip()
                    if company_tip and company_tip.strip()
                    else company_cell.inner_text().strip()
                )

                print(f"Checking company: {company}")

                expected_normalized = self.selected_shipper.lower()
                actual_normalized = re.sub(r"\s+", " ", company).strip().lower()

                if actual_normalized == expected_normalized:
                    print(f"✅ Valid company name found: {company} at Sl. No: {sl_no}")
                else:
                    print(f"❌ Invalid company name found: {company} at Sl. No: {sl_no}")

    def validate_duplicate_country_names(self):
        shipment_tab = self.page.locator("//a[@id='nav-home-tab']")
        if not shipment_tab.is_visible(timeout=10000):  # wait max 5s for results
            print("❌ No search results found in Shipment Grid.")
            return []
        # Locate all company names in the "Company Name" column
        country_elements = self.page.locator("//div[img[@class='trademo-search-flag mr-2']]")
        count = country_elements.count()

        print(f"🔍 Total countries found: {count -1}")

        seen = set()
        duplicates = []

        for i in range(count):
            name = country_elements.nth(i).inner_text().strip()

            if name in seen:
                print(f"❌ Duplicate found: '{name}' at row {i}")
                duplicates.append(name)
            else:
                seen.add(name)

        if not duplicates:
            print("✅ No duplicate country names found!")
        else:
            print(f"⚠️ Total Duplicates Found: {len(duplicates)} -> {duplicates}")

    def normalize_company_name(self, name: str) -> str:
        """
        Normalize company names by shortening common terms.
        Example: "Limited" → "Ltd", "Company" → "Co".
        """
        # Lowercase and strip spaces
        name = name.lower().strip()

        # Replace common full forms with abbreviations
        replacements = {
            r"\blimited\b": "ltd",
        }

        for pattern, replacement in replacements.items():
            name = re.sub(pattern, replacement, name)

        # Collapse multiple spaces
        name = re.sub(r"\s+", " ", name)

        return name

    def check_Shipper_Name_in_theGrid_View(self, validate: bool = True, use_pagination: bool = False):
        """Check shipper names across all pages and collect invalid entries"""
        shipment_tab = self.page.locator("//a[@id='nav-home-tab']")
        if not shipment_tab.is_visible(timeout=10000):  # wait max 5s for results
            print("❌ No search results found in Shipment Grid.")
            return []
        self.page.locator("//a[@id='nav-home-tab']").click()

        if not hasattr(self, "invalid_shipper_entries"):
            self.invalid_shipper_entries = []

        headers = self.page.locator("table thead tr th")
        header_count = headers.count()

        self.S_No = None
        self.Shipper_field = None

        # --- Extract headers ---
        table_headers = []
        for i in range(header_count):
            header_text = headers.nth(i).inner_text().strip()
            table_headers.append(header_text)
            if header_text.lower() in ["s no", "sl no", "serial no"]:
                self.S_No = i
            elif "shipper" in header_text.lower():
                self.Shipper_field = i

        if self.S_No is None:
            raise Exception("❌ 'S No' column not found in table headers")
        if self.Shipper_field is None:
            raise Exception("❌ 'Shipper name' column not found in table headers")

        print(f"✅ Found column indexes → S No: {self.S_No}, Shipper Name: {self.Shipper_field}")

        all_rows_data = []

        # --- Function to process one page ---
        def process_current_page():
            rows = self.page.locator("table tbody tr")
            row_count = rows.count()

            for i in range(row_count):
                row_data = []
                cells = rows.nth(i).locator("td")
                cell_count = cells.count()

                for j in range(cell_count):
                    cell_text = cells.nth(j).inner_text().strip()
                    row_data.append(cell_text)

                validation_note = ""
                if validate:
                    shipper_name = row_data[self.Shipper_field]
                    expected = self.normalize_company_name(self.selected_shipper)
                    actual = self.normalize_company_name(shipper_name)
                    sl_no = row_data[self.S_No]

                    if expected == actual:
                        print(f"✅ PASS: Correct shipper name '{actual}' at Sl. No: {sl_no}")
                    else:
                        print(f"❌ FAIL: Invalid shipper name '{shipper_name}' at Sl. No: {sl_no} "
                              f"(Expected: {self.selected_shipper})")
                        self.invalid_shipper_entries.append({"slNo": sl_no, "Company": shipper_name})
                        validation_note = "❌ Invalid Shipper Name"

                row_data.append(validation_note)
                all_rows_data.append(row_data)

        # --- Handle pagination if enabled ---
        if use_pagination:
            while True:
                process_current_page()
                next_button = self.page.locator('[class="trademo-table-arrow-button"]').nth(1)
                if next_button.is_enabled():
                    next_button.click()
                    self.page.locator("table tbody tr td:nth-child(1)").first.wait_for(
                        state="visible", timeout=100000
                    )
                else:
                    break
        else:
            process_current_page()

        # --- Save to Excel only if invalid found ---
        if self.invalid_shipper_entries:
            os.makedirs("results", exist_ok=True)
            workbook = Workbook()
            sheet = workbook.active
            sheet.title = "Shipper Data"

            sheet.append(table_headers + ["Validation"])

            red_fill = PatternFill(start_color="FF0000", end_color="FF0000", fill_type="solid")

            for row_data in all_rows_data:
                sheet.append(row_data)
                if row_data and "Invalid" in row_data[-1]:
                    shipper_col_index = self.Shipper_field + 1
                    sheet.cell(row=sheet.max_row, column=shipper_col_index).fill = red_fill

            file_path = f"results/shipper_data_{self.selected_shipper}.xlsx"
            workbook.save(file_path)
            print(f"📁 All rows saved to {file_path} (invalid shipper names highlighted in red)")

        else:
            print("📘 No invalid shipper name found. Excel not generated.")

        return self.invalid_shipper_entries

    def Validate_Discover_insight_link(self):
        shipment_tab = self.page.locator("//a[@id='nav-home-tab']")
        if not shipment_tab.is_visible(timeout=10000):  # wait max 5s for results
            print("❌ No search results found in Shipment Grid.")
            return []
        shipment_tab = self.page.locator("//a[@id='nav-home-tab']")
        if not shipment_tab.is_visible(timeout=10000):  # wait max 5s for results
            print("❌ No search results found in Shipment Grid.")
            return []
        expect(self.page.locator('[class="btn-link trademo-link text-capitalize"]')).to_have_text(self.selected_shipper.lower())

        # Test insights link
        with self.page.expect_popup() as page1_info:
            self.page.locator("a").filter(has_text=self.selected_shipper.lower()).click()
        page1 = page1_info.value
        expect(page1.get_by_role("main")).to_contain_text(self.selected_shipper , ignore_case=True)
        page1.close()
        self.page.locator("table tbody tr td:nth-child(4)").first.wait_for(state="visible", timeout=100000)


    def auto_suggest_consignee_search(self , consignee_name:str):
        """Test Consignee search functionality"""
        print(f"Testing Consignee search for: {consignee_name}")

        self.page.get_by_role("textbox", name="Type to search in all").click()
        self.page.locator("(//div[contains(text(),'Consignee')])[1]").click()
        self.page.get_by_role("textbox", name="Search upto 20 Consignee's name or address").fill(consignee_name)
        self.page.wait_for_timeout(3000)
        self.selected_consignee = self.page.locator('[class="tw-font-medium tw-bg-transparent tw-p-0"]').nth(
            0).inner_text().strip()
        self.page.locator('[class="tw-font-medium tw-bg-transparent tw-p-0"]').nth(0).click()
        print(f"Selected consignee name is: {self.selected_consignee}")
        # click on search button
        self.page.locator(".tw-bg-primary-purple-500").click()

    def Validate_importer_tab(self):
        shipment_tab = self.page.locator("//a[@id='nav-home-tab']")
        if not shipment_tab.is_visible(timeout=10000):  # wait max 5s for results
            print("❌ No search results found in Shipment Grid.")
            return []
        # Navigate to importer tab
        self.page.locator("//a[@id='nav-profile-tab']").click()

        # Verify results
        total_record = self.page.locator(".trademo-table-count-text").inner_text().strip()
        total_count = total_record.split("of")[-1].strip()
        expect(self.page.locator(
            '[class=" tw-text-xs tw-p-1 tw-rounded tw-bg-primary-purple-100 tw-text-primary-purple-600 tw-font-medium"]')).to_have_text(
            total_count)

    def Validate_Discover_insight_consignee(self):
        shipment_tab = self.page.locator("//a[@id='nav-home-tab']")
        if not shipment_tab.is_visible(timeout=10000):  # wait max 5s for results
            print("❌ No search results found in Shipment Grid.")
            return []
        # Test insights link
        with self.page.expect_popup() as page2_info:
            self.page.locator("a").filter(has_text=self.selected_consignee.lower()).click()
        page2 = page2_info.value
        expect(page2.get_by_role("main")).to_contain_text(self.selected_consignee, ignore_case=True)
        page2.close()
        self.page.locator("table tbody tr td:nth-child(4)").first.wait_for(state="visible", timeout=100000)

    def check_Consignee_Name_in_theGrid_View(self, validate: bool = True, use_pagination: bool = False):
        """Check shipper names across all pages and collect invalid entries"""
        shipment_tab = self.page.locator("//a[@id='nav-home-tab']")
        if not shipment_tab.is_visible(timeout=10000):  # wait max 5s for results
            print("❌ No search results found in Shipment Grid.")
            return []
        self.page.locator("//a[@id='nav-home-tab']").click()

        if not hasattr(self, "invalid_consignee_entries"):
            self.invalid_consignee_entries = []

        headers = self.page.locator("table thead tr th")
        header_count = headers.count()

        self.S_No = None
        self.Consignee_field = None

        # --- Extract headers ---
        table_headers = []
        for i in range(header_count):
            header_text = headers.nth(i).inner_text().strip()
            table_headers.append(header_text)
            if header_text.lower() in ["s no", "sl no", "serial no"]:
                self.S_No = i
            elif "consignee" in header_text.lower():
                self.Consignee_field = i

        if self.S_No is None:
            raise Exception("❌ 'S No' column not found in table headers")
        if self.Consignee_field is None:
            raise Exception("❌ 'Consignee name' column not found in table headers")

        print(f"✅ Found column indexes → S No: {self.S_No}, Consignee Name: {self.Consignee_field}")

        all_rows_data = []

        # --- Function to process one page ---
        def process_current_page():
            rows = self.page.locator("table tbody tr")
            row_count = rows.count()

            for i in range(row_count):
                row_data = []
                cells = rows.nth(i).locator("td")
                cell_count = cells.count()

                for j in range(cell_count):
                    cell_text = cells.nth(j).inner_text().strip()
                    row_data.append(cell_text)

                validation_note = ""
                if validate:
                    consignee_name = row_data[self.Consignee_field]
                    expected = self.normalize_company_name(self.selected_consignee)
                    actual = self.normalize_company_name(consignee_name)
                    sl_no = row_data[self.S_No]

                    if expected == actual:
                        print(f"✅ PASS: Correct consignee name '{actual}' at Sl. No: {sl_no}")
                    else:
                        print(f"❌ FAIL: Invalid consignee name '{consignee_name}' at Sl. No: {sl_no} "
                              f"(Expected: {self.selected_consignee})")
                        self.invalid_shipper_entries.append({"slNo": sl_no, "Company": consignee_name})
                        validation_note = "❌ Invalid Consignee Name"

                row_data.append(validation_note)
                all_rows_data.append(row_data)

        # --- Handle pagination if enabled ---
        if use_pagination:
            while True:
                process_current_page()
                next_button = self.page.locator('[class="trademo-table-arrow-button"]').nth(1)
                if next_button.is_enabled():
                    next_button.click()
                    self.page.locator("table tbody tr td:nth-child(1)").first.wait_for(
                        state="visible", timeout=100000
                    )
                else:
                    break
        else:
            process_current_page()

        # --- Save to Excel only if invalid found ---
        if self.invalid_consignee_entries:
            os.makedirs("results", exist_ok=True)
            workbook = Workbook()
            sheet = workbook.active
            sheet.title = "Consignee Data"

            sheet.append(table_headers + ["Validation"])

            red_fill = PatternFill(start_color="FF0000", end_color="FF0000", fill_type="solid")

            for row_data in all_rows_data:
                sheet.append(row_data)
                if row_data and "Invalid" in row_data[-1]:
                    consignee_col_index = self.Consignee_field + 1
                    sheet.cell(row=sheet.max_row, column=consignee_col_index).fill = red_fill

            file_path = f"results/consignee_data_{self.selected_consignee}.xlsx"
            workbook.save(file_path)
            print(f"📁 All rows saved to {file_path} (invalid consignee names highlighted in red)")

        else:
            print("📘 No invalid consignee name found. Excel not generated.")

        return self.invalid_consignee_entries

    def check_consignee_Name_Import_tab(self, validate: bool = True):
        """Check consignee names across shipment grid pages and collect invalid entries"""
        shipment_tab = self.page.locator("//a[@id='nav-home-tab']")
        if not shipment_tab.is_visible(timeout=10000):  # wait max 5s for results
            print("❌ No search results found in Shipment Grid.")
            return []
        rows = self.page.locator("table tbody tr")
        row_count = rows.count()

        if validate:
            for i in range(row_count):
                sl_no = rows.nth(i).locator("td").nth(1).inner_text().strip()

                # Try to get 'data-tip' first
                consignee_cell = rows.nth(i).locator("td").nth(2)
                consignee_locator = consignee_cell.locator("[data-tip]").first
                consignee_tip = (
                    consignee_locator.get_attribute("data-tip")
                    if consignee_locator.count() > 0 else None
                )

                consignee_name = (
                    consignee_tip.strip()
                    if consignee_tip and consignee_tip.strip()
                    else consignee_cell.inner_text().strip()
                )

                consignee_name_lower = re.sub(r"\s+", " ", consignee_name).strip().lower()
                expected_lower = self.selected_consignee.lower()

                print(f"Consignee: {consignee_name}")

                if consignee_name_lower == expected_lower:
                    print(f"✅ Valid consignee name found: {consignee_name} at Sl. No: {sl_no}")
                else:
                    print(f"❌ Invalid consignee name found: {consignee_name} at Sl. No: {sl_no}")

    def Chemical_Search_auto_suggest(self,chemical:str):
        expect(self.page.get_by_placeholder(
            "Type to search in all categories or choose from the category below")).to_be_visible()
        self.page.get_by_role("textbox", name="Type to search in all").click()
        # Select category Chemical, enter keyword, and select from autosuggest
        self.page.locator("(//div[normalize-space()='Chemicals'])[1]").click()
        self.page.get_by_role("textbox", name="Search upto 20 Chemical").fill(chemical)
        self.selected_chemical = self.page.locator('[class="tw-font-medium tw-bg-transparent tw-p-0"]').nth(
            0).inner_text().strip()
        self.page.locator('[class="tw-font-medium tw-bg-transparent tw-p-0"]').nth(0).click()
        print(f"Selected chemical name is: {self.selected_chemical}")
        # click on search button
        self.page.locator(".tw-bg-primary-purple-500").click()

    def Check_Chemical_In_shipmentGrid(self, validate: bool = True, use_pagination: bool = False):
        shipment_tab = self.page.locator("//a[@id='nav-home-tab']")
        if not shipment_tab.is_visible(timeout=10000):  # wait max 5s for results
            print("❌ No search results found in Shipment Grid.")
            return []
        self.page.locator("//a[@id='nav-home-tab']").click()
        self.page.locator("table tbody tr td:nth-child(4)").first.wait_for(state="visible", timeout=100000)

        if not hasattr(self, "invalid_entries"):
            self.invalid_entries = []

        # --- Find header indexes dynamically ---
        headers = self.page.locator("table thead tr th")
        header_count = headers.count()

        self.S_No = None
        self.M_field = None
        self.P_desc = None

        table_headers = []
        for i in range(header_count):
            header_text = headers.nth(i).inner_text().strip()
            table_headers.append(header_text)
            if header_text.lower() in ["s no", "sl no", "serial no"]:
                self.S_No = i
            elif header_text.lower() == "matching fields":
                self.M_field = i
            elif header_text.lower() in ["product description", "description"]:
                self.P_desc = i

        if self.S_No is None:
            raise Exception("❌ 'S No' column not found in table headers")
        if self.M_field is None:
            raise Exception("❌ 'Matching Fields' column not found in table headers")
        if self.P_desc is None:
            raise Exception("❌ 'Product Description' column not found in table headers")

        print(f"✅ Found column indexes → S No: {self.S_No}, Matching Field: {self.M_field}, Product: {self.P_desc}")

        all_rows_data = []  # store all rows with extra Validation col
        keywords = self.selected_chemical.lower().split()

        # --- Define function to process current page ---
        def process_current_page():
            rows = self.page.locator("table tbody tr")
            row_count = rows.count()

            for i in range(row_count):
                row_data = []
                cells = rows.nth(i).locator("td")
                cell_count = cells.count()
                for j in range(cell_count):
                    cell_text = cells.nth(j).inner_text().strip()
                    row_data.append(cell_text)

                sl_no = row_data[self.S_No]
                matching_field = row_data[self.M_field]
                product_span = rows.nth(i).locator("td").nth(self.P_desc).locator("[data-tip]").first
                product_tip = product_span.get_attribute("data-tip") if product_span.count() > 0 else None
                product = product_tip.strip() if product_tip else row_data[self.P_desc]

                validation_note = ""  # to add in Excel
                is_invalid = False

                if validate:
                    # ✅ Keyword check
                    if any(k in product.lower() for k in keywords):
                        print(f"✅ PASS: Chemical '{product}' at Sl. No: {sl_no}")
                    else:
                        print(f"❌ FAIL: Invalid Chemical'{product}' at Sl. No: {sl_no}")
                        is_invalid = True
                        self.invalid_entries.append({"slNo": sl_no, "Chemical": product})

                    # ✅ Matching field check
                    if matching_field.lower() == "product description":
                        print(f"✅ Valid matching field '{matching_field}' at Sl. No: {sl_no}")
                    else:
                        print(f"❌ Invalid matching field '{matching_field}' at Sl. No: {sl_no}")
                        is_invalid = True
                        self.invalid_entries.append({"slNo": sl_no, "MatchingField": matching_field})

                    if is_invalid:
                        validation_note = "❌ Invalid Chemical Data"

                row_data.append(validation_note)
                all_rows_data.append(row_data)

        # --- Handle pagination ---
        if use_pagination:
            while True:
                process_current_page()
                next_button = self.page.locator('[class="trademo-table-arrow-button"]').nth(1)
                if next_button.is_enabled():
                    next_button.click()
                    self.page.locator("table tbody tr td:nth-child(4)").first.wait_for(
                        state="visible", timeout=100000
                    )
                else:
                    break
        else:
            process_current_page()

        # --- Save results ---
        if self.invalid_entries:
            os.makedirs("results", exist_ok=True)
            workbook = Workbook()
            sheet = workbook.active
            sheet.title = "Chemical Data"

            # Add Validation column header
            sheet.append(table_headers + ["Validation"])

            red_fill = PatternFill(start_color="FF0000", end_color="FF0000", fill_type="solid")

            for row_data in all_rows_data:
                sheet.append(row_data)
                if row_data and "Invalid" in row_data[-1]:
                    product_col_index = self.P_desc + 1
                    sheet.cell(row=sheet.max_row, column=product_col_index).fill = red_fill

            file_path = f"results/chemical_data_{self.selected_chemical}.xlsx"
            workbook.save(file_path)
            print(f"📁 All rows saved to {file_path} (invalid chemical data highlighted in red)")
        else:
            print("📘 No invalid chemical data found. Excel not generated.")

        return self.invalid_entries

    def auto_suggest_search_port(self,port:str):
        expect(self.page.get_by_placeholder(
            "Type to search in all categories or choose from the category below")).to_be_visible()
        # Select category Chemical, enter keyword, and select from autosuggest
        self.page.get_by_role("textbox", name="Type to search in all").click()
        self.page.locator("(//div[contains(text(),'Ports')])[1]").click()
        self.page.get_by_role("textbox", name="Search upto 20 Ports’s name").fill(port)
        self.page.wait_for_timeout(3000)
        self.selected_port = self.page.locator('[class="tw-font-medium tw-bg-transparent tw-p-0"]').nth(
            0).inner_text().strip()
        self.page.locator('[class="tw-font-medium tw-bg-transparent tw-p-0"]').nth(0).click()
        print(f"Selected port name is: {self.selected_port}")
        # click on search button
        self.page.locator(".tw-bg-primary-purple-500").click()
        self.page.wait_for_timeout(5000)
        self.page.locator("table tbody tr td:nth-child(4)").first.wait_for(state="visible", timeout=100000)
        #expect(self.page.get_by_role("main")).to_contain_text("chennai, tamil nadu, india")

    def Check_Port_description_Shipment_Grid(self, validate: bool = True, use_pagination: bool = False):
        shipment_tab = self.page.locator("//a[@id='nav-home-tab']")
        if not shipment_tab.is_visible(timeout=10000):  # wait max 5s for results
            print("❌ No search results found in Shipment Grid.")
            return []
        self.page.locator("//a[@id='nav-home-tab']").click()

        self.invalid_entries = []

        headers = self.page.locator("table thead tr th")
        header_count = headers.count()

        self.S_No = None
        self.M_field = None
        self.Port_Lading_col = None
        self.Port_Unlading_col = None

        # Extract headers
        table_headers = []
        for i in range(header_count):
            header_text = headers.nth(i).inner_text().strip()
            table_headers.append(header_text)
            if header_text.lower() in ["s no", "sl no", "serial no"]:
                self.S_No = i
            elif header_text.lower() in ["matching field", "matching fields"]:
                self.M_field = i
            elif header_text.lower() in ["port of lading", "ports of lading"]:
                self.Port_Lading_col = i
            elif header_text.lower() in ["port of unlading", "ports of unlading"]:
                self.Port_Unlading_col = i

        if self.S_No is None:
            raise Exception("❌ 'S No' column not found in table headers")
        if self.M_field is None:
            raise Exception("❌ 'Matching Field(s)' column not found in table headers")
        if self.Port_Lading_col is None and self.Port_Unlading_col is None:
            raise Exception("❌ Neither 'Port of Lading' nor 'Port of Unlading' found in headers")

        print(f"✅ Found column indexes → S No: {self.S_No}, Matching Field: {self.M_field}, "
              f"Port Lading: {self.Port_Lading_col}, Port Unlading: {self.Port_Unlading_col}")

        all_rows_data = []  # store all rows with validation info

        # --- process one page ---
        def process_current_page():
            rows = self.page.locator("table tbody tr")
            row_count = rows.count()

            for i in range(row_count):
                row_data = []
                cells = rows.nth(i).locator("td")
                cell_count = cells.count()
                for j in range(cell_count):
                    row_data.append(cells.nth(j).inner_text().strip())

                validation_note = ""  # Excel column
                sl_no = row_data[self.S_No]
                matching_field = row_data[self.M_field]
                port_name = None
                is_invalid = False

                if validate:
                    # --- Port of Lading ---
                    if matching_field.lower() == "port of lading" and self.Port_Lading_col is not None:
                        port_span = rows.nth(i).locator("td").nth(self.Port_Lading_col).locator("[data-tip]").first
                        port_tip = port_span.get_attribute("data-tip") if port_span.count() > 0 else None
                        port_name = port_tip.strip() if port_tip else row_data[self.Port_Lading_col]

                        self.port_name_hyperlink = port_name.split(",")[0].strip()

                        print(self.port_name_hyperlink)

                        if self.selected_port.lower().strip() in port_name.lower().strip():
                            print(f"✅ PASS: Port of Lading '{port_name}' at Sl. No: {sl_no}")
                        else:
                            print(f"❌ FAIL: Invalid Port of Lading '{port_name}' at Sl. No: {sl_no}")
                            is_invalid = True
                            validation_note = "❌ Invalid Port of Lading"

                    # --- Port of Unlading ---
                    elif matching_field.lower() == "port of unlading" and self.Port_Unlading_col is not None:
                        port_span = rows.nth(i).locator("td").nth(self.Port_Unlading_col).locator("[data-tip]").first
                        port_tip = port_span.get_attribute("data-tip") if port_span.count() > 0 else None
                        port_name = port_tip.strip() if port_tip else row_data[self.Port_Unlading_col]

                        self.port_name_hyperlink = port_name.split(",")[0].strip()
                        print(self.port_name_hyperlink)

                        if self.selected_port.lower().strip() in port_name.lower().strip():
                            print(f"✅ PASS: Port of Unlading '{port_name}' at Sl. No: {sl_no}")
                        else:
                            print(f"❌ FAIL: Invalid Port of Unlading '{port_name}' at Sl. No: {sl_no}")
                            is_invalid = True
                            validation_note = "❌ Invalid Port of Unlading"

                    # --- Unexpected Matching Field ---
                    else:
                        print(f"❌ FAIL: Unexpected Matching field '{matching_field}' at Sl. No: {sl_no}")
                        is_invalid = True
                        validation_note = "❌ Invalid Matching Field"

                    if is_invalid:
                        self.invalid_entries.append({
                            "slNo": sl_no,
                            "Port": port_name if port_name else "N/A",
                            "MatchingField": matching_field
                        })

                row_data.append(validation_note)
                all_rows_data.append(row_data)

        # --- handle pagination ---
        if use_pagination:
            while True:
                process_current_page()
                next_button = self.page.locator('[class="trademo-table-arrow-button"]').nth(1)
                if next_button.is_enabled():
                    next_button.click()
                    self.page.locator("table tbody tr td:nth-child(1)").first.wait_for(
                        state="visible", timeout=100000
                    )
                else:
                    break
        else:
            process_current_page()

        # --- save results ---
        if self.invalid_entries:
            os.makedirs("results", exist_ok=True)
            workbook = Workbook()
            sheet = workbook.active
            sheet.title = "Port Data"

            sheet.append(table_headers + ["Validation"])

            red_fill = PatternFill(start_color="FF0000", end_color="FF0000", fill_type="solid")

            for row_data in all_rows_data:
                sheet.append(row_data)
                if row_data and "Invalid" in row_data[-1]:
                    # highlight port column
                    if "lading" in row_data[self.M_field].lower():
                        col_index = self.Port_Lading_col + 1
                    elif "unlading" in row_data[self.M_field].lower():
                        col_index = self.Port_Unlading_col + 1
                    else:
                        col_index = self.M_field + 1
                    sheet.cell(row=sheet.max_row, column=col_index).fill = red_fill

            file_path = f"results/port_data_{self.selected_port}.xlsx"
            workbook.save(file_path)
            print(f"📁 All rows saved to {file_path} (invalid ports highlighted in red)")
        else:
            print("📘 No invalid port entries found. Excel not generated.")

        return self.invalid_entries

    def Validate_Discover_insight_ports(self):
        shipment_tab = self.page.locator("//a[@id='nav-home-tab']")
        if not shipment_tab.is_visible(timeout=10000):  # wait max 5s for results
            print("❌ No search results found in Shipment Grid.")
            return []
        with self.page.expect_popup() as page3_info:
               self.page.locator("span").filter(has_text="Discover more insights about").locator("span").click()
        page3 = page3_info.value
        expect(page3.get_by_role("main")).to_contain_text(self.port_name_hyperlink,ignore_case=True, timeout=100000)
        page3.close()

    def Search_product_manualsuggest(self, product_name: str):
        expect(self.page.get_by_placeholder(
            "Type to search in all categories or choose from the category below")).to_be_visible(timeout=100000)
        self.page.pause()

        # Select category Product, enter keyword, and select from autosuggest
        self.page.get_by_role("textbox", name="Type to search in all").click()
        self.page.get_by_role("textbox", name="Type to search in all categories or choose from the category below").fill(product_name)
        self.page.locator(".tw-bg-primary-purple-500").click()

    def Verify_Shipment_tab_Manual_suggest(self, Extracted_Text: str, validate: bool = True,
                                           use_pagination: bool = False):
        # 🔄 Always reset invalid_entries for fresh validation run
        shipment_tab = self.page.locator("//a[@id='nav-home-tab']")
        if not shipment_tab.is_visible(timeout=10000):  # wait max 5s for results
            print("❌ No search results found in Shipment Grid.")
            return []
        self.invalid_entries = []

        # Open shipment tab
        self.page.pause()
        self.page.locator("//a[@id='nav-home-tab']").click()
        self.page.wait_for_timeout(2000)

        rows = self.page.locator("table tbody tr")
        row_count = rows.count()

        if row_count < 10:
            print(f"⚠️ Only {row_count} rows found (less than 10). Skipping strict check.")
        else:
            expect(rows).to_have_count(10, timeout=100000)

        headers = self.page.locator("table thead tr th")
        header_count = headers.count()

        table_headers = []
        self.S_No = self.M_field = self.Product_col = None
        self.Shipper_col = self.Consignee_col = self.Address_col = None

        for i in range(header_count):
            header_text = headers.nth(i).inner_text().strip()
            table_headers.append(header_text)

            lower = header_text.lower()
            if lower in ["s no", "sl no", "serial no"]:
                self.S_No = i
            elif "matching" in lower:
                self.M_field = i
            elif "product" in lower:
                self.Product_col = i
            elif "shipper" in lower and "standardized" not in lower:
                self.Shipper_col = i
            elif "consignee" in lower and "address" not in lower and "standardized" not in lower:
                self.Consignee_col = i
            elif "address" in lower:
                self.Address_col = i

        if self.S_No is None or self.M_field is None:
            raise Exception("❌ Required columns ('S No' or 'Matching Field') not found in headers")

        extracted_text_lower = Extracted_Text.lower()
        all_rows_data = []

        def process_current_page():
            row_count = rows.count()
            print(f"🔄 Processing {row_count} rows on current page...")

            for i in range(row_count):
                row_data = []
                cells = rows.nth(i).locator("td")
                cell_count = cells.count()

                for j in range(cell_count):
                    row_data.append(cells.nth(j).inner_text().strip())

                validation_note = []
                is_invalid = False

                if validate:
                    sl_no = row_data[self.S_No]
                    matching_field = row_data[self.M_field]
                    matching_fields_list = [mf.strip() for mf in matching_field.split(",")]

                    product = row_data[self.Product_col] if self.Product_col else ""
                    shipper_name = row_data[self.Shipper_col] if self.Shipper_col else ""
                    consignee_name = row_data[self.Consignee_col] if self.Consignee_col else ""

                    consignee_address = shipper_address = ""
                    shipper_std_name = consignee_std_name = ""

                    for mf in matching_fields_list:
                        if mf == "Product Description":
                            parts = split_location(extracted_text_lower)
                            product_span = rows.nth(i).locator("td").nth(self.Product_col).locator("[data-tip]").first
                            product_tip = product_span.get_attribute("data-tip") if product_span.count() > 0 else None
                            product = product_tip.strip() if product_tip else rows.nth(i).locator("td").nth(
                                self.Product_col).inner_text().strip()

                            print(f"🔎 Checking product: {product}")
                            product_lower = product.lower()

                            matched_word = next((word for word in parts if word in product_lower), None)
                            if matched_word:
                                print(f"✅ {mf} contains keyword '{matched_word}' at Sl. No: {sl_no}")
                            else:
                                print(f"❌ {mf} mismatch: {product} at Sl. No: {sl_no}")
                                is_invalid = True
                                validation_note.append("❌ Invalid Product Description in Grid")

                        elif mf == "Shipper Name":
                            if extracted_text_lower in shipper_name.lower():
                                print(f"✅ Shipper name valid at Sl. No: {sl_no}")
                            else:
                                print(f"❌ Shipper name mismatch: {shipper_name} at Sl. No: {sl_no}")
                                is_invalid = True
                                validation_note.append("❌ Invalid Shipper in Grid")

                        elif mf == "Consignee Name":
                            if extracted_text_lower in consignee_name.lower():
                                print(f"✅ Consignee name valid at Sl. No: {sl_no}")
                            else:
                                print(f"❌ Consignee name mismatch: {consignee_name} at Sl. No: {sl_no}")
                                is_invalid = True
                                validation_note.append("❌ Invalid Consignee in Grid")

                        elif mf == "Shipper Address":
                            rows.nth(i).locator("td").nth(1).click()
                            self.page.wait_for_timeout(500)
                            read_more_locator = self.page.get_by_text("Read more").first
                            try:
                                read_more_locator.wait_for(state="visible", timeout=5000)
                                print("🔍 'Read More' found, clicking...")
                                read_more_locator.click()
                                self.page.wait_for_selector("div.read-more-cards", state="visible", timeout=5000)
                                read_more = self.page.locator("div.read-more-cards").first
                                address_text = read_more.inner_text().strip()
                                shipper_address = address_text
                                parts = split_location(extracted_text_lower)
                                address_lower = address_text.lower()
                                matched_word = next((w for w in parts if w in address_lower), None)
                                if matched_word:
                                    print(f"✅ {mf} contains keyword '{matched_word}' at Sl. No: {sl_no}")
                                else:
                                    print(f"❌ {mf} mismatch: {address_text} at Sl. No: {sl_no}")
                                    is_invalid = True
                                    validation_note.append("❌ Invalid shipper address in view")
                            except:
                                print("❌ 'Read more' link not found for Shipper Address")
                            finally:
                                close_btn = self.page.locator("//span[@aria-hidden='true']")
                                if close_btn.is_visible():
                                    close_btn.click()

                        elif mf == "Consignee Address":
                            rows.nth(i).locator("td").nth(1).click()
                            self.page.wait_for_timeout(500)
                            read_more_locator = self.page.get_by_text("Read more").last
                            try:
                                read_more_locator.wait_for(state="visible", timeout=5000)
                                print("🔍 'Read More' found, clicking...")
                                read_more_locator.click()
                                self.page.wait_for_selector("div.read-more-cards", state="visible", timeout=5000)
                                read_more = self.page.locator("div.read-more-cards").last
                                address_text = read_more.inner_text().strip()
                                consignee_address = address_text
                                parts = split_location(extracted_text_lower)
                                address_lower = address_text.lower()
                                matched_word = next((w for w in parts if w in address_lower), None)
                                if matched_word:
                                    print(f"✅ {mf} contains keyword '{matched_word}' at Sl. No: {sl_no}")
                                else:
                                    print(f"❌ {mf} mismatch: {address_text} at Sl. No: {sl_no}")
                                    is_invalid = True
                                    validation_note.append("❌ Invalid consignee address in view")
                            except:
                                print("❌ 'Read more' link not found for Consignee Address")
                            finally:
                                close_btn = self.page.locator("//span[@aria-hidden='true']")
                                if close_btn.is_visible():
                                    close_btn.click()

                    if is_invalid:
                        self.invalid_entries.append({
                            "slNo": sl_no,
                            "matching_field": matching_field,
                            "product": product,
                            "Shipper_Name": shipper_name,
                            "Consignee_Name": consignee_name,
                            "Shipper_Address": shipper_address,
                            "Consignee_Address": consignee_address,
                            "Shipper_Standardized_Name": shipper_std_name,
                            "Consignee_Standardized_Name": consignee_std_name,
                        })

                row_data.append(", ".join(validation_note) if validation_note else "")
                all_rows_data.append(row_data)

        if use_pagination:
            while True:
                process_current_page()
                next_button = self.page.locator('[class="trademo-table-arrow-button"]').nth(1)
                if next_button.is_enabled():
                    next_button.click()
                    self.page.locator("table tbody tr td:nth-child(1)").first.wait_for(state="visible", timeout=100000)
                else:
                    break
        else:
            process_current_page()

        if self.invalid_entries:
            os.makedirs("results", exist_ok=True)
            workbook = Workbook()
            sheet = workbook.active
            sheet.title = "Manual Validation"

            sheet.append(table_headers + ["Validation"])
            red_fill = PatternFill(start_color="FF0000", end_color="FF0000", fill_type="solid")

            for row_data in all_rows_data:
                sheet.append(row_data)
                if row_data and "Invalid" in row_data[-1]:
                    for col in range(2, len(row_data)):
                        sheet.cell(row=sheet.max_row, column=col).fill = red_fill

            file_path = f"results/Manual_Search_{Extracted_Text}.xlsx"
            workbook.save(file_path)
            print(f"📁 All rows saved to {file_path} (invalid entries highlighted in red)")
        else:
            print("📘 No invalid entries found. Excel not generated.")

        return self.invalid_entries

    def Manual_suggest_hs_code(self,hs_code:str):
        expect(self.page.get_by_placeholder(
            "Type to search in all categories or choose from the category below")).to_be_visible()
        # Manual suggest search for HS Code
        self.page.get_by_role("textbox", name="Type to search in all").click()
        self.page.get_by_role("textbox", name="Type to search in all").fill(hs_code)
        self.page.locator(".tw-bg-primary-purple-500").click()
        self.page.wait_for_timeout(3000)
        self.page.locator("table tbody tr td:nth-child(4)").first.wait_for(state="visible", timeout=100000)

    def Manual_suggest_chemical(self, chemical_name: str):
        expect(self.page.get_by_placeholder(
            "Type to search in all categories or choose from the category below")).to_be_visible()
        # Manual suggest search for HS Code
        self.page.get_by_role("textbox", name="Type to search in all").click()
        self.page.get_by_role("textbox", name="Type to search in all").fill(chemical_name)
        self.page.locator(".tw-bg-primary-purple-500").click()
        self.page.wait_for_timeout(3000)
        self.page.locator("table tbody tr td:nth-child(4)").first.wait_for(state="visible", timeout=100000)

    def Manual_suggest_shipper(self,shipper_name:str):
        expect(self.page.get_by_placeholder(
            "Type to search in all categories or choose from the category below")).to_be_visible()
        # Manual suggest search for Shipper
        self.page.get_by_role("textbox", name="Type to search in all").click()
        self.page.get_by_role("textbox", name="Type to search in all").fill(shipper_name)
        self.page.locator(".tw-bg-primary-purple-500").click()
        self.page.wait_for_timeout(3000)
        self.page.locator("table tbody tr td:nth-child(4)").first.wait_for(state="visible", timeout=100000)

    def Manual_suggest_consignee(self,consignee_name:str):
        expect(self.page.get_by_placeholder(
            "Type to search in all categories or choose from the category below")).to_be_visible()
        # Manual suggest search for Consignee
        self.page.get_by_role("textbox", name="Type to search in all").click()
        self.page.get_by_role("textbox", name="Type to search in all").fill(consignee_name)
        self.page.locator(".tw-bg-primary-purple-500").click()
        self.page.locator("table tbody tr td:nth-child(4)").first.wait_for(state="visible", timeout=100000)
        self.page.wait_for_timeout(3000)

    def Manual_suggest_port(self,port_name:str):
        expect(self.page.get_by_placeholder(
            "Type to search in all categories or choose from the category below")).to_be_visible()
        # Manual suggest search for Port
        self.page.get_by_role("textbox", name="Type to search in all").click()
        self.page.get_by_role("textbox", name="Type to search in all").fill(port_name)
        self.page.locator(".tw-bg-primary-purple-500").click()
        self.page.locator("table tbody tr td:nth-child(4)").first.wait_for(state="visible", timeout=100000)
        self.page.wait_for_timeout(3000)

    def auto_suggest_manual_hs_code(self, hs_code: str):
        # Focus and type into search box
        self.page.get_by_role("textbox", name="Type to search in all").click()
        self.page.get_by_role("textbox", name="Type to search in all").fill(hs_code)

        # Locator for the first HS code suggestion
        hs_code_locator = self.page.locator("//div[contains(text(),'HS:')]/mark").first

        # Wait up to 5 seconds for suggestion to appear
        try:
            hs_code_locator.wait_for(state="visible", timeout=5000)
        except TimeoutError:
            pytest.skip(f"⚠️ Search result for HS Code '{hs_code}' not found. Skipping the test.")

        # Continue only if visible
        self.selected_hs_code = hs_code_locator.inner_text().strip()
        hs_code_locator.click()
        print(f"✅ Selected HS Code is: {self.selected_hs_code}")

        # Confirm and wait for results
        self.page.locator(".tw-bg-primary-purple-500").click()
        self.page.wait_for_timeout(3000)
        self.page.locator("table tbody tr td:nth-child(4)").first.wait_for(
            state="visible", timeout=100000
        )

    def auto_suggest_manual_product(self, product_name: str):
        self.page.get_by_role("textbox", name="Type to search in all").click()
        self.page.get_by_role("textbox", name="Type to search in all").fill(product_name)
        self.page.wait_for_timeout(2000)

        # Locator for the first product suggestion
        product_locator = self.page.locator(
            "(//span[contains(text(),'Product')]/ancestor::div[contains(@class,'tw-flex tw-items-center')]/following-sibling::div//div[contains(@class,'tw-px-3')])[1]"
        ).first

        # Check if product suggestion is visible
        if not product_locator.is_visible():
            pytest.skip(f"⚠️ Search result for product '{product_name}' not found. Skipping the test.")

        # Continue only if visible
        self.selected_product = product_locator.inner_text().strip()
        product_locator.click()
        print(f"✅ Selected product is: {self.selected_product}")

        self.page.locator(".tw-bg-primary-purple-500").click()
        self.page.wait_for_timeout(3000)
        self.page.locator("table tbody tr td:nth-child(4)").first.wait_for(
            state="visible", timeout=100000
        )

    def auto_suggest_manual_shipper(self, shipper_name: str):
        # Focus and type into search box
        self.page.get_by_role("textbox", name="Type to search in all").click()
        self.page.get_by_role("textbox", name="Type to search in all").fill(shipper_name)

        # Locator for the first Shipper suggestion
        shipper_locator = self.page.locator(
            "(//span[contains(text(),'Shipper')]/ancestor::div[contains(@class,'tw-flex tw-items-center')]/following-sibling::div//div[contains(@class,'tw-px-3')])[1]"
        ).first

        # Wait up to 5 seconds for suggestion
        try:
            shipper_locator.wait_for(state="visible", timeout=5000)
        except TimeoutError:
            pytest.skip(f"⚠️ Search result for shipper '{shipper_name}' not found. Skipping the test.")

        # If found, select shipper
        self.selected_shipper = shipper_locator.inner_text().strip()
        shipper_locator.click()
        print(f"✅ Selected shipper is: {self.selected_shipper}")

        # Verify and confirm
        expect(self.page.get_by_role("main")).to_contain_text("Shipper")
        self.page.locator(".tw-bg-primary-purple-500").click()
        self.page.wait_for_timeout(3000)

        # Wait for results table
        self.page.locator("table tbody tr td:nth-child(4)").first.wait_for(
            state="visible", timeout=100000
        )

    def auto_suggest_manual_consignee(self,consignee:str):
        self.page.get_by_role("textbox", name="Type to search in all").click()
        self.page.get_by_role("textbox", name="Type to search in all").fill(consignee)
        self.selected_consignee = self.page.locator("(//span[contains(text(),'Consignee')]/ancestor::div[contains(@class,'tw-flex tw-items-center')]/following-sibling::div//div[contains(@class,'tw-px-3')])[1]").nth(
            0).inner_text().strip()
        self.page.locator("(//span[contains(text(),'Consignee')]/ancestor::div[contains(@class,'tw-flex tw-items-center')]/following-sibling::div//div[contains(@class,'tw-px-3')])[1]").nth(0).click()
        expect(self.page.get_by_role("main")).to_contain_text("Consignee")
        self.page.locator(".tw-bg-primary-purple-500").click()
        self.page.wait_for_timeout(3000)
        self.page.locator("table tbody tr td:nth-child(4)").first.wait_for(state="visible", timeout=100000)

    def auto_suggest_manual_chemical(self, chemical_name: str):
        self.page.get_by_role("textbox", name="Type to search in all").click()
        self.page.get_by_role("textbox", name="Type to search in all").fill(chemical_name)

        # Locator for the first chemical suggestion
        chemical_locator = self.page.locator(
            "(//span[contains(text(),'Chemical')]/ancestor::div[contains(@class,'tw-flex tw-items-center')]/following-sibling::div//div[contains(@class,'tw-px-3')])[1]"
        ).first

        # Wait up to 5 seconds for the suggestion to appear
        try:
            chemical_locator.wait_for(state="visible", timeout=50000)
        except TimeoutError:
            pytest.skip(f"⚠️ Search result for chemical '{chemical_name}' not found. Skipping the test.")

        # Continue only if visible
        self.selected_chemical = chemical_locator.inner_text().strip()
        chemical_locator.click()
        print(f"✅ Selected chemical is: {self.selected_chemical}")

        expect(self.page.get_by_role("main")).to_contain_text("Chemical")
        self.page.locator(".tw-bg-primary-purple-500").click()

    def auto_suggest_manual_port(self, port_name: str):
        # Focus and type into search box
        self.page.get_by_role("textbox", name="Type to search in all").click()
        self.page.get_by_role("textbox", name="Type to search in all").fill(port_name)

        # Locator for the first Port suggestion
        port_locator = self.page.locator(
            "(//span[contains(text(),'Port')]/ancestor::div[contains(@class,'tw-flex tw-items-center')]/following-sibling::div//div[contains(@class,'tw-px-3')])[1]"
        ).first

        # Wait up to 5 seconds for suggestion, else skip
        try:
            port_locator.wait_for(state="visible", timeout=5000)
        except TimeoutError:
            pytest.skip(f"⚠️ Search result for port '{port_name}' not found. Skipping the test.")

        # If found, select port
        self.selected_port = port_locator.inner_text().strip()
        port_locator.click()
        print(f"✅ Selected Port is: {self.selected_port}")

        # Verify UI and confirm selection
        expect(self.page.get_by_role("main")).to_contain_text("Port")
        self.page.locator(".tw-bg-primary-purple-500").click()
        self.page.wait_for_timeout(3000)

        # Wait for results table to load
        self.page.locator("table tbody tr td:nth-child(4)").first.wait_for(
            state="visible", timeout=100000
        )

        # Final verification
        expect(self.page.get_by_role("main")).to_contain_text(self.selected_port)

    def Verify_Save_Search_screen(self,HS_code:str):
        # Click on the Save Search button
        self.page.get_by_text("Save Search").first.click()
        # Verify Save Search modal is displayed
        expect(self.page.get_by_role("main")).to_contain_text("Save Search")
        expect(self.page.get_by_role("main")).to_contain_text("Search Category")
        expect(self.page.get_by_role("main")).to_contain_text("Search Phrase")
        self.page.get_by_text("Date Range", exact=True).click()
        expect(self.page.locator('[class="_pill_label_rvvht_133"]').nth(0)).to_contain_text("HS Code")
        expect(self.page.locator('[class="_pill_label_rvvht_133"]').nth(1)).to_contain_text(HS_code)
        expect(self.page.locator('[class="_pill_label_rvvht_133"]').nth(2)).to_contain_text("Jan 01, 2020 to Jul 31, 2025 ")
        expect(self.page.get_by_role("main")).to_contain_text("Date Range")
        expect(self.page.get_by_role("main")).to_contain_text("Applied Filters")
        expect(self.page.get_by_role("main")).to_contain_text("No filters have been added")
        expect(self.page.get_by_role("main")).to_contain_text("Set as Default Search View")
        expect(self.page.get_by_role("main")).to_contain_text("Add a name to this search")
        expect(self.page.get_by_role("main")).to_contain_text("Select a date range for specific")
        expect(self.page.get_by_role("main")).to_contain_text("Share the search with your team")
        expect(self.page.get_by_role("main")).to_contain_text("Would you like to receive email alerts on the search")
        expect(self.page.get_by_role("main")).to_contain_text("Cancel")
        expect(self.page.get_by_role("main")).to_contain_text("Save Search")
        expect(self.page.get_by_role("main")).to_contain_text("Custom Date Range: Jan 01, 2020 to Jul 31, 2025")

    def Verify_SaveSearch_Cancel_Close(self):
        # Click on Cancel button
        self.page.get_by_role("button", name="Cancel").click()
        self.page.wait_for_timeout(1000)
        # Verify Save Search modal is closed
        expect(self.page.get_by_role("main")).to_contain_text("Search Category")
        # Click on the Save Search button again
        self.page.get_by_text("Save Search").first.click()

        # Click on Close icon
        self.page.locator("span").filter(has_text="Save SearchSave SearchSearch").get_by_role("img").nth(1).click()
        # Verify Save Search modal is closed
        expect(self.page.get_by_role("main")).to_contain_text("Search Category")

    def Verify_SaveSearch_button(self):
        import random
        # Click on the Save Search button again
        self.page.get_by_text("Save Search").first.click()

        # Verify the input field “Add a name to this search”
        self.page.get_by_role("textbox", name="Enter name for search").click()
        self.page.get_by_role("textbox", name="Enter name for search").clear()
        random_number = random.randint(1000, 9999)  # 4-digit random number
        hs_code_value = f"HS Code Search{random_number}"

        print(hs_code_value)
        self.page.get_by_role("textbox", name="Enter name for search").fill(hs_code_value)
        # Check the “Custom Date Range” dropdown
        self.page.locator("span").filter(has_text="Save SearchSave SearchSearch").locator("svg").nth(2).click()

        # expect(self.page.locator("#react-select-5-option-1")).to_contain_text("Last 3 Months")
        # expect(self.page.locator("#react-select-5-option-2")).to_contain_text("Year to Date")
        # expect(self.page.locator("#react-select-5-option-3")).to_contain_text("Last 1 Year")
        # expect(self.page.locator("#react-select-5-option-4")).to_contain_text("Last 2 Years")
        # expect(self.page.locator("#react-select-5-option-5")).to_contain_text("Last 3 Years")
        # expect(self.page.locator("#react-select-5-option-6")).to_contain_text("All Data")
        self.page.locator("span").filter(has_text="Save SearchSave SearchSearch").locator("svg").nth(2).click()

        # Check for toggle: “Set as Default Search View”
        # Enable the toggle
        self.page.locator(".slider").first.click()
        expect(self.page.get_by_role("main")).to_contain_text(
            "Enabling this will set the current search as your default, replacing any previous default view")
        # Disable the toggle
        self.page.locator("div").filter(has_text=re.compile(r"^Set as Default Search View$")).locator("span").click()
        expect(self.page.get_by_role("main")).not_to_contain_text(
            "Enabling this will set the current search as your default, replacing any previous default view")

        # Check “Share the search with your team” multi-select dropdown
        self.page.locator("div").filter(has_text=re.compile(r"^You can select multiple options$")).nth(1).click()
        self.page.get_by_text("Swarupa Dash (swarupa.dash@trademo.com)", exact=True).click()
        self.page.locator("div:nth-child(3) > .css-19bqh2r").click()

        # Validate toggle: “Would you like to receive email alerts on the search”
        self.page.locator("div").filter(
            has_text=re.compile(r"^Would you like to receive email alerts on the search$")).locator("span").click()
        expect(self.page.get_by_role("main")).to_contain_text("How frequently would you like to receive the alerts?")
        expect(self.page.get_by_role("main")).to_contain_text("Select all that you want to track via this email alerts")
        expect(self.page.get_by_role("main")).to_contain_text(
            "Select measurement unit bases which you want to generate results.")

        # Disable toggle
        self.page.locator("div").filter(
            has_text=re.compile(r"^Would you like to receive email alerts on the search$")).locator("span").click()
        expect(self.page.get_by_role("main")).not_to_contain_text("How frequently would you like to receive the alerts?")
        expect(self.page.get_by_role("main")).not_to_contain_text("Select all that you want to track via this email alerts")
        expect(self.page.get_by_role("main")).not_to_contain_text(
            "Select measurement unit bases which you want to generate results.")
        # Open modal again, fill all valid inputs, and click Save Search
        self.page.get_by_role("button", name="Save Search").click()
        self.page.wait_for_timeout(1000)
        Skip_locator = self.page.get_by_text("Skip and Save")
        if  Skip_locator.is_visible():
            print("🔍 'Skip and Save' is visible, clickin")
            Skip_locator.click()
            expect(self.page.get_by_role("main")).to_contain_text(
                "Are you sure, you don't want to receive email alerts for this search?")
            expect(self.page.get_by_role("paragraph")).to_contain_text(
                "Our email alert feature will keep you updated on new shipments for this saved search, with actionable insights and new trends.")
            expect(self.page.get_by_role("main")).to_contain_text("Skip and Save")
            expect(self.page.get_by_role("main")).to_contain_text("Set Email Alert")
            self.page.get_by_role("button", name="Skip and Save").click()
        else:
            print("ℹ️ 'Skip and save' not visible.")
        toast = self.page.get_by_role("alert")
        #expect(toast).to_have_text(f"{hs_code_value} has been added to your Saved Searches.")
        self.page.locator('[class="m-1"]').click()
        self.page.get_by_text("Search History").click()
        # Correct way in Python Playwright
        items = [f"HS Code Search{hs_code_value}"]
        expect(self.page.get_by_role("alert")).to_contain_text("HS Code Search")
        self.page.get_by_text("Shipments").click()
















































