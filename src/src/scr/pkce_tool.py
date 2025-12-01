import os
import base64
import hashlib
from typing import Tuple

def generate_pkce_keys() -> Tuple[str, str]:
    """
    Génère un code verifier et en dérive le code challenge PKCE.
    C'est la logique métier minimale requise pour l'étape initiale du PKCE.
    """
    # 1. Génération du Code Verifier (étape cruciale côté client/application)
    # Recommandation : 32 octets aléatoires, encodés en base64url sans padding.
    # Ceci garantit 43 octets de 'verifier' après encodage, respectant les contraintes OAuth.
    random_bytes = os.urandom(32)
    code_verifier = base64.urlsafe_b64encode(random_bytes).rstrip(b'=').decode('ascii')

    # 2. Dérivation du Code Challenge (étape cruciale côté client/application)
    # SHA256 du code verifier, puis encodé en base64url sans padding.
    verifier_hash = hashlib.sha256(code_verifier.encode('utf-8')).digest()
    code_challenge = base64.urlsafe_b64encode(verifier_hash).rstrip(b'=').decode('ascii')
    
    return code_verifier, code_challenge

# --- Exécution et Affichage ---

if __name__ == "__main__":
    print("--- Génération des Clés PKCE (MVP) ---")
    
    verifier, challenge = generate_pkce_keys()
    
    print(f"**Code Verifier (Secret) :** \n{verifier}")
    print("\n---")
    print(f"**Code Challenge (Public) :** \n{challenge}")
    print("\nCe Challenge est envoyé au serveur d'autorisation.")
    print("Le Verifier est conservé en secret pour l'échange final.")