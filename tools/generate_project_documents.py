from __future__ import annotations

from datetime import date
import argparse
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Flowable,
    Frame,
    Image,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parents[1]
EMBLEM = ROOT / "frontend/public/assets/drc-government-emblem.png"
PUBLIC_DOCS = ROOT / "frontend/public/documents"
FINAL_DOCS = ROOT / "output/pdf"
SCREENSHOTS = ROOT / "tmp/pdfs/screenshots"
AUTHOR = "LOKALA LOMBOTO Jonathan"
TODAY = date(2026, 11, 10)
INK = colors.HexColor("#171a1c")
GRAPHITE = colors.HexColor("#202427")
STEEL = colors.HexColor("#545d63")
GOLD = colors.HexColor("#b5963e")
PALE_GOLD = colors.HexColor("#eee8d8")
PAPER = colors.HexColor("#f6f4ed")
LINE = colors.HexColor("#d8d4c9")
MUTED = colors.HexColor("#656d70")
GREEN = colors.HexColor("#537862")
RED = colors.HexColor("#9b3e46")
PAGE_W, PAGE_H = A4


def register_fonts() -> None:
    candidates = [
        (Path("C:/Windows/Fonts/arial.ttf"), Path("C:/Windows/Fonts/arialbd.ttf"), Path("C:/Windows/Fonts/ariali.ttf")),
        (Path("C:/Windows/Fonts/calibri.ttf"), Path("C:/Windows/Fonts/calibrib.ttf"), Path("C:/Windows/Fonts/calibrii.ttf")),
    ]
    for regular, bold, italic in candidates:
        if regular.exists() and bold.exists():
            pdfmetrics.registerFont(TTFont("Institutional", str(regular)))
            pdfmetrics.registerFont(TTFont("Institutional-Bold", str(bold)))
            if italic.exists():
                pdfmetrics.registerFont(TTFont("Institutional-Italic", str(italic)))
            pdfmetrics.registerFontFamily("Institutional", normal="Institutional", bold="Institutional-Bold", italic="Institutional-Italic", boldItalic="Institutional-Bold")
            return
    raise RuntimeError("Arial/Calibri fonts were not found in the Windows font directory.")


register_fonts()
BASE = getSampleStyleSheet()
STYLES = {
    "eyebrow": ParagraphStyle("Eyebrow", fontName="Institutional-Bold", fontSize=8, leading=11, textColor=GOLD, tracking=1.1, spaceAfter=8),
    "title": ParagraphStyle("Title", fontName="Institutional-Bold", fontSize=27, leading=32, textColor=INK, spaceAfter=9),
    "subtitle": ParagraphStyle("Subtitle", fontName="Institutional", fontSize=11, leading=17, textColor=MUTED, spaceAfter=14),
    "h1": ParagraphStyle("H1", fontName="Institutional-Bold", fontSize=17, leading=22, textColor=INK, spaceBefore=9, spaceAfter=9, keepWithNext=True),
    "h2": ParagraphStyle("H2", fontName="Institutional-Bold", fontSize=11, leading=15, textColor=GRAPHITE, spaceBefore=8, spaceAfter=4, keepWithNext=True),
    "body": ParagraphStyle("Body", fontName="Institutional", fontSize=9.1, leading=14, textColor=colors.HexColor("#343a3b"), spaceAfter=7),
    "small": ParagraphStyle("Small", fontName="Institutional", fontSize=7.6, leading=11, textColor=MUTED, spaceAfter=4),
    "bullet": ParagraphStyle("Bullet", fontName="Institutional", fontSize=8.8, leading=13.5, textColor=colors.HexColor("#343a3b"), leftIndent=12, firstLineIndent=-8, bulletIndent=0, spaceAfter=3),
    "tablehead": ParagraphStyle("TableHead", fontName="Institutional-Bold", fontSize=7.2, leading=9.5, textColor=colors.white),
    "table": ParagraphStyle("Table", fontName="Institutional", fontSize=7.1, leading=10, textColor=colors.HexColor("#343a3b")),
    "caption": ParagraphStyle("Caption", fontName="Institutional-Italic" if "Institutional-Italic" in pdfmetrics.getRegisteredFontNames() else "Institutional", fontSize=7.2, leading=10, alignment=TA_CENTER, textColor=MUTED, spaceBefore=5, spaceAfter=7),
    "cover_kicker": ParagraphStyle("CoverKicker", fontName="Institutional-Bold", fontSize=9, leading=14, textColor=colors.HexColor("#d7bd6b"), tracking=1.5, alignment=TA_CENTER),
    "cover_title": ParagraphStyle("CoverTitle", fontName="Institutional-Bold", fontSize=27, leading=33, textColor=colors.HexColor("#f5f3ec"), alignment=TA_CENTER, spaceBefore=15, spaceAfter=12),
    "cover_sub": ParagraphStyle("CoverSub", fontName="Institutional", fontSize=11, leading=17, textColor=colors.HexColor("#d3d4cf"), alignment=TA_CENTER, spaceAfter=20),
    "cover_owner": ParagraphStyle("CoverOwner", fontName="Institutional-Bold", fontSize=12, leading=18, textColor=colors.HexColor("#ead487"), alignment=TA_CENTER, spaceBefore=7),
    "toc": ParagraphStyle("TOC", fontName="Institutional", fontSize=9.2, leading=15, textColor=GRAPHITE, leftIndent=8, spaceAfter=2),
}


class CoverGap(Flowable):
    def __init__(self, height: float):
        super().__init__()
        self.height = height

    def draw(self) -> None:
        pass


