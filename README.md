# Usage

1. Open your bank's web interface
2. Press F12 and switch to Network tab
3. Open list of all transactions in the bank's interface
4. Right-click DevTools and click "Save all as HAR with content"
5. Run the script: `python ./__main__.py ./hars/*.har > transactions.csv`