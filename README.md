# 💶 Carte des Billets 0 Euro Souvenirs

Application Streamlit interactive pour localiser les lieux de vente de billets souvenirs de 0 euros à travers l'Europe.

## 🌟 Fonctionnalités

### 🗺️ Carte interactive
- Visualisation sur une carte OpenStreetMap
- Marqueurs colorés par type de lieu (Monuments, Musées, Offices de Tourisme, Boutiques)
- Pop-ups détaillés avec informations complètes et photos
- Filtres par pays et ville

### ➕ Ajout de lieux avec mapping automatique
- Entrez simplement le CODE et le MILLÉSIME du billet
- Préremplissage automatique depuis la base de données de référence
- Support des images (URL)

### 📊 Statistiques dynamiques
- Nombre de lieux affichés, pays et villes
- Mise à jour en temps réel selon les filtres

## 🚀 Installation

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## 📖 Guides

- [GUIDE_AJOUT_LIEU.md](GUIDE_AJOUT_LIEU.md) - Comment ajouter un lieu
- [GEOCODING_GUIDE.md](GEOCODING_GUIDE.md) - Géocoder les adresses manquantes

## 📁 Structure

```
euro-souvenir-streamlit/
├── streamlit_app.py          # Application principale
├── geocode_missing.py        # Script de géocodage
└── data/
    ├── shop.csv              # Lieux de vente
    └── master_data.csv       # Base de référence des billets
```

**Bon voyage dans la collection de billets 0 Euro !** 🎫✨
