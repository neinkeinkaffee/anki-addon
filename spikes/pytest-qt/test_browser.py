from browser_driver import BrowserDriver


def test_loads_page(qtbot, monkeypatch):
    browser_driver = BrowserDriver(qtbot, monkeypatch)
    browser_driver.patch_qurl_to_return_local_file("spikes/pytest-qt/test.html")

    browser_driver.enter_address_and_hit_return("www.sometest.com")

    browser_driver.assert_browser_window_title("Test Page")
    browser_driver.assert_page_contains("This is a test")





