# Guide de Géocodage 🗺️

Ce guide explique comment utiliser le script `geocode_missing.py` pour ajouter automatiquement les coordonnées GPS manquantes dans votre fichier CSV.

## 📋 Prérequis

Assurez-vous que toutes les dépendances sont installées :

```bash
pip install -r requirements.txt
```

## 🚀 Utilisation

### Étape 1 : Exécuter le script

```bash
python geocode_missing.py
```

### Étape 2 : Suivre les instructions

Le script va :
1. Analyser le fichier `data/euro_souvenir_data.csv`
2. Identifier les lignes sans coordonnées (LATITUDE/LONGITUDE vides)
3. Afficher le nombre de lignes à géocoder
4. Demander confirmation avant de commencer

### Étape 3 : Attendre le traitement

- Le script utilise l'API **Nominatim** (OpenStreetMap) qui est **gratuite**
- Limite : 1 requête par seconde
- Temps estimé : environ 1 seconde par adresse

## 🔍 Stratégies de géocodage

Le script essaie plusieurs approches pour chaque adresse :

1. **Adresse complète** : `ADRESSE, VILLE, PAYS`
2. **Lieu + ville** : `LIEU, VILLE, PAYS`
3. **Ville seulement** : `VILLE, PAYS`

Il s'arrête dès qu'une correspondance est trouvée.

## 💾 Sécurité

- **Sauvegarde automatique** : L'original est sauvegardé dans `euro_souvenir_data_backup.csv`
- **Modifications sélectives** : Seules les lignes **sans coordonnées** sont modifiées
- **Les coordonnées existantes ne sont jamais écrasées**

## 📊 Exemple de sortie

```
================================================================================
GÉOCODAGE DES ADRESSES MANQUANTES
================================================================================

📂 Chargement de data/euro_souvenir_data.csv...

📊 Statistiques:
   - Total de lignes: 95
   - Lignes avec coordonnées: 50
   - Lignes sans coordonnées: 45

⚠ Ce script va essayer de géocoder 45 adresses.
   Note: L'API Nominatim a une limite de 1 requête/seconde.
   Temps estimé: ~45 secondes

▶ Continuer? (o/n): o

🌍 Initialisation du géocodeur Nominatim...

🔄 Démarrage du géocodage...

[1/95] CHÂTEAU COMTAL DE CARCASSONNE
  Tentative: Cité de Carcassonne, CARCASSONNE, France...
  ✓ Trouvé: 43.206, 2.362

[2/95] CHÂTEAU DE PEYREPERTUSE
  Tentative: DUILHAC-SOUS-PEYREPERTUSE, France...
  ✓ Trouvé: 42.872, 2.553

...

================================================================================
RÉSUMÉ
================================================================================
✓ Géocodées avec succès: 42
✗ Échecs: 3

💾 Sauvegarde de l'original vers: data/euro_souvenir_data_backup.csv
💾 Mise à jour du fichier: data/euro_souvenir_data.csv

✓ Terminé! Le fichier CSV a été mis à jour.
```

## ⚠️ Limitations

- **Précision variable** : Certaines adresses peuvent avoir des coordonnées approximatives
- **Échecs possibles** : Adresses incomplètes ou incorrectes peuvent échouer
- **Vérification recommandée** : Vérifiez manuellement les résultats dans l'app Streamlit

## 🔧 En cas d'échec

Si certaines adresses ne sont pas géocodées :

1. Vérifiez que les champs `PAYS`, `VILLE`, `LIEU` ou `ADRESSE` sont remplis
2. Corrigez les fautes d'orthographe dans le CSV
3. Réexécutez le script (seules les lignes vides seront traitées)
4. En dernier recours, ajoutez les coordonnées manuellement

## 🌐 Sources alternatives

Si vous souhaitez utiliser une autre API de géocodage :

- **Google Maps Geocoding API** (payant mais très précis)
- **Mapbox Geocoding** (limite gratuite généreuse)
- **Here Geocoding** (alternative professionnelle)

Modifiez simplement le code dans `geocode_missing.py` pour changer de provider.

## 📝 Notes

- Les coordonnées sont au format décimal (WGS84)
- Format : LATITUDE (Nord/Sud), LONGITUDE (Est/Ouest)
- Les coordonnées existantes ne sont **jamais** modifiées
