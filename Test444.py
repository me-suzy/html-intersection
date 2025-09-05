import os
import tempfile
from html_intersection import repair_all
from html_intersection.core import scan_issues  # Import direct din core

BASE_URL = "https://finante.gov.ro"

def write_file(path: str, content: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def create_budget_document(filename: str, execution_ref: str, wrong_execution: str) -> str:
    """Creează document buget cu referință către execuția bugetară"""
    return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <link rel="canonical" href="{BASE_URL}/buget/{filename}" />
    <title>Bugetul General Consolidat 2024</title>
</head>
<body>
    <h1>Bugetul General Consolidat pentru anul 2024</h1>
    
    <!-- FLAGS_1 -->
    <div class="wrapper country-wrapper">
        <dl id="country-select" class="dropdown country-select">
            <dd>
                <ul style="display: none;">
                    <li><a cunt_code="+40" href="{BASE_URL}/buget/{filename}"><span>Buget</span></a></li>
                    <li><a cunt_code="+1" href="{BASE_URL}/executie/{execution_ref}"><span>Execuție</span></a></li>
                </ul>
            </dd>
        </dl>
    </div>
    <!-- FLAGS -->
    
    <section>
        <h2>Venituri bugetare totale: 450.2 miliarde lei</h2>
        <ul>
            <li>Venituri fiscale: 380.5 mld lei</li>
            <li>Venituri nefiscale: 69.7 mld lei</li>
        </ul>
    </section>
</body>
</html>"""

def create_execution_document(filename: str, budget_ref: str, wrong_budget: str) -> str:
    """Creează document execuție bugetară cu referință către buget"""
    return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <link rel="canonical" href="{BASE_URL}/executie/{filename}" />
    <title>Execuția Bugetară 2024 - Trimestrul III</title>
</head>
<body>
    <h1>Raport Execuție Bugetară - T3 2024</h1>
    
    <!-- FLAGS_1 -->
    <div class="wrapper country-wrapper">
        <dl id="country-select" class="dropdown country-select">
            <dd>
                <ul style="display: none;">
                    <li><a cunt_code="+1" href="{BASE_URL}/executie/{filename}"><span>Execuție</span></a></li>
                    <li><a cunt_code="+40" href="{BASE_URL}/buget/{wrong_budget}"><span>Buget</span></a></li>
                </ul>
            </dd>
        </dl>
    </div>
    <!-- FLAGS -->
    
    <section>
        <h2>Execuție venituri la 30 septembrie 2024</h2>
        <ul>
            <li>Încasări totale: 338.4 miliarde lei (75.2% din plan)</li>
            <li>Venituri fiscale: 285.1 mld lei (75.1% din plan)</li>
            <li>Venituri nefiscale: 53.3 mld lei (76.5% din plan)</li>
        </ul>
    </section>
</body>
</html>"""

def extract_references_from_content(content: str) -> dict:
    """Extrage referințele relevante din conținutul HTML"""
    import re
    
    # Extrage canonical
    canonical = re.search(r'<link rel="canonical" href="([^"]+)"', content)
    
    # Extrage link-urile din FLAGS 
    buget_link = re.search(r'<li><a cunt_code="\+40" href="([^"]+)"', content)
    exec_link = re.search(r'<li><a cunt_code="\+1" href="([^"]+)"', content)
    
    return {
        'canonical': canonical.group(1) if canonical else None,
        'buget_flag': buget_link.group(1) if buget_link else None,
        'exec_flag': exec_link.group(1) if exec_link else None,
    }

def compare_before_after(before_content: str, after_content: str, doc_type: str) -> None:
    """Compară și afișează diferențele între versiunile înainte și după"""
    
    before_refs = extract_references_from_content(before_content)
    after_refs = extract_references_from_content(after_content)
    
    print(f"\n=== Modificări în documentul {doc_type.upper()} ===")
    
    # Verifică link-urile FLAGS
    if before_refs['buget_flag'] != after_refs['buget_flag']:
        print(f"Link Buget în FLAGS:")
        print(f"  ÎNAINTE: {before_refs['buget_flag']}")
        print(f"  DUPĂ:    {after_refs['buget_flag']}")
    
    if before_refs['exec_flag'] != after_refs['exec_flag']:
        print(f"Link Execuție în FLAGS:")
        print(f"  ÎNAINTE: {before_refs['exec_flag']}")
        print(f"  DUPĂ:    {after_refs['exec_flag']}")
    
    if (before_refs == after_refs):
        print(f"Nu s-au făcut modificări în {doc_type}")

def main():
    """Exemplu complet cu documente din finanțe publice"""
    
    print("=== EXEMPLU FINANȚE PUBLICE - GĂSIRE ȘI ÎNLOCUIRE ===")
    
    with tempfile.TemporaryDirectory() as tmp:
        buget_dir = os.path.join(tmp, "buget")
        exec_dir = os.path.join(tmp, "executie")
        
        # Numele documentelor
        budget_file = "buget-general-2024.html"
        execution_file = "executie-bugetara-t3-2024.html"
        
        # Referințe corecte vs greșite
        wrong_budget = "buget-general-2023.html"  # Referință greșită
        
        # Creează documentele cu probleme
        budget_content = create_budget_document(
            budget_file, 
            execution_file,    # FLAGS corect
            execution_file     # Link text corect
        )
        
        execution_content = create_execution_document(
            execution_file,
            budget_file,      # FLAGS corect  
            wrong_budget      # Link FLAGS greșit - va fi reparat
        )
        
        budget_path = os.path.join(buget_dir, budget_file)
        execution_path = os.path.join(exec_dir, execution_file)
        
        write_file(budget_path, budget_content)
        write_file(execution_path, execution_content)
        
        # Citește conținutul înainte de modificări
        with open(budget_path, 'r', encoding='utf-8') as f:
            budget_before = f.read()
        with open(execution_path, 'r', encoding='utf-8') as f:
            execution_before = f.read()
        
        print("=== STAREA INIȚIALĂ ===")
        
        # Scanează problemele
        report_before = scan_issues(buget_dir, exec_dir, BASE_URL)
        
        print("Perechi identificate:")
        for buget_name, exec_name in report_before["ro_to_en"].items():
            print(f"  {buget_name} ↔ {exec_name}")
        
        if report_before["mismatched_pairs"]:
            print("Perechi cu referințe incorecte:")
            for buget, exec_file, details in report_before["mismatched_pairs"]:
                print(f"  {buget} ↔ {exec_file}")
                print(f"    Detalii: {details}")
        
        # Aplică reparațiile
        print("\n=== APLICARE REPARAȚII ===")
        canonical_fixes, flag_fixes, cross_ref_fixes = repair_all(
            buget_dir, exec_dir, BASE_URL, 
            dry_run=False, backup_ext=None
        )
        
        print(f"Canonicals reparate: {canonical_fixes}")
        print(f"Flag-uri reparate: {flag_fixes}")
        print(f"Cross-references reparate: {cross_ref_fixes}")
        
        # Citește conținutul după modificări
        with open(budget_path, 'r', encoding='utf-8') as f:
            budget_after = f.read()
        with open(execution_path, 'r', encoding='utf-8') as f:
            execution_after = f.read()
        
        # Compară și afișează modificările
        compare_before_after(budget_before, budget_after, "buget")
        compare_before_after(execution_before, execution_after, "execuție")
        
        print("\n=== STAREA FINALĂ ===")
        report_after = scan_issues(buget_dir, exec_dir, BASE_URL)
        
        print("Perechi sincronizate:")
        for pair in report_after["bidirectional_pairs"]:
            print(f"  {pair[0]} ↔ {pair[1]} ✓")

if __name__ == "__main__":
    main()