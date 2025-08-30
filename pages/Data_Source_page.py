import time
from playwright.sync_api import Page, expect
from playwright.sync_api import expect, TimeoutError as PlaywrightTimeoutError


class Data_Source_Filter:
    def __init__(self, page: Page):
        self.page = page

    def Validate_Country_dropdown(self):
        self.page.pause()
        # Open the country dropdown
        self.page.locator("[class='tw-flex tw-items-center tw-gap-3 tw-border-none tw-text-sm']").click()
        #The dropdown should open, and a list of countries should be visible. Each country should have a checkbox and Import label
        # Verify All countries,All Imports , All Exports labels are visible
        clear_all_btn = self.page.get_by_role("button", name="Clear All")

        # Wait for the element to be attached to DOM
        if clear_all_btn.is_visible() and clear_all_btn.is_enabled():
            clear_all_btn.click()
            print("✅ 'Clear All' button clicked.")
        else:
            print("ℹ️ 'Clear All' button is either not visible or disabled.")

        expect(self.page.locator("text=All Countries")).to_be_visible()
        expect(self.page.locator('[class="tw-text-sm tw-font-medium tw-gray-900"]').nth(1)).to_contain_text(
            "All Imports")
        expect(self.page.locator('[class="tw-text-sm tw-font-medium tw-gray-900"]').nth(2)).to_contain_text(
            'All Exports')

        # Get all country rows
        country_rows = self.page.locator('[class="tw-flex tw-items-center tw-w-full"]')
        total_rows = country_rows.count()
        print(f"Found {total_rows} country rows.")
        i = 0

        while i < total_rows:
            row = country_rows.nth(i)
            row.scroll_into_view_if_needed()

            # Small delay for lazy loading
            time.sleep(0.3)

            # Extract country name (leftmost text)
            country_name = row.inner_text().strip()
            print(f"🌍 {i + 1}. {country_name}")

            # Locate all checkboxes in the row
            checkboxes = row.locator('input[type="checkbox"]')
            count = checkboxes.count()

            if count == 0:
                print(f"⚠️ No checkbox found for '{country_name}', skipping validation.")
            elif count == 1:
                expect(checkboxes.nth(0)).to_be_visible()
                print(f"✅ Only one checkbox found for '{country_name}' (check UI config)")
            elif count >= 2:
                # First = Import, Second = Export
                expect(checkboxes.nth(0)).to_be_visible()
                print(f"✅ Import Checkbox is present for '{country_name}'")

                expect(checkboxes.nth(1)).to_be_visible()
                print(f"✅ Export Checkbox is present for '{country_name}'")

            i += 1
            total_rows = country_rows.count()

    def All_Countries_Checkbox(self):
        # Click on All Countries checkbox
        all_countries_checkbox = self.page.locator("//div[normalize-space(text())='All Countries']/preceding-sibling::input[@type='checkbox']")
        #All country checkboxes should be selected automatically
        all_countries_checkbox.check()

        # Wait for the checkboxes to update
        self.page.wait_for_timeout(1000)

        # Get all 'All Imports' checkboxes
        import_checkboxes = self.page.locator("//div[normalize-space(.)='All Imports']/preceding-sibling::input[@type='checkbox']").first
        # Get all 'All Exports' checkboxes
        export_checkboxes = self.page.locator("//div[normalize-space(.)='All Exports']/preceding-sibling::input[@type='checkbox']").first
        # Check if import and export checkbox are checked
        expect(import_checkboxes).to_be_checked()
        expect(export_checkboxes).to_be_checked()

        country_rows = self.page.locator('[class="tw-flex tw-items-center tw-w-full"]')
        total_rows = country_rows.count()
        # Select All checkbox selects all countries in the list; all checkboxes get ticked successfully
        i = 0
        while i < 35:
            row = country_rows.nth(i)
            row.scroll_into_view_if_needed()

            # Small delay for lazy loading
            time.sleep(0.3)

            # Extract country name (leftmost text)
            country_name = row.inner_text().strip()
            print(f"🌍 {i + 1}. {country_name}")

            # Locate all checkboxes in the row
            checkboxes = row.locator('input[type="checkbox"]')
            count = checkboxes.count()

            if count == 0:
                print(f"⚠️ No checkbox found for '{country_name}', skipping validation.")
            elif count == 1:
                expect(checkboxes.nth(0)).to_be_visible()
                expect(checkboxes.nth(0)).to_be_checked(timeout=5000)
                print(f"⚠️ Only one checkbox found for '{country_name}' (check UI config)")
            elif count >= 2:
                # First = Import, Second = Export
                expect(checkboxes.nth(0)).to_be_visible()
                expect(checkboxes.nth(0)).to_be_checked(timeout=5000)
                print(f"✅ Import Checkbox is checked for '{country_name}'")

                expect(checkboxes.nth(1)).to_be_visible()
                expect(checkboxes.nth(1)).to_be_checked(timeout=5000)
                print(f"✅ Export Checkbox is checked for '{country_name}'")
            i += 1
            total_rows = country_rows.count()


        # Click on Apply button
        self.page.locator("//span[normalize-space()='Apply']").click()

        # Check Universal search text
        expect(self.page.locator("//span[normalize-space()='Universal Search']")).to_contain_text("Universal Search",timeout=100000)

    def Validate_Cancel_Apply_button(self):
        # Open the country dropdown
        self.page.locator("[class='tw-flex tw-items-center tw-gap-3 tw-border-none tw-text-sm']").click()
        # Step 3 Click the Clear all button
        self.page.get_by_role("button", name="Clear All").click()

        self.page.wait_for_timeout(1000)
        import_checkbox = self.page.locator("//div[normalize-space(.)='All Imports']/preceding-sibling::input[@type='checkbox']").first
        # Get all 'All Exports' checkboxes
        export_checkboxes = self.page.locator("//div[normalize-space(.)='All Exports']/preceding-sibling::input[@type='checkbox']").first

        # Validate all imports checkboxes are uncheckeed
        expect(import_checkbox).to_be_visible(timeout=10000)  # wait until at least one is visible
        expect(import_checkbox).not_to_be_checked()

        # Validate all exports checkboxes are unchecked
        expect(export_checkboxes).to_be_visible(timeout=10000)
        expect(export_checkboxes).not_to_be_checked()

        country_rows = self.page.locator('[class="tw-flex tw-items-center tw-w-full"]')
        total_rows = country_rows.count()
        print(f"Found {total_rows} country rows.")
        #it  should  discard selected filters
        i = 0
        while i < total_rows:
            row = country_rows.nth(i)
            row.scroll_into_view_if_needed()

            # Small delay for lazy loading
            time.sleep(0.3)

            # Extract country name
            country_name = row.inner_text().strip()
            print(f"🌍 {i + 1}. {country_name}")

            # Locate all checkboxes in the row
            checkboxes = row.locator('input[type="checkbox"]')
            count = checkboxes.count()

            if count == 0:
                print(f"⚠️ No checkbox found for '{country_name}', skipping validation.")
            elif count == 1:
                expect(checkboxes.nth(0)).to_be_visible()
                expect(checkboxes.nth(0)).not_to_be_checked(timeout=5000)
                print(f"✅ Import checkbox is unchecked for '{country_name}'")
            elif count >= 2:
                # First = Import, Second = Export
                expect(checkboxes.nth(0)).to_be_visible()
                expect(checkboxes.nth(0)).not_to_be_checked(timeout=5000)
                print(f"✅ Import Checkbox is unchecked for '{country_name}'")

                expect(checkboxes.nth(1)).to_be_visible()
                expect(checkboxes.nth(1)).not_to_be_checked(timeout=5000)
                print(f"✅ Export Checkbox is unchecked for '{country_name}'")
            i += 1
            total_rows = country_rows.count()

        # Step 5 Select any country checkbox
        rows = self.page.locator('[class="tw-flex tw-items-center tw-w-full"]')
        count = rows.count()

        for i in range(count):
            row_text = rows.nth(i).inner_text().strip()
            if "India" in row_text:
                rows.nth(i).locator('input[type="checkbox"]').first.click()
                break

        # Click on Apply button
        self.page.locator("//span[normalize-space()='Apply']").click()
        #Dropdown should close and selected filter should be applied to shipment data
        expect(self.page.locator('[class="tw-flex tw-items-center tw-w-full"]')).not_to_be_visible()
        expect(self.page.locator('[class="tw-text-nowrap"]')).to_contain_text("India Imports")
        print("India import is selected in filter")

