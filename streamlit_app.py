import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from datetime import datetime
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import time

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

# Initialiser les variables de session pour les coordonnées géocodées
if 'geocoded_lat' not in st.session_state:
    st.session_state.geocoded_lat = ''
if 'geocoded_lon' not in st.session_state:
    st.session_state.geocoded_lon = ''
if 'geocode_message' not in st.session_state:
    st.session_state.geocode_message = ''

def is_valid_value(value):
    """Vérifie si une valeur est valide (non NaN, non None, non vide)"""
    if pd.isna(value):
        return False
    if value is None:
        return False
    if isinstance(value, str):
        value_clean = value.strip().lower()
        if not value_clean or value_clean in ['nan', 'null', 'none', '--', '']:
            return False
    return True

def geocode_address_simple(pays, ville, lieu, adresse):
    """Essaie de géocoder une adresse en utilisant plusieurs stratégies"""
    geolocator = Nominatim(user_agent="euro-souvenir-app/1.0")
    queries = []
    
    # Stratégie 1: Adresse complète
    if is_valid_value(adresse):
        parts = [adresse.strip()]
        if is_valid_value(ville):
            parts.append(ville.strip())
        if is_valid_value(pays):
            parts.append(pays.strip())
        if len(parts) >= 2:
            queries.append(", ".join(parts))
    
    # Stratégie 2: Lieu + ville + pays
    if is_valid_value(lieu):
        parts = [lieu.strip()]
        if is_valid_value(ville):
            parts.append(ville.strip())
        if is_valid_value(pays):
            parts.append(pays.strip())
        if len(parts) >= 2:
            queries.append(", ".join(parts))
    
    # Stratégie 3: Ville + pays seulement
    if is_valid_value(ville) and is_valid_value(pays):
        queries.append(f"{ville.strip()}, {pays.strip()}")
    
    # Essayer chaque requête
    for query in queries:
        try:
            location = geolocator.geocode(query, timeout=10)
            if location:
                return location.latitude, location.longitude, f"✅ Coordonnées trouvées pour : {query}"
        except (GeocoderTimedOut, GeocoderServiceError):
            time.sleep(1)
            continue
    
    # Construire le message d'erreur avec suggestions
    missing = []
    if not is_valid_value(adresse):
        missing.append("Adresse")
    if not is_valid_value(lieu):
        missing.append("Lieu")
    if not is_valid_value(ville):
        missing.append("Ville")
    if not is_valid_value(pays):
        missing.append("Pays")
    
    if missing:
        return None, None, f"❌ Coordonnées non trouvées. Veuillez renseigner : {', '.join(missing)}"
    else:
        return None, None, "❌ Coordonnées non trouvées. Vérifiez l'exactitude de l'adresse."

# Chargement des données
@st.cache_data
def load_data():
    df = pd.read_csv('data/shop.csv')
    return df

@st.cache_data
def load_reference_data():
    """Charge les données de référence de tous les billets"""
    df_ref = pd.read_csv('data/master_data.csv')
    return df_ref

def save_data(df):
    df.to_csv('data/shop.csv', index=False)
    st.cache_data.clear()  # Effacer le cache pour recharger les nouvelles données

df = load_data()
df_reference = load_reference_data()

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
if st.sidebar.button("➕ Ajouter un lieu", type="primary", width="stretch"):
    st.session_state.page = 'ajouter'
    st.rerun()

if st.session_state.page == 'ajouter' and st.sidebar.button("🗺️ Retour à la carte", width="stretch"):
    st.session_state.page = 'carte'
    st.rerun()

