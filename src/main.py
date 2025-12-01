from pydantic import BaseModel, Field
from typing import List, Optional

# --- Modèle de données pour une violation détectée ---
class Violation(BaseModel):
    # Le concept Sharia violé (ex: 'Riba', 'Gharar')
    concept: str
    # L'extrait de texte du contrat qui a causé la violation
    snippet: str
    # La gravité de la violation (utilisée pour calculer le score)
    severity: int
    # Recommandation pour la correction
    recommendation: str

# --- Modèle de données pour le rapport d'audit final (Output) ---
class AuditReport(BaseModel):
    # ID de traçabilité de la requête
    reference_id: str
    # Score de conformité sur 100
    compliance_score: int
    # Statut global (CONFORME, VIOLATION, ou A REVOIR)
    global_status: str
    # Liste détaillée des violations trouvées
    violations: List[Violation]
    # Nombre total de mots analysés
    word_count: int

# --- Modèle de données pour la soumission d'audit (Input) ---
class AuditInput(BaseModel):
    # Le texte complet du contrat, du JSON ou du rapport financier à analyser
    content: str = Field(..., description="Contrat ou document financier à analyser.")
    # ID unique pour la traçabilité de la requête
    reference_id: Optional[str] = Field(None, description="ID de référence client ou système.")
