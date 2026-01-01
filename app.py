import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from config import CONFIG
from datetime import datetime, timedelta
from io import BytesIO
import hashlib


def hash_password(password):
    return hashlib.sha256(str.encode(password)).hexdigest()


# Initialisation de l'état de connexion
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

def login():
    st.session_state['logged_in'] = True

def logout():
    st.session_state['logged_in'] = False
    


    
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    st.title("🔐 Connexion")
    user = st.text_input("Utilisateur")
    pw = st.text_input("Mot de passe", type="password")
    if st.button("Se connecter"):
        # Le hash ci-dessous correspond au mot de passe "1234"
        hashed_pw = "02b7ad7649946264047dda4b5184a68fb7cf4dee230ed71e7923f2fa5e58780d"

        if user == "admin" and hash_password(pw) == hashed_pw:
            login()
            st.rerun()
        else:
            st.error("Identifiants incorrects")
    st.stop() # Bloque l'affichage du dashboard


    

# --- CONFIGURATION PAGE ---
st.set_page_config(
    page_title="Fintech Analytics Pro", 
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "Fintech Analytics Pro - Dashboard de suivi des transactions"
    }
)

# --- STYLE CSS MODERNE ---
st.markdown("""
    <style>
    /* Thème général */
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    }
    
    /* Métriques */
    [data-testid="stMetricValue"] {
        font-size: 32px;
        font-weight: 700;
        background: linear-gradient(135deg, #4ECDC4 0%, #44A08D 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 14px;
        color: #B8B8D1;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1.2px;
    }
    
    [data-testid="stMetricDelta"] {
        font-size: 14px;
    }
    
    /* Cards personnalisées */
    .metric-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 25px;
        border: 1px solid rgba(255,255,255,0.1);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        transition: transform 0.3s ease;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
        border-right: 1px solid rgba(78, 205, 196, 0.2);
    }
    
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stMultiSelect label,
    [data-testid="stSidebar"] .stDateInput label,
    [data-testid="stSidebar"] .stTextInput label {
        color: #4ECDC4 !important;
        font-weight: 600;
        font-size: 14px;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(255,255,255,0.05);
        padding: 10px;
        border-radius: 15px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 55px;
        background-color: transparent;
        border-radius: 10px;
        color: #B8B8D1;
        font-weight: 600;
        font-size: 15px;
        padding: 0 24px;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: rgba(0, 245, 160, 0.1);
        color: #00F5A0;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #4ECDC4 0%, #44A08D 100%);
        color: #1a1a2e !important;
    }
    
    /* Boutons */
    div.stButton > button {
        width: 100%;
        border-radius: 12px;
        background: linear-gradient(135deg, #4ECDC4 0%, #44A08D 100%);
        color: #1a1a2e;
        font-weight: 700;
        font-size: 16px;
        padding: 12px 24px;
        border: none;
        box-shadow: 0 4px 15px 0 rgba(78, 205, 196, 0.3);
        transition: all 0.3s ease;
    }
    
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px 0 rgba(78, 205, 196, 0.4);
    }
    
    /* Dataframe */
    [data-testid="stDataFrame"] {
        background-color: rgba(255,255,255,0.05);
        border-radius: 15px;
        border: 1px solid rgba(78, 205, 196, 0.2);
    }
    
    /* Titres */
    h1 {
        background: linear-gradient(135deg, #4ECDC4 0%, #44A08D 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 48px !important;
        font-weight: 800 !important;
        margin-bottom: 30px !important;
    }
    
    h2, h3 {
        color: #E8E8F5;
        font-weight: 700;
    }
    
    /* Alertes */
    .stAlert {
        border-radius: 12px;
        border-left: 4px solid;
        backdrop-filter: blur(10px);
    }
    
    /* Info boxes */
    .info-box {
        background: linear-gradient(135deg, rgba(78, 205, 196, 0.15) 0%, rgba(68, 160, 141, 0.15) 100%);
        border-left: 4px solid #4ECDC4;
        padding: 20px;
        border-radius: 10px;
        margin: 15px 0;
    }
    
    .warning-box {
        background: linear-gradient(135deg, rgba(255, 183, 77, 0.15) 0%, rgba(255, 152, 0, 0.15) 100%);
        border-left: 4px solid #FFB74D;
        padding: 20px;
        border-radius: 10px;
        margin: 15px 0;
    }
    
    .danger-box {
        background: linear-gradient(135deg, rgba(239, 83, 80, 0.15) 0%, rgba(229, 57, 53, 0.15) 100%);
        border-left: 4px solid #EF5350;
        padding: 20px;
        border-radius: 10px;
        margin: 15px 0;
    }
    
    /* Divider */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(78, 205, 196, 0.3), transparent);
        margin: 40px 0;
    }
    </style>
    """, unsafe_allow_html=True)

