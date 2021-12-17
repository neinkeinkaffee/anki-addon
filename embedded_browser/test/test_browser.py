from .browser_driver import BrowserDriver


def test_loads_page_and_navigates_back_and_forth(qtbot, monkeypatch):
    browser_driver = BrowserDriver(qtbot, monkeypatch)
    browser_driver.patch_qurl_with_local_files({
        "www.sometest.com": "test_page_1.html",
        "www.anothertest.com": "test_page_2.html"
    })

    browser_driver.enter_address_and_hit_return("www.sometest.com")
    browser_driver.assert_active_browser_tab_title("Test Page")
    browser_driver.assert_active_browser_tab_contains_html("This is a test")

    browser_driver.enter_address_and_hit_return("www.anothertest.com")
    browser_driver.assert_active_browser_tab_title("Another Test Page")
    browser_driver.assert_active_browser_tab_contains_html("This is another test")

    browser_driver.click_backward_button()
    browser_driver.assert_active_browser_tab_title("Test Page")
    browser_driver.assert_active_browser_tab_contains_html("This is a test")

    browser_driver.click_forward_button()
    browser_driver.assert_active_browser_tab_title("Another Test Page")
    browser_driver.assert_active_browser_tab_contains_html("This is another test")


def test_opens_new_tab_with_duckduckgo_as_default_page(qtbot, monkeypatch):
    browser_driver = BrowserDriver(qtbot, monkeypatch)
    browser_driver.patch_qurl_with_local_files({
        "https://duckduckgo.com": "test_page_1.html",
    })

    browser_driver.open_new_tab()

    browser_driver.assert_tab_count(2)
    browser_driver.assert_address_bar_contains("test_page_1.html")
    browser_driver.assert_active_browser_tab_title("Test Page")
    browser_driver.assert_active_browser_tab_contains_html("This is a test")






