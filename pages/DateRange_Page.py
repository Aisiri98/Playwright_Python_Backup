import time
from playwright.sync_api import Page, expect
from playwright.sync_api import expect, TimeoutError as PlaywrightTimeoutError


class Date_Range_Filter:
    def __init__(self, page: Page):
        self.page = page

    def Click_Date_Range_Drp(self):
        # Click on the Date Range filter
        self.page.locator('[class="form-control"]').click()

    def Validate_All_Options(self):
        options_locator = self.page.locator("ul li[data-range-key]")
        actual_options = [text.strip() for text in options_locator.all_inner_texts()]

        # Define the expected values in correct order
        expected_options = [
            "Last 1 Month",
            "Last 3 Months",
            "Year to Date",
            "Last 1 Year",
            "Last 2 Years",
            "Last 3 Years",
            "All Data",
            "Custom Range"
        ]
        # Verify the available options
        assert actual_options == expected_options, f"Dropdown options mismatch.\nExpected: {expected_options}\nActual: {actual_options}"
        # Select a date range and click Apply (Last 1 month)
        self.page.locator("//li[normalize-space()='Last 1 Month']").click()
        self.page.wait_for_timeout(1000)
        self.page.locator("#reacttourdaterange").get_by_role("textbox").click()
        self.page.get_by_text("Last 3 Months").click()
        self.page.wait_for_timeout(1000)
        self.page.locator("#reacttourdaterange").get_by_role("textbox").click()
        self.page.get_by_text("Year to Date").click()
        self.page.wait_for_timeout(1000)
        self.page.locator("#reacttourdaterange").get_by_role("textbox").click()
        self.page.get_by_text("Last 1 Year").click()
        self.page.wait_for_timeout(1000)
        self.page.locator("#reacttourdaterange").get_by_role("textbox").click()
        self.page.get_by_text("Last 2 Years").click()
        self.page.wait_for_timeout(1000)
        self.page.locator("#reacttourdaterange").get_by_role("textbox").click()
        self.page.get_by_text("Last 3 Years").click()
        self.page.wait_for_timeout(1000)
        self.page.locator("#reacttourdaterange").get_by_role("textbox").click()
        self.page.get_by_text("All Data").click()
        self.page.locator("#reacttourdaterange").get_by_role("textbox").click()
        self.page.get_by_role("button", name="Cancel").click()
        expect(self.page.get_by_text("All Data")).not_to_be_visible()