class ProjectDocument(BaseDocTemplate):
    def __init__(self, filename: Path, document_no: str, short_title: str):
        self.document_no = document_no
        self.short_title = short_title
        super().__init__(str(filename), pagesize=A4, rightMargin=20 * mm, leftMargin=20 * mm, topMargin=26 * mm, bottomMargin=20 * mm, title=short_title, author=AUTHOR, subject="PHP-SHIELD RDC — document institutionnel")
        frame = Frame(self.leftMargin, self.bottomMargin, PAGE_W - self.leftMargin - self.rightMargin, PAGE_H - self.topMargin - self.bottomMargin, id="main", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        self.addPageTemplates([PageTemplate(id="all", frames=frame, onPage=self.decorate)])

    def decorate(self, canvas, doc):
        canvas.saveState()
        if doc.page == 1:
            canvas.setFillColor(INK)
            canvas.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
            canvas.setFillColor(GRAPHITE)
            canvas.circle(PAGE_W * .5, PAGE_H * .48, 184, stroke=0, fill=1)
            canvas.setStrokeColor(colors.HexColor("#806c31"))
            canvas.setLineWidth(.75)
            canvas.circle(PAGE_W * .5, PAGE_H * .48, 185, stroke=1, fill=0)
            canvas.setStrokeColor(GOLD)
            canvas.setLineWidth(2)
            canvas.line(38 * mm, 37 * mm, PAGE_W - 38 * mm, 37 * mm)
            canvas.setFont("Institutional", 7)
            canvas.setFillColor(colors.HexColor("#aeb1ae"))
            canvas.drawCentredString(PAGE_W / 2, 27 * mm, f"{self.short_title.upper()} · VERSION PUBLIQUE · {TODAY.strftime('%d/%m/%Y')}")
            canvas.setFont("Institutional-Bold", 7)
            canvas.setFillColor(colors.HexColor("#d8c176"))
            canvas.drawCentredString(PAGE_W / 2, 21 * mm, f"{AUTHOR} · FONDATEUR ULTIME ET PROPRIÉTAIRE DU PROJET")
        else:
            canvas.setFillColor(PAPER)
            canvas.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
            canvas.setFillAlpha(.065)
            canvas.drawImage(str(EMBLEM), PAGE_W / 2 - 115, PAGE_H / 2 - 115, width=230, height=230, preserveAspectRatio=True, mask="auto")
            canvas.setFillAlpha(1)
            canvas.drawImage(str(EMBLEM), 20 * mm, PAGE_H - 17 * mm, width=9 * mm, height=9 * mm, preserveAspectRatio=True, mask="auto")
            canvas.setFont("Institutional-Bold", 7)
            canvas.setFillColor(INK)
            canvas.drawString(32 * mm, PAGE_H - 13 * mm, "RÉPUBLIQUE DÉMOCRATIQUE DU CONGO")
            canvas.setFont("Institutional", 6.7)
            canvas.setFillColor(MUTED)
            canvas.drawString(32 * mm, PAGE_H - 17 * mm, "PHP-SHIELD RDC · " + self.short_title.upper())
            canvas.setFont("Institutional-Bold", 6.5)
            canvas.setFillColor(GOLD)
            canvas.drawRightString(PAGE_W - 20 * mm, PAGE_H - 15 * mm, f"DOCUMENT {self.document_no}")
            canvas.setStrokeColor(LINE)
            canvas.setLineWidth(.55)
            canvas.line(20 * mm, PAGE_H - 21 * mm, PAGE_W - 20 * mm, PAGE_H - 21 * mm)
            canvas.line(20 * mm, 15 * mm, PAGE_W - 20 * mm, 15 * mm)
            canvas.setFont("Institutional", 6.4)
            canvas.setFillColor(MUTED)
            canvas.drawString(20 * mm, 10.5 * mm, "ÉDITION PUBLIQUE · " + TODAY.strftime("%d/%m/%Y"))
            canvas.setFont("Institutional-Bold", 6.4)
            canvas.setFillColor(STEEL)
            canvas.drawCentredString(PAGE_W / 2, 10.5 * mm, AUTHOR)
            canvas.setFont("Institutional-Bold", 7)
            canvas.setFillColor(INK)
            canvas.drawRightString(PAGE_W - 20 * mm, 10.5 * mm, str(doc.page))
        canvas.restoreState()


def P(text: str, style: str = "body") -> Paragraph:
    return Paragraph(text, STYLES[style])


def bullets(items: list[str]) -> list[Paragraph]:
    return [Paragraph(f"<font color='{GOLD.hexval()}'>●</font>  {item}", STYLES["bullet"]) for item in items]


def heading(title: str, level: str = "h1") -> list[Flowable]:
    return [P(title, level), Table([['']], colWidths=[PAGE_W - 40 * mm], rowHeights=[1], style=TableStyle([("BACKGROUND", (0, 0), (-1, -1), GOLD)])), Spacer(1, 7)]


def note(title: str, body: str, tint=PALE_GOLD, accent=GOLD) -> Table:
    inner = [[P(f"<b>{title}</b><br/>{body}", "small")]]
    return Table(inner, colWidths=[PAGE_W - 50 * mm], style=TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), tint), ("BOX", (0, 0), (-1, -1), .5, LINE),
        ("LINEBEFORE", (0, 0), (0, -1), 2, accent), ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10), ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))


def data_table(rows: list[list[str]], widths: list[float], header=True) -> Table:
    converted = []
    for r, row in enumerate(rows):
        style = "tablehead" if header and r == 0 else "table"
        converted.append([P(str(c), style) for c in row])
    table = Table(converted, colWidths=widths, repeatRows=1 if header else 0, hAlign="LEFT")
    rules = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"), ("GRID", (0, 0), (-1, -1), .35, LINE),
        ("LEFTPADDING", (0, 0), (-1, -1), 7), ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]
    if header:
        rules.append(("BACKGROUND", (0, 0), (-1, 0), GRAPHITE))
    for row in range(1 if header else 0, len(rows)):
        rules.append(("BACKGROUND", (0, row), (-1, row), colors.white if row % 2 else colors.HexColor("#efede5")))
    table.setStyle(TableStyle(rules))
    return table


def cover(story: list[Flowable], no: str, label: str, title: str, subtitle: str, edition: str) -> None:
    story.extend([CoverGap(17 * mm), P("RÉPUBLIQUE DÉMOCRATIQUE DU CONGO", "cover_kicker"), Spacer(1, 20 * mm)])
    logo = Image(str(EMBLEM), width=43 * mm, height=43 * mm)
    seal = Table([[logo]], colWidths=[49 * mm], rowHeights=[49 * mm], hAlign="CENTER", style=TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f4f1e7")), ("BOX", (0, 0), (-1, -1), 1, GOLD),
        ("ROUNDEDCORNERS", [8, 8, 8, 8]), ("ALIGN", (0, 0), (-1, -1), "CENTER"), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 2), ("RIGHTPADDING", (0, 0), (-1, -1), 2),
    ]))
    story.extend([seal, Spacer(1, 17 * mm), P(f"DOCUMENT {no} · {label}", "cover_kicker"), P(title, "cover_title"), P(subtitle, "cover_sub"), Spacer(1, 8 * mm), P("Fondateur ultime &amp; propriétaire du projet", "cover_kicker"), P(AUTHOR, "cover_owner"), Spacer(1, 6 * mm), P(edition, "cover_sub"), PageBreak()])


def section_intro(story: list[Flowable], title: str, deck: str):
    story.extend([P("PHP-SHIELD RDC · DOCUMENTATION INSTITUTIONNELLE", "eyebrow"), P(title, "title"), P(deck, "subtitle")])


