py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install --upgrade pip
pip install html-intersection

html-intersection repair --ro-dir "E:\site\ro" --en-dir "E:\site\en" --base-url https://neculaifantanaru.com --backup-ext .bak

html-intersection fix-canonicals --ro-dir "E:\site\ro" --en-dir "E:\site\en" --base-url https://neculaifantanaru.com
html-intersection fix-flags      --ro-dir "E:\site\ro" --en-dir "E:\site\en" --base-url https://neculaifantanaru.com
html-intersection sync           --ro-dir "E:\site\ro" --en-dir "E:\site\en" --base-url https://neculaifantanaru.com


