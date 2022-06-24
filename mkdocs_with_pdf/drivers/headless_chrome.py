import os
from logging import Logger
from shutil import which
from subprocess import PIPE, Popen
from tempfile import NamedTemporaryFile


class HeadlessChromeDriver:
    """ 'Headless Chrome' executor """

    __driver_args = [
        '--disable-web-security',
        '--no-sandbox',
        '--headless',
        '--disable-gpu',
        '--disable-web-security',
        '-–allow-file-access-from-files',
        '--run-all-compositor-stages-before-draw',
        '--virtual-time-budget=10000',
        '--dump-dom'
    ]

    def __init__(self, program_path: str, logger: Logger):
        if not which(program_path):
            raise RuntimeError(
                'No such `Headless Chrome` program or not executable'
                + f': "{program_path}".')

        self._program_path = program_path
        self._logger = logger

    def render(self, html: str) -> str:
        temp = NamedTemporaryFile(delete=False, suffix='.html')
        try:
            temp.write(html.encode('utf-8'))
            temp.close()

            self._logger.info("Rendering on `Headless Chrome`(execute JS).")
            command_line = [self._program_path] + \
                self.__driver_args + [temp.name]
            with Popen(command_line, stdout=PIPE) as chrome:
                command_output = chrome.stdout.read().decode('utf-8')
                """
                    Popen append a unnecessary \n on final stdout string.
                    The \n is removed applying  command_output[:-1]
                """
                rendered_html = command_output[:-1]

                return rendered_html

        except Exception as e:
            self._logger.error(f'Failed to render by JS: {e}')
        finally:
            os.unlink(temp.name)

        return html
