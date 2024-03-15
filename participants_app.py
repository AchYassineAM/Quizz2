import streamlit as st
import pandas as pd

def participants_tab():
    # Charger le fichier Excel contenant les participants
    file_path = "data/participants.xlsx"
    df = pd.read_excel(file_path)

    # Créer un DataFrame temporaire pour stocker les scores et les chronomètres
    scores_df = pd.DataFrame(index=df.index, columns=["Score", "Chronomètre"])

    # Afficher l'image
    st.image("palliers.png", use_column_width=True)

    # Créer un onglet pour afficher les participants
    with st.sidebar:
        st.title("Filtres")
        search_term = st.text_input("Rechercher par nom/prénom", "")
        group_filter = st.selectbox("Filtrer par groupe", df['GROUPE'].unique())
        tente_filter = st.selectbox("Filtrer par tente", df['TENTE'].unique())

    # Filtrer les données en fonction des filtres sélectionnés
    filtered_df = df[(df['GROUPE'] == group_filter) & (df['TENTE'] == tente_filter)]
    if search_term:
        filtered_df = filtered_df[filtered_df.apply(lambda row: search_term.lower() in row['NOM'].lower() or search_term.lower() in row['PRENOM'].lower(), axis=1)]

    # Afficher les résultats dans le tableau avec des champs de saisie pour les scores et les chronomètres
    for index, row in filtered_df.iterrows():
        with st.beta_expander(f"{row['NOM']} {row['PRENOM']}"):
            score_input = st.number_input("Score", key=f"score_{index}", value=scores_df.loc[index, "Score"] if not pd.isna(scores_df.loc[index, "Score"]) else 0)
            chronometer_input = st.number_input("Chronomètre (en minutes)", key=f"chronometer_{index}", value=scores_df.loc[index, "Chronomètre"] if not pd.isna(scores_df.loc[index, "Chronomètre"]) else 0)
            scores_df.loc[index, "Score"] = score_input
            scores_df.loc[index, "Chronomètre"] = chronometer_input

    # Afficher les informations détaillées lorsque l'utilisateur sélectionne un participant
    selected_index = st.table_cursor_click_select(data=filtered_df)
    if selected_index is not None:
        selected_row = filtered_df.iloc[selected_index]
        st.write("Informations du participant:")
        st.write(f"Nom: {selected_row['NOM']}")
        st.write(f"Prénom: {selected_row['PRENOM']}")
        st.write(f"Groupe: {selected_row['GROUPE']}")
        st.write(f"Palier: {selected_row['PALIER']}")
        st.write(f"Tente: {selected_row['TENTE']}")
        st.write(f"Score: {scores_df.loc[selected_index, 'Score']}")
        st.write(f"Chronomètre: {scores_df.loc[selected_index, 'Chronomètre']} minutes")

    # Bouton de téléchargement du fichier CSV
    st.write("")  # Ajouter un espace entre le tableau et le bouton de téléchargement
    if st.button("Télécharger les résultats au format CSV"):
        st.write("Téléchargement en cours...")
        download_link = create_download_link(filtered_df, file_type='csv', file_name='resultats_participants.csv')
        st.markdown(download_link, unsafe_allow_html=True)

def create_download_link(df, file_type, file_name):
    if file_type == 'csv':
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()  # Encodage en base 64 pour la compatibilité avec HTML
        href = f'<a href="data:file/csv;base64,{b64}" download="{file_name}">Cliquez ici pour télécharger</a>'
    elif file_type == 'xlsx':
        xlsx = df.to_excel(index=False)
        b64 = base64.b64encode(xlsx).decode()  # Encodage en base 64 pour la compatibilité avec HTML
        href = f'<a href="data:file/xlsx;base64,{b64}" download="{file_name}">Cliquez ici pour télécharger</a>'
    return href
