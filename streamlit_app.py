import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from datetime import datetime

# Configuration de la page
st.set_page_config(
    page_title="Billets 0 Euro Souvenirs",
    page_icon="💶",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialiser l'état de session pour la navigation
if 'page' not in st.session_state:
    st.session_state.page = 'carte'

# Chargement des données
@st.cache_data
def load_data():
    df = pd.read_csv('data/euro_souvenir_data.csv')
    return df

def save_data(df):
    df.to_csv('data/euro_souvenir_data.csv', index=False)
    st.cache_data.clear()  # Effacer le cache pour recharger les nouvelles données

df = load_data()

# Filtrer les données avec coordonnées valides
df_with_coords = df.dropna(subset=['LATITUDE', 'LONGITUDE'])

# Sidebar - Filtres en premier
st.sidebar.header("🔍 Filtres")

# Filtre par pays
pays_list = ['Tous'] + sorted(df['PAYS'].dropna().unique().tolist())
selected_pays = st.sidebar.selectbox("Pays", pays_list)

# Filtre par ville
if selected_pays != 'Tous':
    df_filtered = df[df['PAYS'] == selected_pays]
else:
    df_filtered = df

villes_list = ['Toutes'] + sorted(df_filtered['VILLE'].dropna().unique().tolist())
selected_ville = st.sidebar.selectbox("Ville", villes_list)

# Appliquer les filtres pour calculer les stats
if selected_pays != 'Tous':
    df_display = df_with_coords[df_with_coords['PAYS'] == selected_pays]
else:
    df_display = df_with_coords

if selected_ville != 'Toutes':
    df_display = df_display[df_display['VILLE'] == selected_ville]

# Statistiques dans la sidebar (après filtres)
st.sidebar.markdown("---")
st.sidebar.header("📊 Statistiques")

col1, col2 = st.sidebar.columns(2)
with col1:
    st.metric("Lieux affichés", len(df_display))
with col2:
    st.metric("Pays", df_display['PAYS'].nunique())
st.metric("Villes", df_display['VILLE'].nunique())

# Bouton pour ajouter un lieu
st.sidebar.markdown("---")
if st.sidebar.button("➕ Ajouter un lieu", type="primary", use_container_width=True):
    st.session_state.page = 'ajouter'
    st.rerun()

if st.session_state.page == 'ajouter' and st.sidebar.button("🗺️ Retour à la carte", use_container_width=True):
    st.session_state.page = 'carte'
    st.rerun()

# PAGE D'AJOUT DE LIEU
if st.session_state.page == 'ajouter':
    st.title("➕ Ajouter un nouveau lieu")
    st.markdown("Remplissez les informations ci-dessous pour ajouter un nouveau lieu de vente de billets 0 euros.")
    
    with st.form("add_location_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Informations principales")
            titre = st.text_input("Titre *", placeholder="Ex: TOUR EIFFEL")
            code = st.text_input("Code", placeholder="Ex: UEBU")
            milesime = st.text_input("Millésime", placeholder="Ex: 2025-6")
            
            pays = st.text_input("Pays *", placeholder="Ex: France")
            ville = st.text_input("Ville *", placeholder="Ex: PARIS")
            lieu = st.text_input("Lieu", placeholder="Ex: Tour Eiffel")
            adresse = st.text_area("Adresse", placeholder="Ex: Av. Gustave Eiffel, 75007 Paris")
            
        with col2:
            st.subheader("Détails du lieu")
            
            # Mode de vente - liste déroulante des valeurs existantes
            modes_vente = [''] + sorted(df['Mode de vente'].dropna().unique().tolist())
            mode_vente = st.selectbox("Mode de vente", modes_vente)
            
            # Type de lieu - liste déroulante des valeurs existantes
            types_lieu = [''] + sorted(df['TYPE DE LIEU'].dropna().unique().tolist())
            type_lieu = st.selectbox("Type de lieu", types_lieu)
            
            commentaire = st.text_area("Commentaire", placeholder="Informations supplémentaires...")
            prix = st.text_input("Prix indicatif (€)", placeholder="Ex: 2,00 €")
            
            st.subheader("Coordonnées GPS (optionnel)")
            col_lat, col_lon = st.columns(2)
            with col_lat:
                latitude = st.text_input("Latitude", placeholder="Ex: 48.857298")
            with col_lon:
                longitude = st.text_input("Longitude", placeholder="Ex: 2.302035")
            
            image = st.text_input("URL Image", placeholder="URL de l'image (optionnel)")
        
        st.markdown("---")
        col_submit, col_cancel = st.columns([1, 1])
        
        with col_submit:
            submitted = st.form_submit_button("💾 Enregistrer", type="primary", use_container_width=True)
        with col_cancel:
            cancelled = st.form_submit_button("❌ Annuler", use_container_width=True)
        
        if submitted:
            # Validation
            if not titre or not pays or not ville:
                st.error("⚠️ Les champs Titre, Pays et Ville sont obligatoires!")
            else:
                # Créer une nouvelle ligne
                date_ajout = datetime.now().strftime("%d/%m/%Y")
                
                # Trouver le prochain numéro de ligne
                max_id = df['#'].max() if '#' in df.columns and not df['#'].isna().all() else 0
                if pd.isna(max_id):
                    max_id = 0
                new_id = max_id + 1                
                new_row = {
                    '#': new_id,
                    'TITRE': titre,
                    'CODE': code if code else '',
                    'MILESIME': milesime if milesime else '',
                    'PAYS': pays,
                    'VILLE': ville,
                    'LIEU': lieu if lieu else '',
                    'ADRESSE': adresse if adresse else '',
                    'Mode de vente': mode_vente if mode_vente else '',
                    'TYPE DE LIEU': type_lieu if type_lieu else '',
                    'COMMENTAIRE': commentaire if commentaire else '',
                    'PRIX INDICATIF (€)': prix if prix else '',
                    'DATE': date_ajout,
                    'IMAGE': image if image else '',
                    'LATITUDE': float(latitude) if latitude else None,
                    'LONGITUDE': float(longitude) if longitude else None
                }
                
                # Ajouter la nouvelle ligne au DataFrame
                df_new = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                
                # Sauvegarder
                save_data(df_new)
                
                st.success(f"✅ Le lieu '{titre}' a été ajouté avec succès!")
                st.balloons()
                
                # Revenir à la carte après 2 secondes
                st.info("🔄 Retour à la carte...")
                import time
                time.sleep(2)
                st.session_state.page = 'carte'
                st.rerun()
        
        if cancelled:
            st.session_state.page = 'carte'
            st.rerun()

# PAGE CARTE (par défaut)
elif st.session_state.page == 'carte':
    st.title("💶 Carte des Billets 0 Euro Souvenirs")
    st.markdown("Découvrez où acheter vos billets souvenirs de 0 euros à travers l'Europe")

# Créer la carte
if len(df_display) > 0:
    # Centre de la carte
    center_lat = df_display['LATITUDE'].mean()
    center_lon = df_display['LONGITUDE'].mean()
    
    # Créer la carte Folium
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=6 if selected_ville == 'Toutes' else 13,
        tiles='OpenStreetMap'
    )
    
    # Ajouter des marqueurs pour chaque lieu
    for idx, row in df_display.iterrows():
        popup_html = f"""
        <div style="width: 300px;">
            <h4>{row['TITRE']}</h4>
            <b>Lieu:</b> {row['LIEU']}<br>
            <b>Ville:</b> {row['VILLE']}<br>
            <b>Adresse:</b> {row['ADRESSE']}<br>
            <b>Type:</b> {row['TYPE DE LIEU']}<br>
            <b>Mode de vente:</b> {row['Mode de vente']}<br>
            <b>Millésime:</b> {row['MILESIME']}<br>
            {f"<b>Prix indicatif:</b> {row['PRIX INDICATIF (€)']}<br>" if pd.notna(row['PRIX INDICATIF (€)']) else ""}
            {f"<b>Commentaire:</b> {row['COMMENTAIRE']}<br>" if pd.notna(row['COMMENTAIRE']) else ""}
        </div>
        """
        
        # Couleur du marqueur selon le type de lieu
        icon_color = 'blue'
        if pd.notna(row['TYPE DE LIEU']):
            if 'Monument' in str(row['TYPE DE LIEU']):
                icon_color = 'red'
            elif 'Musée' in str(row['TYPE DE LIEU']):
                icon_color = 'green'
            elif 'Office' in str(row['TYPE DE LIEU']):
                icon_color = 'orange'
            elif 'Boutique' in str(row['TYPE DE LIEU']):
                icon_color = 'purple'
        
        folium.Marker(
            location=[row['LATITUDE'], row['LONGITUDE']],
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=row['TITRE'],
            icon=folium.Icon(color=icon_color, icon='info-sign')
        ).add_to(m)
    
    # Afficher la carte
    st_folium(m, width=None, height=600)
    
    # Légende des couleurs
    st.markdown("### Légende")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("🔴 **Monument**")
    with col2:
        st.markdown("🟢 **Musée**")
    with col3:
        st.markdown("🟠 **Office de Tourisme**")
    with col4:
        st.markdown("🟣 **Boutique**")
else:
    st.warning("Aucun lieu avec coordonnées GPS pour cette sélection")
