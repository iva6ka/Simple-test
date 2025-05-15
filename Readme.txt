=== How to Run the Script (macOS) ===

1. Make sure Python 3 and pip are installed:

   ▶ Check Python version:
      python3 --version

   ▶ If pip is missing, install it:
      python3 -m ensurepip --upgrade
      python3 -m pip install --upgrade pip

2. Install required packages (only once):
   python3 -m pip install selenium

3. Run the script:
   python3 demoqa_test.py

4. Optional arguments:

   --headless
       Run the browser in headless mode (invisible window).

   --proxy
       Enable proxy usage.

   --proxy-url URL
       Set custom proxy address (e.g., socks5://123.45.67.89:8080)

       If only --proxy is used, the default proxy will be applied.

=== Examples ===

▶ Basic usage:
   python3 demoqa_test.py

▶ Headless mode:
   python3 demoqa_test.py --headless

▶ With default proxy (DEFAULT_PROXY_URL from code):
   python3 demoqa_test.py --proxy

▶ With custom proxy:
   python3 demoqa_test.py --proxy --proxy-url http://123.45.67.89:8080

▶ Headless + custom proxy:
   python3 demoqa_test.py --headless --proxy --proxy-url socks5://123.45.67.89:8080
