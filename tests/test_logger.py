import os
import datetime as dt
import shutil
from decolog.logger import Logger


test_logger = Logger(
    app_name="TEST", dir_path=os.path.join(os.path.abspath("."), "tests")
)


@test_logger
def foo(a, b):
    return "end of foo"


def test_logger(caplog, verbose=False):
    logger = Logger(
        app_name="TEST", dir_path=os.path.join(os.path.abspath("."), "tests")
    )

    text_to_log = "hello world"

    logger.log.info(text_to_log)

    assert caplog.text[:4] == "INFO"
    assert logger.app_name in caplog.text
    assert "hello world" in caplog.text
    with open(f"./tests/test_{dt.date.today().strftime('%Y%m%d')}.log") as f:
        for line in f:
            pass
    assert dt.date.today().isoformat() in line
    assert logger.app_name in line
    assert text_to_log in line
    assert "INFO" in line


def test_log_function(caplog):
    foo("arg a", b="second")

    assert "foo(*('arg a',), **{'b': 'second'})" in caplog.text


def test_folder_creation():
    dir_path = os.path.join(os.path.abspath("."), "tests")

    logger = Logger(app_name="TEST", dir_path=os.path.join(dir_path, "log_folder"))

    assert "log_folder" in os.listdir(dir_path)
    assert isinstance(logger, Logger)

    shutil.rmtree(os.path.join(dir_path, "log_folder"))


def test_long_args_non_verbose(caplog):
    a = "1111111111111111111111111111111111111111111111"
    b = list(a)

    foo(a, b=b)

    message = caplog.records[0].message

    assert message.count("...") == 2

    b = {
        0: "a",
        1: "a",
        2: "a",
        3: "a",
        4: "a",
        5: "a",
        6: "a",
        7: "a",
        8: "a",
        9: "a",
        10: "a",
        11: "a",
        12: "a",
        13: "a",
        14: "a",
        15: "a",
        16: "a",
        18: "a",
        19: "a",
    }

    foo(a="", b=b)

    message = caplog.records[-1].message

    assert message.count("...") == 1


def test_long_args_verbose(caplog):
    a = "1111111111111111111111111111111111111111111111"
    b = list(a)

    verbose_logger = Logger(
        app_name="TEST",
        dir_path=os.path.join(os.path.abspath("."), "tests"),
        is_verbose=True
    )

    breakpoint()

    verbose_logger.log.info(f"{a} {b}")

    message = caplog.records[0].message

    assert message.count("...") == 0

    b = {
        0: "a",
        1: "a",
        2: "a",
        3: "a",
        4: "a",
        5: "a",
        6: "a",
        7: "a",
        8: "a",
        9: "a",
        10: "a",
        11: "a",
        12: "a",
        13: "a",
        14: "a",
        15: "a",
        16: "a",
        18: "a",
        19: "a",
    }

    verbose_logger.log.info(b)

    message = caplog.records[-1].message

    assert message.count("...") == 0
