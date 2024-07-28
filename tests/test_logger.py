import os
import datetime as dt
from src.decolog.logger import Logger



def test_logger(caplog):
    logger = Logger(
        app_name = 'TEST',
        dir_path = os.path.join(os.path.abspath('.'), 'tests')
    )

    text_to_log = 'hello world'

    logger.log.info(text_to_log)

    assert caplog.text[:4] == 'INFO'
    assert logger.app_name in caplog.text
    assert 'hello world' in caplog.text
    with open('./tests/test_20240727.log') as f:
        for line in f:
            pass
    assert dt.date.today().isoformat() in line
    assert logger.app_name in line
    assert text_to_log in line
    assert 'INFO' in line
