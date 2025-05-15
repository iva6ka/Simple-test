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

   --proxy http://ip:port
       Use a proxy server (e.g., --proxy http://123.45.67.89:8080)

=== Examples ===

▶ Basic usage:
   python3 demoqa_test.py

▶ Headless mode:
   python3 demoqa_test.py --headless

▶ With proxy:
   python3 demoqa_test.py --proxy http://123.45.67.89:8080

▶ Headless + proxy:
   python3 demoqa_test.py --headless --proxy http://123.45.67.89:8080
