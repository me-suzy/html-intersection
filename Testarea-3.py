import re

from html_intersection.core import _fix_double_html_suffix  # reuse library normalization


BASE_URL = "https://neculaifantanaru.com"


RO_BLOCK = (
    """
                <!-- RO -->
                  <li><a href="https://neculaifantanaru.com/93-la-suta-din-totalul-unui-spatiu-temporar.html"></a>Romana</li>
				  <li><a href="https://neculaifantanaru.com/93-percent-of-the-total-of-a-temporary-space.html"></a>Engleza</li>
    """
).strip()


EN_BLOCK = (
    """
                <!-- EN -->
                  <li><a href="https://neculaifantanaru.com/93-la-suta-din-totalul-unui-spatiu-temporar.html"></a>Romana</li>
				  <li><a href="https://neculaifantanaru.com/bebe.html"></a>Engleza</li>
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
    ro_hrefs = extract_hrefs(RO_BLOCK)
    en_hrefs = extract_hrefs(EN_BLOCK)

    print("Before:")
    print("  RO:")
    for h in ro_hrefs:
        print(f"    {h}")
    print("  EN:")
    for h in en_hrefs:
        print(f"    {h}")

    # Expected EN English link is the RO English link
    ro_eng_href = _fix_double_html_suffix(ro_hrefs[1]) if len(ro_hrefs) > 1 else ""
    en_eng_href = _fix_double_html_suffix(en_hrefs[1]) if len(en_hrefs) > 1 else ""

    updated_en_block = EN_BLOCK
    if ro_eng_href and en_eng_href != ro_eng_href:
        # Replace second href (index 1) in EN block
        updated_en_block = replace_nth_href(EN_BLOCK, ro_eng_href, 1)

    print("\nAfter (EN updated if needed):")
    print(updated_en_block)

    # Quick assertion
    new_en_hrefs = extract_hrefs(updated_en_block)
    if len(new_en_hrefs) > 1 and new_en_hrefs[1] == ro_eng_href:
        print("\nOK: EN Engleza link now matches RO Engleza link")
    else:
        print("\nERROR: EN Engleza link did not update")


if __name__ == "__main__":
    main()


