from pyppeteer import launch
from pyppeteer.page import Page


async def _wait_for_html_rendered(page: Page, timeout: int = 30000):
    check_dur_msecs: int = 500
    max_checks: float = timeout / check_dur_msecs
    last_html_size: int = 0
    check_counts: int = 1
    stable_count: int = 0
    min_stable_size: int = 3

    while check_counts <= max_checks:
        html = await page.content()

        current_html_size = len(html)
        await page.evaluate('''document.body.innerHTML.length;''')

        if last_html_size != 0 and current_html_size == last_html_size: 
            stable_count = stable_count + 1
        else:
            stable_count = 0

        if stable_count >= min_stable_size:
            print("Page rendered fully..")
            break

        last_html_size = current_html_size
        await page.waitFor(check_dur_msecs)


async def get_page_content(url: str) -> str:
    browser = await launch(
        autoClose=False,
        handleSIGINT=False,
        handleSIGTERM=False,
        handleSIGHUP=False
    )
    page: Page = await browser.newPage()
    await page.setJavaScriptEnabled(True)
    await page.setExtraHTTPHeaders(
        {
            "accept": (
                "text/html,application/xhtml+xml,application/xml;q=0.9,"
                "image/avif,image/webp,image/apng,"
                "*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
            )
        }
    )
    await page.setUserAgent((
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
        "(KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
    ))
    await page.goto(url, {"waitUntil": 'load'})
    await _wait_for_html_rendered(page)

    content = await page.content()
    await browser.close()

    return content
