import re
import pickle
import tempfile
import pytest

from io import StringIO
from types import SimpleNamespace

from _pytest.config import Config, create_terminal_writer
from _pytest._io.terminalwriter import TerminalWriter
from _pytest.reports import TestReport
from pytest_tui.tui1 import main as tui1
from pytest_tui.tui2 import main as tui2
from pytest_tui.utils import (
    test_session_starts_matcher,
    errors_section_matcher,
    failures_section_matcher,
    warnings_summary_matcher,
    passes_section_matcher,
    short_test_summary_matcher,
    lastline_matcher,
    MARKERS,
    REPORTFILE,
    MARKEDTERMINALOUTPUTFILE,
    UNMARKEDTERMINALOUTPUTFILE,
)


# Don't collect tests from any of these files
collect_ignore = [
    "setup.py",
    "plugin.py",
]

# A list of TestReport objects generated by Pytest during test run;
# each TestReport represents a single test's operation during one of
# Pytest's three phases: setup | call | teardown
reports = []


def pytest_addoption(parser):
    """Define the plugin's option flags as presented by Pytest"""
    group = parser.getgroup("tui")
    group.addoption(
        "--tui",
        action="store_true",
        help="automatically launch default text user interface after run is finished",
    )
    group.addoption(
        "--tui1",
        action="store_true",
        help="automatically launch text user interface 'tui1' (textual) [DEFAULT]",
    )
    group.addoption(
        "--tui2",
        action="store_true",
        help="automatically launch text user interface 'tui2' (pytermtk)",
    )
    group.addoption(
        "--tuin",
        action="store_true",
        help="generate pytest-tui output files, but do not launch user interface",
    )


def add_ansi_to_report(config: Config, report: TestReport):
    """
    If the report has longreprtext (traceback info), mark it up with ANSI codes
    From https://stackoverflow.com/questions/71846269/algorithm-for-extracting-first-and-last-lines-from-sectionalized-output-file
    """
    buf = StringIO()
    buf.isatty = lambda: True

    reporter = config.pluginmanager.getplugin("terminalreporter")
    original_writer = reporter._tw
    writer = create_terminal_writer(config, file=buf)
    reporter._tw = writer

    reporter._outrep_summary(report)
    buf.seek(0)
    ansi = buf.read()
    buf.close()

    report.ansi = SimpleNamespace()
    setattr(report.ansi, "val", ansi)

    reporter._tw = original_writer


def pytest_report_teststatus(report: TestReport, config: Config):
    """Construct list(s) of individual TestReport instances"""
    if hasattr(report, "longreprtext") and report.longreprtext:
        add_ansi_to_report(config, report)
    reports.append(report)


