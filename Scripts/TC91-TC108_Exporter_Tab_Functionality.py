import csv
import os
import sys
import pytest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pages.exporter_tab_page import ExportTab
@pytest.mark.usefixtures("browser_setup")

class TestTrademo:
    """Exporter Tab functionality"""

    def test_Trademo_IndiaTC91(self, browser_setup, Reset,Check_Country):
        page = browser_setup
        export_page = ExportTab(page)
        Check_Country()
        print("🔍 Running TC91: Verify that the Rank and Trends tabs are present and functional in the Exporters tab")
        Reset()
        export_page.exporter_tab()
        export_page.trends_rank_option()

    def test_Trademo_IndiaTC92(self, browser_setup, Reset, Check_Country):
        page = browser_setup
        export_page = ExportTab(page)
        Check_Country()
        print("🔍 Running TC92: Verify that the Exporters Rank tab displays Company Name, Shipments, Shipment Value (USD), columns.")
        Reset()
        export_page.exporter_tab()
        export_page.Click_Rank_tab()
        export_page.verify_rank_table_headers()

    def test_Trademo_IndiaTC93(self, browser_setup, Reset, Check_Country):
        page = browser_setup
        export_page = ExportTab(page)
        Check_Country()
        print(
            "🔍 Running TC93: Validate One Jurisdiction Country Per Company for the Exporters tab.")
        Reset()
        export_page.exporter_tab()
        export_page.verify_rank_table_headers()
        export_page.Exporter_apply_filter()
        Reset()

    def test_Trademo_IndiaTC94(self, browser_setup, Reset, Check_Country):
        page = browser_setup
        export_page = ExportTab(page)
        Check_Country()
        print(
            "🔍 Running TC94: Verify that the Enable 2nd Level Hierarchy toggle functionality -> Rank tab under the Exporters tab.")
        Reset()
        export_page.exporter_tab()
        export_page.verify_rank_table_headers()
        export_page.Enable_second_level_hierarchy()
        export_page.second_level_hierarchy_Edit()
        export_page.Disable_second_level_hierarchy()
        Reset()

    def test_Trademo_IndiaTC95(self, browser_setup, Reset, Check_Country):
        page = browser_setup
        export_page = ExportTab(page)
        Check_Country()
        print(
            "🔍 Running TC95: Verify that Number of Second Level Entities shows the correct count after enabling the 2nd level hierarchy ->Rank tab under the Exporters tab.")
        Reset()
        export_page.exporter_tab()
        export_page.verify_rank_table_headers()
        export_page.Enable_second_level_hierarchy()
        # export_page.validate_countries_per_company()
        export_page.Disable_second_level_hierarchy()

    def test_Trademo_IndiaTC96(self, browser_setup, Reset, Check_Country):
        page = browser_setup
        export_page = ExportTab(page)
        Check_Country()
        print(
            "🔍 Running TC96: Verify that the download button exports correct data when 2nd level hierarchy is enabled in Exporters → Rank tab.")
        Reset()
        export_page.exporter_tab()
        export_page.verify_rank_table_headers()
        export_page.Enable_second_level_hierarchy()
        export_page.Download_option()
        export_page.Validate_Colmn_Shown_In_the_Grid_Download_Rank_2nd_level()

    def test_Trademo_IndiaTC97(self, browser_setup, Reset, Check_Country):
        page = browser_setup
        export_page = ExportTab(page)
        Check_Country()
        print(
            "🔍 Running TC97: Verify Analyse By and Filter By filter functionality (Shipments, Value (USD))→ Rank tab under Exporters ")
        Reset()
        export_page.exporter_tab()
        export_page.verify_rank_table_headers()
        export_page.Analyse_By_Shipment()
        export_page.Analyse_By_Shipment_Value_USD()
        export_page.Filter_by_Shipment_Value()
        export_page.Filter_by_Shipment()

    def test_Trademo_IndiaTC98(self, browser_setup, Reset, Check_Country):
        page = browser_setup
        export_page = ExportTab(page)
        Check_Country()
        print(
            "🔍 Running TC98: Verify that selecting a checkbox enables the options (Download, Export to CRM, Bookmark, More Download Options, Fetch Contacts, and Apply Filter)→ Rank tab under Exporters ")
        Reset()
        export_page.exporter_tab()
        page.pause()
        export_page.verify_rank_table_headers()
        export_page.Validate_option_on_selecting_deselect_checkbox()

    def test_Trademo_IndiaTC99(self, browser_setup, Reset,Close_modal, Check_Country):
        page = browser_setup
        export_page = ExportTab(page)
        Check_Country()
        print(
            "🔍 Running TC99: Verify that the functionality of all options (Download, Export to CRM, Bookmark, Merge, Fetch Contacts, More Download Options and Apply Filter) works correctly after selecting multiple companies in the Rank tab under Exporters .")
        Reset()
        export_page.exporter_tab()
        page.pause()
        export_page.verify_rank_table_headers()
        export_page.Validate_Merge_option()
        export_page.Validate_Export_CRM()
        export_page.Close_modal()
        export_page.Fetch_contacts()
        export_page.Bookmark()
        export_page.Download_option_Ranktab()
        export_page.Validate_Colmn_Shown_In_the_Grid_Download_Rank()
        export_page.Exporter_apply_filter()

    def test_Trademo_IndiaTC100(self, browser_setup, Reset,Close_modal, Check_Country):
        page = browser_setup
        export_page = ExportTab(page)
        Check_Country()
        print(
            "🔍 Running TC100: Verify that the Exporters Trends tab displays Company Name, shipment value trends and the % overall change column.")
        Reset()
        export_page.exporter_tab()
        export_page.verify_trend_headers()

    def test_Trademo_IndiaTC101(self, browser_setup, Reset,Close_modal, Check_Country):
        page = browser_setup
        export_page = ExportTab(page)
        Check_Country()
        print(
            "🔍 Running TC101: Verify that the Exporters Trends view displays Yearly, Quarterly, and Monthly time range dropdown")
        Reset()
        export_page.exporter_tab()
        export_page.verify_trend_headers()
        export_page.Verify_Monthly_data()
        export_page.Verify_Quaterly_Data()
        export_page.Verify_Yearly_Data()

    def test_Trademo_IndiaTC102(self, browser_setup, Reset,Close_modal, Check_Country):
        page = browser_setup
        export_page = ExportTab(page)
        Check_Country()
        print(
            "🔍 Running TC102: Verify that Enable 2nd Level Hierarchy toggle functionality -> Trends tab under Exporters")
        Reset()
        export_page.exporter_tab()
        export_page.verify_trend_headers()
        export_page.Enable_Trends_second_level_hierarchy()
        export_page.Trends_second_level_hierarchy_Edit()
        export_page.Disable_Trends_second_level_hierarchy()
        Reset()

    def test_Trademo_IndiaTC103(self, browser_setup, Reset, Close_modal, Check_Country):
        page = browser_setup
        export_page = ExportTab(page)
        Check_Country()
        print(
            "🔍 Running TC103: Verify that Number of Second Level Entities shows the correct count after enabling the 2nd level hierarchy in the  Exporters→ Trends tab")
        Reset()
        export_page.exporter_tab()
        export_page.verify_trend_headers()
        export_page.Enable_Trends_second_level_hierarchy()

    def test_Trademo_IndiaTC104(self, browser_setup, Reset, Close_modal, Check_Country):
        page = browser_setup
        export_page = ExportTab(page)
        Check_Country()
        print(
            "🔍 Running TC104: Verify that the download button exports correct data when 2nd level hierarchy is enabled in  Exporters→ Trends tab.")
        Reset()
        export_page.exporter_tab()
        export_page.verify_trend_headers()
        export_page.Enable_Trends_second_level_hierarchy()
        export_page.Download_option()
        export_page.Validate_Colmn_Shown_In_the_Grid_Download_Trends_2nd_level()

    def test_Trademo_IndiaTC105(self, browser_setup, Reset, Check_Country):
        page = browser_setup
        export_page = ExportTab(page)
        Check_Country()
        print(
            "🔍 Running TC105: Verify Analyse By filter functionality (Shipments, Value (USD))→ Trends tab. in  Exporters")
        Reset()
        export_page.exporter_tab()
        export_page.verify_trend_headers()
        export_page.Analyse_By_Shipment()
        export_page.Analyse_By_Shipment_Value_USD()
        export_page.Filter_by_Shipment_Trends()
        export_page.Filter_by_Shipment_Value_Trends()

    def test_Trademo_IndiaTC106(self, browser_setup, Reset, Check_Country):
        page = browser_setup
        export_page = ExportTab(page)
        Check_Country()
        print(
            "🔍 Running TC106: Verify that selecting a checkbox in  Exporters→ Trends enables the options (Download, Export to CRM, Bookmark, More Download Options, Fetch Contacts, and Apply Filter) ")
        Reset()
        export_page.exporter_tab()
        export_page.verify_trend_headers()
        export_page.Validate_option_on_selecting_deselect_checkbox()

    def test_Trademo_IndiaTC107(self, browser_setup, Reset, Check_Country):
        page = browser_setup
        export_page = ExportTab(page)
        Check_Country()
        print(
            "🔍 Running TC107: Verify that the functionality of all options (Download, Export to CRM, Bookmark, More Download Options, merge Fetch Contacts, and Apply Filter) works correctly after selecting multiple companies in the  Exporters→ Trends tab")
        Reset()
        export_page.exporter_tab()
        export_page.verify_trend_headers()
        export_page.Validate_Merge_option()
        export_page.Validate_Export_CRM()
        export_page.Close_modal()
        export_page.Fetch_contacts()
        export_page.Bookmark()
        export_page.Download_option_Trendtab()
        export_page.Validate_Colmn_Shown_In_the_Grid_Download_Trends()

    def test_Trademo_IndiaTC108(self, browser_setup, Reset, Check_Country):
        page = browser_setup
        export_page = ExportTab(page)
        Check_Country()
        print(
            "🔍 Running TC108: Verify that the functionality of all options (Download, Export to CRM, Bookmark, More Download Options, merge Fetch Contacts, and Apply Filter) works correctly after selecting multiple companies in the  Exporters→ Trends tab")
        Reset()
        export_page.exporter_tab()
        export_page.verify_rank_table_headers()
        export_page.validate_data_after_applying_filter()
        Reset()
        export_page.Validate_Tab_count_after_Manual_search()



















