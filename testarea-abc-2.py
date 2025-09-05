from html_intersection import (
    fix_canonicals,
    fix_flags_match_canonical,
    sync_cross_references,
    repair_all
)
import os
import tempfile

def create_test_html_files():
    """Creează fișiere HTML de test cu probleme specifice"""

    # Fișier cu canonical greșit
    html_with_wrong_canonical = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test Page</title>
        <link rel="canonical" href="https://example.com/wrong-page.html">
        <meta charset="UTF-8">
    </head>
    <body>
        <!-- FLAGS_1 -->
        <div class="flags">
            <a href="https://neculaifantanaru.com/test-page.html">RO</a>
            <a href="https://neculaifantanaru.com/en/test-page-en.html">EN</a>
        </div>
        <!-- FLAGS -->

        <h1>Test Page</h1>
        <p>Aceasta este o pagină de test.</p>
    </body>
    </html>
    """

    # Fișier cu flags care nu se potrivesc cu canonical
    html_with_mismatched_flags = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Another Test</title>
        <link rel="canonical" href="https://neculaifantanaru.com/another-test.html">
    </head>
    <body>
        <!-- FLAGS_1 -->
        <div class="flags">
            <a href="https://neculaifantanaru.com/different-page.html">RO</a>
            <a href="https://neculaifantanaru.com/en/different-page-en.html">EN</a>
        </div>
        <!-- FLAGS -->

        <h1>Another Test</h1>
    </body>
    </html>
    """

    # Creează un director temporar pentru teste
    test_dir = tempfile.mkdtemp()

    # Salvează fișierele
    file1_path = os.path.join(test_dir, "test-page.html")
    file2_path = os.path.join(test_dir, "another-test.html")

    with open(file1_path, 'w', encoding='utf-8') as f:
        f.write(html_with_wrong_canonical)

    with open(file2_path, 'w', encoding='utf-8') as f:
        f.write(html_with_mismatched_flags)

    return test_dir, file1_path, file2_path

def test_html_intersection_functions():
    """Testează funcțiile disponibile în pachetul html_intersection"""

    print("=== Test HTML Intersection Package ===")
    print()

    # Creează fișierele de test
    test_dir, file1, file2 = create_test_html_files()

    print(f"Directorul de test: {test_dir}")
    print(f"Fișier 1: {os.path.basename(file1)}")
    print(f"Fișier 2: {os.path.basename(file2)}")
    print()

    # Test 1: fix_canonicals
    print("1. Testing fix_canonicals...")
    try:
        result = fix_canonicals(file1)
        print(f"   ✓ fix_canonicals completat")
        print(f"   Rezultat: {type(result)} - {len(str(result)) if result else 0} caractere")
    except Exception as e:
        print(f"   ✗ Eroare fix_canonicals: {e}")

    print()

    # Test 2: fix_flags_match_canonical
    print("2. Testing fix_flags_match_canonical...")
    try:
        result = fix_flags_match_canonical(file2)
        print(f"   ✓ fix_flags_match_canonical completat")
        print(f"   Rezultat: {type(result)} - {len(str(result)) if result else 0} caractere")
    except Exception as e:
        print(f"   ✗ Eroare fix_flags_match_canonical: {e}")

    print()

    # Test 3: sync_cross_references
    print("3. Testing sync_cross_references...")
    try:
        result = sync_cross_references(test_dir)
        print(f"   ✓ sync_cross_references completat")
        print(f"   Rezultat: {type(result)} - {len(str(result)) if result else 0} caractere")
    except Exception as e:
        print(f"   ✗ Eroare sync_cross_references: {e}")

    print()

    # Test 4: repair_all
    print("4. Testing repair_all...")
    try:
        result = repair_all(test_dir)
        print(f"   ✓ repair_all completat")
        print(f"   Rezultat: {type(result)} - {len(str(result)) if result else 0} caractere")
    except Exception as e:
        print(f"   ✗ Eroare repair_all: {e}")

    print()

    # Verifică dacă fișierele au fost modificate
    print("5. Verificare modificări...")
    try:
        with open(file1, 'r', encoding='utf-8') as f:
            content1 = f.read()
            if "canonical" in content1:
                print("   ✓ Fișierul 1 conține încă canonical")

        with open(file2, 'r', encoding='utf-8') as f:
            content2 = f.read()
            if "FLAGS" in content2:
                print("   ✓ Fișierul 2 conține încă FLAGS")

    except Exception as e:
        print(f"   ✗ Eroare la verificarea fișierelor: {e}")

    return test_dir

def test_individual_modules():
    """Testează modulele individuale din pachet"""

    print("\n=== Test Module Individual ===")

    # Test import din core
    try:
        from html_intersection.core import fix_canonicals
        print("✓ Import din core reușit")
    except Exception as e:
        print(f"✗ Eroare import core: {e}")

    # Test import din utils
    try:
        from html_intersection import utils
        print("✓ Import utils reușit")
        print(f"  Funcții în utils: {dir(utils)}")
    except Exception as e:
        print(f"✗ Eroare import utils: {e}")

    # Test import din cli
    try:
        from html_intersection import cli
        print("✓ Import cli reușit")
        print(f"  Funcții în cli: {dir(cli)}")
    except Exception as e:
        print(f"✗ Eroare import cli: {e}")

def cleanup_test_directory(test_dir):
    """Șterge directorul de test"""
    import shutil
    try:
        shutil.rmtree(test_dir)
        print(f"\n✓ Director de test șters: {test_dir}")
    except Exception as e:
        print(f"\n✗ Nu s-a putut șterge directorul: {e}")

if __name__ == "__main__":
    print("Testing html-intersection package...")
    print("Funcții disponibile:", ["fix_canonicals", "fix_flags_match_canonical", "sync_cross_references", "repair_all"])
    print()

    try:
        # Test funcțiile principale
        test_dir = test_html_intersection_functions()

        # Test modulele individuale
        test_individual_modules()

        print("\n=== Test complet ===")

        # Cleanup
        response = input("\nVrei să ștergi directorul de test? (y/n): ")
        if response.lower() in ['y', 'yes', 'da']:
            cleanup_test_directory(test_dir)

    except ImportError as e:
        print(f"Eroare la importul librăriei: {e}")
    except Exception as e:
        print(f"Eroare neașteptată: {e}")