def add_project_document(path: Path) -> None:
    story: list[Flowable] = []
    cover(story, "01", "PRÉSENTATION DU PROJET", "PHP-SHIELD RDC", "Plateforme de gouvernance de la sécurité applicative PHP et de la résilience cybernétique.", "VISION · ARCHITECTURE · SÉCURITÉ · FEUILLE DE ROUTE · NOVEMBRE 2026")
    section_intro(story, "Présentation du projet", "Une base de décision claire pour comprendre l’ambition, l’architecture proposée et le niveau de maturité actuel.")
    story.extend([note("Statut du document", "Dossier de présentation d’un projet technique proposé pour évaluation. Il ne constitue ni une décision d’achat, ni une homologation, ni une accréditation et ne revendique pas un déploiement institutionnel."), Spacer(1, 11), P("Fiche d’identité", "h2"), data_table([
        ["Élément", "Description"], ["Nom", "PHP-SHIELD RDC — plateforme de gestion de la sécurité des applications PHP."],
        ["Porteur du projet", f"{AUTHOR}, fondateur ultime et propriétaire de l’application."],
        ["Public visé", "Équipes techniques, administrateurs et responsables de gouvernance habilités."],
        ["Périmètre cible", "Actifs applicatifs et environnements explicitement autorisés par leurs responsables."],
        ["Édition", "Dossier public de présentation — 5 novembre 2026."],
    ], [38 * mm, 132 * mm]), Spacer(1, 10), P("Sommaire", "h2")])
    toc = ["01  Synthèse exécutive", "02  Contexte et objectifs", "03  Périmètre fonctionnel", "04  Architecture et flux", "05  Données et contrôles de sécurité", "06  Maturité et feuille de route", "07  Gouvernance et limites", "08  Préparation d’un pilote", "09  Indicateurs de réussite", "10  Glossaire"]
    story.extend([P(x, "toc") for x in toc])
    story.append(PageBreak())

    story.extend(heading("01 · Synthèse exécutive"))
    story.extend([P("PHP-SHIELD RDC vise à fournir un espace de travail centralisé pour inventorier les applications PHP autorisées, comprendre leur environnement technique, organiser l’analyse des dépendances et suivre la correction de constats de sécurité. L’objectif de gestion est concret : lorsqu’une vulnérabilité importante est annoncée, une équipe doit pouvoir repérer rapidement les actifs potentiellement concernés, identifier les interlocuteurs et suivre les actions correctives."),
        P("Le dépôt contient aujourd’hui une interface React/Vite, une API FastAPI de fondation, un modèle de données SQLAlchemy, une première migration Alembic, une base PostgreSQL prévue par Docker Compose et un parcours d’aperçu public. Le site GitHub Pages ne sert que le frontend statique. Les fonctions métier de registre et d’audit sont encore à construire; la démonstration ne doit donc pas être interprétée comme une plateforme de scan en production."),
        note("Positionnement", "Le projet est une proposition technique portée par le fondateur. Toute adoption, connexion à un système réel, désignation d’autorité ou mise en production nécessite une évaluation et une validation explicites par les organismes compétents.", colors.HexColor("#f1e7e3"), RED), Spacer(1, 8), P("Résultats attendus à terme", "h2"), *bullets([
            "Constituer un référentiel maintenu des applications, serveurs, environnements et responsables.",
            "Réduire le délai d’identification des applications touchées par une alerte de sécurité.",
            "Structurer la priorisation du risque et l’affectation des mesures correctives.",
            "Produire des synthèses traçables à partir de données vérifiées et datées.",
            "Déployer des contrôles uniquement sur des périmètres explicitement autorisés.",
        ])])

    story.extend(heading("02 · Contexte et objectifs"))
    story.extend([P("Les équipes qui gèrent des applications PHP ont besoin d’une vue fiable des versions de runtime, dépendances, environnements d’hébergement, résultats d’audit et mesures de remédiation. Un inventaire incomplet transforme une alerte de vulnérabilité en enquête manuelle, parfois urgente. PHP-SHIELD propose de relier ces informations à une gouvernance des accès et à un historique d’opérations."),
        P("Objectifs produit", "h2"), *bullets([
            "Inventorier les applications et leur contexte d’hébergement, avec un propriétaire métier et technique.",
            "Centraliser les versions PHP, SAPIs, extensions et métadonnées utiles aux vérifications autorisées.",
            "Préparer l’audit des dépendances Composer et l’analyse statique de code PHP.",
            "Classer les constats avec sévérité, justification, preuve, périmètre et état de traitement.",
            "Relier les constats aux responsables, échéances, mesures et vérifications de clôture.",
            "Proposer des exports lisibles par les équipes techniques et les décideurs.",
        ]), P("Principes de conception", "h2"), P("Privilégier des données vérifiables et des états vides explicites; séparer démonstration et données opérationnelles; appliquer le moindre privilège; rendre les audits déclenchés, autorisés et journalisables; documenter les limites et les dépendances."), PageBreak()])

    story.extend(heading("03 · Périmètre fonctionnel"))
    story.append(P("Le tableau distingue les éléments d’interface actuellement visibles de capacités encore prévues. Un écran ou un bouton ne constitue pas à lui seul la preuve qu’un moteur métier ou un stockage opérationnel existe."))
    story.append(data_table([
        ["Domaine", "État constaté", "Capacité cible"],
        ["Connexion", "Page de connexion, aperçu démo et API d’authentification de fondation.", "Comptes nominatifs, habilitations, gestion d’échec et contrôles adaptés à l’environnement."],
        ["Vue d’ensemble", "Shell visuel; données vides via API et jeu explicitement simulé en démo.", "Indicateurs fondés sur l’inventaire et les événements persistés."],
        ["Applications", "Vue de module et états d’attente.", "Registre versionné, propriétaire, criticité, cycle de vie et liens d’environnement."],
        ["Infrastructure", "Vue de module et états d’attente.", "Inventaire de serveurs, environnements et relations avec les applications."],
        ["Audits PHP / web", "Écrans préparatoires; aucun scan lancé par l’aperçu.", "Moteurs et adaptateurs isolés, périmètres autorisés, résultats reproductibles."],
        ["Constats & remédiation", "Vues préparatoires; absence de résultats réels dans le dépôt actuel.", "Enregistrement de preuves, priorisation, affectation, suivi et clôture."],
        ["Rapports", "Exports PDF et Excel du tableau de posture disponible.", "Rapports gouvernés, historisés, vérifiés et adaptés aux rôles."],
        ["PWA / interface", "Interface installable, thèmes, recherche et navigation adaptative.", "Amélioration progressive, tests d’accessibilité et cache hors ligne maîtrisé."],
    ], [28 * mm, 65 * mm, 77 * mm]))
    story.extend([Spacer(1, 8), note("Données de démonstration", "Les chiffres affichés en mode aperçu sont illustratifs et signalés comme simulés. Ils ne décrivent pas des serveurs, applications, vulnérabilités ou opérations réels. L’API de fondation retourne un état vide pour le tableau de bord.", colors.HexColor("#f1e7e3"), RED), PageBreak()])

    story.extend(heading("04 · Architecture et flux"))
    story.append(P("L’architecture sépare l’interface statique, l’API et le stockage. Cette séparation permet d’héberger l’aperçu public indépendamment du service privé et de ne pas exposer la base de données dans GitHub Pages."))
    nodes = [
        [P("<b>Interface web</b><br/>React · TypeScript · Vite<br/>PWA · rapports client", "table"), P("<b>API applicative</b><br/>FastAPI · endpoints REST<br/>Session HTTP-only", "table"), P("<b>Stockage relationnel</b><br/>PostgreSQL<br/>SQLAlchemy · Alembic", "table")],
        [P("<b>GitHub Pages</b><br/>Aperçu frontend uniquement", "table"), P("<b>Service privé</b><br/>Authentification et API<br/>à déployer séparément", "table"), P("<b>Schéma initial</b><br/>Utilisateurs · rôles<br/>institutions · services", "table")],
    ]
    arch = Table(nodes, colWidths=[56 * mm, 56 * mm, 56 * mm], rowHeights=[24 * mm, 22 * mm], hAlign="CENTER")
    arch.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e9e4d5")), ("BACKGROUND", (0, 1), (-1, 1), colors.white), ("GRID", (0, 0), (-1, -1), .5, LINE), ("ALIGN", (0, 0), (-1, -1), "CENTER"), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("LEFTPADDING", (0, 0), (-1, -1), 7), ("RIGHTPADDING", (0, 0), (-1, -1), 7)]))
    story.extend([arch, P("Vue logique de référence — les moteurs d’audit et la persistance métier ne sont pas encore intégrés.", "caption"), P("Composants du dépôt", "h2"), data_table([
        ["Couche", "Technologies et rôle"],
        ["Frontend", "React, TypeScript et Vite; thème clair/sombre, navigation par modules, connexion, aperçu et exports PDF/XLSX."],
        ["Backend", "FastAPI; santé, authentification de fondation, consultation de session, déconnexion et réponse dashboard vide."],
        ["Identité", "SQLAlchemy définit utilisateurs actifs, empreinte de mot de passe, rôles, institutions et départements."],
        ["Migrations", "Alembic fournit la migration initiale des tables d’identité et d’organisation."],
        ["Exécution", "Docker Compose décrit les services de développement; secrets et paramètres réels restent à configurer."],
        ["Publication", "GitHub Actions construit l’interface et publie l’aperçu Pages; cela ne déploie pas l’API ni PostgreSQL."],
    ], [34 * mm, 136 * mm]), Spacer(1, 9), note("Limite de déploiement", "GitHub Pages ne peut pas exécuter le backend FastAPI ni joindre la base PostgreSQL. L’URL publique sert un aperçu statique. Un environnement institutionnel exigerait une API dédiée, des secrets protégés, un domaine contrôlé et une validation de sécurité."), PageBreak()])

    story.extend(heading("05 · Données et contrôles de sécurité"))
    story.extend([P("La base relationnelle commence par les entités d’identité et d’organisation. Les objets applicatifs métier, les résultats d’audit, les vulnérabilités et les actions de remédiation ne sont pas encore modélisés dans cette version."), P("Contrôles déjà présents dans la fondation", "h2"), *bullets([
        "Les mots de passe sont vérifiés par empreinte côté serveur; le flux d’administration initial est une commande de bootstrap interactive.",
        "Les sessions utilisent un cookie signé HTTP-only avec durée de huit heures et SameSite=Lax; l’attribut Secure est activé hors développement.",
        "L’API autorise les origines CORS explicitement déclarées et exige un secret d’au moins 32 caractères hors développement.",
        "Aucune inscription publique n’est prévue; la création initiale d’un administrateur est manuelle côté serveur.",
        "Les journaux, restrictions d’accès métier, MFA et limite distribuée des tentatives demeurent à finaliser avant usage réel.",
    ]), P("Socle de données", "h2"), data_table([
        ["Entité initiale", "Rôle"], ["Utilisateur", "Adresse unique, empreinte de mot de passe, état actif et horodatages."],
        ["Rôle", "Nom de rôle et relation plusieurs-à-plusieurs avec les comptes."],
        ["Institution", "Organisation de rattachement, avec nom unique."],
        ["Département", "Service lié à une institution; suppression de l’institution protégée par contrainte."],
    ], [42 * mm, 128 * mm]), Spacer(1, 8), note("Règle opérationnelle", "Tout contrôle actif doit viser un actif confié ou explicitement autorisé, un périmètre limité, une fenêtre approuvée, un propriétaire averti et un plan de retour arrière. L’aperçu public ne doit jamais être utilisé comme preuve d’un scan réel.", colors.HexColor("#f1e7e3"), RED), PageBreak()])

    story.extend(heading("06 · Maturité et feuille de route"))
    story.append(P("Les phases suivantes donnent un ordre de réalisation proposé. Une étape est considérée prête seulement lorsqu’elle a une logique vérifiable, des contrôles d’accès, des validations, un comportement d’erreur documenté et des tests appropriés."))
    story.append(data_table([
        ["Phase", "Contenu envisagé", "Critère de sortie"],
        ["1 · Fondation", "Structure, interface, identité visuelle, API, schéma initial, authentification de base, migrations, conteneurs et CI.", "Installation reproductible; migration depuis une base vide; tests des parcours et des erreurs."],
        ["2 · Cœur PHP-SHIELD", "Registre, inventaire, versions PHP, dépendances Composer, premiers constats et priorisation.", "Données persistées; permissions; preuves; tests métier; aucun résultat non vérifié."],
        ["3 · Analyses avancées", "Adaptateurs Semgrep/PHPStan/Psalm/ZAP selon les besoins; exécutions isolées; suivi de remédiation.", "Autorisation vérifiée; exécution contenue; traçabilité; gestion des délais et résultats."],
        ["4 · Gouvernance", "Rapports, exports, audit trail, alertes d’avis de sécurité et règles de conservation.", "Données sources réconciliées; attribution; historiques et contrôle de publication."],
        ["5 · Préparation pilote", "Essais intégrés, sécurité, sauvegarde/restauration, procédures et réception.", "Validation technique, procédures approuvées et plan de continuité testé."],
    ], [27 * mm, 78 * mm, 65 * mm]))
    story.extend([Spacer(1, 9), P("Les outils d’analyse sont des pistes d’intégration, pas des capacités actuellement déployées. Leur sélection devra être compatible avec les contraintes d’exploitation, de licence, de confidentialité et de sécurité de l’environnement retenu."), P("Gestion de version", "h2"), P("Le dépôt est la source du code. Les secrets ne doivent pas être versionnés. Les modifications doivent passer par des revues, des contrôles automatisés, un suivi des migrations et une procédure de publication. Un succès GitHub Pages atteste de la publication du frontend, pas d’une mise en service opérationnelle de l’ensemble du produit."), PageBreak()])

    story.extend(heading("07 · Gouvernance, risques et limites"))
    story.extend([P("La plateforme vise un contexte institutionnel sensible. Il faut éviter toute ambiguïté entre proposition, démonstration, pilote autorisé et système accrédité. Les données opérationnelles ne doivent entrer qu’après désignation des responsables, définition de la classification et validation du dispositif d’hébergement."), data_table([
        ["Risque", "Réponse attendue"],
        ["Maturité surestimée", "Étiqueter clairement les écrans en construction, les données démo et les intégrations planifiées."],
        ["Accès inadapté", "Finaliser les rôles et permissions au niveau métier, MFA selon politique, révocation et journalisation."],
        ["Audit hors périmètre", "Exiger une autorisation documentée, une cible et une fenêtre; isoler le moteur; limiter les requêtes."],
        ["Exposition de données", "Chiffrement en transit et au repos, secrets gérés, minimisation, sauvegardes protégées et règles de rétention."],
        ["Dépendance à un service", "Surveiller les composants, corriger les vulnérabilités, documenter versions et procédure de mise à jour."],
        ["Rapport trompeur", "Date, origine, version, périmètre, hypothèses et statut de validation affichés sur chaque export."],
    ], [42 * mm, 128 * mm]), Spacer(1, 9), P("Périmètre de responsabilité", "h2"), P("Les propriétaires des actifs autorisent les contrôles et valident les constats. Les administrateurs gèrent l’environnement et les comptes. Les auditeurs déclenchent les contrôles permis et documentent les preuves. Les décideurs approuvent les priorités et les ressources. Le porteur du projet fournit le produit à évaluer; les institutions compétentes conservent la décision d’adoption, d’hébergement et d’accréditation."), note("Aucune approbation revendiquée", "Les mentions DRC, DANTIC et Présidence décrivent le contexte de conception visé. Elles ne signifient pas que le produit est une plateforme officielle ou validée par ces institutions.", colors.HexColor("#f1e7e3"), RED), PageBreak()])

    story.extend(heading("08 · Préparation d’un pilote"))
    story.extend([P("Avant un pilote, réunir le propriétaire métier, le responsable technique, l’administrateur d’infrastructure, le responsable sécurité, le référent protection des données et les personnes chargées de l’exploitation. Le pilote doit être limité à quelques actifs explicitement autorisés et à des données de test maîtrisées."), P("Préparation technique", "h2"), *bullets([
        "Choisir un hébergement privé pour API et base de données; isoler développement, test et production.",
        "Configurer HTTPS, secrets uniques et rotation, origines web, sauvegarde chiffrée et surveillance des erreurs.",
        "Définir rôles, droits sur les actifs, processus d’arrivée/départ et revue périodique des accès.",
        "Établir les règles de collecte, classification, durée de conservation et accès aux preuves.",
        "Définir autorisations de scan, limites de débit, plages horaires, coordonnées d’urgence et procédure d’arrêt.",
        "Valider une restauration de sauvegarde et la reprise après indisponibilité de l’API ou de la base.",
        "Tester les migrations depuis une base vide puis depuis une version antérieure réaliste.",
    ]), P("Décisions à obtenir avant le pilote", "h2"), data_table([
        ["Décision", "Évidence attendue"], ["Autorisation de périmètre", "Liste des applications, environnements, propriétaires, plages et opérations permises."],
        ["Gouvernance des données", "Classification, responsabilités, conservation, localisation et règles d’accès."],
        ["Modèle d’exploitation", "Hébergement, supervision, sauvegardes, mises à jour, astreinte et plan d’incident."],
        ["Réception", "Tests signés, seuils de qualité, limites reconnues et mécanisme de désactivation."],
    ], [48 * mm, 122 * mm]), PageBreak()])

    story.extend(heading("09 · Indicateurs de réussite"))
    story.append(P("Les indicateurs devront être calculés à partir d’enregistrements horodatés et contrôlés; les valeurs d’exemple de la démonstration ne sont pas des résultats de référence."))
    story.append(data_table([
        ["Indicateur", "Définition proposée", "Usage"],
        ["Couverture d’inventaire", "Actifs connus et validés / périmètre déclaré.", "Identifier les angles morts et les écarts de registre."],
        ["Délai d’affectation", "Temps entre un constat validé et l’assignation d’un responsable.", "Mesurer la réactivité de gouvernance."],
        ["Délai de correction", "Temps de la validation au correctif confirmé, ventilé par sévérité.", "Prioriser les risques et améliorer la coordination."],
        ["Âge des constats", "Nombre et durée des constats encore ouverts par niveau.", "Repérer les retards et les besoins d’escalade."],
        ["Taux de vérification", "Actions corrigées dont le résultat est contrôlé après changement.", "Éviter une clôture uniquement déclarative."],
        ["Qualité des données", "Part des actifs avec responsable, version et date de révision connus.", "Évaluer la fiabilité de l’inventaire."],
    ], [37 * mm, 79 * mm, 54 * mm]))
    story.extend([Spacer(1, 9), P("Aucun seuil universel ne doit être inventé. Les responsables métier et sécurité fixeront les objectifs selon le risque, les contraintes de service et la politique en vigueur."), P("Conclusion", "h2"), P("PHP-SHIELD RDC propose une trajectoire cohérente pour structurer la sécurité des applications PHP, à condition de transformer le socle actuel en produit gouverné, éprouvé et exploité. La priorité suivante est d’achever le registre et son modèle de permissions, puis de connecter un premier parcours de données contrôlé, avec migrations et tests d’intégration."), PageBreak()])

    story.extend(heading("10 · Glossaire"))
    story.append(data_table([
        ["Terme", "Définition"], ["Actif", "Application, service ou infrastructure inscrite au périmètre de gestion."],
        ["Audit autorisé", "Analyse lancée avec l’accord du propriétaire, sur un périmètre et une fenêtre définis."],
        ["Constat", "Observation de sécurité appuyée par une preuve et un contexte de validation."],
        ["CVE", "Identifiant public de référence d’une vulnérabilité divulguée."],
        ["Composer", "Gestionnaire de dépendances PHP et manifeste du graphe de composants."],
        ["MFA", "Authentification multifacteur; son activation n’est pas encore intégrée à la fondation décrite."],
        ["Migration", "Évolution versionnée et reproductible du schéma de base de données."],
        ["PWA", "Application web progressive installable; elle n’embarque pas l’API privée."],
        ["SAST", "Analyse statique du code source sans exécution de l’application cible."],
        ["SCA", "Analyse des composants et dépendances logiciels."],
        ["Remédiation", "Action documentée visant à corriger ou réduire un risque confirmé."],
        ["Périmètre", "Ensemble explicite des actifs, opérations et limites autorisés pour une analyse."],
    ], [36 * mm, 134 * mm]))
    story.extend([Spacer(1, 13), note("Propriété du projet", f"PHP-SHIELD RDC est présenté dans ce dossier comme un projet fondé et détenu par {AUTHOR}. Toute décision d’adoption ou de déploiement institutionnel reste soumise à l’évaluation des autorités compétentes.", colors.HexColor("#e8e3d2"), GOLD)])
    doc = ProjectDocument(path, "01", "Présentation du projet")
    doc.build(story)


