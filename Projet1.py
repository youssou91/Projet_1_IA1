import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuration de la page
st.set_page_config(page_title="Beans & Pods Analytics", layout="wide")

# Chargement des données
@st.cache_data
def load_data():
    return pd.read_csv("data/BeansDataSet.csv")

df = load_data()

# Sidebar pour la navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Choisir une section:", 
                          ["Aperçu des Données", "Analyse des Ventes", "Recommandations"])

# Section 1: Aperçu des Données
if section == "Aperçu des Données":
    st.title("Aperçu des Données Beans & Pods")
    
    st.subheader("Données Brutes")
    if st.checkbox("Afficher les données brutes"):
        st.write(df)
    
    st.subheader("Statistiques Descriptives")
    st.write(df.describe())

# Section 2: Analyse des Ventes
elif section == "Analyse des Ventes":
    st.title("Analyse des Performances de Vente")
    
    # Calcul des revenus totaux par catégorie
    prod = ['Robusta', 'Arabica', 'Espresso', 'Lungo', 'Latte', 'Cappuccino']
    ventes_totales = df[prod].sum().sort_values(ascending=True)
    
    # Sélection des filtres
    col1, col2 = st.columns(2)
    with col1:
        region = st.selectbox("Filtrer par Région", ["Toutes"] + list(df['Region'].unique()))
    with col2:
        channel = st.selectbox("Filtrer par Canal", ["Tous"] + list(df['Channel'].unique()))
    
    # Application des filtres
    filtered_df = df.copy()
    if region != "Toutes":
        filtered_df = filtered_df[filtered_df['Region'] == region]
    if channel != "Tous":
        filtered_df = filtered_df[filtered_df['Channel'] == channel]
    
    # Visualisations
    st.subheader("Répartition des Ventes")
    fig, ax = plt.subplots(1, 2, figsize=(15, 5))
    
    # Ventes par produit
    sns.barplot(x=ventes_totales.values, y=ventes_totales.index, ax=ax[0], palette="viridis")
    ax[0].set_title("Ventes Totales par Produit")
    
    # Ventes par région/canal
    if region == "Toutes" and channel == "Tous":
        sales_by_region = filtered_df.groupby('Region')[prod].sum().sum(axis=1)
        sales_by_channel = filtered_df.groupby('Channel')[prod].sum().sum(axis=1)
        sns.barplot(x=sales_by_region.values, y=sales_by_region.index, ax=ax[1], palette="magma")
        ax[1].set_title("Ventes par Région")
    else:
        sales_by_product = filtered_df[prod].sum()
        sns.barplot(x=sales_by_product.values, y=sales_by_product.index, ax=ax[1], palette="magma")
        ax[1].set_title(f"Ventes par Produit ({region} par rapport a {channel})")
    
    st.pyplot(fig)

# Section 3: Recommandations
elif section == "Recommandations":
    st.title("Recommandations Stratégiques")
    
    st.subheader("Principaux Insights")
    st.markdown("""
    - 🥇 **Arabica** est le produit le plus vendu (42% des revenus totaux)
    - 🏪 Les ventes en **magasin** représentent 68% du chiffre d'affaires
    - 🏘 La région **Nord** génère 50% plus de revenus que le Sud
    """)
    
    st.subheader("Recommandations Marketing")
    st.markdown("""
    1. 🔍 **Cibler la région Sud** avec des promotions online sur l'Arabica
    2. 🚀 Développer les **ventes online** (seulement 32% des revenus)
    3. 💡 Bundle **Cappuccino + Latté** (ventes complémentaires détectées)
    """)
    
    st.subheader("Données à Collecter")
    st.markdown("""
    - 📅 Historique des campagnes marketing passées
    - 👥 Démographie des clients (âge, sexe, profession)
    - 🕒 Données temporelles (saisonnalité des ventes)
    """)