# PAGE D'AJOUT DE LIEU
if st.session_state.page == 'ajouter':
    st.title("➕ Ajouter un nouveau lieu")
    st.markdown("Remplissez les informations ci-dessous pour ajouter un nouveau lieu de vente de billets 0 euros.")
    
    # Lien vers le guide avec image
    with st.expander("📖 Comment trouver le CODE et le MILLÉSIME sur votre billet ?"):
        st.markdown("""
        ### 🔍 Où trouver les informations ?
        
        **CODE (4 lettres)** : En bas du billet, généralement en petits caractères  
        Exemple : `UEBU`, `XEJE`, `NEAA`
        
        **MILLÉSIME (année-numéro)** : À côté du code  
        Exemple : `2025-6`, `2024-1`, `2023-3`
        
        Sur l'image ci-dessous :
        - 🔵 **Souligné en bleu** = CODE (4 lettres)
        - 🟢 **Souligné en vert** = MILLÉSIME (année-numéro)
        """)
        st.image('data/guide.jpg', caption='Où trouver le CODE et le MILLÉSIME', width=600)
    
    # Initialiser les variables de session pour stocker les infos du billet
    if 'billet_info' not in st.session_state:
        st.session_state.billet_info = None
    
    # Section 1 : Identification du billet
    st.markdown("### 1️⃣ Identifier votre billet")
    col_code, col_milesime, col_search = st.columns([2, 2, 1])
    
    with col_code:
        code_input = st.text_input("CODE * (4 lettres)", placeholder="Ex: UEBU", key="code_input")
    with col_milesime:
        milesime_input = st.text_input("MILLÉSIME * (année-numéro)", placeholder="Ex: 2025-6", key="milesime_input")
    with col_search:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔍 Rechercher", type="primary"):
            if code_input and milesime_input:
                # Construire l'ID complet
                billet_id = f"{code_input}_{milesime_input}"
                
                # Chercher dans le DataFrame de référence
                billet_match = df_reference[df_reference['#'] == billet_id]
                
                if not billet_match.empty:
                    st.session_state.billet_info = billet_match.iloc[0].to_dict()
                    st.success(f"✅ Billet trouvé : {st.session_state.billet_info['TITLE']}")
                else:
                    st.session_state.billet_info = None
                    st.error("❌ Billet non trouvé. Vérifiez le CODE et le MILLÉSIME.")
            else:
                st.warning("⚠️ Veuillez entrer le CODE et le MILLÉSIME")
    
    # Afficher les infos du billet trouvé
    if st.session_state.billet_info:
        st.info(f"""
        **Billet identifié :**  
        📌 {st.session_state.billet_info['TITLE']}  
        🌍 {st.session_state.billet_info['CITY']}, {st.session_state.billet_info['COUNTRY']}  
        🔗 [Plus d'infos]({st.session_state.billet_info['INFO_LINK']})
        """)
    
    st.markdown("---")
    st.markdown("### 2️⃣ Informations du lieu de vente et billet")
    
    # Variables temporaires pour stocker les valeurs du formulaire avant géocodage
    if 'temp_lieu' not in st.session_state:
        st.session_state.temp_lieu = ''
    if 'temp_adresse' not in st.session_state:
        st.session_state.temp_adresse = ''
    
    with st.form("add_location_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📍 Localisation")
            
            # Toujours afficher les champs grisés avec message si vides
            if st.session_state.billet_info:
                titre = st.text_input("Titre *", value=st.session_state.billet_info['TITLE'], disabled=True)
                code = st.text_input("Code", value=code_input, disabled=True)
                milesime = st.text_input("Millésime", value=milesime_input, disabled=True)
                pays = st.text_input("Pays *", value=st.session_state.billet_info['COUNTRY'], disabled=True)
                ville = st.text_input("Ville *", value=st.session_state.billet_info['CITY'], disabled=True)
            else:
                titre = st.text_input("Titre *", value="", disabled=True, help="⚠️ Remplissez d'abord la section 1️⃣ ci-dessus")
                code = st.text_input("Code", value="", disabled=True, help="⚠️ Remplissez d'abord la section 1️⃣ ci-dessus")
                milesime = st.text_input("Millésime", value="", disabled=True, help="⚠️ Remplissez d'abord la section 1️⃣ ci-dessus")
                pays = st.text_input("Pays *", value="", disabled=True, help="⚠️ Remplissez d'abord la section 1️⃣ ci-dessus")
                ville = st.text_input("Ville *", value="", disabled=True, help="⚠️ Remplissez d'abord la section 1️⃣ ci-dessus")
            
            lieu = st.text_input("Lieu *", placeholder="Ex: Tour Eiffel", key="form_lieu")
            adresse = st.text_area("Adresse *", placeholder="Ex: Av. Gustave Eiffel, 75007 Paris", key="form_adresse")
            
        with col2:
            st.subheader("ℹ️ Détails du lieu")
            
            # Mode de vente - liste déroulante des valeurs existantes
            modes_vente = [''] + sorted(df['Mode de vente'].dropna().unique().tolist())
            mode_vente = st.selectbox("Mode de vente", modes_vente)
            
            # Type de lieu - liste déroulante des valeurs existantes
            types_lieu = [''] + sorted(df['TYPE DE LIEU'].dropna().unique().tolist())
            type_lieu = st.selectbox("Type de lieu", types_lieu)
            
            commentaire = st.text_area("Commentaire", placeholder="Informations supplémentaires...")
            prix = st.text_input("Prix indicatif (€)", placeholder="Ex: 2,00 €")
            
            image = st.text_input("🖼️ URL Image du lieu", placeholder="https://exemple.com/image.jpg")
            
            # Champs de coordonnées (peuvent être remplis manuellement ou par géocodage)
            col_lat, col_lon = st.columns(2)
            with col_lat:
                latitude_input = st.text_input(
                    "Latitude", 
                    value=st.session_state.geocoded_lat if st.session_state.geocoded_lat else "",
                    placeholder="Ex: 48.857298",
                    key="form_latitude"
                )
            with col_lon:
                longitude_input = st.text_input(
                    "Longitude", 
                    value=st.session_state.geocoded_lon if st.session_state.geocoded_lon else "",
                    placeholder="Ex: 2.302035",
                    key="form_longitude"
                )
        
        st.markdown("---")
        col_submit, col_geo, col_cancel = st.columns([2, 2, 1])
        
        with col_geo:
            geocode_btn = st.form_submit_button("🌍 Ajouter coordonnées GPS", width="stretch")
        
        with col_submit:
            submitted = st.form_submit_button("💾 Enregistrer", type="primary", width="stretch")
        with col_cancel:
            cancelled = st.form_submit_button("❌ Annuler", width="stretch")
        
        # Géocodage si le bouton est cliqué
        if geocode_btn:
            if lieu or adresse:
                with st.spinner("🔍 Recherche des coordonnées GPS..."):
                    lat, lon, message = geocode_address_simple(pays, ville, lieu, adresse)
                    st.session_state.geocoded_lat = str(lat) if lat else ''
                    st.session_state.geocoded_lon = str(lon) if lon else ''
                    st.session_state.geocode_message = message
                    st.rerun()
            else:
                st.session_state.geocode_message = "⚠️ Veuillez remplir au moins le champ Lieu ou Adresse"
                st.rerun()
        
        if submitted:
            # Validation
            if not titre or not pays or not ville or not lieu or not adresse:
                st.error("⚠️ Les champs Titre, Pays, Ville, Lieu et Adresse sont obligatoires!")
            else:
                # Créer une nouvelle ligne
                date_ajout = datetime.now().strftime("%d/%m/%Y")
                
                # Construire l'ID avec CODE_MILESIME si disponible
                if code and milesime:
                    new_id = f"{code}_{milesime}"
                else:
                    # Sinon utiliser un compteur
                    max_num = 0
                    for idx in df['#'].dropna():
                        if isinstance(idx, str) and '_' in idx:
                            continue
                        try:
                            num = int(idx)
                            if num > max_num:
                                max_num = num
                        except:
                            continue
                    new_id = max_num + 1                
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
                    'LATITUDE': float(latitude_input) if latitude_input else None,
                    'LONGITUDE': float(longitude_input) if longitude_input else None
                }
                
                # Ajouter la nouvelle ligne au DataFrame
                df_new = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                
                # Sauvegarder
                save_data(df_new)
                
                st.success(f"✅ Le lieu '{titre}' a été ajouté avec succès!")
                st.balloons()
                
                # Réinitialiser les infos du billet et géocodage
                st.session_state.billet_info = None
                st.session_state.geocoded_lat = ''
                st.session_state.geocoded_lon = ''
                st.session_state.geocode_message = ''
                
                # Revenir à la carte après 2 secondes
                st.info("🔄 Retour à la carte...")
                import time
                time.sleep(2)
                st.session_state.page = 'carte'
                st.rerun()
        
        if cancelled:
            st.session_state.billet_info = None
            st.session_state.geocoded_lat = ''
            st.session_state.geocoded_lon = ''
            st.session_state.geocode_message = ''
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
        # Construire le HTML du popup avec image si disponible
        popup_html = f"""
        <div style="width: 350px; font-family: Arial, sans-serif;">
            <h4 style="margin-bottom: 10px; color: #1f77b4;">{row['TITRE']}</h4>
        """
        
        # Ajouter l'image si disponible
        if pd.notna(row['IMAGE']) and str(row['IMAGE']).strip():
            popup_html += f"""
            <img src="{row['IMAGE']}" style="width: 100%; max-height: 200px; object-fit: cover; border-radius: 5px; margin-bottom: 10px;">
            """
        
        popup_html += f"""
            <div style="line-height: 1.6;">
                <b>🏢 Lieu:</b> {row['LIEU']}<br>
                <b>🏙️ Ville:</b> {row['VILLE']}<br>
                <b>📍 Adresse:</b> {row['ADRESSE']}<br>
                <b>🏛️ Type:</b> {row['TYPE DE LIEU']}<br>
                <b>💳 Mode de vente:</b> {row['Mode de vente']}<br>
                <b>📅 Millésime:</b> {row['MILESIME']}<br>
        """
        
        if pd.notna(row['PRIX INDICATIF (€)']):
            popup_html += f"<b>💰 Prix indicatif:</b> {row['PRIX INDICATIF (€)']}<br>"
        
        if pd.notna(row['COMMENTAIRE']):
            popup_html += f"<b>ℹ️ Commentaire:</b> {row['COMMENTAIRE']}<br>"
        
        popup_html += """
            </div>
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
            popup=folium.Popup(popup_html, max_width=370),
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