def add_screenshot(story: list[Flowable], filename: str, caption: str):
    image_path = SCREENSHOTS / filename
    if not image_path.exists():
        raise FileNotFoundError(f"The illustrated user manual requires a real application screenshot at {image_path}")
    im = Image(str(image_path))
    max_width = PAGE_W - 44 * mm
    max_height = 106 * mm
    scale = min(max_width / im.imageWidth, max_height / im.imageHeight)
    im.drawWidth = im.imageWidth * scale
    im.drawHeight = im.imageHeight * scale
    frame = Table([[im]], colWidths=[max_width], hAlign="CENTER", style=TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.white), ("BOX", (0, 0), (-1, -1), .7, LINE),
        ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.extend([frame, P(caption, "caption")])


def add_manual_document(path: Path, *, screenshots: bool) -> None:
    story: list[Flowable] = []

    def figure(number: int, filename: str, caption: str, steps: list[tuple[str, str]]) -> None:
        if screenshots:
            add_screenshot(story, filename, f"Figure {number} · {caption}")
            return
        step_width = 170 * mm / len(steps)
        flow = Table(
            [[P(f"<b>{index + 1:02d} · {label}</b><br/>{description}", "table") for index, (label, description) in enumerate(steps)]],
            colWidths=[step_width] * len(steps),
            style=TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), PALE_GOLD),
                ("BOX", (0, 0), (-1, -1), .5, LINE),
                ("INNERGRID", (0, 0), (-1, -1), .5, LINE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LINEABOVE", (0, 0), (-1, 0), 1.5, GOLD),
                ("LEFTPADDING", (0, 0), (-1, -1), 9),
                ("RIGHTPADDING", (0, 0), (-1, -1), 9),
                ("TOPPADDING", (0, 0), (-1, -1), 9),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
            ]),
        )
        story.append(KeepTogether([flow, P(f"Schéma {number} · {caption}", "caption")]))

    cover(story, "02", "MANUEL D’UTILISATION", "Guide utilisateur", "Parcours détaillé de l’espace PHP-SHIELD RDC, de la connexion aux exports.", "GUIDE PRATIQUE · VERSION PUBLIQUE · NOVEMBRE 2026")
    section_intro(story, "Manuel d’utilisation", "Ce guide accompagne l’utilisateur dans l’aperçu public actuel et explique les limites à connaître avant un environnement connecté.")
    edition = "Les captures proviennent de l’application publiée." if screenshots else "Les schémas de parcours reprennent les commandes de l’interface."
    story.extend([note("Édition publique", f"{edition} Les valeurs de l’aperçu sont simulées. Ouvrez <link href='https://propheticpowerfulman.github.io/php-shield-DRC/' color='#61501d'><u>PHP-SHIELD RDC</u></link> pour suivre les étapes dans l’application."), P("Repères rapides", "h2"), data_table([
        ["Vous voulez…", "Où aller"], ["Découvrir l’application sans compte serveur", "Depuis l’écran de connexion, choisir « Ouvrir l’aperçu public »."],
        ["Tester la navigation", "Utiliser le menu latéral ou rechercher un module dans l’en-tête."],
        ["Générer un rapport", "Ouvrir Rapports, contrôler le badge de source, puis choisir PDF ou Excel."],
        ["Installer l’application", "Choisir Installer la PWA et suivre les étapes du navigateur."],
        ["Obtenir un accès institutionnel", "Contacter l’administrateur; aucun compte public ne peut être créé depuis l’interface."],
    ], [58 * mm, 112 * mm]), Spacer(1, 10), P("Sommaire", "h2"), *[P(x, "toc") for x in ["01  Préparer l’accès", "02  Lire l’écran de connexion", "03  Ouvrir l’aperçu de démonstration", "04  Comprendre le tableau de bord", "05  Naviguer dans les modules", "06  Utiliser la recherche", "07  Produire un rapport PDF ou Excel", "08  Personnaliser et installer la PWA", "09  Affichage mobile et tablette", "10  Dépannage et sécurité", "11  Foire aux questions"]], PageBreak()])

    story.extend(heading("01 · Préparer l’accès"))
    story.extend([P("L’adresse publique de GitHub Pages héberge le frontend PHP-SHIELD RDC. Cette publication permet d’examiner la navigation et l’expérience de démonstration; elle n’exécute ni le backend FastAPI ni la base de données."), P("Pour parcourir l’aperçu", "h2"), *bullets([
        "Utiliser un navigateur récent avec JavaScript activé et une connexion HTTPS.",
        "Aucun compte réel n’est requis pour l’aperçu public.",
        "Les deux documents de référence se téléchargent depuis le bloc « Documentation du projet » du login.",
        "Pour un environnement de développement connecté, consulter le README et l’administrateur de l’API.",
    ]), P("Accès de démonstration", "h2"), data_table([
        ["Méthode", "Instructions"], ["Par bouton", "Sur l’écran de connexion, choisir « Ouvrir l’aperçu public ». C’est la méthode la plus simple."],
        ["Par identifiants affichés", "Identifiant : demo@php-shield.cd · Mot de passe : RDC-DEMO-2026. Ces valeurs ouvrent uniquement le mode aperçu de cette édition publique."],
        ["Données", "Mode lecture seule; aucun scan n’est exécuté et aucune donnée présentée ne décrit un environnement réel."],
    ], [47 * mm, 123 * mm]), Spacer(1, 8), note("Ne pas réutiliser", "Les identifiants ci-dessus ne sont pas des identifiants institutionnels ni un accès au backend privé. Ne transmettez pas de secrets réels à la page de démonstration.", colors.HexColor("#f1e7e3"), RED), PageBreak()])

    story.extend(heading("02 · Lire l’écran de connexion"))
    story.append(P("L’écran d’entrée présente la marque et le contexte de la plateforme, indique l’état du service d’authentification, propose un formulaire de connexion et rend visible l’accès en lecture seule. Depuis cette page, le mode clair/sombre, l’installation PWA et les deux documents du projet sont accessibles."))
    figure(1, "01-login.png", "Accéder à PHP-SHIELD RDC et à sa documentation.", [
        ("Connexion", "Saisir les identifiants si le service est connecté."),
        ("Aperçu public", "Ouvrir une session de démonstration depuis l’accueil."),
        ("Documentation", "Télécharger la présentation ou le manuel en PDF."),
    ])
    story.extend([P("Se connecter", "h2"), *bullets([
        "Saisir une adresse professionnelle dans le premier champ et le mot de passe fourni par l’administrateur dans le second.",
        "Utiliser l’icône en forme d’œil pour vérifier la saisie si nécessaire; le bouton « Accès oublié ? » indique le canal actuel de réinitialisation.",
        "Cliquer sur « Ouvrir ma session ». Une erreur d’authentification est affichée dans la page; aucun compte ne peut s’inscrire lui-même.",
        "Pour l’aperçu public, préférer le bouton direct plutôt que d’essayer des comptes réels.",
    ]), P("Télécharger les documents", "h2"), P("Le bloc « Documentation du projet » est accessible depuis l’écran de connexion. « Présentation du projet » expose la vision, l’architecture, les principes de sécurité et la feuille de route. « Manuel d’utilisation » détaille les parcours à suivre dans l’application."), PageBreak()])

    story.extend(heading("03 · Ouvrir l’aperçu de démonstration"))
    story.extend([P("Après activation de « Ouvrir l’aperçu public », l’interface charge le tableau de bord en mode lecture seule. Le bandeau « Jeu de démonstration · données simulées » reste affiché pour distinguer les valeurs d’exemple de données opérationnelles."), P("Ce que l’aperçu permet", "h2"), *bullets([
        "Parcourir les vues du menu et la présentation des différents espaces.",
        "Observer le rendu des indicateurs et des graphiques d’illustration.",
        "Tester le thème, la recherche et les exports PDF/Excel de posture.",
        "Examiner la navigation responsive sur ordinateur, tablette et téléphone.",
    ]), P("Ce qu’il ne fait pas", "h2"), *bullets([
        "Aucun inventaire réel, audit de code, scan web ou contrôle d’infrastructure n’est lancé.",
        "Les vues Applications, Infrastructure, Vulnérabilités, Audits et Remédiation sont des espaces préparatoires; elles n’enregistrent pas encore les objets métier.",
        "Le site Pages ne possède pas de session serveur persistante; l’aperçu est local au navigateur.",
        "Les rapports de posture générés en mode aperçu reprennent des valeurs de démonstration et portent une mention correspondante.",
    ]), Spacer(1, 8), note("Interpréter les graphiques", "Les métriques affichées après entrée en mode démo servent à expliquer les visualisations. Elles ne constituent pas une mesure de maturité, un résultat de scan ou une statistique institutionnelle."), PageBreak()])

    story.extend(heading("04 · Comprendre le tableau de bord"))
    story.append(P("L’en-tête fixe identifie l’espace courant et conserve les principaux outils. Le bandeau annonce le mode de données. Les indicateurs synthétisent les exemples affichés, puis les graphiques montrent l’évolution simulée des audits et la répartition des constats."))
    figure(2, "02-overview.png", "Ordre de lecture de la vue d’ensemble.", [
        ("Source", "Repérer le bandeau de démonstration."),
        ("Indicateurs", "Lire les volumes et les taux de couverture."),
        ("Graphiques", "Comparer l’activité et la sévérité des constats."),
    ])
    story.extend([P("Lire les indicateurs", "h2"), data_table([
        ["Zone", "Interprétation"], ["Applications / Serveurs", "Comptages d’exemple pendant la démo; n’indiquent pas un inventaire réel."],
        ["Couverture d’audit", "Rapport entre les applications auditées et le nombre d’applications illustratives affichées."],
        ["Corrections clôturées", "Ratio présenté avec la série d’exemple de corrections ouvertes et résolues."],
        ["Vulnérabilités ouvertes", "Distribution simulée par classe de sévérité; consulter la légende et le bandeau de source."],
        ["Évolution des audits", "Courbe d’illustration sur six mois, explicitement étiquetée comme série de démonstration."],
    ], [43 * mm, 127 * mm]), Spacer(1, 8), P("Lorsque l’API est raccordée et retourne des données, l’application doit afficher des états distincts. La version actuelle de l’API renvoie un tableau de bord vide et un message indiquant qu’aucune donnée n’est inventoriée."), PageBreak()])

    story.extend(heading("05 · Naviguer dans les modules"))
    story.append(P("Le menu latéral est organisé par domaines. Chaque commande ouvre une vue distincte. Sur téléphone, le bouton de menu ouvre le panneau latéral; choisissez une rubrique, puis refermez le panneau avec le bouton × ou en touchant la zone extérieure."))
    figure(3, "03-module.png", "Accéder à une rubrique et interpréter son état.", [
        ("Menu ou recherche", "Choisir « Infrastructure », par exemple."),
        ("Module", "Confirmer le nom de la rubrique dans l’en-tête."),
        ("État des données", "Consulter le résumé et les prérequis de raccordement."),
    ])
    story.extend([data_table([
        ["Module", "Ce que présente la vue actuelle", "Niveau fonctionnel"],
        ["Vue d’ensemble", "Posture, métriques et graphiques de l’aperçu.", "Interface raccordée au dashboard; démo simulée ou réponse API vide."],
        ["Applications", "Registre et état de raccordement.", "Espace d’attente; aucun enregistrement durable."],
        ["Infrastructure", "Environnements, serveurs et statut de l’inventaire.", "Espace d’attente; aucun inventaire connecté."],
        ["Vulnérabilités", "Registre des constats.", "Aucun résultat réel ne s’affiche."],
        ["Audits PHP / web", "Préparation et périmètre autorisé.", "Moteurs non activés; aucun scan automatique."],
        ["Remédiation", "Suivi d’actions et d’échéances.", "Module métier à raccorder."],
        ["Rapports", "Export de posture PDF/Excel.", "Fonction d’export prête à partir des valeurs visibles."],
        ["Utilisateurs & rôles", "Informations sur les identités.", "Création de comptes côté serveur uniquement."],
        ["Paramètres", "État des services et options d’interface.", "Thème stocké localement; paramètres sensibles non modifiables."],
    ], [32 * mm, 70 * mm, 68 * mm]), PageBreak()])

    story.extend(heading("06 · Utiliser la recherche"))
    story.extend([P("La recherche est dans l’en-tête fixe. Sur ordinateur, saisir un terme dans le champ ou utiliser le raccourci Ctrl+K (⌘K sur Mac). Sur mobile, toucher la loupe ouvre un panneau sous l’en-tête; la liste reste accessible sans quitter la vue."), *bullets([
        "La liste initiale présente les sections accessibles; taper un nom réduit les résultats.",
        "Choisir un résultat ouvre sa vue dédiée.",
        "La touche Entrée sélectionne le premier résultat filtré; Échap, le bouton × ou un clic hors panneau ferment la recherche.",
        "La recherche porte sur la navigation interne, pas sur le contenu des actifs ni sur des données serveur.",
    ]), P("Navigation latérale", "h2"), P("Sur ordinateur, utiliser le bouton à trois lignes dans l’en-tête pour replier ou déployer le menu. Le choix est conservé sur l’appareil. Sur téléphone, le même bouton ouvre un tiroir par-dessus la vue; le voile extérieur permet de le fermer."), note("Raccourci", "Ctrl+K (Windows/Linux) ou ⌘K (macOS) ouvre rapidement la recherche. Si le navigateur intercepte ce raccourci, utiliser la loupe ou le champ directement."), PageBreak()])

    story.extend(heading("07 · Produire un rapport PDF ou Excel"))
    story.append(P("Le module Rapports affiche une synthèse des valeurs accessibles, le niveau de source et deux actions d’export. En mode aperçu, le badge et l’avertissement identifient le jeu simulé. En mode API, les valeurs viennent du dashboard renvoyé par le service."))
    figure(4, "04-reports.png", "Contrôler la provenance puis exporter un rapport.", [
        ("Rapports", "Ouvrir le centre des rapports depuis le menu."),
        ("Provenance", "Vérifier le badge de source et les valeurs de synthèse."),
        ("Export", "Choisir « Télécharger le PDF » ou « Télécharger le classeur »."),
    ])
    story.extend([P("Exporter en PDF", "h2"), *bullets([
        "Vérifier le badge de provenance et la mention démo/API.",
        "Cliquer sur « Télécharger le PDF » et attendre le message de réussite.",
        "Le document inclut la posture synthétique, la date, l’emblème, un filigrane, les valeurs accessibles et une mention de données simulées si l’aperçu est actif.",
        "Ouvrir le PDF téléchargé et vérifier les métadonnées, les indicateurs et la provenance avant de le diffuser.",
    ]), P("Exporter en Excel", "h2"), *bullets([
        "Choisir « Télécharger le classeur ». Le fichier XLSX s’ouvre dans Excel ou un tableur compatible.",
        "Les onglets Synthèse, Sévérité et Notes structurent les valeurs et leur provenance.",
        "Vérifier le bandeau « Données de démonstration » avant tout partage de classeur issu de l’aperçu.",
    ]), note("Contrôle avant diffusion", "Les exports de posture ne sont pas un certificat d’audit. En mode démo, ne pas les présenter comme des résultats d’infrastructure ou des constats validés."), PageBreak()])

    story.extend(heading("08 · Personnaliser et installer la PWA"))
    story.extend([P("Thème clair/sombre", "h2"), P("Le bouton soleil/lune de l’en-tête permet de passer d’un thème à l’autre. Le choix est mémorisé localement et n’affecte pas les autres utilisateurs. La palette claire utilise des surfaces ivoire/grège douces afin de limiter l’éblouissement."), P("Installer l’application", "h2"), *bullets([
        "Depuis le login ou le tableau de bord, toucher « Installer la PWA » / « Installer l’app » si le navigateur le propose.",
        "Confirmer l’installation dans le navigateur. Sur iPhone/iPad, ouvrir le menu Partager de Safari puis « Sur l’écran d’accueil ».",
        "L’icône utilise l’emblème du projet et l’application s’ouvre dans une fenêtre dédiée selon les capacités du navigateur.",
        "L’interface déjà visitée peut être disponible hors connexion; les données API et fonctions serveur exigent le service en ligne.",
    ]), note("Cache et données", "L’installation PWA ne rend pas le backend local ni les modules métier disponibles hors connexion. Ne considérez pas les éléments cachés de l’interface comme une copie hors ligne d’un inventaire réel."), P("Déconnexion", "h2"), P("Depuis le menu latéral, choisir « Déconnexion ». Pour le mode aperçu, cela revient à l’écran de connexion; une session API active est invalidée par la commande de déconnexion côté serveur."), PageBreak()])

    story.extend(heading("09 · Affichage mobile et tablette"))
    story.extend([P("L’interface s’adapte aux écrans étroits : menu latéral en tiroir, cartes d’indicateurs en grille réduite, graphiques empilés, champs de saisie adaptés aux claviers tactiles et panneau de recherche sous l’en-tête fixe."), P("Conseils d’usage sur téléphone", "h2"), *bullets([
        "Faire défiler le contenu verticalement; l’identité de la rubrique demeure dans l’en-tête fixe.",
        "Toucher le menu pour afficher les rubriques; sélectionner une vue ferme le tiroir.",
        "Utiliser la loupe pour retrouver un module, plutôt que faire défiler tout le menu.",
        "Les cartes de posture passent à deux colonnes; les graphiques se placent l’un sous l’autre.",
        "Les boutons et liens restent accessibles au toucher; privilégier le format PDF pour une lecture rapide et Excel pour explorer les feuilles.",
    ]), P("Accessibilité", "h2"), P("Les contrôles disposent de libellés ou de texte visible et peuvent être activés par clavier. En cas de difficulté, agrandir la page dans le navigateur et utiliser la navigation par clavier; signaler tout problème de contraste ou d’élément hors écran au porteur du projet."), PageBreak()])

    story.extend(heading("10 · Dépannage et sécurité"))
    story.append(data_table([
        ["Symptôme", "Cause probable", "Action"],
        ["Service d’authentification indisponible", "API séparée non déployée ou inaccessible depuis GitHub Pages.", "Choisir l’aperçu public ou demander l’adresse d’un environnement API connecté."],
        ["Connexion refusée", "Identifiants incorrects, compte inactif ou service indisponible.", "Vérifier la saisie; contacter l’administrateur; ne pas essayer de comptes réels dans l’aperçu."],
        ["Dashboard vide", "API fondation renvoyant intentionnellement des compteurs nuls.", "Confirmer l’URL du service et l’état des modules; ne pas inventer de données."],
        ["PDF/XLSX ne se télécharge pas", "Navigateur bloque les téléchargements ou script d’export interrompu.", "Autoriser les téléchargements pour le site et réessayer; vérifier l’espace disponible."],
        ["PWA non proposée", "Navigateur, HTTPS, manifeste ou service worker requis.", "Recharger le site en HTTPS ou suivre les instructions manuelles d’installation."],
        ["Menu/recherche difficile sur mobile", "Panneau ouvert ou viewport zoomé.", "Fermer avec ×, Échap ou le voile; recentrer la page et toucher le contrôle visé."],
    ], [47 * mm, 61 * mm, 62 * mm]))
    story.extend([Spacer(1, 10), P("Bonnes pratiques", "h2"), *bullets([
        "Ne jamais placer des mots de passe réels, clés API, adresses internes ou rapports sensibles dans l’aperçu public.",
        "Ne lancer aucun audit sur un domaine, serveur ou dépôt sans autorisation explicite du propriétaire.",
        "Vérifier le contexte de démonstration et la classification des exports avant partage.",
        "Dans un environnement privé, activer HTTPS, gérer les secrets hors du code, créer les comptes côté serveur et organiser sauvegardes et surveillance.",
    ]), PageBreak()])

    story.extend(heading("11 · Foire aux questions"))
    faqs = [
        ("Le site est-il déjà un système de production institutionnel ?", "Non. Il s’agit d’une proposition technique et d’un aperçu frontend. Le dépôt ne revendique pas d’homologation, d’accréditation ou de déploiement institutionnel."),
        ("Les statistiques visibles sont-elles réelles ?", "Non en mode aperçu. Elles sont explicitement étiquetées comme simulées. L’API actuelle renvoie un état vide."),
        ("La démonstration va-t-elle scanner une cible ?", "Non. Aucun scan n’est exécuté par le parcours public; les moteurs métiers restent à intégrer."),
        ("Puis-je créer mon compte depuis le login ?", "Non. L’inscription publique est désactivée. Dans un environnement API, l’administrateur crée le premier compte côté serveur."),
        ("La PWA fonctionne-t-elle complètement hors ligne ?", "L’interface visitée peut se rouvrir selon le cache; données et services backend restent dépendants du réseau."),
        ("À qui attribuer la conception et la propriété du projet ?", f"Le projet PHP-SHIELD RDC est porté par {AUTHOR}, présenté comme son fondateur ultime et propriétaire."),
        ("Où signaler une question sur le contenu ?", "Contacter le porteur du projet ou l’administrateur de l’environnement concerné en utilisant les canaux définis par l’organisation."),
    ]
    for q, a in faqs:
        story.extend([P(q, "h2"), P(a)])
    story.extend([Spacer(1, 10), note("Fin du manuel", f"PHP-SHIELD RDC · Manuel d’utilisation · Document 02 · {TODAY.strftime('%d/%m/%Y')}<br/><b>Fondateur ultime &amp; propriétaire du projet · {AUTHOR}</b>", colors.HexColor("#e8e3d2"), GOLD)])
    doc = ProjectDocument(path, "02", "Manuel d’utilisation")
    doc.build(story)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate PHP-SHIELD RDC institutional PDF documents.")
    parser.add_argument("--document", choices=("all", "presentation", "manual"), default="all")
    parser.add_argument("--require-screenshots", action="store_true", help="Require all four PNG screenshots for the manual edition.")
    args = parser.parse_args()
    if not EMBLEM.exists():
        raise FileNotFoundError(f"Project emblem is missing: {EMBLEM}")
    PUBLIC_DOCS.mkdir(parents=True, exist_ok=True)
    FINAL_DOCS.mkdir(parents=True, exist_ok=True)
    files = []
    if args.document in ("all", "presentation"):
        files.append(("PHP-SHIELD-RDC-Presentation-du-projet.pdf", add_project_document))
    if args.document in ("all", "manual"):
        required = ["01-login.png", "02-overview.png", "03-module.png", "04-reports.png"]
        missing = [name for name in required if not (SCREENSHOTS / name).exists()]
        if missing and args.require_screenshots:
            parser.error(f"Add genuine app screenshots under {SCREENSHOTS}: {', '.join(missing)}")
        files.append(("PHP-SHIELD-RDC-Manuel-d-utilisation.pdf", lambda target: add_manual_document(target, screenshots=not missing)))
    for name, builder in files:
        target = FINAL_DOCS / name
        builder(target)
        (PUBLIC_DOCS / name).write_bytes(target.read_bytes())
        print(f"Generated {target} ({target.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
