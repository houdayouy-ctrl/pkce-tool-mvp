import re
from typing import List
from .models import AuditInput, AuditReport, Violation
from ..sharia_rules import SHARIA_RULES, MAX_PENALTY

# --- Initialisation du Moteur NLP (pour usage futur) ---
# NOTE: L'initialisation de spaCy peut être coûteuse, nous la faisons une seule fois au chargement du module.
try:
    import spacy
    # Charge le modèle français que nous avons installé précédemment
    NLP_ENGINE = spacy.load("fr_core_news_sm") 
    print("Moteur NLP spaCy chargé avec succès.")
except ImportError:
    # Si spaCy n'est pas installé (ce qui ne devrait pas arriver ici)
    print("Avertissement: Le moteur spaCy n'est pas disponible. Utilisation du mode regex strict.")
    NLP_ENGINE = None

# --- Fonction principale d'analyse ---
def analyze_text(audit_input: AuditInput) -> AuditReport:
    """
    Analyse le contenu du contrat pour détecter les violations de conformité Sharia.
    
    Args:
        audit_input: L'objet AuditInput contenant le texte et l'ID de référence.

    Returns:
        Un objet AuditReport détaillé.
    """
    content = audit_input.content
    reference_id = audit_input.reference_id if audit_input.reference_id else "N/A"
    
    # 1. Pré-traitement du texte (minuscules pour une détection simple)
    # Dans le MVP, nous traitons le texte brut et le mettons en minuscules.
    text_to_analyze = content.lower()
    
    total_penalty = 0
    violations_list: List[Violation] = []
    
    # 2. Détection des violations (MVP: Recherche de chaînes de caractères)
    for concept, rule in SHARIA_RULES.items():
        for keyword in rule["keywords"]:
            # Utiliser la recherche de sous-chaîne pour le MVP (simple et rapide)
            if keyword in text_to_analyze:
                # Si le mot-clé est trouvé, on détecte le contexte (snippet)
                
                # Utiliser regex pour trouver l'occurrence exacte et le contexte
                # La regex cherche le mot-clé et capture 30 caractères de chaque côté
                pattern = re.compile(rf".{{0,30}}{re.escape(keyword)}.{0,30}", re.IGNORECASE | re.DOTALL)
                match = pattern.search(content)

                snippet = match.group(0).strip() if match else f"[... {keyword} ...]"
                
                # Ajout de la pénalité pour cette violation
                total_penalty += rule["severity"]
                
                # Création de l'objet Violation
                violations_list.append(
                    Violation(
                        concept=concept,
                        snippet=snippet,
                        severity=rule["severity"],
                        recommendation=rule["recommendation"]
                    )
                )
                
                # Arrêter de compter les pénalités pour un même concept une fois détecté
                # (Dans un MVP, on compte la pénalité une fois par concept)
    
    # 3. Calcul du Score de Conformité
    # Le score commence à 100 et est réduit par la pénalité totale
    compliance_score = max(0, 100 - total_penalty)
    
    # 4. Définition du Statut Global
    if compliance_score == 100:
        global_status = "CONFORME"
    elif compliance_score >= 70:
        global_status = "A REVOIR (Risque Faible)"
    else:
        global_status = "VIOLATION (Risque Élevé)"
        
    # 5. Calcul du nombre de mots
    word_count = len(content.split())
    
    # 6. Création du Rapport Final
    return AuditReport(
        reference_id=reference_id,
        compliance_score=compliance_score,
        global_status=global_status,
        violations=violations_list,
        word_count=word_count,
    )


# --- Exemple d'utilisation (pour tester le module seul) ---
if __name__ == '__main__':
    # Exemple de contrat non-conforme (Contrat de prêt classique)
    non_compliant_contract = """
    CONTRAT DE PRÊT HYPOTHÉCAIRE
    Ce contrat stipule que la partie A (l'Emprunteur) recevra un prêt de 500,000 EUR. 
    L'amortissement sera effectué sur 20 ans au taux d'intérêt fixe de 4.5%. 
    Toute spéculation est strictement interdite sur les actifs sous-jacents. 
    Une pénalité de retard de 0.1% par jour sera appliquée en cas de non-paiement.
    """
    
    input_data = AuditInput(
        content=non_compliant_contract,
        reference_id="CONTRACT-2025-001"
    )
    
    report = analyze_text(input_data)
    
    print("\n" + "="*50)
    print(f"RAPPORT D'AUDIT SHARIA - ID: {report.reference_id}")
    print("="*50)
    print(f"Statut Global: {report.global_status}")
    print(f"Score de Conformité: {report.compliance_score}/100")
    print(f"Nombre de Mots: {report.word_count}")
    print("-" * 50)
    
    if report.violations:
        print("VIOLATIONS DÉTECTÉES:")
        for v in report.violations:
            print(f"\n- CONCEPT: {v.concept} (Pénalité: -{v.severity})")
            print(f"  Extrait: '{v.snippet}'")
            print(f"  Correction: {v.recommendation}")
    else:
        print("Aucune violation majeure de la Charia détectée.")
    print("="*50) 