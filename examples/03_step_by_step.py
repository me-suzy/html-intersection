from html_intersection.core import fix_canonicals, fix_flags_match_canonical, sync_cross_references


if __name__ == "__main__":
    ro = r"E:\\site\\ro"
    en = r"E:\\site\\en"
    base = "https://neculaifantanaru.com"

    c = fix_canonicals(ro, en, base)
    f = fix_flags_match_canonical(ro, en, base)
    x = sync_cross_references(ro, en, base)
    print("Step results:", c, f, x)


