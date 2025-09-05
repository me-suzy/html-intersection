from html_intersection.core import repair_all


if __name__ == "__main__":
    c, f, x = repair_all(
        ro_directory=r"E:\\path\\to\\site\\ro",
        en_directory=r"E:\\path\\to\\site\\en",
        base_url="https://neculaifantanaru.com",
        dry_run=True,
    )
    print("Dry-run results:", c, f, x)


