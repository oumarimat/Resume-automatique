# Cahier des Charges - Générateur Automatique de Résumés PDF

## 1. Contexte et Objectifs
### 1.1 Contexte
Dans un contexte de surabondance d'informations, la lecture intégrale de documents longs (rapports, thèses, articles scientifiques) est chronophage. Il existe un besoin d'outils capables de synthétiser automatiquement ces documents tout en préservant l'information essentielle.

### 1.2 Objectif Principal
Développer une application web performante capable d'analyser des fichiers PDF de grande taille et de générer des résumés de haute qualité selon trois méthodes : **Extractive**, **Abstractive**, et **Hybride**.

## 2. Spécifications Fonctionnelles

### 2.1 Gestion des Fichiers
*   **Upload** : L'utilisateur doit pouvoir charger un fichier PDF via une interface "Drag & Drop".
*   **Validation** : Le système doit vérifier que le fichier est bien au format PDF.
*   **Taille** : Gestion des fichiers volumineux (jusqu'à 16 Mo ou plus selon configuration).

### 2.2 Traitement du Texte (Pipeline)
1.  **Extraction** : Récupération du texte brut depuis le PDF (support des PDF natifs et scannés via OCR).
2.  **Nettoyage** : Suppression des en-têtes, pieds de page, et numéros de page parasites.
3.  **Segmentation (Chunking)** : Découpage intelligent du texte en blocs cohérents (phrases complètes) respectant une limite de tokens (ex: 1000 tokens) pour l'IA.

### 2.3 Moteurs de Résumé
L'application doit proposer trois modes :
1.  **Résumé Extractif** :
    *   Méthode statistique (TF-IDF / Cosine Similarity).
    *   Sélectionne les phrases les plus importantes du texte original.
    *   Avantage : Factuel, pas d'hallucination.
2.  **Résumé Abstractif** :
    *   Utilisation d'un LLM (Large Language Model) : **Google Gemini 2.0 Flash**.
    *   Méthode "Map-Reduce" : Résumé de chaque segment puis synthèse globale.
    *   Avantage : Fluide, reformulé, synthétique.
3.  **Résumé Hybride** :
    *   Combinaison des deux approches.
    *   Utilise l'extractif pour identifier les points clés, puis l'abstractif pour les rédiger.

### 2.4 Export
*   Affichage du résumé directement dans l'interface.
*   Possibilité de copier le texte dans le presse-papier.
*   Téléchargement du résumé au format `.txt`.

## 3. Spécifications Techniques

### 3.1 Stack Technologique
*   **Langage** : Python 3.10+
*   **Backend** : Flask (Serveur Web léger et robuste).
*   **Frontend** : HTML5, CSS3 (Design moderne, Flexbox/Grid), JavaScript (AJAX pour les appels asynchrones).
*   **IA / LLM** : Google Generative AI (Gemini API).
*   **NLP & Traitement** :
    *   `PyMuPDF` (Extraction rapide).
    *   `NLTK` (Tokenisation et découpage de phrases).
    *   `Scikit-learn` (Calculs vectoriels pour l'extractif).
    *   `NetworkX` (Algorithme TextRank).

### 3.2 Architecture Modulaire
Le projet suit une architecture propre et maintenable :
*   `app.py` : Point d'entrée serveur (API & Routing).
*   `pdf_processing/` : Modules de bas niveau (extraction, nettoyage).
*   `summarization/` : Logique métier des résumés.
*   `models/` : Gestion des appels API externes.
*   `static/` & `templates/` : Interface utilisateur.

## 4. Interface Utilisateur (UI/UX)

### 4.1 Design System
*   **Style** : "Premium", moderne, épuré.
*   **Couleurs** : Palette harmonieuse (Indigo/Blanc/Gris doux).
*   **Composants** :
    *   Zone de dépôt animée.
    *   Sélecteurs de mode (Radio buttons stylisés).
    *   Indicateurs de chargement (Spinners).
    *   Design Responsive (Mobile & Desktop).

### 4.2 Expérience Utilisateur
*   Feedback immédiat lors de l'upload.
*   Traitement asynchrone (l'interface ne fige pas pendant le calcul).
*   Gestion des erreurs claire (ex: "Fichier trop lourd", "Erreur API").

 