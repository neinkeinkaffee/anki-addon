from .browser_driver import BrowserDriver


def test_loads_page_and_navigates_back_and_forth(qtbot, monkeypatch):
    browser_driver = BrowserDriver(qtbot, monkeypatch)
    browser_driver.patch_qurl_with_local_files({
        "www.sometest.com": "test_page_1.html",
        "www.anothertest.com": "test_page_2.html"
    })

    browser_driver.enter_address_and_hit_return("www.sometest.com")
    browser_driver.assert_browser_window_title("Test Page")
    browser_driver.assert_page_contains("This is a test")

    browser_driver.enter_address_and_hit_return("www.anothertest.com")
    browser_driver.assert_browser_window_title("Another Test Page")
    browser_driver.assert_page_contains("This is another test")

    browser_driver.click_backwards_button()
    browser_driver.assert_browser_window_title("Test Page")
    browser_driver.assert_page_contains("This is a test")

    browser_driver.click_forwards_button()
    browser_driver.assert_browser_window_title("Another Test Page")
    browser_driver.assert_page_contains("This is another test")






