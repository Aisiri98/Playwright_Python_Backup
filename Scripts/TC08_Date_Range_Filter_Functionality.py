import allure , pytest ,sys,os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pages.DateRange_Page import Date_Range_Filter

@pytest.mark.usefixtures("browser_setup")
class TestTrademo:
    """Validating Date Range filter functionality"""
    #Verifying Data source Filter functionality
    def test_Trademo_IndiaTC01(self,browser_setup,Check_Country, Reset):
        page = browser_setup
        """Test Case 8: Verify that the Date Range filter and options work with Apply and Cancel buttons"""
        print("🔍 Running TC08: Verify that the Date Range filter and options work with Apply and Cancel buttons")
        date_range_page = Date_Range_Filter(page)
        Check_Country()
        Reset()
        date_range_page.Click_Date_Range_Drp()
        date_range_page.Validate_All_Options()


