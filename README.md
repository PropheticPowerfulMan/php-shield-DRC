# PHP-SHIELD RDC

Plateforme proposée pour l'inventaire et le suivi de la sécurité des applications PHP. Projet technique en cours d'évaluation : aucune approbation ni mise en production institutionnelle n'est revendiquée.

## État

Fondation initiale : application React/Vite, API FastAPI, modèle de données SQLAlchemy/Alembic, PostgreSQL et Redis via Docker Compose. Le registre, l'authentification complète, les moteurs d'audit et les rapports restent à réaliser dans les phases suivantes. Aucun résultat de scan ni statistique fictive n'est fourni.

L'emblème fourni par le propriétaire est attendu dans `frontend/public/assets/drc-government-emblem.png`. Il est utilisé sans modification. S'il manque, l'interface affiche une marque typographique.

## Documentation publique

La présentation du projet et le manuel d’utilisation sont téléchargeables en PDF depuis l’écran de connexion de l’[aperçu public](https://propheticpowerfulman.github.io/php-shield-DRC/). Les fichiers servis par l’application se trouvent dans `frontend/public/documents/`.

Sur Windows, `python tools/generate_project_documents.py --document manual` régénère le guide avec ReportLab. Pour une édition avec captures, placez `01-login.png`, `02-overview.png`, `03-module.png` et `04-reports.png` dans `tmp/pdfs/screenshots/`, puis ajoutez `--require-screenshots` à la commande.

## Prérequis

Docker et Docker Compose, ou Python 3.11+ avec PostgreSQL/Redis et Node.js 20+.

## Lancement Docker

1. Copier `.env.example` en `.env` et remplacer chaque secret.
2. `docker compose up --build`
3. API et OpenAPI : http://localhost:8000/docs ; UI : http://localhost:8080.

Créer le premier administrateur après le démarrage : `docker compose exec api python -m app.bootstrap_admin`. Le mot de passe est saisi de façon interactive; aucun compte par défaut ni inscription publique n'existe. La session utilise un cookie HTTP-only, `SameSite=Lax` et une expiration de huit heures.

Ne l'exposez pas comme service de production avant d'avoir achevé les permissions métier, le MFA, la limitation distribuée des tentatives et la revue de sécurité. GitHub Pages héberge uniquement l'aperçu frontend; l'API d'authentification doit être déployée séparément.

## Développement local

API : `cd backend; python -m venv .venv; .venv\Scripts\activate; pip install -e .; alembic upgrade head; uvicorn app.main:app --reload`

Interface : `cd frontend; npm install; npm run dev`.

## Vérifications

Backend : `cd backend; pytest`. Frontend : `cd frontend; npm run build`.

## Phases

1. Fondation et shell institutionnel.
2. Registre, inventaire et audits PHP/Composer/risk.
3. Adaptateurs d'analyse isolés, remédiation et alertes.
4. Rapports, gouvernance et audit trail.
5. Essais de bout en bout, validation sécurité et préparation pilote.

Ne lancez d'audits que sur des actifs explicitement autorisés. La publication GitHub Pages ne convient qu'au frontend statique et ne déploie ni API ni données; la configuration reste à activer lorsque l'accès GitHub est disponible.
