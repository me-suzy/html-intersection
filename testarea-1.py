import os
import tempfile

from html_intersection.core import repair_all, scan_issues


BASE_URL = "https://neculaifantanaru.com"


def write_file(path: str, content: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def make_ro_html(filename: str, canonical_path: str, ro_link: str, en_link: str) -> str:
    return f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8" />
  <link rel="canonical" href="{BASE_URL}/{canonical_path}" />
  <title>{filename}</title>
  <style>/* minimal */</style>
  <!-- FLAGS_1 -->
  <div class="wrapper country-wrapper">
    <dl id="country-select" class="dropdown country-select">
      <dt><a href="javascript:void(0);"><span><span style="background-position:0px -671px"></span><span>Romania</span></span><i class="fa fa-chevron-down"></i></a></dt>
      <dd>
        <ul style="display: none;">
          <li><a cunt_code="+40" href="{ro_link}"><span style="background-position:0px -671px"></span><span>Romania</span></a></li>
          <li><a cunt_code="+1" href="{en_link}"><span style="background-position:0px -44px"></span><span>United States</span></a></li>
        </ul>
      </dd>
    </dl>
  </div>
  <!-- FLAGS -->
</head>
<body>RO: {filename}</body>
</html>
""".strip()


def make_en_html(filename: str, canonical_path: str, en_link: str, ro_link: str) -> str:
    return f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8" />
  <link rel="canonical" href="{BASE_URL}/{canonical_path}" />
  <title>{filename}</title>
  <style>/* minimal */</style>
  <!-- FLAGS_1 -->
  <div class="wrapper country-wrapper">
    <dl id="country-select" class="dropdown country-select">
      <dt><a href="javascript:void(0);"><span><span style="background-position:0px -671px"></span><span>United States</span></span><i class="fa fa-chevron-down"></i></a></dt>
      <dd>
        <ul style="display: none;">
          <li><a cunt_code="+1" href="{en_link}"><span style="background-position:0px -44px"></span><span>United States</span></a></li>
          <li><a cunt_code="+40" href="{ro_link}"><span style="background-position:0px -671px"></span><span>Romania</span></a></li>
        </ul>
      </dd>
    </dl>
  </div>
  <!-- FLAGS -->
</head>
<body>EN: {filename}</body>
</html>
""".strip()


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        ro_dir = os.path.join(tmp, "ro")
        en_dir = os.path.join(tmp, "en")

        # Pair 1: visio-aurea (will be fully auto-fixed)
        ro_visio = "visio-aurea.html"
        en_visio = "visio-aurea.html"
        ro_visio_path = os.path.join(ro_dir, ro_visio)
        en_visio_path = os.path.join(en_dir, en_visio)

        ro_visio_html = make_ro_html(
            ro_visio,
            canonical_path="visio-aurea.html",  # correct canonical
            ro_link=f"{BASE_URL}/visio-aurea-WRONG.html",  # wrong +40 to be fixed
            en_link=f"{BASE_URL}/en/visio-aurea.html.html",  # double .html -> will be normalized and fixed
        )
        en_visio_html = make_en_html(
            en_visio,
            canonical_path="en/visio-aurea.html",  # correct canonical
            en_link=f"{BASE_URL}/en/visio-aurea.html.html",  # wrong own +1 (double .html) -> fix to canonical
            ro_link=f"{BASE_URL}/visio-aurea-WRONG.html",  # wrong +40 to be fixed
        )

        write_file(ro_visio_path, ro_visio_html)
        write_file(en_visio_path, en_visio_html)

        # Pair 2: ochii-capteaza ... vs the-eyes-capture ... (mismatched; will be reported)
        ro_ochii = "ochii-capteaza-momente-care-devin-puncte-de-cotitura-in-reflectia-personala.html"
        en_eyes = "the-eyes-capture-moments-that-become-turning-points-in-personal-reflection.html"
        ro_ochii_path = os.path.join(ro_dir, ro_ochii)
        en_eyes_path = os.path.join(en_dir, en_eyes)

        ro_ochii_html = make_ro_html(
            ro_ochii,
            canonical_path=ro_ochii,  # correct canonical
            ro_link=f"{BASE_URL}/{ro_ochii}",  # correct own +40
            en_link=f"{BASE_URL}/en/the-memory-of-a-dusty-thought.html",  # invalid/mismatched
        )
        en_eyes_html = make_en_html(
            en_eyes,
            canonical_path=f"en/{en_eyes}",  # correct canonical
            en_link=f"{BASE_URL}/en/{en_eyes}",  # correct own +1
            ro_link=f"{BASE_URL}/ochii-surprind-momente-care-devin-puncte-de-cotitura-in-reflectia-personala.html",  # invalid/mismatched
        )

        write_file(ro_ochii_path, ro_ochii_html)
        write_file(en_eyes_path, en_eyes_html)

        print("== Initial scan ==")
        report_before = scan_issues(ro_dir, en_dir, BASE_URL)
        print("RO->EN:")
        for ro_name, en_name in report_before["ro_to_en"].items():
            print(f"  {ro_name} -> {en_name}")
        print("EN->RO:")
        for en_name, ro_name in report_before["en_to_ro"].items():
            print(f"  {en_name} -> {ro_name}")
        if report_before["invalid_links"]:
            print("Invalid links:")
            for msg in report_before["invalid_links"]:
                print(f"  {msg}")
        if report_before["mismatched_pairs"]:
            print("Pairs with no common links:")
            for ro_name, en_name, details in report_before["mismatched_pairs"]:
                print(f"  {ro_name} <-> {en_name}: {details}")
        if report_before["unmatched_ro"] or report_before["unmatched_en"]:
            print("Unmatched files:")
            for ro_name in report_before["unmatched_ro"]:
                print(f"  RO {ro_name}")
            for en_name in report_before["unmatched_en"]:
                print(f"  EN {en_name}")

        c, f, x = repair_all(ro_dir, en_dir, BASE_URL, dry_run=False, backup_ext=None)
        print(f"== Repair counts ==\nCanonicals: {c}; Flags: {f}; Cross-ref: {x}")

        print("== After repair scan ==")
        report_after = scan_issues(ro_dir, en_dir, BASE_URL)
        print("RO->EN:")
        for ro_name, en_name in report_after["ro_to_en"].items():
            print(f"  {ro_name} -> {en_name}")
        print("EN->RO:")
        for en_name, ro_name in report_after["en_to_ro"].items():
            print(f"  {en_name} -> {ro_name}")
        if report_after["invalid_links"]:
            print("Invalid links:")
            for msg in report_after["invalid_links"]:
                print(f"  {msg}")
        if report_after["mismatched_pairs"]:
            print("Pairs with no common links:")
            for ro_name, en_name, details in report_after["mismatched_pairs"]:
                print(f"  {ro_name} <-> {en_name}: {details}")
        if report_after["unmatched_ro"] or report_after["unmatched_en"]:
            print("Unmatched files:")
            for ro_name in report_after["unmatched_ro"]:
                print(f"  RO {ro_name}")
            for en_name in report_after["unmatched_en"]:
                print(f"  EN {en_name}")

        # Show that visio-aurea was fully corrected
        with open(ro_visio_path, "r", encoding="utf-8") as fr:
            ro_visio_content = fr.read()
        with open(en_visio_path, "r", encoding="utf-8") as fe:
            en_visio_content = fe.read()

        print("== visio-aurea (RO) snippet ==")
        for line in ro_visio_content.splitlines():
            if 'cunt_code="+40"' in line or 'cunt_code="+1"' in line or 'rel="canonical"' in line:
                print(line.strip())
        print("== visio-aurea (EN) snippet ==")
        for line in en_visio_content.splitlines():
            if 'cunt_code="+40"' in line or 'cunt_code="+1"' in line or 'rel="canonical"' in line:
                print(line.strip())


if __name__ == "__main__":
    main()


