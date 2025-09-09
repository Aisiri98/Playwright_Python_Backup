import csv
import os
import sys
import pytest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pages.analytics_tab_page import AnalyticsTab
@pytest.mark.usefixtures("browser_setup")

class TestTrademo:
    """Exporter Tab functionality"""

    def test_Trademo_IndiaTC109(self, browser_setup, Reset,Check_Country,Close_modal):
        page = browser_setup
        analytics_page = AnalyticsTab(page)
        Close_modal()
        Check_Country()
        print("🔍 Running TC109: Verify the presence of Total Shipments, and Shipment Value display with counts")
        Reset()
        analytics_page.analytics_tab()
        analytics_page.verify_total_shipments_and_value()

    def test_Trademo_IndiaTC112(self, browser_setup, Reset,Check_Country):
        page = browser_setup
        analytics_page = AnalyticsTab(page)
        Check_Country()
        print("🔍 Running TC112: Verify that the Import Trends view displays a graph and trends button functionality.")
        Reset()
        analytics_page.analytics_tab()
        analytics_page.Verify_Import_Section()
        analytics_page.Verify_Trends_Screen()
        analytics_page.Validate_checkbox()
        analytics_page.Validate_download_excel()
        analytics_page.Verify_SortBy_dropdown_Trends()
        analytics_page.Validate_close_screen()

    def test_Trademo_IndiaTC113(self,browser_setup, Reset,Check_Country):
        page = browser_setup
        analytics_page = AnalyticsTab(page)
        Check_Country()
        print("🔍 Running TC113: Verify that the Countries of Origin displays a graph and trends and view button functionality")
        Reset()
        analytics_page.analytics_tab()
        analytics_page.Verify_Import_Section()
        analytics_page.Verify_Trends_Screen()
        analytics_page.Validate_checkbox()
        analytics_page.Validate_download_excel()
        analytics_page.Verify_SortBy_dropdown_Trends()
        analytics_page.Validate_Time_Range_drp_Yearly()
        analytics_page.Validate_Time_Range_drp_Monthly()
        analytics_page.Validate_Time_Range_drp_Quaterly()
        analytics_page.Validate_close_screen()

    def test_Trademo_IndiaTC115(self,browser_setup, Reset,Check_Country):
        page = browser_setup
        analytics_page = AnalyticsTab(page)
        Check_Country()
        print("🔍 Running TC116: Verify the 6-digit HS Code section and Trends functionality")
        Reset()
        analytics_page.analytics_tab()
        analytics_page.Validate_6digit_hs_code_screen()
        analytics_page.validate_6digit_Hscode_Trends_headercheck()
        analytics_page.Validate_checkbox()
        analytics_page.Validate_download_excel()
        analytics_page.Verify_SortBy_dropdown_Trends()
        analytics_page.Enable_Toggle_second_level()
        analytics_page.Validate_close_screen()

    def test_Trademo_IndiaTC116(self,browser_setup, Reset,Check_Country):
        page = browser_setup
        analytics_page = AnalyticsTab(page)
        Check_Country()
        print("🔍 Running TC116: Verify View All functionality in 6-digit HS Code section")
        Reset()
        analytics_page.analytics_tab()
        analytics_page.Validate_6digit_hs_code_screen()
        analytics_page.validate_6digit_Hscode_View_all_headercheck()
        analytics_page.Validate_download_excel()
        analytics_page.Verify_SortBy_dropdown_Viewall()
        analytics_page.Enable_Toggle_second_level_Viewall()
        analytics_page.Validate_close_screen()
        analytics_page.Validate_6digit_hs_code_screen()
        analytics_page.validate_6digit_Hscode_View_all_headercheck()
        analytics_page.Verify_ViewModal_SearchBar()
        analytics_page.Apply_filter_icon()
        analytics_page.Validate_preselected_code_inthe_cargo_filter()
        analytics_page.Validate_HSCode_In_ShipmentGrid()

    def test_Trademo_IndiaTC117(self, browser_setup, Reset, Check_Country):
        page = browser_setup
        analytics_page = AnalyticsTab(page)
        Check_Country()
        print("🔍 Running TC117: Verify the Consignee states in Analytics tab with “Trends” and “View All” functionality")
        Reset()
        analytics_page.analytics_tab()
        analytics_page.Validate_consignee_states_screen()
        analytics_page.validate_Consignee_Trends_headercheck()
        analytics_page.Validate_checkbox()
        analytics_page.Validate_download_excel()
        analytics_page.Verify_SortBy_dropdown_Trends()
        analytics_page.Enable_Toggle_second_level_consignee()
        analytics_page.Validate_close_screen_consignee()

    def test_Trademo_IndiaTC118(self, browser_setup, Reset, Check_Country):
        page = browser_setup
        analytics_page = AnalyticsTab(page)
        Check_Country()
        print("🔍 Running TC118: Verify the Customs House Agent Name section in the Analytics tab with “Trends” and “View All” functionality")
        Reset()
        analytics_page.analytics_tab()
        analytics_page.Validate_custom_house_agent_screen()
        analytics_page.validate_Customhouseagent_Trends_headercheck()
        analytics_page.Validate_download_excel()
        analytics_page.Verify_SortBy_dropdown_Trends()
        analytics_page.Validate_Time_Range_drp_Yearly()
        analytics_page.Validate_Time_Range_drp_Monthly()
        analytics_page.Validate_Time_Range_drp_Quaterly()
        analytics_page.Validate_close_screen_consignee()
        Reset()
        analytics_page.Validate_custom_house_agent_screen()
        analytics_page.Custom_House_Agent_Name_View_All()
        analytics_page.Apply_filter_custom_house()
        analytics_page.Validate_preselected_code_inthe_customs_filter()
        analytics_page.Validate_Customs_house_In_ShipmentGrid()

    def test_Trademo_IndiaTC119(self, browser_setup, Reset, Check_Country):
        page = browser_setup
        analytics_page = AnalyticsTab(page)
        Check_Country()
        print("🔍 Running TC119: Verify Port of Lading sections with Trends and View All functionalities in the Analytics tab")
        Reset()
        analytics_page.analytics_tab()
        analytics_page.Validate_port_laiding_screen()
        analytics_page.validate_port_lading_Trends_headercheck()
        analytics_page.Validate_download_excel()
        analytics_page.Verify_SortBy_dropdown_Trends()
        analytics_page.Validate_Time_Range_drp_Yearly()
        analytics_page.Validate_Time_Range_drp_Monthly()
        analytics_page.Validate_Time_Range_drp_Quaterly()
        analytics_page.Validate_close_screen_consignee()
        Reset()
        analytics_page.Validate_port_laiding_screen()
        analytics_page.Port_lading_View_All()
        analytics_page.Apply_filter_Ports_lading()
        analytics_page.Validate_preselected_code_inthe_port_lading_filter()
        analytics_page.Validate_Port_lading_In_ShipmentGrid()

    def test_Trademo_IndiaTC120(self, browser_setup, Reset, Check_Country):
        page = browser_setup
        analytics_page = AnalyticsTab(page)
        Check_Country()
        print(
            "🔍 Running TC120: Verify Port of Unlading sections with Trends and View All functionalities in the Analytics tab")
        Reset()
        analytics_page.analytics_tab()
        analytics_page.Validate_port_unlaiding_screen()
        analytics_page.validate_port_unlading_Trends_headercheck()
        analytics_page.Validate_download_excel()
        analytics_page.Verify_SortBy_dropdown_Trends()
        analytics_page.Validate_Time_Range_drp_Yearly()
        analytics_page.Validate_Time_Range_drp_Monthly()
        analytics_page.Validate_Time_Range_drp_Quaterly()
        analytics_page.Validate_close_screen_consignee()
        Reset()
        analytics_page.Validate_port_unlaiding_screen()
        analytics_page.Port_Unlading_View_All()
        analytics_page.Apply_filter_Ports_Unlading()
        analytics_page.Validate_preselected_code_inthe_port_unlading_filter()
        analytics_page.Validate_Port_unlading_In_ShipmentGrid()

    def test_Trademo_IndiaTC121(self, browser_setup, Reset, Check_Country):
        page = browser_setup
        analytics_page = AnalyticsTab(page)
        Check_Country()
        print(
            "🔍 Running TC121: Verify “Mode of Transportation” section in Analytics tab – Pie Chart, Trends, and View All functionality")
        Reset()
        analytics_page.analytics_tab()
        analytics_page.Validate_mode_transportation_screen()
        analytics_page.validate_mode_transportation_Trends_headercheck()
        analytics_page.Validate_download_excel()
        analytics_page.Verify_SortBy_dropdown_Trends()
        analytics_page.Validate_Time_Range_drp_Yearly()
        analytics_page.Validate_Time_Range_drp_Monthly()
        analytics_page.Validate_Time_Range_drp_Quaterly()
        analytics_page.Validate_close_screen_consignee()
        Reset()
        analytics_page.Validate_mode_transportation_screen()
        analytics_page.Transport_mode_View_All()
        analytics_page.Apply_filter_Transport_mode()
        analytics_page.Validate_preselected_mode_inthe_freight_filter()
        analytics_page.Validate_Transport_Mode_In_ShipmentGrid()



