FILE_MAP = {
    "MoneyGramFacture": "MoneyGramFacture_cleaned.csv",
    "MoneyGramTr": "MoneyGramTr_cleaned.csv",
    "RIA": "RIA_cleaned (1).csv",
    "SmallWorld": "SmallWorld_cleaned.csv",
    "Western": "Western_cleaned.csv"
}

# --- CHARGEMENT & NETTOYAGE ---
@st.cache_data(ttl=3600)
def load_data(name):
    df = pd.read_csv(FILE_MAP[name])
    conf = CONFIG[name]
    rename_map = {
        conf['date']: 'Date', 
        conf['montant']: 'Montant', 
        conf['id']: 'ID_Transaction', 
        conf['devise']: 'Devise', 
        conf['commission']: 'Commission'
    }
    if conf['pays'] and conf['pays'] in df.columns: 
        rename_map[conf['pays']] = 'Pays'
    
    df_clean = df.rename(columns=rename_map)
    df_clean['Date'] = pd.to_datetime(df_clean['Date'], errors='coerce')
    df_clean['Montant'] = pd.to_numeric(df_clean['Montant'], errors='coerce').fillna(0)
    df_clean['Commission'] = pd.to_numeric(df_clean['Commission'], errors='coerce').fillna(0)
    
    valid_cols = [c for c in ['Date', 'Montant', 'Pays', 'ID_Transaction', 'Devise', 'Commission'] 
                  if c in df_clean.columns]
    return df_clean[valid_cols].dropna(subset=['Date'])

# Chargement Global avec gestion d'erreurs
@st.cache_data(ttl=3600)
def load_all_data():
    all_dfs = []
    for name in FILE_MAP.keys():
        try:
            temp = load_data(name)
            temp['Prestataire'] = name
            all_dfs.append(temp)
        except Exception as e:
            st.sidebar.warning(f"⚠️ Erreur chargement {name}")
    return pd.concat(all_dfs, ignore_index=True) if all_dfs else pd.DataFrame()

full_df = load_all_data()

# --- SIDEBAR MODERNE ---
with st.sidebar:
    st.markdown("### 🚀 **Horizon Transfert**")
    st.markdown("---")
    
    option = st.selectbox(
        "📊 Type d'analyse",
        ["🌐 Vue Globale"] + [f"🏢 {name}" for name in FILE_MAP.keys()],
        index=0
    )
    
    # Nettoyer le nom de l'option
    if option == "🌐 Vue Globale":
        selected_option = "Global"
    else:
        selected_option = option.replace("🏢 ", "")
    
    st.markdown("---")
    search_id = st.text_input("🔍 Rechercher ID / MTCN", placeholder="Entrez un ID...")
    
    st.markdown("---")
    st.markdown("### 📅 **Filtres Avancés**")
    
    pays_list = sorted(full_df['Pays'].dropna().unique()) if 'Pays' in full_df.columns else []
    selected_pays = st.multiselect("🌍 Pays de destination", pays_list)
    
    col1, col2 = st.columns(2)
    with col1:
        date_min = full_df['Date'].min() if not full_df.empty else datetime.now()
    with col2:
        date_max = full_df['Date'].max() if not full_df.empty else datetime.now()
    
    date_range = st.date_input(
        "📆 Période d'analyse",
        [date_min, date_max],
        min_value=date_min,
        max_value=date_max
    )
    
    st.markdown("---")
    st.markdown("### ℹ️ **Informations**")
    st.info(f"📁 **{len(FILE_MAP)}** sources de données  \n💾 **{len(full_df):,}** transactions totales")
    
    if st.sidebar.button("🚪 Déconnexion"):
        logout()

