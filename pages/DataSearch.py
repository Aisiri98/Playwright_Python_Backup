import time
from playwright.sync_api import expect
from playwright.sync_api import Page, expect, TimeoutError as PlaywrightTimeoutError


class DashboardPage:
    def __init__(self, page):
        self.page = page
        self.email_input = page.locator("#email")  # Update selectors as per actual DOM
        self.password_input = page.locator("#password")
        self.login_button = page.locator("button[type='submit']")
        self.country_dropdown = page.locator("[class='tw-flex tw-items-center tw-gap-3 tw-border-none tw-text-sm']")
        self.label_all_countries = page.locator("text=All Countries")
        self.label_all_imports = page.locator('[class="tw-text-sm tw-font-medium tw-gray-900"]').nth(1)
        self.label_all_exports = page.locator('[class="tw-text-sm tw-font-medium tw-gray-900"]').nth(2)
        self.country_rows = page.locator('[class="tw-flex tw-items-center tw-w-full"]')

    def login(self, email: str, password: str):
        self.page.goto("https://accounts.trademo.com/")
        self.page.get_by_placeholder("Enter registered email address").fill(email)
        self.page.get_by_placeholder("Enter your password").fill(password)
        self.page.get_by_role("button", name="Sign In on Trademo").click()

        try:
            self.page.wait_for_selector("text=Shipments", timeout=6000)
            print("User is logged in")
            expect(self.page.locator('[class*="tw-bg-user-pill-bg"]')).to_be_visible()
        except (PlaywrightTimeoutError, AssertionError):
            print("Session already active with same user ID")
            self.page.get_by_role("button", name="Confirm and Sign In").click()
            print("User is logged in after confirming.")
            expect(self.page.locator("text=Shipments")).to_be_visible(timeout=100000)

    def open_country_dropdown(self):
        self.country_dropdown.click()

    def verify_labels(self):
        expect(self.label_all_countries).to_be_visible()
        expect(self.label_all_imports).to_contain_text("All Imports")
        expect(self.label_all_exports).to_contain_text("All Exports")

    def validate_country_checkboxes(self):
        total_rows = self.country_rows.count()
        print(f"Found {total_rows} country rows.")
        for i in range(total_rows):
            row = self.country_rows.nth(i)
            row.scroll_into_view_if_needed()
            time.sleep(0.3)  # for lazy loading
            country_name = row.inner_text().strip()
            print(f"🌍 {i + 1}. {country_name}")

            import_checkbox = row.locator('input[type="checkbox"]').first
            export_checkbox = row.locator('input[type="checkbox"]').last

            if import_checkbox.count() == 0:
                print(f"⚠️ No Import checkbox for '{country_name}'")
            else:
                expect(import_checkbox).to_be_visible(timeout=5000)
                print(f"✅ Import Checkbox present for '{country_name}'")

            if export_checkbox.count() == 0:
                print(f"⚠️ No Export checkbox for '{country_name}'")
            else:
                expect(export_checkbox).to_be_visible(timeout=5000)
                print(f"✅ Export Checkbox present for '{country_name}'")
