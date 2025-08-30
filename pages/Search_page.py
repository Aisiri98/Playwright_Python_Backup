import os
import re

from openpyxl import Workbook
from openpyxl.styles import PatternFill
from playwright.sync_api import Page, expect
from playwright.sync_api import expect, TimeoutError as PlaywrightTimeoutError
invalid_entries =[]

class Search:
    def __init__(self, page: Page):
        self.page = page

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

    def check_hs_code_in_shipmentgrid(self, file_name: str, validate: bool = True):
        self.page.locator("//a[@id='nav-home-tab']").click()
        self.page.wait_for_timeout(3000)

        # Initialize invalid_entries on first call only
        if not hasattr(self, "invalid_entries"):
            self.invalid_entries = []

        # --- Find column indexes dynamically ---
        headers = self.page.locator("table thead tr th")
        header_count = headers.count()

        self.hs_code_idx = None
        self.s_no_idx = None
        self.m_field_idx = None

        for i in range(header_count):
            header_text = headers.nth(i).inner_text().strip().lower()
            if header_text == "hs code":
                self.hs_code_idx = i
            elif header_text in ["s no", "sl no"]:
                self.s_no_idx = i
            elif header_text == "matching fields":
                self.m_field_idx = i

        # Validate we found all indexes
        if self.hs_code_idx is None:
            raise Exception("❌ HS Code column not found in the table headers")
        if self.s_no_idx is None:
            raise Exception("❌ S No column not found in the table headers")
        if self.m_field_idx is None:
            raise Exception("❌ Matching field column not found in the table headers")

        print(f"✅ Found 'HS Code' at index {self.hs_code_idx}")
        print(f"✅ Found 'S No' at index {self.s_no_idx}")
        print(f"✅ Found 'Matching Fields' at index {self.m_field_idx}")

        # --- Validate rows ---
        rows = self.page.locator("table tbody tr")
        row_count = rows.count()

        if validate:
            for i in range(row_count):
                sl_no = rows.nth(i).locator("td").nth(self.s_no_idx).inner_text().strip()
                hs_code = rows.nth(i).locator("td").nth(self.hs_code_idx).inner_text().strip()
                matching_field = rows.nth(i).locator("td").nth(self.m_field_idx).inner_text().strip()

                # ✅ Validate HS Code
                if hs_code.startswith(self.selected_hs_code):
                    print(f"✅ Valid HS Code: {hs_code} at Sl. No: {sl_no}")
                else:
                    print(f"❌ Invalid HS Code: {hs_code} at Sl. No: {sl_no}")
                    self.invalid_entries.append({
                        "sl_no": sl_no, "hs_code": hs_code, "matching_field": matching_field
                    })

                # ✅ Validate Matching Field
                if matching_field.lower() == "hs code":
                    print(f"✅ Valid Matching field {matching_field}at Sl. No: {sl_no}")
                else:
                    print(f"❌ Invalid Matching field: {matching_field} at Sl. No: {sl_no}")
                    self.invalid_entries.append({
                        "sl_no": sl_no, "hs_code": hs_code, "matching_field": matching_field
                    })

        # Check if "Next" button exists and is enabled
        # next_button = self.page.locator('[class="trademo-table-arrow-button"]').nth(1)
        # if next_button.is_visible() and next_button.is_enabled():
        #     next_button.click()
        #     self.page.locator("table tbody tr td:nth-child(4)").first.wait_for(
        #         state="visible", timeout=100000
        #     )
        #     self.check_hs_code_in_shipmentgrid(file_name, validate)
        # else:
        #     print("✅ All pages validated")

            if not self.invalid_entries:
                print("📘 No invalid HS code found.")
                return

            # Save invalid entries to Excel
            os.makedirs("results", exist_ok=True)
            workbook = Workbook()
            sheet = workbook.active
            sheet.title = "Invalid HS Codes"

            # Write headers
            sheet.append(["Sl. No", "HS Code", "Matching Field"])

            # Red fill style
            red_fill = PatternFill(start_color="FF0000", end_color="FF0000", fill_type="solid")

            for item in self.invalid_entries:
                row = sheet.max_row + 1
                sheet.cell(row=row, column=1, value=item["sl_no"])
                hs_code_cell = sheet.cell(row=row, column=2, value=item["hs_code"])
                matching_field_cell = sheet.cell(row=row, column=3, value=item["matching_field"])
                hs_code_cell.fill = red_fill
                matching_field_cell.fill = red_fill

            workbook.save(os.path.join("results", file_name))
            print(f"📁 Invalid HSCode data saved to '{file_name}'")

    def Validate_Discover_Insights(self):
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
        self.page.locator("table tbody tr td:nth-child(4)").first.wait_for(state="visible", timeout=100000)

    def check_product_description_in_shipment_grid(self, file_name: str = None,validate: bool = True):
        """Check product descriptions across all pages"""
        if not hasattr(self, "invalid_entries"):
            self.invalid_entries = []

            # --- Find header indexes dynamically ---
        headers = self.page.locator("table thead tr th")
        header_count = headers.count()

        self.S_No = None
        self.M_field = None
        self.P_desc = None

        for i in range(header_count):
            header_text = headers.nth(i).inner_text().strip().lower()
            if header_text in ["s no", "sl no", "serial no"]:  # flexible match
                self.S_No = i
            elif header_text == "matching fields":
                self.M_field = i
            elif header_text in ["product description", "description"]:
                self.P_desc = i

        if self.S_No is None:
            raise Exception("❌ 'S No' column not found in table headers")
        if self.M_field is None:
            raise Exception("❌ 'Matching Fields' column not found in table headers")
        if self.P_desc is None:
            raise Exception("❌ 'Product Description' column not found in table headers")

        print(f"✅ Found column indexes → S No: {self.S_No}, Matching Field: {self.M_field}, Product: {self.P_desc}")

        rows = self.page.locator("table tbody tr")
        row_count = rows.count()

        # Split search text into keywords (e.g., "lab coat" → ["lab", "coat"])
        keywords = self.selected_product.lower().split()

        if validate:
            for i in range(row_count):
                sl_no = rows.nth(i).locator("td").nth(self.S_No).inner_text().strip()
                matching_field = rows.nth(i).locator("td").nth(self.M_field).inner_text().strip()

                # Extract product description
                product_span = rows.nth(i).locator("td").nth(self.P_desc).locator("[data-tip]").first
                product_tip = product_span.get_attribute("data-tip") if product_span.count() > 0 else None
                product = product_tip.strip() if product_tip else rows.nth(i).locator("td").nth(
                    self.P_desc).inner_text().strip()

                print(f"🔎 Checking product: {product}")

                # ✅ Check if ANY keyword is in product
                if any(k in product.lower() for k in keywords):
                    print(f"✅ Valid product found: {product} at Sl. No: {sl_no}")
                else:
                    print(f"❌ Invalid product found: {product} at Sl. No: {sl_no}")
                    self.invalid_entries.append({"sl_no": sl_no, "product": product, "matching_field": matching_field})

                # Validate matching field
                if matching_field.lower() == "product description":
                    print(f"✅ Valid matching field: {matching_field} at Sl. No: {sl_no}")
                else:
                    print(f"❌ Invalid matching field: {matching_field} at Sl. No: {sl_no}")
                    self.invalid_entries.append({"sl_no": sl_no, "product": product, "matching_field": matching_field})

        # --- Handle pagination ---
        # next_button = self.page.locator('[class="trademo-table-arrow-button"]').nth(1)
        # if next_button.is_enabled():
        #     next_button.click()
        #     self.page.locator("table tbody tr td").first.wait_for(state="visible", timeout=100000)
        #     self.check_product_description_in_shipment_grid(file_name, validate)  # recursive call
        # else:
        #     print("✅ All pages validated")

            if not self.invalid_entries:
                print("📘 No invalid products found.")
                return

            # Default filename if not passed
            if not file_name:
                os.makedirs("results", exist_ok=True)
                file_name = "results/invalid_product_autosuggest.xlsx"

            # Save invalid entries to Excel
            workbook = Workbook()
            sheet = workbook.active
            sheet.title = "Invalid Products"

            # Write headers
            sheet.append(["Sl. No", "Product", "Matching Field"])

            # Red fill style
            red_fill = PatternFill(start_color="FF0000", end_color="FF0000", fill_type="solid")

            for item in self.invalid_entries:
                row = sheet.max_row + 1
                sheet.cell(row=row, column=1, value=item["sl_no"])
                prod_cell = sheet.cell(row=row, column=2, value=item["product"])
                match_cell = sheet.cell(row=row, column=3, value=item["matching_field"])
                prod_cell.fill = red_fill
                match_cell.fill = red_fill

            workbook.save(os.path.join("results", file_name))
            print(f"📁 Invalid Product data saved to '{file_name}'")

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
        # Navigate to exporter tab
        self.page.locator("//a[@id='nav-contact-tab']").click()

        # Verify The Exporters tab label should update to Exporters (1) and display the selected Shipper name under the Company Name section
        total_record = self.page.locator(".trademo-table-count-text").inner_text().strip()
        total_count = total_record.split("of")[-1].strip()
        expect(self.page.locator(
            '[class=" tw-text-xs tw-p-1 tw-rounded tw-bg-primary-purple-100 tw-text-primary-purple-600 tw-font-medium"]')).to_have_text(
            total_count)

    def check_shipper_name(self, file_name: str, validate: bool = True):
        """Check shipper names across all pages and collect invalid entries"""

        if not hasattr(self, "invalid_shipper_entries"):
            self.invalid_shipper_entries = []

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
                    self.invalid_shipper_entries.append({"sl_no": sl_no, "company": company})

            # --- Pagination check ---
            # next_button = self.page.locator('[class="trademo-table-arrow-button"]').nth(1)
            # if next_button.is_enabled():
            #     next_button.click()
            #     self.page.locator("table tbody tr td:nth-child(4)").first.wait_for(
            #         state="visible", timeout=100000
            #     )
            #     self.check_shipper_name(file_name)  # recursive call
            # else:
            #     print("✅ All pages validated")

                if not self.invalid_shipper_entries:
                    print("📘 No invalid shipper found.")
                    return

                # Save invalid entries to Excel
                os.makedirs("results", exist_ok=True)
                workbook = Workbook()
                sheet = workbook.active
                sheet.title = "Invalid Shipper"

                # Write headers
                sheet.append(["Sl. No", "Company"])

                # Red fill style for invalid cells
                red_fill = PatternFill(start_color="FF0000", end_color="FF0000", fill_type="solid")

                for item in self.invalid_shipper_entries:
                    row = sheet.max_row + 1
                    sheet.cell(row=row, column=1, value=item["sl_no"])
                    company_cell = sheet.cell(row=row, column=2, value=item["company"])
                    company_cell.fill = red_fill

                # Save Excel file
                workbook.save(os.path.join("results", file_name))
                print(f"📁 Invalid shipper data saved to '{file_name}'")


    def Validate_Discover_insight_link(self):
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
        # Navigate to importer tab
        self.page.locator("//a[@id='nav-profile-tab']").click()

        # Verify results
        total_record = self.page.locator(".trademo-table-count-text").inner_text().strip()
        total_count = total_record.split("of")[-1].strip()
        expect(self.page.locator(
            '[class=" tw-text-xs tw-p-1 tw-rounded tw-bg-primary-purple-100 tw-text-primary-purple-600 tw-font-medium"]')).to_have_text(
            total_count)

    def Validate_Discover_insight_consignee(self):
        # Test insights link
        with self.page.expect_popup() as page2_info:
            self.page.locator("a").filter(has_text=self.selected_consignee.lower()).click()
        page2 = page2_info.value
        expect(page2.get_by_role("main")).to_contain_text(self.selected_consignee, ignore_case=True)
        page2.close()
        self.page.locator("table tbody tr td:nth-child(4)").first.wait_for(state="visible", timeout=100000)

    def check_consignee_Name_Shipment_Grid(self, file_name: str, validate: bool = True):
        """Check consignee names across shipment grid pages and collect invalid entries"""

        if not hasattr(self, "invalid_consignee_entries"):
            self.invalid_consignee_entries = []

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
                    self.invalid_consignee_entries.append({
                        "sl_no": sl_no,
                        "consignee_name": consignee_name,
                        "expected": self.selected_consignee
                    })

            # --- Pagination check ---
            # next_button = self.page.locator('[class="trademo-table-arrow-button"]').nth(1)
            # if next_button.is_enabled():
            #     next_button.click()
            #     self.page.locator("table tbody tr td:nth-child(4)").first.wait_for(
            #         state="visible", timeout=100000
            #     )
            #     self.check_consignee_Name_Shipment_Grid(file_name)  # recursive call
            # else:
            #     print("✅ All pages validated")

                if not self.invalid_consignee_entries:
                    print("📘 No invalid consignee found.")
                    return

                # Save invalid entries to Excel
                os.makedirs("results", exist_ok=True)
                workbook = Workbook()
                sheet = workbook.active
                sheet.title = "Invalid Consignee"

                # Write headers
                sheet.append(["Sl. No", "Consignee Name", "Expected"])

                # Red fill style for invalid cells
                red_fill = PatternFill(start_color="FF0000", end_color="FF0000", fill_type="solid")

                for item in self.invalid_consignee_entries:
                    row = sheet.max_row + 1
                    sheet.cell(row=row, column=1, value=item["sl_no"])
                    consignee_cell = sheet.cell(row=row, column=2, value=item["consignee_name"])
                    consignee_cell.fill = red_fill
                    sheet.cell(row=row, column=3, value=item["expected"])

                # Save Excel file
                workbook.save(os.path.join("results", file_name))
                print(f"📁 Invalid consignee data saved to '{file_name}'")

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

    def Check_Chemical_In_shipmentGrid(self, file_name: str, validate: bool = True):
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

        for i in range(header_count):
            header_text = headers.nth(i).inner_text().strip().lower()
            if header_text in ["s no", "sl no", "serial no"]:  # flexible match
                self.S_No = i
            elif header_text == "matching fields":
                self.M_field = i
            elif header_text in ["product description", "description"]:
                self.P_desc = i

        if self.S_No is None:
            raise Exception("❌ 'S No' column not found in table headers")
        if self.M_field is None:
            raise Exception("❌ 'Matching Fields' column not found in table headers")
        if self.P_desc is None:
            raise Exception("❌ 'Product Description' column not found in table headers")

        print(f"✅ Found column indexes → S No: {self.S_No}, Matching Field: {self.M_field}, Product: {self.P_desc}")

        rows = self.page.locator("table tbody tr")
        row_count = rows.count()

        # Split search text into keywords (e.g., "lab coat" → ["lab", "coat"])
        keywords = self.selected_chemical.lower().split()

        if validate:
            for i in range(row_count):
                sl_no = rows.nth(i).locator("td").nth(self.S_No).inner_text().strip()
                matching_field = rows.nth(i).locator("td").nth(self.M_field).inner_text().strip()

                # Extract product description
                product_span = rows.nth(i).locator("td").nth(self.P_desc).locator("[data-tip]").first
                product_tip = product_span.get_attribute("data-tip") if product_span.count() > 0 else None
                product = product_tip.strip() if product_tip else rows.nth(i).locator("td").nth(
                    self.P_desc).inner_text().strip()

                print(f"🔎 Checking product: {product}")

                is_invalid = False

                # ✅ Check if ANY keyword is in product
                if any(k in product.lower() for k in keywords):
                    print(f"✅ Valid product found: {product} at Sl. No: {sl_no}")
                else:
                    print(f"❌ Invalid product found: {product} at Sl. No: {sl_no}")
                    is_invalid = True

                # Validate matching field
                if matching_field.lower() == "product description":
                    print(f"✅ Valid matching field: {matching_field} at Sl. No: {sl_no}")
                else:
                    print(f"❌ Invalid matching field: {matching_field} at Sl. No: {sl_no}")
                    is_invalid = True

                # If either field is invalid, store the whole row
                if is_invalid:
                    self.invalid_entries.append({
                        "slNo": sl_no,
                        "Chemical": product,
                        "matching_field": matching_field
                    })

        # --- Check next page ---
        # next_button = self.page.locator('[class="trademo-table-arrow-button"]').nth(1)
        # if next_button.is_enabled():
        #     next_button.click()
        #     self.page.locator("table tbody tr td:nth-child(4)").first.wait_for(
        #         state="visible", timeout=100000
        #     )
        #     self.Check_Chemical_In_shipmentGrid(file_name)
        # else:
        #     print("✅ All pages validated")

            if not self.invalid_entries:
                print("📘 No invalid chemical found.")
                return

            # Save invalid entries to Excel
            os.makedirs("results", exist_ok=True)
            workbook = Workbook()
            sheet = workbook.active
            sheet.title = "Invalid Chemical"

            # Write headers
            sheet.append(["Sl. No", "Chemical", "Matching Field"])

            # Red fill style
            red_fill = PatternFill(start_color="FF0000", end_color="FF0000", fill_type="solid")

            for item in self.invalid_entries:
                row = sheet.max_row + 1
                sheet.cell(row=row, column=1, value=item["slNo"])
                chemical_cell = sheet.cell(row=row, column=2, value=item["Chemical"])
                matching_field_cell = sheet.cell(row=row, column=3, value=item["matching_field"])
                chemical_cell.fill = red_fill
                matching_field_cell.fill = red_fill

            # Save Excel file
            workbook.save(os.path.join("results", file_name))
            print(f"📁 Invalid chemical data saved to '{file_name}'")


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

    def Check_Port_description_Shipment_Grid(self, file_name: str, validate: bool = True):
        if not hasattr(self, "invalid_entries"):
            self.invalid_entries = []

        # --- Get header indexes dynamically ---
        headers = self.page.locator("table thead tr th")
        expect(self.page.locator("table thead tr th").first).to_be_visible()
        header_count = headers.count()

        self.S_No = None
        self.M_field = None
        self.P_desc = None
        self.Port_Lading_col = None
        self.Port_Unlading_col = None

        for i in range(header_count):
            header_text = headers.nth(i).inner_text().strip().lower()

            if header_text in ["s no", "sl no", "serial no"]:
                self.S_No = i
            elif header_text in ["matching field", "matching fields"]:
                self.M_field = i
            elif header_text in ["product description", "description"]:
                self.P_desc = i
            elif header_text in ["port of lading", "loading port"]:
                self.Port_Lading_col = i
            elif header_text in ["port of unlading", "unloading port"]:
                self.Port_Unlading_col = i

        # --- Safety checks ---
        if self.S_No is None:
            raise Exception("❌ 'S No' column not found in table headers")
        if self.M_field is None:
            raise Exception("❌ 'Matching Field(s)' column not found in table headers")
        if self.Port_Lading_col is None and self.Port_Unlading_col is None:
            raise Exception("❌ Neither 'Port of Lading' nor 'Port of Unlading' column found in table headers")

        print(f"✅ Column Indexes => S_No: {self.S_No}, M_field: {self.M_field}, "
              f"Port_Lading: {self.Port_Lading_col}, Port_Unlading: {self.Port_Unlading_col}")

        # --- Validate rows if requested ---
        rows = self.page.locator("table tbody tr")
        row_count = rows.count()

        if validate:
            for i in range(row_count):
                matching_field = rows.nth(i).locator("td").nth(self.M_field).inner_text().strip()
                sl_no = rows.nth(i).locator("td").nth(self.S_No).inner_text().strip()

                is_invalid = False
                port_name = None

                # --- Handle Port of Lading ---
                if matching_field.lower() == "port of lading" and self.Port_Lading_col is not None:
                    product_span = rows.nth(i).locator("td").nth(self.Port_Lading_col).locator("[data-tip]").first
                    product_tip = product_span.get_attribute("data-tip") if product_span.count() > 0 else None
                    port_name = product_tip.strip() if product_tip else rows.nth(i).locator("td").nth(
                        self.Port_Lading_col).inner_text().strip()

                    self.port_name_hyperlink = port_name.split(",")[0].strip()

                    print(self.port_name_hyperlink)

                    if self.selected_port.lower().strip() in port_name.lower().strip():
                        print(f"✅ Port of Lading match: {port_name} at Sl. No: {sl_no}")
                    else:
                        print(f"❌ Invalid Port of Lading: {port_name} at Sl. No: {sl_no}")
                        is_invalid = True

                # --- Handle Port of Unlading ---
                elif matching_field.lower() == "port of unlading" and self.Port_Unlading_col is not None:
                    product_span = rows.nth(i).locator("td").nth(self.Port_Unlading_col).locator("[data-tip]").first
                    product_tip = product_span.get_attribute("data-tip") if product_span.count() > 0 else None
                    port_name = product_tip.strip() if product_tip else rows.nth(i).locator("td").nth(
                        self.Port_Unlading_col).inner_text().strip()

                    if self.selected_port.lower().strip() in port_name.lower().strip():
                        print(f"✅ Port of Unlading match: {port_name} at Sl. No: {sl_no}")
                    else:
                        print(f"❌ Invalid Port of Unlading: {port_name} at Sl. No: {sl_no}")
                        is_invalid = True

                # --- Invalid Matching Field ---
                else:
                    print(f"❌ Invalid Matching field: {matching_field} at Sl. No: {sl_no}")
                    is_invalid = True
        #         #Check next page
        #         next_button = self.page.locator('[class="trademo-table-arrow-button"]').nth(1)
        #         if next_button.is_enabled():
        #             next_button.click()
        #             self.page.locator("table tbody tr td:nth-child(4)").first.wait_for(
        #                 state="visible", timeout=100000
        #             )
        #             self.Check_Port_description_Shipment_Grid(file_name)
        #         else:
        #             print("✅ All pages validated")
        #
        #         # --- If invalid, store data ---
        #         if is_invalid:
        #             self.invalid_entries.append({
        #                 "slNo": sl_no,
        #                 "Port": port_name if port_name else "N/A",
        #                 "matching_field": matching_field
        #             })
        #
        # # --- Save invalid entries ---
        # if not self.invalid_entries:
        #     print("📘 No invalid entries found.")
        #     return
        #
        # os.makedirs("results", exist_ok=True)
        # workbook = Workbook()
        # sheet = workbook.active
        # sheet.title = "Invalid Port"
        #
        # # Headers
        # sheet.append(["Sl. No", "Port", "Matching Field"])
        #
        # # Red fill style
        # red_fill = PatternFill(start_color="FF0000", end_color="FF0000", fill_type="solid")
        #
        # for item in self.invalid_entries:
        #     row = sheet.max_row + 1
        #     sheet.cell(row=row, column=1, value=item["slNo"])
        #     port_cell = sheet.cell(row=row, column=2, value=item["Port"])
        #     match_field_cell = sheet.cell(row=row, column=3, value=item["matching_field"])
        #
        #     # Apply red fill
        #     port_cell.fill = red_fill
        #     match_field_cell.fill = red_fill
        # workbook.save(os.path.join("results", file_name))
        # print(f"📁 Invalid Port data saved to 'results/{file_name}'")

    def Validate_Discover_insight_ports(self):
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

    def Verify_Shipment_tab_Manual_suggest(self, Extracted_Text: str, validate: bool = True):
        if not hasattr(self, "invalid_entries"):
            self.invalid_entries = []

        # Click on the Shipment tab
        self.page.locator("//a[@id='nav-home-tab']").click()
        rows = self.page.locator("table tbody tr")
        row_count = rows.count()
        extracted_text_lower = Extracted_Text.lower()

        if validate:
            for i in range(row_count):
                # ✅ Initialize variables for each row
                consignee_address = ""
                Shipper_Standardized_Name = ""
                Consignee_Standardized_Name = ""

                view = rows.nth(i).locator("td").nth(1)
                matching_field = rows.nth(i).locator("td").nth(3).inner_text().strip()
                sl_no = rows.nth(i).locator("td").nth(2).inner_text().strip()
                shipper_name = rows.nth(i).locator("td").nth(8).inner_text().strip()
                consignee_name = rows.nth(i).locator("td").nth(9).inner_text().strip()

                product_span = rows.nth(i).locator("td").nth(6).locator("[data-tip]").first
                product_tip = product_span.get_attribute("data-tip") if product_span.count() > 0 else None
                product = product_tip.strip() if product_tip and product_tip.strip() else rows.nth(i).locator("td").nth(
                    6).inner_text().strip()

                is_invalid = False
                matching_fields_list = [mf.strip() for mf in matching_field.split(",")]

                for mf in matching_fields_list:
                    if mf == "Product Description":
                        if extracted_text_lower in product.lower():
                            print(f"✅ Product contains keyword: {product} at Sl. No: {sl_no}")
                        else:
                            print(f"❌ Product does not contain keyword: {product} at Sl. No: {sl_no}")
                            is_invalid = True

                    elif mf == "Shipper Name":
                        if extracted_text_lower in shipper_name.lower():
                            print(f"✅ Shipper name contains keyword: {shipper_name} at Sl. No: {sl_no}")
                        else:
                            print(f"❌ Shipper name mismatch: {shipper_name} at Sl. No: {sl_no}")
                            is_invalid = True

                    elif mf == "Consignee Name":
                        if extracted_text_lower in consignee_name.lower():
                            print(f"✅ Consignee name contains keyword: {consignee_name} at Sl. No: {sl_no}")
                        else:
                            print(f"❌ Search keyword not found in consignee name: {consignee_name} at Sl. No: {sl_no}")
                            is_invalid = True

                    elif mf == "Consignee Address":
                        view.click()
                        read_more_locator = self.page.get_by_text("Read more").last
                        self.page.wait_for_timeout(1000)  # wait for rendering

                        if read_more_locator.is_visible():
                            print("🔍 'Read More' is visible, clicking...")
                            read_more_locator.click()
                        consignee_address = self.page.locator("span > .read-more-cards").last.inner_text().strip()

                        if extracted_text_lower in consignee_address.lower():
                            print(f"✅ Address contains keyword {consignee_address} at Sl. No: {sl_no}")
                        else:
                            print(
                                f"❌ Search keyword not found in consignee address: {consignee_address} at Sl. No: {sl_no}")
                            is_invalid = True
                        self.page.locator("//span[@aria-hidden='true']").click()

                    elif mf == "Shipper Standardized Name":
                        view.click()
                        read_more_locator = self.page.get_by_text("Read more").first
                        self.page.wait_for_timeout(1000)

                        if read_more_locator.is_visible():
                            read_more_locator.click()

                        Shipper_Standardized_Name = self.page.locator(" //span[normalize-space(text())='Shipper Standardized Name'] /ancestor::div[contains(@class,'col-5')] /following-sibling::div[contains(@class,'col-7')]//a").inner_text().strip()
                        if extracted_text_lower in Shipper_Standardized_Name.lower():
                            print(
                                f"✅ Shipper Standardized Name contains keyword {Shipper_Standardized_Name} at Sl. No: {sl_no}")
                        else:
                            print(
                                f"❌ Search keyword not found in shipper standardized name: {Shipper_Standardized_Name} at Sl. No: {sl_no}")
                            is_invalid = True
                        self.page.locator("//span[@aria-hidden='true']").click()

                    elif mf == "Consignee Standardized Name":
                        view.click()
                        Consignee_Standardized_Name = self.page.locator(" //span[normalize-space(text())='Consignee Standardized Name'] /ancestor::div[contains(@class,'col-5')] /following-sibling::div[contains(@class,'col-7')]//a").inner_text().strip()
                        if extracted_text_lower in Consignee_Standardized_Name.lower():
                            print(
                                f"✅ Consignee Standardized Name contains keyword {Consignee_Standardized_Name} at Sl. No: {sl_no}")
                        else:
                            print(
                                f"❌ Search keyword not found in consignee standardized name: {Consignee_Standardized_Name} at Sl. No: {sl_no}")
                            is_invalid = True
                        self.page.locator("//span[@aria-hidden='true']").click()

                if is_invalid:
                    self.invalid_entries.append({
                        "matching_field": matching_field,
                        "slNo": sl_no,
                        "product": product,
                        "Shipper_Name": shipper_name,
                        "Consignee_Name": consignee_name,
                        "Consignee_Address": consignee_address,
                        "Shipper_Standardized_Name": Shipper_Standardized_Name,
                        "Consignee_Standardized_Name": Consignee_Standardized_Name
                    })

        # Handle next page
        # next_button = self.page.locator('[class="trademo-table-arrow-button"]').nth(1)
        # if next_button.is_enabled():
        #     next_button.click()
        #     self.page.locator("table tbody tr td:nth-child(4)").first.wait_for(state="visible", timeout=100000)
        #     self.Verify_Shipment_tab_Manual_suggest(Extracted_Text)
        # else:
        #     print("✅ All pages validated")
            if not self.invalid_entries:
                print("📘 No invalid entries found.")
                return

            # Save invalid entries to Excel
            os.makedirs("results", exist_ok=True)
            workbook = Workbook()
            sheet = workbook.active
            sheet.title = "Invalid Data"

            sheet.append([
                "Sl. No", "Product Description", "Shipper Name", "Consignee Name",
                "Consignee Address", "Shipper Standardized Name", "Consignee Standardized Name", "Matching Field"
            ])
            red_fill = PatternFill(start_color="FF0000", end_color="FF0000", fill_type="solid")

            for item in self.invalid_entries:
                row = sheet.max_row + 1
                sheet.cell(row=row, column=1, value=item.get("slNo"))
                sheet.cell(row=row, column=2, value=item.get("product"))
                sheet.cell(row=row, column=3, value=item.get("Shipper_Name"))
                sheet.cell(row=row, column=4, value=item.get("Consignee_Name"))
                sheet.cell(row=row, column=5, value=item.get("Consignee_Address"))
                sheet.cell(row=row, column=6, value=item.get("Shipper_Standardized_Name"))
                sheet.cell(row=row, column=7, value=item.get("Consignee_Standardized_Name"))
                sheet.cell(row=row, column=8, value=item.get("matching_field"))

                # Highlight invalid values in red
                for col in range(2, 9):
                    cell = sheet.cell(row=row, column=col)
                    if cell.value:
                        cell.fill = red_fill

            file_path = f"results/Manual_Search_{Extracted_Text}.xlsx"
            print(f"📁 Invalid data saved to '{file_path}'")

    def Manual_suggest_hs_code(self,hs_code:str):
        expect(self.page.get_by_placeholder(
            "Type to search in all categories or choose from the category below")).to_be_visible()
        # Manual suggest search for HS Code
        self.page.get_by_role("textbox", name="Type to search in all").click()
        self.page.get_by_role("textbox", name="Type to search in all").fill(hs_code)
        self.page.locator(".tw-bg-primary-purple-500").click()

    def Manual_suggest_shipper(self,shipper_name:str):
        expect(self.page.get_by_placeholder(
            "Type to search in all categories or choose from the category below")).to_be_visible()
        # Manual suggest search for Shipper
        self.page.get_by_role("textbox", name="Type to search in all").click()
        self.page.get_by_role("textbox", name="Type to search in all").fill(shipper_name)
        self.page.locator(".tw-bg-primary-purple-500").click()
        expect(self.page.locator("table tbody tr")).to_have_count(10, timeout=100000)
        self.page.wait_for_timeout(3000)

    def Manual_suggest_consignee(self,consignee_name:str):
        expect(self.page.get_by_placeholder(
            "Type to search in all categories or choose from the category below")).to_be_visible()
        # Manual suggest search for Consignee
        self.page.get_by_role("textbox", name="Type to search in all").click()
        self.page.get_by_role("textbox", name="Type to search in all").fill(consignee_name)
        self.page.locator(".tw-bg-primary-purple-500").click()
        expect(self.page.locator("table tbody tr")).to_have_count(10, timeout=100000)
        self.page.wait_for_timeout(3000)

    def Manual_suggest_port(self,port_name:str):
        expect(self.page.get_by_placeholder(
            "Type to search in all categories or choose from the category below")).to_be_visible()
        # Manual suggest search for Port
        self.page.get_by_role("textbox", name="Type to search in all").click()
        self.page.get_by_role("textbox", name="Type to search in all").fill(port_name)
        self.page.locator(".tw-bg-primary-purple-500").click()
        expect(self.page.locator("table tbody tr")).to_have_count(10, timeout=100000)
        self.page.wait_for_timeout(3000)

    def auto_suggest_manual_hs_code(self, hs_code:str):
        self.page.pause()
        self.page.get_by_role("textbox", name="Type to search in all").click()
        self.page.get_by_role("textbox", name="Type to search in all").fill(hs_code)
        self.selected_hs_code = self.page.locator('[class="tw-font-medium tw-bg-transparent tw-p-0"]').nth(0).inner_text().strip()
        self.page.locator('[class="tw-font-medium tw-bg-transparent tw-p-0"]').nth(0).click()
        print(f"Selected HS Code is: {self.selected_hs_code}")
        self.page.locator(".tw-bg-primary-purple-500").click()
        self.page.wait_for_timeout(3000)

    def auto_suggest_manual_product(self, product_name: str):
        self.page.get_by_role("textbox", name="Type to search in all").click()
        self.page.get_by_role("textbox", name="Type to search in all").fill(product_name)
        self.selected_product = self.page.locator('[class="tw-font-medium tw-bg-transparent tw-p-0"]').nth(
            0).inner_text().strip()
        self.page.locator('[class="tw-font-medium tw-bg-transparent tw-p-0"]').nth(0).click()
        print(f"Selected product is: {self.selected_product}")
        self.page.locator(".tw-bg-primary-purple-500").click()
        self.page.wait_for_timeout(3000)
        self.page.locator("table tbody tr td:nth-child(4)").first.wait_for(state="visible", timeout=100000)

    def auto_suggest_manual_shipper(self, shipper_name:str):
        self.page.get_by_role("textbox", name="Type to search in all").click()
        self.page.get_by_role("textbox", name="Type to search in all").fill(shipper_name)
        self.selected_shipper = self.page.locator('[class="tw-font-medium tw-bg-transparent tw-p-0"]').nth(
            0).inner_text().strip()
        self.page.locator('[class="tw-font-medium tw-bg-transparent tw-p-0"]').nth(0).click()
        expect(self.page.get_by_role("main")).to_contain_text("Shipper")
        self.page.locator(".tw-bg-primary-purple-500").click()

    def auto_suggest_manual_consignee(self,consignee:str):
        self.page.get_by_role("textbox", name="Type to search in all").click()
        self.page.get_by_role("textbox", name="Type to search in all").fill(consignee)
        self.selected_consignee = self.page.locator('[class="tw-font-medium tw-bg-transparent tw-p-0"]').nth(
            0).inner_text().strip()
        self.page.locator('[class="tw-font-medium tw-bg-transparent tw-p-0"]').nth(0).click()
        expect(self.page.get_by_role("main")).to_contain_text("Consignee")
        self.page.locator(".tw-bg-primary-purple-500").click()

    def auto_suggest_manual_chemical(self, chemical_name:str):
        self.page.get_by_role("textbox", name="Type to search in all").click()
        self.page.get_by_role("textbox", name="Type to search in all").fill(chemical_name)
        self.selected_chemical= self.page.locator('[class="tw-font-medium tw-bg-transparent tw-p-0"]').nth(
            0).inner_text().strip()
        self.page.locator('[class="tw-font-medium tw-bg-transparent tw-p-0"]').nth(0).click()
        expect(self.page.get_by_role("main")).to_contain_text("Chemical")
        self.page.locator(".tw-bg-primary-purple-500").click()

    def auto_suggest_manual_port(self, port_name: str):
        self.page.get_by_role("textbox", name="Type to search in all").click()
        self.page.get_by_role("textbox", name="Type to search in all").fill(port_name)
        self.selected_port = self.page.locator('[class="tw-font-medium tw-bg-transparent tw-p-0"]').first.inner_text().strip()
        self.page.locator('[class="tw-font-medium tw-bg-transparent tw-p-0"]').first.click()
        expect(self.page.get_by_role("main")).to_contain_text("Port")
        self.page.locator(".tw-bg-primary-purple-500").click()
        self.page.wait_for_timeout(3000)
        self.page.locator("table tbody tr td:nth-child(4)").first.wait_for(state="visible", timeout=100000)
        expect(self.page.get_by_role("main")).to_contain_text(self.selected_port)
        print(f"Selected Port is: {self.selected_port}")

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
















































