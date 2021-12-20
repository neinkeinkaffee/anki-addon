import os

from .browser_driver import BrowserDriver


FIXTURES_PATH = f"file:///{os.getcwd()}/test/fixtures"


def test_loads_page_and_navigates_back_and_forth(qtbot):
    browser = BrowserDriver(qtbot)

    browser.enter_address_and_hit_return(f"{FIXTURES_PATH}/page_1.html")
    browser.assert_address_bar_contains("page_1.html")
    browser.assert_active_browser_tab_contains_html("This is a test")
    browser.assert_active_browser_tab_title("Test Page")

    browser.enter_address_and_hit_return(f"{FIXTURES_PATH}/page_2.html")
    browser.assert_address_bar_contains("page_2.html")
    browser.assert_active_browser_tab_contains_html("This is another test")
    browser.assert_active_browser_tab_title("Another Test Page")

    browser.click_backward_button()
    browser.assert_address_bar_contains("page_1.html")
    browser.assert_active_browser_tab_contains_html("This is a test")
    browser.assert_active_browser_tab_title("Test Page")

    browser.click_forward_button()
    browser.assert_address_bar_contains("page_2.html")
    browser.assert_active_browser_tab_contains_html("This is another test")
    browser.assert_active_browser_tab_title("Another Test Page")


def test_opens_new_tab_with_blank_default_page(qtbot):
    browser = BrowserDriver(qtbot)

    browser.open_new_tab()

    browser.assert_tab_count(2)
    browser.assert_address_bar_contains("about:blank")
    browser.assert_active_browser_tab_title("about:blank")


def test_backward_and_forward_buttons_are_tab_sensitive(qtbot):
    browser = BrowserDriver(qtbot)
    browser.assert_backward_button_disabled()

    browser.open_new_tab()
    browser.enter_address_and_hit_return(f"{FIXTURES_PATH}/page_1.html")
    browser.enter_address_and_hit_return(f"{FIXTURES_PATH}/page_2.html")
    browser.assert_backward_button_enabled()
    browser.switch_to_tab(0)
    browser.assert_backward_button_disabled()

    browser.switch_to_tab(1)
    browser.click_backward_button()
    browser.assert_forward_button_enabled()
    browser.switch_to_tab(0)
    browser.assert_forward_button_disabled()


def test_closes_tabs_but_keeps_last_tab_open(qtbot):
    browser = BrowserDriver(qtbot)

    browser.open_new_tab()
    browser.assert_tab_count(2)

    browser.close_active_tab()
    browser.assert_tab_count(1)

    browser.close_active_tab()
    browser.assert_tab_count(1)


def test_calls_callback_on_clicking_context_menu_action(qtbot):
    browser = BrowserDriver(qtbot)

    browser.enter_address_and_hit_return(f"{FIXTURES_PATH}/page_with_test_span.html")
    browser.select_test_span_and_trigger_copy_to_card_action()

    browser.assert_context_menu_callback_called_with_expected_text("selection test")