# --- LOGIQUE FILTRAGE ---
working_df = full_df if selected_option == "Global" else load_data(selected_option)
mask = pd.Series([True] * len(working_df))

if selected_pays and 'Pays' in working_df.columns: 
    mask &= working_df['Pays'].isin(selected_pays)
if len(date_range) == 2: 
    mask &= (working_df['Date'].dt.date >= date_range[0]) & (working_df['Date'].dt.date <= date_range[1])
if search_id: 
    mask &= working_df['ID_Transaction'].astype(str).str.contains(search_id, case=False, na=False)

final_df = working_df[mask]

# --- HEADER AVEC ICÔNE ---
col_header1, col_header2 = st.columns([3, 1])
with col_header1:
    st.title(f"📊 Rapport {selected_option}")
    st.markdown(f"*dernière connexion: {datetime.now().strftime('%d/%m/%Y à %H:%M')}*")

# --- KPI CARDS AMÉLIORÉES ---
st.markdown("### 📈 Indicateurs Clés de Performance")

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    total_montant = final_df['Montant'].sum()
    delta_montant = (total_montant / full_df['Montant'].sum() * 100) if not full_df.empty and full_df['Montant'].sum() > 0 else 0
    st.metric(
        "💰 Volume Total",
        f"{total_montant:,.0f} FCFA",
        f"{delta_montant:.1f}% du total"
    )

with kpi2:
    nb_transactions = len(final_df)
    delta_tx = (nb_transactions / len(full_df) * 100) if not full_df.empty else 0
    st.metric(
        "🔢 Transactions",
        f"{nb_transactions:,}",
        f"{delta_tx:.1f}% du total"
    )

with kpi3:
    total_commission = final_df['Commission'].sum()
    st.metric(
        "📈 Commissions",
        f"{total_commission:,.0f} FCFA",
        f"{final_df['Commission'].mean():.0f} moy."
    )

with kpi4:
    marge = (total_commission / total_montant * 100) if total_montant != 0 else 0
    st.metric(
        "🎯 Marge Nette",
        f"{marge:.2f}%",
        "Rentabilité"
    )

st.markdown("---")

# --- ONGLETS AVEC ANALYSES ---
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Tendances & Prévisions",
    "🚩 Alertes & Fraude",
    "🌍 Analyse Géographique",
    "💎 Rentabilité"
])

