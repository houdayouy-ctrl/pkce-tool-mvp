# PKCE Tool (MVP)

Ce dépôt contient le code pour le projet "pkce-tool-mvp" avec un accent particulier sur la mise en œuvre du **Proof Key for Code Exchange (PKCE)**, un mécanisme de sécurité pour le flux d'autorisation OAuth 2.0.

L'objectif de cette version (MVP) est de valider la logique essentielle d'authentification et de sécurité avant d'intégrer dans un audit  complet.

##  Composant Principal : PKCE Tool

Le script clé est `src/src/scr/pkce_tool.py` (ou le `pkce_tool_mvp.py` si vous l'avez renommé).

Le PKCE est utilisé pour prévenir les attaques d'interception de code d'autorisation dans les applications clientes publiques (comme les applications mobiles ou de bureau).

### Logique Métier (MVP)

Le script `pkce_tool.py` implémente les deux fonctions principales du protocole PKCE :

1.  **Génération du Code Verifier** : Une chaîne aléatoire et secrète (le secret temporaire du client).
2.  **Dérivation du Code Challenge** : La version hachée (SHA256) et encodée en Base64 URL du Verifier. Ce challenge est envoyé au serveur d'autorisation.

##  Démarrage et Utilisation

### 1. Pré-requis

* Python 3.x
* Git (pour le clonage et la gestion des versions)

### 2. Installation de l'Environnement Virtuel

Je vous recommande de créer un environnement virtuel pour isoler les dépendances du projet :

```bash
python -m venv venv
# Pour activer l'environnement (PowerShell)
.\venv\Scripts\activate
# Pour activer l'environnement (Bash/Linux/macOS)
source venv/bin/activate
