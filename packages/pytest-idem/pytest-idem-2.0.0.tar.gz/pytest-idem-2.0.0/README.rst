***********
PYTEST-IDEM
***********
**A pytest plugin to help with testing idem projects**

INSTALLATION
============

Install with pip::

    pip install pytest-idem

DEVELOPMENT INSTALLATION
========================


Clone the `pytest-idem` repo and install with pip::

    git clone https://gitlab.com/vmware/idem/pytest-idem.git
    pip install -e pytest-idem


ACCT
====

Some projects, specifically need credentials from idem's ctx generator.
A ctx fixture exists, but it won't work unless you override the `acct_file` and `acct_profile` fixtures::

    @pytest.fixture
    def acct_subs() -> List[str]:
        return ["azurerm", "vultr"]


    @pytest.fixture
    def acct_profile() -> str:
        return "test_development_idem_cloud"

Once these fixtures are overridden, the `ctx` fixture will become available to your test::

    test_cloud_instance_present(hub, ctx):
        hub.state.cloud.present(ctx, "instance_name")
