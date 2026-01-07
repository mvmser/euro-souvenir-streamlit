#!/usr/bin/env python3
"""
Script pour ajouter les coordonnées GPS manquantes dans euro_souvenir_data.csv
Utilise l'API Nominatim (OpenStreetMap) pour le géocodage gratuit
"""

import pandas as pd
import time
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import sys

def is_valid_value(value):
    """
    Vérifie si une valeur est valide (non NaN, non None, non vide)
    """
    if pd.isna(value):
        return False
    if value is None:
        return False
    if isinstance(value, str):
        value_clean = value.strip().lower()
        if not value_clean or value_clean in ['nan', 'null', 'none', '--', '']:
            return False
    return True

def geocode_address(geolocator, pays, ville, lieu, adresse):
    """
    Essaie de géocoder une adresse en utilisant plusieurs stratégies
    """
    # Liste des requêtes à essayer, par ordre de priorité
    queries = []
    
    # Construire les parties valides
    parts = []
    
    # Stratégie 1: Adresse complète
    if is_valid_value(adresse):
        parts = [adresse.strip()]
        if is_valid_value(ville):
            parts.append(ville.strip())
        if is_valid_value(pays):
            parts.append(pays.strip())
        if len(parts) >= 2:  # Au moins adresse + ville ou pays
            queries.append(", ".join(parts))
    
    # Stratégie 2: Lieu + ville + pays
    if is_valid_value(lieu):
        parts = [lieu.strip()]
        if is_valid_value(ville):
            parts.append(ville.strip())
        if is_valid_value(pays):
            parts.append(pays.strip())
        if len(parts) >= 2:  # Au moins lieu + ville ou pays
            queries.append(", ".join(parts))
    
    # Stratégie 3: Ville + pays seulement
    if is_valid_value(ville) and is_valid_value(pays):
        queries.append(f"{ville.strip()}, {pays.strip()}")
    
    # Essayer chaque requête
    for query in queries:
        try:
            print(f"  Tentative: {query[:80]}...")
            location = geolocator.geocode(query, timeout=10)
            
            if location:
                print(f"  ✓ Trouvé: {location.latitude}, {location.longitude}")
                return location.latitude, location.longitude
            else:
                print(f"  ✗ Aucun résultat")
                
        except (GeocoderTimedOut, GeocoderServiceError) as e:
            print(f"  ⚠ Erreur: {e}")
            time.sleep(2)
            continue
    
    return None, None

def main():
    # Fichier CSV
    csv_file = 'data/euro_souvenir_data.csv'
    
    print("=" * 80)
    print("GÉOCODAGE DES ADRESSES MANQUANTES")
    print("=" * 80)
    
    # Charger le CSV
    print(f"\n📂 Chargement de {csv_file}...")
    df = pd.read_csv(csv_file)
    
    # Trouver les lignes sans coordonnées
    missing_coords = df['LATITUDE'].isna() | df['LONGITUDE'].isna()
    rows_to_geocode = df[missing_coords]
    
    print(f"\n📊 Statistiques:")
    print(f"   - Total de lignes: {len(df)}")
    print(f"   - Lignes avec coordonnées: {len(df[~missing_coords])}")
    print(f"   - Lignes sans coordonnées: {len(rows_to_geocode)}")
    
    if len(rows_to_geocode) == 0:
        print("\n✓ Toutes les lignes ont déjà des coordonnées!")
        return
    
    # Demander confirmation
    print(f"\n⚠ Ce script va essayer de géocoder {len(rows_to_geocode)} adresses.")
    print("   Note: L'API Nominatim a une limite de 1 requête/seconde.")
    print(f"   Temps estimé: ~{len(rows_to_geocode)} secondes")
    
    response = input("\n▶ Continuer? (o/n): ")
    if response.lower() not in ['o', 'oui', 'y', 'yes']:
        print("Annulé.")
        return
    
    # Initialiser le géocodeur
    print("\n🌍 Initialisation du géocodeur Nominatim...")
    geolocator = Nominatim(user_agent="euro-souvenir-app/1.0")
    
    # Géocoder chaque ligne
    geocoded_count = 0
    failed_count = 0
    
    print("\n🔄 Démarrage du géocodage...\n")
    
    for idx, row in rows_to_geocode.iterrows():
        print(f"[{idx + 1}/{len(df)}] {row['TITRE']}")
        
        lat, lon = geocode_address(
            geolocator,
            row['PAYS'],
            row['VILLE'],
            row['LIEU'],
            row['ADRESSE']
        )
        
        if lat and lon:
            df.at[idx, 'LATITUDE'] = lat
            df.at[idx, 'LONGITUDE'] = lon
            geocoded_count += 1
        else:
            print(f"  ✗ Échec du géocodage")
            failed_count += 1
        
        # Respecter la limite de l'API (1 req/sec)
        time.sleep(1.1)
        print()
    
    # Résumé
    print("=" * 80)
    print("RÉSUMÉ")
    print("=" * 80)
    print(f"✓ Géocodées avec succès: {geocoded_count}")
    print(f"✗ Échecs: {failed_count}")
    
    if geocoded_count > 0:
        # Sauvegarder le CSV mis à jour
        backup_file = csv_file.replace('.csv', '_backup.csv')
        print(f"\n💾 Sauvegarde de l'original vers: {backup_file}")
        df.to_csv(backup_file, index=False)
        
        print(f"💾 Mise à jour du fichier: {csv_file}")
        df.to_csv(csv_file, index=False)
        
        print("\n✓ Terminé! Le fichier CSV a été mis à jour.")
    else:
        print("\n⚠ Aucune modification n'a été apportée au CSV.")
    
    # Afficher les lignes qui n'ont toujours pas de coordonnées
    still_missing = df['LATITUDE'].isna() | df['LONGITUDE'].isna()
    if still_missing.sum() > 0:
        print(f"\n⚠ {still_missing.sum()} lignes n'ont toujours pas de coordonnées:")
        print(df[still_missing][['TITRE', 'PAYS', 'VILLE', 'LIEU', 'ADRESSE']].to_string())

if __name__ == "__main__":
    main()
