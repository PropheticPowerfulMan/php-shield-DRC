# PHP-SHIELD RDC

Plateforme proposée pour l'inventaire et le suivi de la sécurité des applications PHP. Projet technique en cours d'évaluation : aucune approbation ni mise en production institutionnelle n'est revendiquée.

## État

Fondation initiale : application React/Vite, API FastAPI, modèle de données SQLAlchemy/Alembic, PostgreSQL et Redis via Docker Compose. Le registre, l'authentification complète, les moteurs d'audit et les rapports restent à réaliser dans les phases suivantes. Aucun résultat de scan ni statistique fictive n'est fourni.

L'emblème fourni par le propriétaire est attendu dans `frontend/public/assets/drc-government-emblem.png`. Il est utilisé sans modification. S'il manque, l'interface affiche une marque typographique.

## Prérequis

Docker et Docker Compose, ou Python 3.11+ avec PostgreSQL/Redis et Node.js 20+.

## Lancement Docker

1. Copier `.env.example` en `.env` et remplacer chaque secret.
2. `docker compose up --build`
3. API et OpenAPI : http://localhost:8000/docs ; UI : http://localhost:8080.

Ce socle n'a pas de compte bootstrap ni d'inscription publique. Ne l'exposez pas comme service de production avant d'avoir achevé l'authentification, les autorisations, les migrations et la revue de sécurité.

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
