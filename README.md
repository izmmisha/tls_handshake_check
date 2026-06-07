# Usage
## Prepare
Windows
```
python3 -m venv venv
venv\Scripts\activate.bat
```
Other
```
python3 -m venv venv
source venv/bin/activate
```
## Install dependencies
```
python3 -m pip install -r requirements.txt
```
### Execute
```
python3 -m pytest --sni <host_name> --host <ip/host_name> --port 443
```
Output example:
```
% python -mpytest --sni google.com --host google.com --port 443
=========================================================================== test session starts ===========================================================================
platform darwin -- Python 3.14.5, pytest-9.0.3, pluggy-1.6.0 
cachedir: .pytest_cache
configfile: pytest.ini
plugins: asyncio-1.4.0
asyncio: mode=Mode.STRICT, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collected 8 items                                                                                                                                                         

test_handshake.py::test_handshake_single[t13d1516h2_8daaf6152771_d8a2da3f94cd/client_hello/chrome_148_0_7778_179-443-google.com-google.com] [0.0828s] PASSED        [ 12%]
test_handshake.py::test_handshake_single[t13d1717h2_5b57614c22b0_3cbfd9057e0d/client_hello/linux_firefox_140_11_0esr-443-google.com-google.com] [0.0823s] PASSED    [ 25%]
test_handshake.py::test_handshake_single[t13d3012h2_1d37bd780c83_882d495ac381/client_hello/curl-443-google.com-google.com] [0.0953s] PASSED                         [ 37%]
test_handshake.py::test_handshake_single[t13d2013h2_a09f3c656075_7f0f34a4126d/client_hello/safari_26_5_11_4-443-google.com-google.com] [0.0852s] PASSED             [ 50%]
test_handshake.py::test_handshake_parallel[t13d1516h2_8daaf6152771_d8a2da3f94cd/client_hello/chrome_148_0_7778_179-443-google.com-google.com] [0.1793s] PASSED      [ 62%]
test_handshake.py::test_handshake_parallel[t13d1717h2_5b57614c22b0_3cbfd9057e0d/client_hello/linux_firefox_140_11_0esr-443-google.com-google.com] [0.0972s] PASSED  [ 75%]
test_handshake.py::test_handshake_parallel[t13d3012h2_1d37bd780c83_882d495ac381/client_hello/curl-443-google.com-google.com] [0.0947s] PASSED                       [ 87%]
test_handshake.py::test_handshake_parallel[t13d2013h2_a09f3c656075_7f0f34a4126d/client_hello/safari_26_5_11_4-443-google.com-google.com] [0.0992s] PASSED           [100%]

============================================================================ 8 passed in 1.07s ============================================================================
```