with tab1:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("#### 📊 Évolution du Volume de Transactions")
        daily = final_df.groupby('Date')['Montant'].sum().reset_index().sort_values('Date')
        
        if len(daily) > 7:
            daily['Prévision'] = daily['Montant'].rolling(window=7).mean()
            daily['Tendance'] = daily['Montant'].rolling(window=3).mean()
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=daily['Date'], y=daily['Montant'],
                mode='lines+markers',
                name='Volume Réel',
                line=dict(color='#4ECDC4', width=3),
                marker=dict(size=6, color='#4ECDC4')
            ))
            fig.add_trace(go.Scatter(
                x=daily['Date'], y=daily['Prévision'],
                mode='lines',
                name='Prévision (7j)',
                line=dict(color='#44A08D', width=2, dash='dash')
            ))
            
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#E8E8F5'),
                xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)'),
                yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)'),
                hovermode='x unified',
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("⚠️ Données insuffisantes pour les prévisions (minimum 7 jours requis)")
    
    with col2:
        st.markdown("#### 🔮 Prévision")
        if len(daily) > 7:
            next_day_forecast = daily['Prévision'].iloc[-1]
            st.markdown(f"""
            <div class="info-box">
                <h3 style="color: #4ECDC4; margin: 0;">
                    {next_day_forecast:,.0f} FCFA
                </h3>
                <p style="color: #B8B8D1; margin: 5px 0 0 0;">
                    Besoin estimé pour demain
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            avg_7d = daily['Montant'].tail(7).mean()
            avg_30d = daily['Montant'].tail(30).mean() if len(daily) >= 30 else daily['Montant'].mean()
            
            st.markdown("##### 📊 Statistiques")
            st.metric("Moyenne 7j", f"{avg_7d:,.0f}")
            st.metric("Moyenne 30j", f"{avg_30d:,.0f}")
            
            trend = "↗️ Hausse" if avg_7d > avg_30d else "↘️ Baisse"
            st.info(f"Tendance: **{trend}**")

with tab2:
    st.markdown("### 🔍 Détection d'Anomalies")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🆔 Doublons d'ID de Transaction")
        dupes = final_df[final_df.duplicated('ID_Transaction', keep=False)]
        if not dupes.empty:
            st.markdown(f"""
            <div class="danger-box">
                <h3 style="color: #EF5350; margin: 0;">⚠️ {len(dupes)} doublons détectés</h3>
                <p style="margin: 10px 0 0 0;">Action requise: vérification immédiate</p>
            </div>
            """, unsafe_allow_html=True)
            st.dataframe(
                dupes.sort_values('Montant', ascending=False),
                use_container_width=True,
                height=300
            )
        else:
            st.markdown("""
            <div class="info-box">
                <h3 style="color: #4ECDC4; margin: 0;">✅ Aucun doublon</h3>
                <p style="margin: 10px 0 0 0;">Toutes les transactions sont uniques</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### 💰 Transactions Exceptionnelles (> 1M)")
        big_transactions = final_df[final_df['Montant'] > 1000000]
        if not big_transactions.empty:
            st.markdown(f"""
            <div class="warning-box">
                <h3 style="color: #FFB74D; margin: 0;">⚡ {len(big_transactions)} alertes</h3>
                <p style="margin: 10px 0 0 0;">Montants inhabituellement élevés</p>
            </div>
            """, unsafe_allow_html=True)
            st.dataframe(
                big_transactions.sort_values('Montant', ascending=False),
                use_container_width=True,
                height=300
            )
        else:
            st.markdown("""
            <div class="info-box">
                <h3 style="color: #4ECDC4; margin: 0;">✅ Aucune anomalie</h3>
                <p style="margin: 10px 0 0 0;">Tous les montants sont dans les normes</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Analyse supplémentaire
    st.markdown("---")
    st.markdown("#### 📊 Distribution des Montants")
    fig_hist = px.histogram(
        final_df, 
        x='Montant', 
        nbins=50,
        title="Répartition des montants de transaction",
        color_discrete_sequence=['#4ECDC4']
    )
    fig_hist.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#E8E8F5'),
        xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)'),
        height=300
    )
    st.plotly_chart(fig_hist, use_container_width=True)

with tab3:
    if 'Pays' in final_df.columns and not final_df['Pays'].isna().all():
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("#### 🌍 Répartition par Pays")
            rep_pays = final_df.groupby('Pays')['Montant'].sum().sort_values(ascending=False)
            
            fig_pie = px.pie(
                names=rep_pays.index,
                values=rep_pays.values,
                hole=0.5,
                color_discrete_sequence=['#4ECDC4', '#44A08D', '#95E1D3', '#F38181', '#AA96DA', '#FCBAD3', '#FFFFD2']
            )
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            fig_pie.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#E8E8F5'),
                height=400,
                showlegend=True
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            st.markdown("#### 📊 Top 10 Destinations")
            top_pays = final_df.groupby('Pays').agg({
                'Montant': 'sum',
                'ID_Transaction': 'count',
                'Commission': 'sum'
            }).sort_values('Montant', ascending=False).head(10)
            
            top_pays.columns = ['Volume Total', 'Nb Transactions', 'Commissions']
            top_pays['Marge %'] = (top_pays['Commissions'] / top_pays['Volume Total'] * 100).round(2)
            
            st.dataframe(
                top_pays.style.format({
                    'Volume Total': '{:,.0f}',
                    'Nb Transactions': '{:,}',
                    'Commissions': '{:,.0f}',
                    'Marge %': '{:.2f}%'
                }),
                use_container_width=True,
                height=400
            )
    else:
        st.info("ℹ️ Données géographiques non disponibles pour cette sélection")

with tab4:
    st.markdown("### 💎 Analyse de Rentabilité par Prestataire")
    
    if 'Prestataire' in final_df.columns:
        comm_analysis = final_df.groupby('Prestataire').agg({
            'Montant': 'sum',
            'Commission': 'sum',
            'ID_Transaction': 'count'
        }).reset_index()
        
        comm_analysis.columns = ['Prestataire', 'Volume', 'Commission', 'Nb Transactions']
        comm_analysis['Efficacité %'] = (comm_analysis['Commission'] / comm_analysis['Volume'] * 100).round(2)
        comm_analysis['Commission Moy'] = (comm_analysis['Commission'] / comm_analysis['Nb Transactions']).round(0)
        comm_analysis = comm_analysis.sort_values('Efficacité %', ascending=False)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            fig_bar = px.bar(
                comm_analysis,
                x='Prestataire',
                y='Efficacité %',
                title='Efficacité par Prestataire (%)',
                color='Efficacité %',
                color_continuous_scale=['#95E1D3', '#4ECDC4', '#44A08D'],
                text='Efficacité %'
            )
            fig_bar.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
            fig_bar.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#E8E8F5'),
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)'),
                height=400
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        
        with col2:
            st.markdown("#### 📊 Tableau Comparatif")
            st.dataframe(
                comm_analysis.style.format({
                    'Volume': '{:,.0f}',
                    'Commission': '{:,.0f}',
                    'Nb Transactions': '{:,}',
                    'Efficacité %': '{:.2f}%',
                    'Commission Moy': '{:,.0f}'
                }).background_gradient(subset=['Efficacité %'], cmap='Greens'),
                use_container_width=True,
                height=400
            )
    else:
        st.info("ℹ️ Analyse de rentabilité disponible uniquement en vue globale")

# --- FOOTER & EXPORT ---
st.markdown("---")
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    st.markdown("### 📥 Exporter les Données")
    
with col2:
    csv = final_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        "📄 Télécharger CSV",
        data=csv,
        file_name=f"rapport_{selected_option}_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

with col3:
    # Correction de l'export Excel
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        final_df.to_excel(writer, index=False, sheet_name='Données')
    excel_data = output.getvalue()
    
    st.download_button(
        "📊 Télécharger Excel",
        data=excel_data,
        file_name=f"rapport_{selected_option}_{datetime.now().strftime('%Y%m%d')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

st.markdown("### 📋 Aperçu des Données Filtrées")
st.dataframe(
    final_df.head(100),
    use_container_width=True,
    height=400
)

# Footer info
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #B8B8D1; padding: 20px;">
    <p>🚀 <strong>Fintech Analytics Pro</strong> | Dashboard de suivi des transactions de transfert d'argent</p>
    <p style="font-size: 12px;">Développé avec ❤️ par Mohamed Mbacke  | © 2026</p>
    <p style="font-size: 12px;">Email: mbackem500@gmail.com</p>
</div>
""", unsafe_allow_html=True)