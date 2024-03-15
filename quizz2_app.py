import streamlit as st
import pandas as pd
from participants_app import participants_tab

# Charger le fichier Excel contenant les 99 questions et réponses
file_path = "99Questions.xlsx"
df = pd.read_excel(file_path)



# Créer une barre de navigation pour les onglets
st.title("Quiz App - Générer 10 Questions")
menu = ["Générateur", "Participants"]
choice = st.sidebar.selectbox("Onglets", menu)

# Afficher le contenu correspondant à l'onglet sélectionné
if choice == "Générateur":
    st.write("Contenu de la page principale...")
elif choice == "Participants":
    with st.beta_container():
        participants_tab()


# Filtre pour la tranche de questions à retirer
range_filter = st.slider("Tranche de questions à retirer (de 1 à 99)", 1, 99, (1, 99))

# Filtres pour les questions spécifiques à inclure
question1_filter = st.number_input("Question 1 à inclure (de 0 à 99)", min_value=0, max_value=99, step=1)
question2_filter = st.number_input("Question 2 à inclure (de 0 à 99)", min_value=0, max_value=99, step=1)
question3_filter = st.number_input("Question 3 à inclure (de 0 à 99)", min_value=0, max_value=99, step=1)

# Bouton pour générer les questions aléatoires
if st.button("Générer"):
    # Appliquer le filtre pour la tranche de questions à retirer
    filtered_df = df[(df['Numéro'] < range_filter[0]) | (df['Numéro'] > range_filter[1])]

    # Inclure les questions spécifiques à inclure
    questions_to_include = [question1_filter, question2_filter, question3_filter]
    included_df = filtered_df[filtered_df['Numéro'].isin(questions_to_include)]

    # Sélectionner les questions aléatoires nécessaires pour compléter la sélection
    remaining_questions = 10 - included_df.shape[0]
    random_questions = filtered_df[~filtered_df['Numéro'].isin(included_df['Numéro'])].sample(n=remaining_questions, random_state=42)

    # Concaténer les questions sélectionnées
    final_selected_questions = pd.concat([included_df, random_questions])

    # Afficher le tableau résultant
    st.write('<style>table { table-layout: fixed; }</style>', unsafe_allow_html=True)
    st.write('<style>th, td { word-wrap: break-word; }</style>', unsafe_allow_html=True)
    st.write(final_selected_questions[['Numéro', 'Question', 'Réponse']].to_html(escape=False), unsafe_allow_html=True)
else:
    # Afficher le tableau complet si le bouton n'a pas encore été cliqué
    st.write('<style>table { table-layout: fixed; }</style>', unsafe_allow_html=True)
    st.write('<style>th, td { word-wrap: break-word; }</style>', unsafe_allow_html=True)
    st.write(df[['Numéro', 'Question', 'Réponse']].to_html(escape=False), unsafe_allow_html=True)


