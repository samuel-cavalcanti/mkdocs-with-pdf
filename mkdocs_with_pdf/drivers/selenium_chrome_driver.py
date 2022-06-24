from logging import Logger
from typing import Optional
from selenium.webdriver import Chrome, ChromeOptions

from pathlib import Path
import tempfile


class SeleniumChromeDriver:
    __options: ChromeOptions
    __executable_path: Optional[str]
    __log: Logger

    def __init__(self, logger: Logger, program_path: Optional[str] = None) -> None:

        self.__executable_path = program_path
        self.__log = logger
        self.__options = ChromeOptions()
        self.__options.add_argument('--headless')

    def render(self, html: str) -> str:
        temp = tempfile.NamedTemporaryFile(delete=False, suffix='.html')

        self.__log.info("Rendering on `Web drive Chrome`(execute JS).")
        file_path = Path(temp.name)

        file_path.write_text(html)

        rendered_html = self.__run_web_browser(f'file://{file_path}')

        return rendered_html

    def __run_web_browser(self, url: str) -> str:
        if self.__executable_path:
            driver = Chrome(options=self.__options,
                            executable_path=self.__executable_path)
        else:
            driver = Chrome(options=self.__options)

        driver.get(url)

        page = driver.page_source

        driver.quit()

        return page
