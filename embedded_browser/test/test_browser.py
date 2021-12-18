from .browser_driver import BrowserDriver

FIXTURES_DIR = "/Users/gesa/repos/anki-addon/embedded_browser/test/fixtures"


def test_loads_page_and_navigates_back_and_forth(qtbot, monkeypatch):
    browser_driver = BrowserDriver(qtbot, monkeypatch)

    browser_driver.enter_address_and_hit_return(f"{FIXTURES_DIR}/page_1.html")
    browser_driver.assert_address_bar_contains("page_1.html")
    browser_driver.assert_active_browser_tab_contains_html("This is a test")
    browser_driver.assert_active_browser_tab_title("Test Page")

    browser_driver.enter_address_and_hit_return(f"{FIXTURES_DIR}/page_2.html")
    browser_driver.assert_address_bar_contains("page_2.html")
    browser_driver.assert_active_browser_tab_contains_html("This is another test")
    browser_driver.assert_active_browser_tab_title("Another Test Page")

    browser_driver.click_backward_button()
    browser_driver.assert_address_bar_contains("page_1.html")
    browser_driver.assert_active_browser_tab_contains_html("This is a test")
    browser_driver.assert_active_browser_tab_title("Test Page")

    browser_driver.click_forward_button()
    browser_driver.assert_address_bar_contains("page_2.html")
    browser_driver.assert_active_browser_tab_contains_html("This is another test")
    browser_driver.assert_active_browser_tab_title("Another Test Page")


def test_opens_new_tab_with_blank_default_page(qtbot, monkeypatch):
    browser = BrowserDriver(qtbot, monkeypatch)

    browser.open_new_tab()

    browser.assert_tab_count(2)
    browser.assert_address_bar_contains("about:blank")
    browser.assert_active_browser_tab_title("about:blank")


def test_backward_and_forward_buttons_are_tab_sensitive(qtbot, monkeypatch):
    browser = BrowserDriver(qtbot, monkeypatch)
    browser.assert_backward_button_disabled()

    browser.open_new_tab()
    browser.enter_address_and_hit_return(f"{FIXTURES_DIR}/page_1.html")
    browser.enter_address_and_hit_return(f"{FIXTURES_DIR}/page_2.html")
    browser.assert_backward_button_enabled()
    browser.switch_to_tab(0)
    browser.assert_backward_button_disabled()

    browser.switch_to_tab(1)
    browser.click_backward_button()
    browser.assert_forward_button_enabled()
    browser.switch_to_tab(0)
    browser.assert_forward_button_disabled()

def test_closes_tab(qtbot, monkeypatch):
    browser = BrowserDriver(qtbot, monkeypatch)

    browser.open_new_tab()
    browser.assert_tab_count(2)

    browser.close_active_tab()
    browser.assert_tab_count(1)

    browser.close_active_tab()
    browser.assert_tab_count(1)
