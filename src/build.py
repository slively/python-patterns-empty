from subprocess import check_call
import sys


def format() -> None:
    check_call(["black", "src"])


def lint() -> None:
    check_call(["flake8", "--exclude=.venv,ansible,vendor,__pycache__"])


def typecheck() -> None:
    check_call(
        [
            "mypy",
            "--warn-unused-configs",
            "--show-error-codes",
            "--exclude",
            "'(.venv|ansible|vendor*)/$'",
            "--config-file",
            "./pyproject.toml",
            "./src",
        ]
    )


def test() -> None:
    check_call(["python", "-m", "unittest", "-f"])


def test_single() -> None:
    check_call(["python", "-m", "unittest", "-f", sys.argv[-1]])


def build() -> None:
    lint()
    typecheck()
    test()
