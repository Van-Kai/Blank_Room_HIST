from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, slow_mo=1000)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://127.0.0.1:8080/?lf=%E5%BC%98%E6%AF%85%E6%A5%BC&zc=5&z=4")

    # 定位到搜索框并截图
    search_input = page.locator(selector="id=screenshot")  # 百度首页的搜索框选择器
    search_input.screenshot(path="search_input_screenshot.png")

    context.close()
    browser.close()