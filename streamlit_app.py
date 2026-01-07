import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# Configuration de la page
st.set_page_config(
    page_title="Billets 0 Euro Souvenirs",
    page_icon="💶",
    layout="wide"
)

# Titre de l'application
st.title("💶 Carte des Billets 0 Euro Souvenirs")
st.markdown("Découvrez où acheter vos billets souvenirs de 0 euros à travers l'Europe")

# Chargement des données
@st.cache_data
def load_data():
    df = pd.read_csv('data/euro_souvenir_data.csv')
    return df

df = load_data()

# Filtrer les données avec coordonnées valides
df_with_coords = df.dropna(subset=['LATITUDE', 'LONGITUDE'])

# Sidebar pour les filtres
st.sidebar.header("Filtres")

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

# Appliquer les filtres
if selected_pays != 'Tous':
    df_display = df_with_coords[df_with_coords['PAYS'] == selected_pays]
else:
    df_display = df_with_coords

if selected_ville != 'Toutes':
    df_display = df_display[df_display['VILLE'] == selected_ville]

# Statistiques
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total de lieux", len(df))
with col2:
    st.metric("Lieux avec coordonnées", len(df_with_coords))
with col3:
    st.metric("Pays", df['PAYS'].nunique())
with col4:
    st.metric("Villes", df['VILLE'].nunique())

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
    
    # Tableau des données
    st.markdown("### Liste des lieux")
    display_columns = ['TITRE', 'VILLE', 'LIEU', 'ADRESSE', 'TYPE DE LIEU', 'Mode de vente', 'PRIX INDICATIF (€)']
    st.dataframe(
        df_display[display_columns],
        use_container_width=True,
        hide_index=True
    )
else:
    st.warning("Aucun lieu avec coordonnées GPS pour cette sélection")

# Afficher les lieux sans coordonnées
st.markdown("---")
st.markdown("### Lieux sans coordonnées GPS (à compléter)")
df_without_coords = df[df['LATITUDE'].isna() | df['LONGITUDE'].isna()]
if len(df_without_coords) > 0:
    st.info(f"Il y a {len(df_without_coords)} lieux sans coordonnées GPS")
    display_columns_no_coords = ['TITRE', 'PAYS', 'VILLE', 'LIEU', 'ADRESSE']
    st.dataframe(
        df_without_coords[display_columns_no_coords],
        use_container_width=True,
        hide_index=True
    )
