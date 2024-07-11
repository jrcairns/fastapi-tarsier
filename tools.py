from langchain.agents import tool
from tarsier import Tarsier, GoogleVisionOCRService

tag_to_xpath = {}

async def setup_tools(page, config):
    ocr_service = GoogleVisionOCRService(config['google_cloud_credentials'])
    tarsier = Tarsier(ocr_service)

    @tool
    async def read_page() -> str:
        """
        Use to read the current state of the page
        """
        return await read_page_impl(page, tarsier)

    @tool
    async def click(element_id: int) -> str:
        """
        Click on an element based on element_id and return the new page state
        """
        x_path = tag_to_xpath[element_id]
        print(x_path)
        element = page.locator(x_path)
        await element.scroll_into_view_if_needed()
        await page.wait_for_timeout(1000)
        await element.click()
        await page.wait_for_timeout(2000)
        return await read_page_impl(page, tarsier)

    @tool
    async def type_text(element_id: int, text: str) -> str:
        """
        Input text into a textbox based on element_id and return the new page state
        """
        x_path = tag_to_xpath[element_id]
        print(x_path)
        await page.locator(x_path).press_sequentially(text)
        return await read_page_impl(page, tarsier)

    @tool
    async def press_key(key: str) -> str:
        """
        Press a key on the keyboard and return the new page state
        """
        await page.keyboard.press(key)
        await page.wait_for_timeout(2000)
        return await read_page_impl(page, tarsier)

    return [read_page, click, type_text, press_key]

async def read_page_impl(page, tarsier) -> str:
    page_text, inner_tag_to_xpath = await tarsier.page_to_text(page)
    tag_to_xpath.clear()
    tag_to_xpath.update(inner_tag_to_xpath)
    return page_text