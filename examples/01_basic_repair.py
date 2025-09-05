from html_intersection.core import repair_all


if __name__ == "__main__":
    c, f, x = repair_all(
        ro_directory=r"E:\\Carte\\BB\\17 - Site Leadership\\Principal 2022\\ro",
        en_directory=r"E:\\Carte\\BB\\17 - Site Leadership\\Principal 2022\\en",
        base_url="https://neculaifantanaru.com",
        dry_run=False,
        backup_ext=".bak",
    )
    print("Results:", c, f, x)


