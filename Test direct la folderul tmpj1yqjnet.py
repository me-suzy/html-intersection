from html_intersection import repair_all
import os
import re

def test_existing_directory_with_format_update():
    """Actualizează fișierele existente la formatul corect și testează"""

    # Folosește directorul existent
    base_dir = r"C:\Users\necul\AppData\Local\Temp\tmpj1yqjnet"
    ro_dir = os.path.join(base_dir, "ro")
    en_dir = os.path.join(base_dir, "en")
    base_url = "https://neculaifantanaru.com"

    print(f"Lucram cu directorul existent: {base_dir}")

    # Verifică că directoarele există
    if not os.path.exists(ro_dir) or not os.path.exists(en_dir):
        print("⚠️ Directoarele nu există!")
        return

    ro_file = os.path.join(ro_dir, "test-page.html")
    en_file = os.path.join(en_dir, "test-page-en.html")

    # Actualizează fișierele la formatul corect cu cunt_code
    print("Actualizare la formatul cu cunt_code...")

    # Actualizează fișierul RO
    if os.path.exists(ro_file):
        with open(ro_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Înlocuiește div.flags cu format cunt_code
        new_flags = '''    <!-- FLAGS_1 -->
    <div class="wrapper country-wrapper">
        <dl id="country-select" class="dropdown country-select">
            <dt><a href="javascript:void(0);"><span><span style="background-position:0px -671px"></span><span>Romania</span></span><i class="fa fa-chevron-down"></i></a></dt>
            <dd>
                <ul style="display: none;">
                    <li><a cunt_code="+40" href="https://neculaifantanaru.com/test-page.html"><span style="background-position:0px -671px"></span><span>Romania</span></a></li>
                    <li><a cunt_code="+1" href="https://neculaifantanaru.com/en/test-page-en.html"><span style="background-position:0px -44px"></span><span>United States</span></a></li>
                </ul>
            </dd>
        </dl>
    </div>
    <!-- FLAGS -->'''

        # Înlocuiește secțiunea FLAGS
        updated_content = re.sub(
            r'<!-- FLAGS_1 -->.*?<!-- FLAGS -->',
            new_flags,
            content,
            flags=re.DOTALL
        )

        with open(ro_file, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        print("✓ Fișier RO actualizat")

    # Actualizează fișierul EN cu problema (RO link greșit)
    if os.path.exists(en_file):
        with open(en_file, 'r', encoding='utf-8') as f:
            content = f.read()

        new_flags = '''    <!-- FLAGS_1 -->
    <div class="wrapper country-wrapper">
        <dl id="country-select" class="dropdown country-select">
            <dt><a href="javascript:void(0);"><span><span style="background-position:0px -671px"></span><span>Romania</span></span><i class="fa fa-chevron-down"></i></a></dt>
            <dd>
                <ul style="display: none;">
                    <li><a cunt_code="+40" href="https://neculaifantanaru.com/test-page9.html"><span style="background-position:0px -671px"></span><span>Romania</span></a></li>
                    <li><a cunt_code="+1" href="https://neculaifantanaru.com/en/test-page-en.html"><span style="background-position:0px -44px"></span><span>United States</span></a></li>
                </ul>
            </dd>
        </dl>
    </div>
    <!-- FLAGS -->'''

        updated_content = re.sub(
            r'<!-- FLAGS_1 -->.*?<!-- FLAGS -->',
            new_flags,
            content,
            flags=re.DOTALL
        )

        with open(en_file, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        print("✓ Fișier EN actualizat (cu problema RO link)")

    # Afișează starea înainte
    print("\nÎNAINTE de repair:")
    with open(en_file, 'r', encoding='utf-8') as f:
        content = f.read()
        ro_match = re.search(r'<li><a\s+cunt_code="\+40"\s+href="([^"]+)"', content)
        if ro_match:
            print(f"EN file RO link: {ro_match.group(1)}")

    # Rulează repair_all
    print("\nRulare repair_all...")
    result = repair_all(ro_dir, en_dir, base_url)
    print(f"Rezultat repair_all: {result}")

    # Afișează starea după
    print("\nDUPĂ repair:")
    with open(en_file, 'r', encoding='utf-8') as f:
        content = f.read()
        ro_match = re.search(r'<li><a\s+cunt_code="\+40"\s+href="([^"]+)"', content)
        if ro_match:
            print(f"EN file RO link: {ro_match.group(1)}")

if __name__ == "__main__":
    test_existing_directory_with_format_update()