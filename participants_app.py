import streamlit as st
import pandas as pd
import base64

def participants_tab():
    # Charger le fichier Excel contenant les participants
    file_path = "participants.xlsx"
    df = pd.read_excel(file_path)

    # Créer un DataFrame temporaire pour stocker les scores et les chronomètres
    scores_df = pd.DataFrame(index=df.index, columns=["Score", "Chronomètre_minutes", "Chronomètre_seconds"])

    # Afficher l'image
    st.image("palliers.png", use_column_width=True)

    # Créer un onglet pour afficher les participants
    with st.sidebar:
        st.title("Filtres")
        search_term = st.text_input("Rechercher par nom/prénom", "")
        group_filter = st.selectbox("Filtrer par groupe", df['GROUPE'].unique())

    # Filtrer les données en fonction des filtres sélectionnés
    filtered_df = df[(df['GROUPE'] == group_filter)]
    if search_term:
        filtered_df = filtered_df[filtered_df.apply(lambda row: search_term.lower() in row['NOM'].lower() or search_term.lower() in row['PRENOM'].lower(), axis=1)]

    # Afficher les résultats dans le tableau avec des champs de saisie pour les scores et les chronomètres
    for index, row in filtered_df.iterrows():
        with st.expander(f"{row['NOM']} {row['PRENOM']}"):
            score_input = st.number_input("Score", key=f"score_{index}", value=scores_df.loc[index, "Score"] if not pd.isna(scores_df.loc[index, "Score"]) else 0)
            minutes_input = st.number_input("Minutes", key=f"chronometer_minutes_{index}", value=scores_df.loc[index, "Chronomètre_minutes"] if not pd.isna(scores_df.loc[index, "Chronomètre_minutes"]) else 0)
            seconds_input = st.number_input("Secondes", key=f"chronometer_seconds_{index}", value=scores_df.loc[index, "Chronomètre_seconds"] if not pd.isna(scores_df.loc[index, "Chronomètre_seconds"]) else 0, min_value=0, max_value=59, step=1)
            milliseconds_input = st.number_input("Millisecondes", key=f"chronometer_milliseconds_{index}", value=scores_df.loc[index, "Chronomètre_milliseconds"] if not pd.isna(scores_df.loc[index, "Chronomètre_milliseconds"]) else 0, min_value=0, max_value=999, step=1)
            chronometer_input = minutes_input * 60 + seconds_input + milliseconds_input / 1000
            scores_df.loc[index, "Chronomètre_minutes"] = minutes_input
            scores_df.loc[index, "Chronomètre_seconds"] = seconds_input

            

    # Afficher les informations détaillées lorsque l'utilisateur sélectionne un participant
    st.write("Informations du participant:")
    clicked_index = st.write(filtered_df)

    if clicked_index is not None:
        selected_row = filtered_df.iloc[clicked_index]
        st.write(f"Nom: {selected_row['NOM']}")
        st.write(f"Prénom: {selected_row['PRENOM']}")
        st.write(f"Groupe: {selected_row['GROUPE']}")
        st.write(f"Palier: {selected_row['PALIER']}")
        st.write(f"Tente: {selected_row['TENTE']}")
        st.write(f"Score: {scores_df.loc[clicked_index, 'Score']}")
        st.write(f"Chronomètre: {scores_df.loc[clicked_index, 'Chronomètre']} minutes")

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
