# 📸 Guide des Images pour les Lieux

## Où trouver et héberger des images

Pour enrichir votre carte avec des images, voici quelques options :

### 🌐 Services d'hébergement gratuits

1. **Imgur** (recommandé)
   - Site : https://imgur.com
   - Gratuit et simple
   - Accepte tous les formats d'images
   - Générer un lien direct : Clic droit → "Copier l'adresse de l'image"

2. **Google Photos**
   - Télécharger votre photo
   - Cliquer sur "Partager" → "Créer un lien"
   - Modifier l'URL pour obtenir le lien direct

3. **GitHub**
   - Si vous avez un compte GitHub
   - Créer un dossier `images/` dans votre repo
   - Upload des images
   - Utiliser l'URL brute

### 🎯 Types d'images recommandées

#### Pour les lieux de vente :
- Photo de la façade du bâtiment
- Photo de l'entrée
- Photo du distributeur/point de vente
- Photo de la boutique

#### Pour les billets :
- Scan ou photo du billet (recto)
- Scan ou photo du billet (verso) avec CODE et MILLÉSIME visibles
- Photo du billet dans son lieu

### 📏 Bonnes pratiques

✅ **Résolution recommandée** : 800x600 pixels minimum  
✅ **Format** : JPG, PNG ou WEBP  
✅ **Poids** : Moins de 2 MB pour un chargement rapide  
✅ **Orientation** : Paysage de préférence pour les popups  

### 💡 Exemples d'URLs valides

```
https://i.imgur.com/abc1234.jpg
https://example.com/images/tour-eiffel.png
https://raw.githubusercontent.com/user/repo/main/images/lieu.jpg
```

### ⚠️ À éviter

❌ URLs avec authentification requise  
❌ Images trop lourdes (>5 MB)  
❌ Liens temporaires ou expirants  
❌ Images protégées par droits d'auteur sans permission  

### 🔒 Droits d'auteur

- Utilisez vos propres photos
- Ou des photos avec licence libre (Creative Commons, etc.)
- Créditez l'auteur si nécessaire dans le commentaire

### 📝 Comment l'image s'affiche

L'image apparaîtra :
- 🗺️ Dans le popup de la carte quand on clique sur le marqueur
- 📐 Redimensionnée automatiquement (max 350px de largeur)
- 🎨 Avec coins arrondis pour un rendu agréable

### 🛠️ En cas de problème

**L'image ne s'affiche pas ?**

1. Vérifiez que l'URL est complète (commence par `https://`)
2. Testez l'URL dans un navigateur
3. Vérifiez que l'image est publiquement accessible
4. Essayez un autre service d'hébergement

**L'image est trop grande/petite ?**

- L'application redimensionne automatiquement
- Pour un meilleur résultat, utilisez des images de ratio 16:9 ou 4:3

### 🎨 Exemple complet

```
Lieu : Tour Eiffel
Image URL : https://i.imgur.com/example.jpg

↓ Résultat sur la carte ↓

┌─────────────────────────────────┐
│  [Photo de la Tour Eiffel]      │
│                                 │
│  🏢 Lieu: Tour Eiffel           │
│  📍 Adresse: Av. Gustave...     │
│  💳 Mode: Libre service         │
└─────────────────────────────────┘
```

## 🎯 Ressources utiles

- **Imgur** : https://imgur.com
- **Unsplash** (photos libres) : https://unsplash.com
- **Pexels** (photos libres) : https://www.pexels.com
- **Compresser des images** : https://tinypng.com
