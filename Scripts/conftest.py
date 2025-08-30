import csv
import os
import sys
import pytest
import allure
from playwright.sync_api import sync_playwright, Page, expect
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


# ---------- CSV LOADER ----------
def load_CSV_data(file_path='./test_data/login.csv'):
    """Load email, password & country from CSV."""
    with open(file_path, mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        first_row = next(reader)
        print("Loaded row:", first_row)
        return first_row['email'], first_row['password'], first_row['country']


# ---------- BROWSER FIXTURE ----------
@pytest.fixture(scope="class")
def browser_setup(request):
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(
        record_video_dir="videos/",
        viewport={"width": 1280, "height": 720}
    )
    page = context.new_page()

    # login steps...
    email, password, country = load_CSV_data()
    page.goto("https://accounts.trademo.com/", wait_until="load")
    page.get_by_placeholder("Enter registered email address").fill(email)
    page.get_by_placeholder("Enter your password").fill(password)
    page.get_by_role("button", name="Sign In on Trademo").click()

    try:
        page.wait_for_selector("text=Shipments", timeout=6000)
        expect(page.locator('[class*="tw-bg-user-pill-bg"]')).to_be_visible()
    except (PlaywrightTimeoutError, AssertionError):
        page.get_by_role("button", name="Confirm and Sign In").click()
        expect(page.locator("text=Shipments")).to_be_visible(timeout=100000)

    request.cls.page = page
    request.cls.context = context

    yield page

    video_path = page.video.path() if page.video else None
    page.close()
    context.close()
    browser.close()
    playwright.stop()

    if video_path and os.path.exists(video_path):
        if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
            allure.attach.file(video_path, name="Test Video",
                               attachment_type=allure.attachment_type.MP4)
        else:
            os.remove(video_path)




# ---------- COUNTRY SELECTION FIXTURE ----------
@pytest.fixture(scope="class")
def Check_Country(browser_setup: Page):
    """Fixture that returns a function to ensure the given country from CSV is selected in the Data Source filter."""

    page = browser_setup

    def _check_country():
        _, _, country = load_CSV_data()   # ✅ get country from CSV
        source_type = "Imports"           # default (can extend later if needed)

        page.wait_for_selector(".tw-text-nowrap > span", timeout=10000)
        text_content = page.locator(".tw-text-nowrap > span").text_content()

        expected_text = f"{country} {source_type}"
        if expected_text not in text_content:
            page.locator("[class='tw-flex tw-items-center tw-gap-3 tw-border-none tw-text-sm']").click()

            clear_all_btn = page.get_by_role("button", name="Clear All")
            if clear_all_btn.is_visible() and clear_all_btn.is_enabled():
                clear_all_btn.click()
                print("✅ 'Clear All' button clicked.")

            rows = page.locator('[class="tw-flex tw-items-center tw-w-full"]')
            for i in range(rows.count()):
                row_text = rows.nth(i).inner_text().strip()
                if country in row_text:
                    rows.nth(i).locator('input[type="checkbox"]').first.click()
                    break

            page.locator("//span[normalize-space()='Apply']").click()
            print(f"✅ {expected_text} is selected in filter")
        else:
            print(f"ℹ️ {expected_text} is already selected in filter. No action needed.")

    return _check_country   # 👈 VERY IMPORTANT

@pytest.fixture
def Reset(browser_setup: Page):
    """Fixture to click Reset if it's visible."""

    page = browser_setup

    def _reset():
        reset_locator = page.get_by_text(" Reset").first
        if reset_locator.is_visible():
            print("🔍 'Reset' is visible, clicking...")
            reset_locator.click()
            expect(page.get_by_placeholder("Type to search in all categories or choose from the category below")).to_be_visible()
        else:
            print("ℹ️ 'Reset' not visible.")

    return _reset
@pytest.fixture
def Reset_Default_view(browser_setup: Page):
    """Fixture to click Reset if it's visible."""

    page = browser_setup

    def _reset_default_view():
        page.locator("//a[@id='nav-home-tab']").click()
        expect(page.locator("//a[@id='nav-home-tab']")).to_be_visible(timeout=6000)
        # In the shipment grid, click on Customise Shipment Grid button
        page.get_by_role("button", name="dashboard_customize Customise").click()
        expect(page.locator("#custom-shipment-grid-modal")).to_contain_text(
            "Select columns for your grid.*You can select and display maximum of 15 columns.")
        # Verify the available section categories
        expect(page.locator("#custom-shipment-grid-modal")).to_contain_text("primary details")
        # Click Reset Default View
        page.get_by_role("button", name="Reset Default View").click()
        expect(page.get_by_text("user configuration set")).to_be_visible()

    return _reset_default_view   # 👈 return the function, not the call

@pytest.fixture
def Close_modal(browser_setup: Page):
    """Fixture to click Reset if it's visible."""

    page = browser_setup

    def _closemodal():
        Close_btn = page.get_by_role("button", name="Close")
        if Close_btn.is_visible():
            print("🔍 'Close' is visible, clicking...")
            Close_btn.click()
        else:
            print("ℹ️ 'Close' not visible.")

    return _closemodal


