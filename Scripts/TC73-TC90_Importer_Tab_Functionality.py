import csv
import os
import sys
import pytest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pages.importer_tab_page import ImportTab


@pytest.mark.usefixtures("browser_setup")
class TestTrademo:
    """Test class for Trademo platform functionality"""

    def test_Trademo_IndiaTC73(self, browser_setup, Reset,Check_Country):
        page = browser_setup
        import_page = ImportTab(page)
        Check_Country()
        print("🔍 Running TC73: Verify that the Rank and Trends tabs are present and functional in the Importers tab")
        Reset()
        import_page.importer_tab()
        import_page.trends_rank_option()

    def test_Trademo_IndiaTC74(self, browser_setup,Reset):
        page = browser_setup
        import_page = ImportTab(page)
        print("🔍 Running TC74: Verify that the Importers Rank tab displays Company Name, Shipments, Consignee State, and Shipment Value (USD) columns.")
        Reset()
        import_page.importer_tab()
        import_page.verify_table_headers()

    def test_Trademo_IndiaTC75(self, browser_setup, Reset):
        page = browser_setup
        import_page = ImportTab(page)
        Reset()
        import_page.importer_tab()
        print(
            "🔍 Running TC75: Validate One Jurisdiction Country Per Company for the Importers tab.")
        import_page.importer_apply_filter()

    def test_Trademo_IndiaTC76(self, browser_setup, Reset):
        page = browser_setup
        import_page = ImportTab(page)
        Reset()
        print(
            "🔍 Running TC76: Verify that the Enable 2nd Level Hierarchy toggle functionality -> Rank tab under the Importers tab.")
        import_page.importer_tab()
        import_page.click_enable_second_level_hierarchy()
        import_page.Ranks_2nd_level_hierarchy_Edit()

    def test_Trademo_IndiaTC77(self, browser_setup, Reset):
        page = browser_setup
        import_page = ImportTab(page)
        Reset()
        print(
            "🔍 Running TC77: Verify that Number of Second Level Entities shows the correct count after enabling the 2nd level hierarchy ->Rank tab under the Importers tab")
        import_page.importer_tab()
        import_page.ranks_second_level_hierarchy()

    def test_Trademo_IndiaTC78(self, browser_setup, Reset):
        page = browser_setup
        import_page = ImportTab(page)
        Reset()
        print(
            "🔍 Running TC78: Verify that Number of Second Level Entities shows the correct count after enabling the 2nd level hierarchy ->Rank tab under the Importers tab.")
        import_page.importer_tab()
        import_page.Enable_2nd_level_hierachy_Rank()
        import_page.Download_option()
        import_page.Validate_Colmn_Shown_In_the_Grid_Download()

    def test_Trademo_IndiaTC79(self, browser_setup, Reset):
        page = browser_setup
        import_page = ImportTab(page)
        Reset()
        print("🔍 Running TC79: Verify Analyse By and Filter By filter functionality (Shipments, Value (USD))→ Rank tab under importers")
        import_page.importer_tab()
        import_page.Analyse_By_Shipment()
        import_page.Analyse_By_Shipment_Value_USD()
        import_page.Filter_by_Shipment_Value()
        import_page.Filter_by_Shipment()

    def test_Trademo_IndiaTC80(self, browser_setup, Reset):
        page = browser_setup
        import_page = ImportTab(page)
        Reset()
        print(
            "🔍 Running TC80: Verify that selecting a checkbox in the Rank tab enables the options (Download, Export to CRM, Bookmark, More Download Options, Fetch Contacts, and Apply Filter)")
        import_page.importer_tab()
        import_page.Validate_option_on_clicking_checkbox()

    def test_Trademo_IndiaTC81(self, browser_setup, Reset):
        page = browser_setup
        import_page = ImportTab(page)
        Reset()
        print("🔍 Running TC81: Verify that the functionality of all options (Download, Export to CRM, Bookmark, Merge, Fetch Contacts, More Download Options and Apply Filter) works correctly after selecting multiple companies in the Rank tab under importers.")
        import_page.importer_tab()
        import_page.Validate_Merge_option()
        import_page.Download_option_Ranktab()
        import_page.Validate_Colmn_Shown_In_the_Grid_Download_Rank()
        import_page.Validate_Export_CRM()
        import_page.Fetch_contacts()
        import_page.Bookmark()
        import_page.importer_apply_filter()

    def test_Trademo_IndiaTC82(self, browser_setup, Reset):
        page = browser_setup
        import_page = ImportTab(page)
        Reset()
        print(
            "🔍 Running TC82: Verify that the Importers Trends tab displays Company Name, Total shipment value trends, and the % overall change column.")
        import_page.importer_tab()
        import_page.verify_trend_headers()

    def test_Trademo_IndiaTC83(self, browser_setup, Reset):
        page = browser_setup
        import_page = ImportTab(page)
        Reset()
        print(
            "🔍 Running TC83: Verify that the Trends view displays Yearly, Quarterly, and Monthly time range dropdown")
        import_page.importer_tab()
        import_page.verify_trend_headers()
        import_page.Verify_Monthly_data()
        import_page.Verify_Quaterly_Data()
        import_page.Verify_Yearly_Data()

    def test_Trademo_IndiaTC84(self, browser_setup, Reset):
        page = browser_setup
        import_page = ImportTab(page)
        Reset()
        print(
            "🔍 Running TC84: Verify that Enable 2nd Level Hierarchy toggle functionality -> Trends tab.")
        import_page.importer_tab()
        import_page.verify_trend_headers()
        import_page.Trends_2nd_level_hierarchy()

    def test_Trademo_IndiaTC85(self, browser_setup, Reset):
        page = browser_setup
        import_page = ImportTab(page)
        Reset()
        print(
            "🔍 Running TC85: Verify that Number of Second Level Entities shows the correct count after enabling the 2nd level hierarchy in the Importers→ Trends tab")
        import_page.importer_tab()
        import_page.verify_trend_headers()
        import_page.Trends_2nd_level_hierarchy()

    def test_Trademo_IndiaTC86(self, browser_setup, Reset,Check_Country):
        page = browser_setup
        import_page = ImportTab(page)
        Check_Country()
        Reset()
        print(
            "🔍 Running TC86: Verify that the download button exports correct data when 2nd level hierarchy is enabled in Importers→ Trends tab.")
        import_page.importer_tab()
        import_page.verify_trend_headers()
        import_page.Enable_Trends_2nd_level_hierarchy()
        import_page.Download_option()
        import_page.Validate_Colmn_Shown_In_the_Grid_Download()

    def test_Trademo_IndiaTC87(self, browser_setup, Reset):
        page = browser_setup
        import_page = ImportTab(page)
        Reset()
        print(
            "🔍 Running TC87: Verify  Analyse By and Filter by filter functionality (Shipments, Value (USD))→ Trends tab. in importers")
        import_page.importer_tab()
        import_page.verify_trend_headers()
        import_page.Analyse_By_Shipment()
        import_page.Analyse_By_Shipment_Value_USD()
        import_page.Filter_by_Shipment_Trends()
        import_page.Filter_by_Shipment_Value_Trends()


    def test_Trademo_IndiaTC88(self, browser_setup, Reset):
        page = browser_setup
        import_page = ImportTab(page)
        Reset()
        print(
            "🔍 Running TC88: Verify that selecting a checkbox in Importers→ Trends enables the options (Download, Export to CRM, Bookmark, More Download Options, Fetch Contacts, and Apply Filter) ")
        import_page.importer_tab()
        import_page.verify_trend_headers()
        import_page.Validate_option_on_clicking_checkbox()

    def test_Trademo_IndiaTC89(self, browser_setup, Reset):
        page = browser_setup
        import_page = ImportTab(page)
        Reset()
        print(
            "🔍 Running TC89: Verify that the functionality of all options (Download, Export to CRM, Bookmark, More Download Options, merge Fetch Contacts, and Apply Filter) works correctly after selecting multiple companies in the Importers→ Trends tab ")
        import_page.importer_tab()
        import_page.verify_trend_headers()
        import_page.Validate_Merge_option()
        import_page.Download_option_Trendtab()
        import_page.Validate_Colmn_Shown_In_the_Grid_Download_Trends()
        import_page.Validate_Export_CRM()
        import_page.Fetch_contacts()
        import_page.Bookmark()

    def test_Trademo_IndiaTC90(self, browser_setup, Reset):
        page = browser_setup
        import_page = ImportTab(page)
        Reset()
        print(
            "🔍 Running TC90: Verify that clicking Apply Filter for any company in Importers tab redirects to the shipment grid and displays data filtered by that specific company.")
        import_page.importer_tab()
        import_page.verify_table_headers()
        import_page.validate_data_after_applying_filter()
        Reset()
        import_page.Validate_Tab_count_after_Manual_search()






































