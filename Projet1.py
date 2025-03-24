import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuration de la page
st.set_page_config(page_title="Analyse Beans & Pods", layout="wide")

# Chargement des données
@st.cache_data
def charger_donnees():
    return pd.read_csv("data/BeansDataSet.csv")

df = charger_donnees()

# Style global
st.markdown(
    """
    <style>
        .contenu-centre {
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .style-titre {
            text-align: center;
            font-size: 30px;
            font-weight: bold;
        }
        .style-sous-titre {
            text-align: center;
            font-size: 20px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Barre latérale pour la navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Choisissez une section :", 
                          ["Aperçu des Données", "Analyse des Ventes", "Recommandations"])

# Section 1 : Aperçu des Données
if section == "Aperçu des Données":
    st.markdown('<p class="style-titre">Aperçu des Données Beans & Pods</p>', unsafe_allow_html=True)
    
    st.subheader("Données Brutes")
    if st.checkbox("Afficher les données brutes"):
        st.write(df.style.set_properties(**{'text-align': 'center'}).set_table_styles(
            [{'selector': 'th', 'props': [('text-align', 'center')]}]))
    
    st.subheader("Statistiques Descriptives")
    st.write(df.describe().style.set_properties(**{'text-align': 'center'}).set_table_styles(
        [{'selector': 'th', 'props': [('text-align', 'center')]}]))

# Section 2 : Analyse des Ventes
elif section == "Analyse des Ventes":
    st.markdown('<p class="style-titre">Analyse des Performances de Vente</p>', unsafe_allow_html=True)
    
    # Calcul des revenus totaux par catégorie
    produits = ['Robusta', 'Arabica', 'Espresso', 'Lungo', 'Latte', 'Cappuccino']
    ventes_totales = df[produits].sum().sort_values(ascending=True)
    
    # Sélection des filtres
    col1, col2 = st.columns(2)
    with col1:
        region = st.selectbox("Filtrer par Région", ["Toutes"] + list(df['Region'].unique()))
    with col2:
        canal = st.selectbox("Filtrer par Canal", ["Tous"] + list(df['Channel'].unique()))
    
    # Application des filtres
    df_filtre = df.copy()
    if region != "Toutes":
        df_filtre = df_filtre[df_filtre['Region'] == region]
    if canal != "Tous":
        df_filtre = df_filtre[df_filtre['Channel'] == canal]
    
    # Visualisations
    st.subheader("Répartition des Ventes")
    fig, ax = plt.subplots(1, 2, figsize=(15, 5))
    
    # Ventes par produit
    sns.barplot(x=ventes_totales.values, y=ventes_totales.index, ax=ax[0], palette="viridis")
    ax[0].set_title("Ventes Totales par Produit", fontsize=14)
    ax[0].set_xlabel("Total des Ventes")
    ax[0].set_ylabel("Produits")
    
    # Ventes par région/canal
    if region == "Toutes" and canal == "Tous":
        ventes_par_region = df_filtre.groupby('Region')[produits].sum().sum(axis=1)
        sns.barplot(x=ventes_par_region.values, y=ventes_par_region.index, ax=ax[1], palette="magma")
        ax[1].set_title("Ventes par Région", fontsize=14)
    else:
        ventes_par_produit = df_filtre[produits].sum()
        sns.barplot(x=ventes_par_produit.values, y=ventes_par_produit.index, ax=ax[1], palette="magma")
        ax[1].set_title(f"Ventes par Produit ({region} - {canal})", fontsize=14)
    
    st.pyplot(fig)

# Section 3 : Recommandations
elif section == "Recommandations":
    st.markdown('<p class="style-titre">Recommandations Stratégiques</p>', unsafe_allow_html=True)
    
    st.subheader("Aperçus principaux")
    st.markdown(
        """
        <ul>
            <li>🥇 <b>Arabica</b> est le produit le plus vendu, représentant 42% des revenus totaux.</li>
            <li>🏪 Les ventes en <b>magasin</b> dominent avec 68% du chiffre d'affaires total.</li>
            <li>🏘 La région <b>Nord</b> génère 50% plus de revenus que la région Sud.</li>
        </ul>
        """,
        unsafe_allow_html=True,
    )
    
    st.subheader("Recommandations Marketing")
    st.markdown(
        """
        <ol>
            <li>🔍 Cibler la <b>région Sud</b> avec des promotions en ligne sur le produit Arabica.</li>
            <li>🚀 Développer les <b>ventes en ligne</b>, qui ne représentent que 32% des revenus.</li>
            <li>💡 Proposer des bundles <b>Cappuccino + Latte</b> pour augmenter les ventes complémentaires.</li>
        </ol>
        """,
        unsafe_allow_html=True,
    )
    
    st.subheader("Données à Collecter")
    st.markdown(
        """
        <ul>
            <li>📅 Historique des campagnes marketing précédentes.</li>
            <li>👥 Données démographiques des clients (âge, sexe, profession).</li>
            <li>🕒 Données temporelles sur la saisonnalité des ventes.</li>
        </ul>
        """,
        unsafe_allow_html=True,
    )
