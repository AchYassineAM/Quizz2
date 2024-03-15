import streamlit as st
import pandas as pd
import numpy as np
import openpyxl

# Charger le fichier Excel contenant les 99 questions et réponses
file_path = "99Questions.xlsx"
df = pd.read_excel("99Questions.xlsx")

# Titre de l'application
st.title("Quiz App")

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
    st.write(final_selected_questions[['Numéro', 'Question', 'Réponse']])
else:
    # Afficher le tableau complet si le bouton n'a pas encore été cliqué
    st.write(df[['Numéro', 'Question', 'Réponse']])
