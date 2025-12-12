# Resume-automatique
## 🎥 Démonstration vidéo
👉 Cliquez ici pour voir la vidéo :  
https://github.com/oumarimat/Resume-automatique/blob/main/video/resume.mp4
Cahier des Charges - Générateur Automatique de Résumés PDF
1. Contexte et Objectifs
1.1 Contexte
Dans un contexte de surabondance d’informations, la lecture intégrale de documents longs (rapports, thèses, articles scientifiques) est chronophage. Il existe un besoin d’outils capables de synthétiser automatiquement ces documents tout en préservant l’information essentielle.

1.2 Objectif Principal
Développer une application web performante capable d’analyser des fichiers PDF de grande taille et de générer des résumés de haute qualité selon trois méthodes : Extractive, Abstractive, et Hybride.

2. Spécifications fonctionnelles
2.1 Gestion des Fichiers
Upload : L’utilisateur doit pouvoir charger un fichier PDF via une interface « Drag & Drop ».
Validation : Le système doit vérifier que le fichier est bien au format PDF.
Taille : Gestion des fichiers volumineux (jusqu’à 16 Mo ou plus selon configuration).
2.2 Traitement du Texte (Pipeline)
Extraction : Récupération du texte brut depuis le PDF (support des PDF natifs et scannés via OCR).
Nettoyage : Suppression des en-têtes, pieds de page, et numéros de page parasites.
Segmentation (Chunking) : Découpage intelligent du texte en blocs cohérents (phrases complètes) respectant une limite de tokens (ex : 1000 tokens) pour l’IA.
2.3 Moteurs de Résumé
L’application doit proposer trois modes :

Extracteur de CV :
Méthode statistique (TF-IDF / similarité cosinus).
Sélectionne les phrases les plus importantes du texte original.
Avantage : Factual, pas d’hallucination.
Résumé du CV :
Utilisation d’un LLM (Large Language Model) : Google Gemini 2.0 Flash.
Méthode « Map-Reduce » : Résumé de chaque segment puis synthèse globale.
Avantage : Fluide, reformulé, synthétique.
CV Hybride :
Combinaison des deux approches.
Utilise l’extractif pour identifier les points clés, puis l’abstractif pour les rédiger.
2.4 Exportation
Affichage du résumé directement dans l’interface.
Possibilité de copier le texte dans le presse-papier.
Téléchargement du résumé au format ..txt
3. Techniques de spécifications
3.1 Stack Technologique
Langage : Python 3.10+
Backend : Flask (Serveur Web léger et robuste).
Frontend : HTML5, CSS3 (Design moderne, Flexbox/Grid), JavaScript (AJAX pour les appels asynchrones).
IA / LLM : Google Generative AI (Gemini API).
NLP & Traitement :
PyMuPDF (Extraction rapide).
NLTK (Tokenisation et découpage de phrases).
Scikit-learn (Calculs vectoriels pour l’extractif).
NetworkX (Algorithme TextRank).
3.2 Modulaire d’architecture
Le projet suit une architecture propre et maintenable :

app.py : Point d’entrée serveur (API & Routing).
pdf_processing/ : Modules de bas niveau (extraction, nettoyage).
summarization/ : Logique métier des résumés.
models/ : Gestion des appels API externes.
static/ & templates/ : Utilisateur d’interface.
4. Interface utilisateur (UI/UX)
4.1 Système de conception
Style : « Premium », moderne, épuré.
Couleurs : Palette harmonieuse (Indigo/Blanc/Gris doux).
Composants :
Zone de dépôt animée.
Sélecteurs de mode (Boutons radio stylisés).
Indicateurs de chargement (Spinners).
Design responsive (mobile et bureau).
4.2 Expérience Utilisateur
Feedback immédiat lors de l’upload.
Traitement asynchrone (l’interface ne fige pas pendant le calcul).
Gestion des erreurs claire (ex : « Fichier trop lourd », « Erreur API »).
