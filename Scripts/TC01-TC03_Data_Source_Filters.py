import allure , pytest ,sys,os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pages.Data_Source_page import Data_Source_Filter

@pytest.mark.usefixtures("browser_setup")
class TestTrademo:
    """Validating Data Source filter functionality"""
    #Verifying Data source Filter functionality
    def test_Trademo_IndiaTC01(self,browser_setup):
        page = browser_setup
        """Test Case 1: Verify that the Data Source filter dropdown opens and displays countries with Import checkboxes"""
        print("🔍 Running TC01: Verify that the Data Source filter dropdown opens and displays countries with Import checkboxes")
        data_Source_page = Data_Source_Filter(page)
        data_Source_page.Validate_Country_dropdown()

    def test_Trademo_IndiaTC02(self,browser_setup):
        page = browser_setup
        """Test Case 2: Verify that the "Select All" checkbox selects all countries in the Data Source dropdown"""
        print("🔍 Running TC02: Verify that the Select All checkbox selects all countries in the Data Source dropdown")
        data_Source_page = Data_Source_Filter(page)
        data_Source_page.All_Countries_Checkbox()

    def test_Trademo_IndiaTC03(self,browser_setup):
        page = browser_setup
        #page = self.page
        """Test Case 3: Verify that the Cancel and Apply buttons work correctly in the Data Source filter dropdown"""
        print("🔍 Running TC03: Verify that the Cancel and Apply buttons work correctly in the Data Source filter dropdown")
        data_Source_page = Data_Source_Filter(page)
        data_Source_page.Validate_Cancel_Apply_button()















