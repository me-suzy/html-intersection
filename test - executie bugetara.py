import re
from html_intersection.core import _fix_double_html_suffix  # reuse library normalization

BASE_URL = "https://finante.gov.ro"

BUDGET_BLOCK = (
    """
                <!-- BUDGET -->
                  <li><a href="https://finante.gov.ro/buget-general-2024.html">Buget General 2024</a></li>
                  <li><a href="https://finante.gov.ro/executie-bugetara-2024.html">Execuție Bugetară 2024</a></li>
    """
).strip()

EXECUTION_BLOCK = (
    """
                <!-- EXECUTION -->
                  <li><a href="https://finante.gov.ro/buget-general-2024.html">Buget General 2024</a></li>
                  <li><a href="https://finante.gov.ro/executie-bugetara-greșită.html">Execuție Bugetară GREȘITĂ</a></li>
    """
).strip()

def extract_hrefs(block: str) -> list[str]:
    return re.findall(r'href="([^"]+)"', block)

def replace_nth_href(block: str, new_href: str, index: int) -> str:
    # Replace the nth occurrence (0-based) of href value in the block
    matches = list(re.finditer(r'href="([^"]+)"', block))
    if index < 0 or index >= len(matches):
        return block
    m = matches[index]
    start, end = m.span(1)
    return block[:start] + new_href + block[end:]

def main() -> None:
    budget_hrefs = extract_hrefs(BUDGET_BLOCK)
    execution_hrefs = extract_hrefs(EXECUTION_BLOCK)

    print("=== ÎNAINTE DE INTERSECȚIE ===")
    print("BUDGET (ce ar trebui să fie corect):")
    for i, h in enumerate(budget_hrefs):
        print(f"    {i}: {h}")
    print("EXECUTION (cu link greșit):")
    for i, h in enumerate(execution_hrefs):
        print(f"    {i}: {h}")

    # Expected EXECUTION second link should match BUDGET second link
    budget_exec_href = _fix_double_html_suffix(budget_hrefs[1]) if len(budget_hrefs) > 1 else ""
    execution_exec_href = _fix_double_html_suffix(execution_hrefs[1]) if len(execution_hrefs) > 1 else ""

    print(f"\n=== ANALIZA INTERSECȚIEI ===")
    print(f"BUDGET spune că execuția este:     {budget_exec_href}")
    print(f"EXECUTION spune că execuția este:  {execution_exec_href}")
    print(f"Sunt identice? {budget_exec_href == execution_exec_href}")

    updated_execution_block = EXECUTION_BLOCK
    if budget_exec_href and execution_exec_href != budget_exec_href:
        print(f"\n🔧 REPARARE: Înlocuiesc link-ul greșit cu cel corect...")
        # Replace second href (index 1) in EXECUTION block
        updated_execution_block = replace_nth_href(EXECUTION_BLOCK, budget_exec_href, 1)

    print(f"\n=== DUPĂ REPARARE ===")
    print("EXECUTION Block actualizat:")
    print(updated_execution_block)

    # Verification
    new_execution_hrefs = extract_hrefs(updated_execution_block)
    print(f"\n=== VERIFICARE FINALĂ ===")
    if len(new_execution_hrefs) > 1 and new_execution_hrefs[1] == budget_exec_href:
        print("✅ SUCCES: Link-ul execuție din EXECUTION acum se potrivește cu BUDGET")
        print(f"   Ambele pointează către: {budget_exec_href}")
    else:
        print("❌ EROARE: Link-ul execuție nu s-a actualizat corect")

    print(f"\n=== COMPARAȚIE SIDE-BY-SIDE ===")
    print("ÎNAINTE                                    DUPĂ")
    print("-" * 80)
    original_links = extract_hrefs(EXECUTION_BLOCK)
    updated_links = extract_hrefs(updated_execution_block)
    for i, (orig, upd) in enumerate(zip(original_links, updated_links)):
        status = "✅ REPARAT" if orig != upd else "   unchanged"
        print(f"{i}: {orig[:40]:<40} -> {upd[:40]:<40} {status}")

if __name__ == "__main__":
    main()