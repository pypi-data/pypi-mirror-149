import logging
import pathlib
from typing import Any
from typing import Dict
from typing import List
from unittest import mock

import pytest
from dict_tools import data

import pytest_idem.runner

log = logging.getLogger("pytest_idem.plugin")

TESTS_DIR = pathlib.Path()


@pytest.fixture(scope="session", autouse=True)
def tests_dir(request: pytest.Session):
    """
    When the test starts, verify that TESTS_DIR is available in non-fixture functions in this module
    """
    global TESTS_DIR
    TESTS_DIR = pathlib.Path(request.config.rootdir) / "tests"
    yield TESTS_DIR


@pytest.fixture(scope="module")
def acct_key():
    key = pytest_idem.runner.generate_acct_key()
    yield key


@pytest.fixture(scope="session")
def acct_subs() -> List[str]:
    log.error("Override the 'acct_subs' fixture in your own conftest.py")
    return []


@pytest.fixture(scope="session")
def acct_profile() -> str:
    log.error("Override the 'acct_profile' fixture in your own conftest.py")
    return ""


@pytest.fixture(scope="session")
def ctx(hub, acct_subs: List[str], acct_profile: str) -> Dict[str, Any]:
    """
    Set up the context for idem-cloud executions
    :param hub:
    :param acct_subs: The output of an overridden fixture of the same name
    :param acct_profile: The output of an overridden fixture of the same name
    """
    # Add idem's namespace to the hub
    if not hasattr(hub, "idem"):
        hub.pop.sub.add(dyne_name="idem")

    ctx = data.NamespaceDict(
        {"run_name": "test", "test": False, "acct": data.NamespaceDict()}
    )

    old_opts = hub.OPT

    if acct_subs and acct_profile:

        if not (
            hub.OPT.get("acct")
            and hub.OPT.acct.get("acct_file")
            and hub.OPT.acct.get("acct_key")
        ):
            if not hasattr(hub, "acct"):
                hub.pop.sub.add(dyne_name="acct")
            # Get the account information from environment variables
            log.debug("Loading temporary config from idem and acct")
            with mock.patch("sys.argv", ["pytest_idem"]):
                hub.pop.config.load(["acct"], "acct", parse_cli=False)

        # Make sure the loop is running
        hub.pop.loop.create()

        # Add the profile to the account
        if hub.OPT.acct.acct_file and hub.OPT.acct.acct_key:
            hub.pop.Loop.run_until_complete(
                hub.acct.init.unlock(hub.OPT.acct.acct_file, hub.OPT.acct.acct_key)
            )
        ctx["acct"] = hub.pop.Loop.run_until_complete(
            hub.acct.init.gather(acct_subs, acct_profile)
        )

    hub.OPT = old_opts

    yield ctx


@pytest.fixture(scope="session")
def idem_runpy(hub, acct_subs: List[str], acct_profile: str) -> Dict[str, Any]:
    return pathlib.Path(__file__).parent / "run.py"


@pytest.fixture(scope="module")
def esm_cache():
    """
    An ESM cache that exists only in memory for easy testing of state output when running yaml blocks
    """
    CACHE = {}
    yield CACHE
