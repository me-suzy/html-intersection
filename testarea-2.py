import os
import re
import tempfile

from html_intersection.core import fix_flags_match_canonical


BASE_URL = "https://neculaifantanaru.com"


CANON_RE = re.compile(r'<link\s+rel="canonical"\s+href="([^"]+)"\s*/?>', re.IGNORECASE)
EN_RE = re.compile(r'<li><a\s+cunt_code="\\?\+1"\s+href="([^"]+)"')


def write_file(path: str, content: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def make_ro_html(ro_name: str, en_name: str) -> str:
    # Include the simple example the user gave, plus the library-recognized flags
    simple = f"""
                <!-- RO -->
                  <li><a href="{BASE_URL}/{ro_name}"></a>Romana</li>
                  <li><a href="{BASE_URL}/en/{en_name}"></a>Engleza</li>
    """.rstrip()
    flags = f"""
  <!-- FLAGS_1 -->
  <div class="wrapper country-wrapper">
    <dl id="country-select" class="dropdown country-select">
      <dd>
        <ul style="display: none;">
          <li><a cunt_code="+40" href="{BASE_URL}/{ro_name}">RO</a></li>
          <li><a cunt_code="+1" href="{BASE_URL}/en/{en_name}">EN</a></li>
        </ul>
      </dd>
    </dl>
  </div>
  <!-- FLAGS -->
    """.rstrip()
    return f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8" />
  <link rel="canonical" href="{BASE_URL}/{ro_name}" />
  <title>{ro_name}</title>
  {simple}
  {flags}
</head>
<body>RO: {ro_name}</body>
</html>
""".strip()


def make_en_html(ro_name: str, en_name: str) -> str:
    simple = f"""
                <!-- EN -->
                  <li><a href="{BASE_URL}/{ro_name}"></a>Romana</li>
                  <li><a href="{BASE_URL}/bebe.html"></a>Engleza</li>
    """.rstrip()
    flags = f"""
  <!-- FLAGS_1 -->
  <div class="wrapper country-wrapper">
    <dl id="country-select" class="dropdown country-select">
      <dd>
        <ul style="display: none;">
          <li><a cunt_code="+1" href="{BASE_URL}/bebe.html">EN</a></li>
          <li><a cunt_code="+40" href="{BASE_URL}/{ro_name}">RO</a></li>
        </ul>
      </dd>
    </dl>
  </div>
  <!-- FLAGS -->
    """.rstrip()
    return f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8" />
  <link rel="canonical" href="{BASE_URL}/en/{en_name}" />
  <title>{en_name}</title>
  {simple}
  {flags}
</head>
<body>EN: {en_name}</body>
<html>
""".strip()


def extract_pair_info(path: str) -> tuple[str, str]:
    content = open(path, "r", encoding="utf-8").read()
    can = CANON_RE.search(content)
    en = EN_RE.search(content)
    return (can.group(1) if can else "", en.group(1) if en else "")


def main() -> None:
    ro_name = "93-la-suta-din-totalul-unui-spatiu-temporar.html"
    en_name = "93-percent-of-the-total-of-a-temporary-space.html"

    with tempfile.TemporaryDirectory() as tmp:
        ro_dir = os.path.join(tmp, "ro")
        en_dir = os.path.join(tmp, "en")
        ro_path = os.path.join(ro_dir, ro_name)
        en_path = os.path.join(en_dir, en_name)

        write_file(ro_path, make_ro_html(ro_name, en_name))
        write_file(en_path, make_en_html(ro_name, en_name))

        # Before
        can_before, en_before = extract_pair_info(en_path)
        print("Before:")
        print(f"  EN canonical: {can_before}")
        print(f"  EN +1 link : {en_before}")

        # Fix own flags to match canonical
        n = fix_flags_match_canonical(ro_dir, en_dir, BASE_URL, dry_run=False, backup_ext=None)
        print(f"Fixes applied: {n}")

        # After
        can_after, en_after = extract_pair_info(en_path)
        print("After:")
        print(f"  EN canonical: {can_after}")
        print(f"  EN +1 link : {en_after}")

        # Expectation: en_before was .../bebe.html, en_after should equal can_after
        if en_after == can_after:
            print("OK: Wrong EN link replaced with canonical")
        else:
            print("ERROR: EN link was not corrected")


if __name__ == "__main__":
    main()


