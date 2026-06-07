import pytest

def pytest_addoption(parser):
    parser.addoption("--port", type=int, default=443, help="TCP port number to connect to (default: 443)")
    parser.addoption("--sni", type=str, required=True, help="SNI used in clientHello")
    parser.addoption("--host", type=str, required=True, help="Host to connect to (ip address or hostname)")


def pytest_generate_tests(metafunc):
    if "port" in metafunc.fixturenames:
        metafunc.parametrize("port", [metafunc.config.getoption("port")])
    if "fix_sni" in metafunc.fixturenames:
        metafunc.parametrize("fix_sni", [metafunc.config.getoption("sni")])
    if "host" in metafunc.fixturenames:
        metafunc.parametrize("host", [metafunc.config.getoption("host")])

@pytest.hookimpl(wrapper=True)
def pytest_runtest_makereport(item, call):
    report = yield
    if report.when == "call":
        terminalreporter = item.config.pluginmanager.get_plugin("terminalreporter")
        if terminalreporter:
            duration_text = f"[{report.duration:.4f}s] "
            terminalreporter._tw.write(duration_text, cyan=True)
    return report
