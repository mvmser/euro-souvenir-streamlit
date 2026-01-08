# 📖 Guide : Comment ajouter un lieu de vente

## 🔍 Trouver les informations sur votre billet 0 Euro

Pour ajouter un nouveau lieu de vente, vous devez d'abord identifier votre billet à partir de deux informations clés :

### 1️⃣ Le CODE (4 lettres)

Le **CODE** est un identifiant unique de 4 lettres qui se trouve sur le billet.

**Où le trouver ?**
- 📍 En bas du billet, généralement en petits caractères
- Format : 4 lettres majuscules (ex: `UEBU`, `XEJE`, `NEAA`)
- Exemple : Pour la Tour Eiffel → `UEBU`

```
┌─────────────────────────────────┐
│                                 │
│      TOUR EIFFEL                │
│                                 │
│      [Image du monument]        │
│                                 │
│      UEBU ← CODE ici !         │
└─────────────────────────────────┘
```

### 2️⃣ Le MILLÉSIME (année-numéro)

Le **MILLÉSIME** indique l'édition du billet.

**Où le trouver ?**
- 📍 À côté du code, au dos du billet, ou en bas
- Format : `ANNÉE-NUMÉRO` (ex: `2025-6`, `2024-1`, `2023-3`)
- Le numéro indique la version/édition de l'année

```
┌─────────────────────────────────┐
│                                 │
│      TOUR EIFFEL                │
│                                 │
│      [Image du monument]        │
│                                 │
│      UEBU  2025-6 ← MILLÉSIME ! │
└─────────────────────────────────┘
```

## ✨ Fonctionnement du formulaire

### Étape 1 : Saisir CODE et MILLÉSIME

Entrez uniquement ces deux informations. Le système va :
- ✅ Chercher automatiquement le billet dans la base de données
- ✅ Préremplir : Titre, Code, Millésime, Pays, Ville
- ✅ Ajouter un lien vers la fiche du billet

### Étape 2 : Compléter les informations du lieu

Vous devez ensuite renseigner :
- **LIEU** : Nom exact du lieu de vente (ex: "Tour Eiffel", "Office de Tourisme")
- **ADRESSE** : Adresse complète et précise
- **Mode de vente** : Comment le billet est vendu (liste déroulante)
- **Type de lieu** : Catégorie du lieu (liste déroulante)
- **Commentaire** : Informations pratiques (accès, horaires, particularités...)
- **Prix indicatif** : Prix en euros (ex: "2,00 €")
- **Coordonnées GPS** : Latitude et Longitude (optionnel, peut être ajouté plus tard)
- **URL Image** : Lien vers une photo du lieu ou du billet

### Étape 3 : URL de l'image

Pour l'URL de l'image, vous pouvez :
- Héberger l'image sur un service gratuit (Imgur, Google Photos, etc.)
- Utiliser l'URL d'une image existante sur le web
- Format : `https://exemple.com/image.jpg`

**L'image sera affichée :**
- 🗺️ Sur la carte dans le popup du marqueur
- 📊 Pour identifier visuellement le lieu

## 💡 Exemples pratiques

### Exemple 1 : Tour Eiffel
```
CODE: UEBU
MILLÉSIME: 2025-6

↓ Système remplit automatiquement ↓

TITRE: TOUR EIFFEL
PAYS: France
VILLE: PARIS

↓ Vous complétez ↓

LIEU: Tour Eiffel
ADRESSE: Av. Gustave Eiffel, 75007 Paris
Mode de vente: Libre service
Type de lieu: Monument
Commentaire: Disponible au RDC après la sécurité
Prix: 2,00 €
Latitude: 48.857298
Longitude: 2.302035
Image: https://exemple.com/tour-eiffel.jpg
```

### Exemple 2 : Bratislava
```
CODE: EEAB
MILLÉSIME: 2025-2

↓ Système remplit automatiquement ↓

TITRE: BRATISLAVA
PAYS: Slovaquie
VILLE: BRATISLAVA

↓ Vous complétez ↓

LIEU: Souvenirs art and craft from bratislava
ADRESSE: Ventúrska 266/7, 811 01 Bratislava
Mode de vente: Libre service
Type de lieu: Boutique souvenirs
Prix: 4,90 €
```

## ❓ Questions fréquentes

**Q: Je ne trouve pas le CODE sur mon billet**
- R: Vérifiez au dos du billet, en bas ou sur les bords. Il est parfois en très petit.

**Q: Le système ne trouve pas mon billet**
- R: Vérifiez que le CODE et le MILLÉSIME sont corrects. Si le billet est très récent, il n'est peut-être pas encore dans la base.

**Q: Je n'ai pas les coordonnées GPS**
- R: Pas de problème ! Laissez les champs vides et utilisez le script `geocode_missing.py` plus tard pour les ajouter automatiquement.

**Q: Où trouver une image du lieu ?**
- R: Vous pouvez :
  - Prendre une photo vous-même et l'héberger en ligne
  - Utiliser Google Maps Street View
  - Chercher sur le site officiel du lieu
  - Laisser vide si vous n'avez pas d'image

## 🎯 Conseils

- ✅ **Soyez précis** : Plus l'adresse est détaillée, mieux c'est pour le géocodage
- ✅ **Ajoutez des commentaires** : Informations pratiques (horaires, accès, particularités)
- ✅ **Vérifiez le prix** : Indiquez le prix que vous avez payé
- ✅ **Mode de vente important** : Précisez si c'est en libre-service, à la caisse, distributeur...
- ✅ **Type de lieu** : Aide à la catégorisation et l'affichage sur la carte

## 🚀 Après l'ajout

Une fois le lieu ajouté :
1. 🗺️ Il apparaît immédiatement sur la carte
2. 🎨 La couleur du marqueur dépend du type de lieu
3. 📍 Cliquez sur le marqueur pour voir tous les détails
4. 🔍 Utilisez les filtres pour le retrouver facilement
