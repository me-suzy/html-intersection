import os
import tempfile

from html_intersection.core import repair_all, scan_issues


BASE_URL = "https://neculaifantanaru.com"


def write_file(path: str, content: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def make_ro_html(filename: str, ro_href: str, en_href: str) -> str:
    return f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8" />
  <link rel="canonical" href="{BASE_URL}/{filename}" />
  <title>{filename}</title>
  <!-- FLAGS_1 -->
  <div class=\"wrapper country-wrapper\">
    <dl id=\"country-select\" class=\"dropdown country-select\">
      <dd>
        <ul style=\"display: none;\"> 
          <li><a cunt_code=\"+40\" href=\"{ro_href}\">RO</a></li>
          <li><a cunt_code=\"+1\" href=\"{en_href}\">EN</a></li>
        </ul>
      </dd>
    </dl>
  </div>
  <!-- FLAGS -->
</head>
<body>RO page: {filename}</body>
</html>
""".strip()


def make_en_html(filename: str, en_href: str, ro_href: str) -> str:
    return f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8" />
  <link rel="canonical" href="{BASE_URL}/en/{filename}" />
  <title>{filename}</title>
  <!-- FLAGS_1 -->
  <div class=\"wrapper country-wrapper\">
    <dl id=\"country-select\" class=\"dropdown country-select\">
      <dd>
        <ul style=\"display: none;\"> 
          <li><a cunt_code=\"+1\" href=\"{en_href}\">EN</a></li>
          <li><a cunt_code=\"+40\" href=\"{ro_href}\">RO</a></li>
        </ul>
      </dd>
    </dl>
  </div>
  <!-- FLAGS -->
</head>
<body>EN page: {filename}</body>
</html>
""".strip()


def print_report(tag: str, report: dict) -> None:
    print(f"== {tag} ==")
    print("RO->EN:")
    for ro_name, en_name in report["ro_to_en"].items():
        print(f"  {ro_name} -> {en_name}")
    print("EN->RO:")
    for en_name, ro_name in report["en_to_ro"].items():
        print(f"  {en_name} -> {ro_name}")
    if report["invalid_links"]:
        print("Invalid links:")
        for msg in report["invalid_links"]:
            print(f"  {msg}")
    if report["mismatched_pairs"]:
        print("Pairs with no common links:")
        for ro_name, en_name, details in report["mismatched_pairs"]:
            print(f"  {ro_name} <-> {en_name}: {details}")
    if report["unmatched_ro"] or report["unmatched_en"]:
        print("Unmatched files:")
        for ro_name in report["unmatched_ro"]:
            print(f"  RO {ro_name}")
        for en_name in report["unmatched_en"]:
            print(f"  EN {en_name}")


def main() -> None:
    # Accounting-themed pages
    ro_invoice = "factura-001.html"
    en_invoice = "invoice-001.html"

    ro_trial = "balanta-2024.html"
    en_trial = "trial-balance-2024.html"

    ro_journal = "registru-jurnal.html"  # unmatched
    en_cashflow = "cash-flow-2024.html"  # unmatched

    with tempfile.TemporaryDirectory() as tmp:
        ro_dir = os.path.join(tmp, "ro")
        en_dir = os.path.join(tmp, "en")

        # Pair A: factura-001 <-> invoice-001
        # - RO points correctly to EN
        # - EN incorrectly points to a non-existent RO (will be corrected)
        write_file(
            os.path.join(ro_dir, ro_invoice),
            make_ro_html(
                filename=ro_invoice,
                ro_href=f"{BASE_URL}/{ro_invoice}",
                en_href=f"{BASE_URL}/en/{en_invoice}",
            ),
        )
        write_file(
            os.path.join(en_dir, en_invoice),
            make_en_html(
                filename=en_invoice,
                en_href=f"{BASE_URL}/en/{en_invoice}",
                ro_href=f"{BASE_URL}/factura-999.html",  # wrong; will be fixed to factura-001.html
            ),
        )

        # Pair B: balanta-2024 <-> trial-balance-2024
        # - RO points correctly to EN
        # - EN incorrectly points to non-existent RO (will be corrected)
        write_file(
            os.path.join(ro_dir, ro_trial),
            make_ro_html(
                filename=ro_trial,
                ro_href=f"{BASE_URL}/{ro_trial}",
                en_href=f"{BASE_URL}/en/{en_trial}",
            ),
        )
        write_file(
            os.path.join(en_dir, en_trial),
            make_en_html(
                filename=en_trial,
                en_href=f"{BASE_URL}/en/{en_trial}",
                ro_href=f"{BASE_URL}/bilant-2023.html",  # wrong; will be fixed to balanta-2024.html
            ),
        )

        # Unmatched examples
        write_file(
            os.path.join(ro_dir, ro_journal),
            make_ro_html(
                filename=ro_journal,
                ro_href=f"{BASE_URL}/{ro_journal}",
                en_href=f"{BASE_URL}/en/nonexistent.html",
            ),
        )
        write_file(
            os.path.join(en_dir, en_cashflow),
            make_en_html(
                filename=en_cashflow,
                en_href=f"{BASE_URL}/en/{en_cashflow}",
                ro_href=f"{BASE_URL}/nonexistent.html",
            ),
        )

        # Before
        report_before = scan_issues(ro_dir, en_dir, BASE_URL)
        print_report("Before", report_before)

        # Repair all (canonicals, own flags, cross refs)
        c, f, x = repair_all(ro_dir, en_dir, BASE_URL, dry_run=False, backup_ext=None)
        print(f"\n== Repair counts ==\nCanonicals: {c}; Flags: {f}; Cross-ref: {x}")

        # After
        report_after = scan_issues(ro_dir, en_dir, BASE_URL)
        print()
        print_report("After", report_after)


if __name__ == "__main__":
    main()