@pytest.hookimpl(trylast=True)
def pytest_configure(config: Config) -> None:
    """
    Write console output to a file for use by TUI
    This code works by looking at every line sent by Pytest to the terminal,
    and based on its category, marking or not marking it
    """
    config.option.verbose = (
        1  # force verbose mode for easier parsing of final test results
    )
    config.option.reportchars = (
        "A"  # force "display all" mode so all results can be shown
    )

    if any(
        [
            config.option.tui,
            config.option.tui1,
            config.option.tui2,
            config.option.tuin,
        ]
    ):
        tr = config.pluginmanager.getplugin("terminalreporter")
        if tr is not None:
            # identify and mark the very first line of terminal output
            try:
                config._pytuifirsttime
            except AttributeError:
                config._pytuifirsttime = True

            config._pytui_unmarked_outputfile = tempfile.TemporaryFile("wb+")
            config._pytui_marked_outputfile = tempfile.TemporaryFile("wb+")
            oldwrite = tr._tw.write

            # identify and mark each results section
            def tee_write(s, **kwargs):
                if re.search(test_session_starts_matcher, s):
                    config._pytui_marked_outputfile.write(
                        (MARKERS["pytest_tui_test_session_starts"] + "\n").encode(
                            "utf-8"
                        )
                    )

                if re.search(errors_section_matcher, s):
                    config._pytui_marked_outputfile.write(
                        (MARKERS["pytest_tui_errors_section"] + "\n").encode("utf-8")
                    )

                if re.search(failures_section_matcher, s):
                    config._pytui_marked_outputfile.write(
                        (MARKERS["pytest_tui_failures_section"] + "\n").encode("utf-8")
                    )

                if re.search(warnings_summary_matcher, s):
                    config._pytui_marked_outputfile.write(
                        (MARKERS["pytest_tui_warnings_summary"] + "\n").encode("utf-8")
                    )

                if re.search(passes_section_matcher, s):
                    config._pytui_marked_outputfile.write(
                        (MARKERS["pytest_tui_passes_section"] + "\n").encode("utf-8")
                    )

                if re.search(short_test_summary_matcher, s):
                    config._pytui_marked_outputfile.write(
                        (MARKERS["pytest_tui_short_test_summary"] + "\n").encode(
                            "utf-8"
                        )
                    )

                if re.search(lastline_matcher, s):
                    config._pytui_marked_outputfile.write(
                        (MARKERS["pytest_tui_last_line"] + "\n").encode("utf-8")
                    )

                # Write this line's text along with its markup info to console
                oldwrite(s, **kwargs)

                # Mark up this line's text by passing it to an instance of TerminalWriter's
                # 'markup' method. Do not pass "flush" to the method   s it will throw an error.
                s1 = s
                kwargs.pop("flush") if "flush" in kwargs.keys() else None
                s1 = TerminalWriter().markup(s, **kwargs)

                # Encode the marked up line so it can be written to the config object.
                # The Pytest config object can be used by plugins for conveying staeful
                # info across an entire test run session.
                if isinstance(s1, str):
                    marked_up = s1.encode("utf-8")
                config._pytui_marked_outputfile.write(marked_up)

                # Write this line's original (unmarked) text to unmarked file
                s_orig = s
                kwargs.pop("flush") if "flush" in kwargs.keys() else None
                s_orig = TerminalWriter().markup(s, **kwargs)
                if isinstance(s_orig, str):
                    unmarked_up = s_orig.encode("utf-8")
                config._pytui_unmarked_outputfile.write(unmarked_up)

            # Write to both terminal/console and tempfiles:
            # _pytui_marked_outputfile, _pytui_unmarked_outputfile
            tr._tw.write = tee_write


def pytest_unconfigure(config: Config):
    """
    Write terminal and test results info to files for use by TUI
    """
    # Write terminal output to file
    if hasattr(config, "_pytui_marked_outputfile"):
        # get terminal contents, then write file
        config._pytui_marked_outputfile.seek(0)
        markedsessionlog = config._pytui_marked_outputfile.read()
        config._pytui_marked_outputfile.close()

    if hasattr(config, "_pytui_unmarked_outputfile"):
        # get terminal contents, then write file
        config._pytui_unmarked_outputfile.seek(0)
        unmarkedsessionlog = config._pytui_unmarked_outputfile.read()
        config._pytui_unmarked_outputfile.close()

        # Undo our patching in the terminal reporter
        config.pluginmanager.getplugin("terminalreporter")

        # Write marked-up results to file
        with open(MARKEDTERMINALOUTPUTFILE, "wb") as marked_file:
            marked_file.write(markedsessionlog)

        # Write un-marked-up results to file
        with open(UNMARKEDTERMINALOUTPUTFILE, "wb") as unmarked_file:
            unmarked_file.write(unmarkedsessionlog)

        # Write the reports list to file
        with open(REPORTFILE, "wb") as report_file:
            pickle.dump(reports, report_file)

    # Launch the selected TUI
    if any(
        [
            config.option.tui,
            config.option.tui1,
            config.option.tui2,
            config.option.tuin,
        ]
    ):
        pytui_tui(config)


def pytui_tui(config: Config) -> None:
    """
    Final code invocation after Pytest run has completed.
    This method calls the Pytui TUI to display final results.
    """
    # disable capturing while TUI runs to avoid error `redirected stdin is pseudofile, has
    # no fileno()`; adapted from https://githubmemory.com/repo/jsbueno/terminedia/issues/25
    if not any(
        [
            config.option.tui,
            config.option.tui1,
            config.option.tui2,
            config.option.tuin,
        ]
    ):
        return
    capmanager = config.pluginmanager.getplugin("capturemanager")
    try:
        capmanager.suspend_global_capture(in_=True)
    finally:
        if config.getoption("--tui") or config.getoption("--tui1"):
            tui1()
        elif config.getoption("--tui2"):
            tui2()
        elif not config.getoption("--tuin"):
            print("Invalid pytest-tui option")
        capmanager.resume_global_capture()
