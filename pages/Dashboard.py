from playwright.sync_api import expect


class DashboardPage:
    def __init__(self,page):
        self.page=page
        self.invalid_entries = []

    def Get_table_rows(self):
       return self.page.locator("table tbody tr")

    def Verify_HSCode(self,expected_hs_code_prefix:str):
        rows = self.Get_table_rows()
        row_count = rows.count()

        for i in range(row_count):
            hs_code = rows.nth(i).locator("td").nth(8).inner_text().strip()
            sl_no = rows.nth(i).locator("td").nth(2).inner_text().strip()

            if hs_code.startswith(expected_hs_code_prefix):
                print(f"✅ Valid HS Code found: {hs_code} at Sl. No: {sl_no}")
            else:
                print(f"❌ Invalid HS Code found: {hs_code} at Sl. No: {sl_no}")
                self.invalid_entries.append({"slNo": sl_no, "hsCode": hs_code})
        # Pagination: click "Next" if enabled
        # next_button = page.locator('[class="trademo-table-arrow-button"]').nth(1)
        # if next_button.is_enabled():
        #     next_button.click()
        #     page.wait_for_timeout(1000)  # Wait for page to update
        #     check_hs_codes_on_page(page, expected_hs_code_prefix)
        # else:
        #     print("✅ All pages validated")
        #     with open("invalid_hs_codes.json", "w") as f:
        #         json.dump(invalid_entries, f, indent=2)
    def HS_Code_validate(self):
        return self.page.get_by_text("HS:")

    def HS_Code_Search(self):
        self.page.get_by_role("textbox", name="Type to search in all").click()
        self.page.get_by_text("HS Code", exact=True).click()
        self.page.get_by_role("textbox", name="Search upto 20 Harmonised").fill("392330")
        self.page.get_by_text("HS:392330 - Plastics and").click()
        self.page.get_by_role("textbox", name="Search upto 20 Harmonised").press("Enter")
        expect(self.HS_Code_validate()).to_be_visible()
        self.page.get_by_text("Discover more insights about").click()

        self.page.locator("//a[@id='nav-home-tab']").click()
        self.page.wait_for_timeout(3000)

