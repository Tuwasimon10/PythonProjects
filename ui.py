import pandas as pd
import joblib
import streamlit as st
import numpy as np

def load():
    model = joblib.load('flower.pkl')
    return model

def main():
    st.title("Iris Flower Species Prediction")

    st.write("""
    ### Flower Species Predictor:
    """)

    # User input form for Iris features
    sepal_length = st.number_input('Sepal Length)
    sepal_width = st.number_input('Sepal Width)
    petal_length = st.number_input('Petal Length)
    petal_width = st.number_input('Petal Width)

    # Load the saved model
    model = load()

    # Convert user input to a numpy array
    features = np.array([[sepal_length, sepal_width, petal_length, petal_width]])

    if st.button("Predict"):
        # Make a prediction
        prediction = model.predict(features)

        # Map prediction to class name
        species = {0: 'Setosa', 1: 'Versicolor', 2: 'Virginica'}
        predicted_species = species[prediction[0]]

        st.write(f"The predicted species is: **{predicted_species}**")

main()
