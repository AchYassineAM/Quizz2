import streamlit as st
import pandas as pd
import base64

def participants_tab():
    # Charger le fichier Excel contenant les participants
    file_path = "participants.xlsx"
    df = pd.read_excel(file_path)

    # Créer un DataFrame temporaire pour stocker les scores et le temps total
    scores_df = pd.DataFrame(index=df.index, columns=["Score", "Temps_total"])

    # Afficher l'image
    st.image("palliers.png", use_column_width=True)

    # Créer un onglet pour afficher les participants
    with st.sidebar:
        st.title("Filtres")
        search_term = st.text_input("Rechercher par nom/prénom", "")
        unique_groups = ['Tous'] + df['GROUPE'].unique().tolist()  # Ajouter 'Tous' à la liste des groupes uniques
        group_filter = st.selectbox("Filtrer par groupe", unique_groups)

    # Filtrer les données en fonction des filtres sélectionnés
    if group_filter == 'Tous':
        filtered_df = df
    else:
        filtered_df = df[df['GROUPE'] == group_filter]

    if search_term:
        filtered_df = filtered_df[filtered_df.apply(lambda row: search_term.lower() in row['NOM'].lower() or search_term.lower() in row['PRENOM'].lower(), axis=1)]

    # Afficher les résultats dans le tableau avec des champs de saisie pour les scores et le temps total
    for index, row in filtered_df.iterrows():
        with st.expander(f"{row['NOM']} {row['PRENOM']}"):
            score_input = st.number_input("Score", key=f"score_{index}", value=scores_df.loc[index, "Score"] if not pd.isna(scores_df.loc[index, "Score"]) else 0)
            minutes_input = st.number_input("Minutes", key=f"minutes_{index}", value=0)
            seconds_input = st.number_input("Secondes", key=f"seconds_{index}", value=0, min_value=0, max_value=59, step=1)
            milliseconds_input = st.number_input("Millisecondes", key=f"milliseconds_{index}", value=0, min_value=0, max_value=999, step=1)
            
            # Concaténer les valeurs de temps total au format mm:ss:SSS
            total_time_input = f"{minutes_input:02d}:{seconds_input:02d}:{milliseconds_input:03d}"
            scores_df.loc[index, "Temps_total"] = total_time_input  # Mettre à jour la valeur du temps total

            # Mettre à jour la valeur du score
            scores_df.loc[index, "Score"] = score_input

    # Afficher les informations détaillées lorsque l'utilisateur sélectionne un participant
    st.write("Informations du participant:")
    details_df = filtered_df.copy()  # Créer une copie du DataFrame filtré pour y ajouter les colonnes Score et Temps_total
    details_df["Score"] = scores_df["Score"]
    details_df["Temps_total"] = scores_df["Temps_total"]
    clicked_index = st.write(details_df)

    # Bouton de téléchargement du fichier CSV
    st.write("")  # Ajouter un espace entre le tableau et le bouton de téléchargement
    if st.button("Télécharger les résultats au format CSV"):
        st.write("Téléchargement en cours...")
        download_link = create_download_link(details_df, file_type='csv', file_name='resultats_participants.csv')
        st.markdown(download_link, unsafe_allow_html=True)

def create_download_link(df, file_type, file_name):
    if file_type == 'csv':
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()  # Encodage en base 64 pour la compatibilité avec HTML
        href = f'<a href="data:text/csv;base64,{b64}" download="{file_name}">Cliquez ici pour télécharger</a>'
        return href  # Assurez-vous de retourner la valeur de href

participants_tab()
