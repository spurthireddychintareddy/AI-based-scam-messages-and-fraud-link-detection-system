import streamlit as st
import pickle
import re

st.title("🚨 Scam Message Detector")

# Load model
import os
import pickle

base_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(base_dir, 'model.pkl')

with open(model_path, 'rb') as f:
    model = pickle.load(f)
vectorizer = pickle.load(open('vectorizer.pkl', 'rb'))

user_input = st.text_area("Enter message or URL:")

# Function to detect suspicious URLs
def check_url(url):
    suspicious_words = ["login", "verify", "bank", "update", "free", "win"]

    if any(word in url.lower() for word in suspicious_words):
        return "⚠️ Suspicious URL"

    if "http" in url and len(url) > 30:
        return "⚠️ Possibly Suspicious Link"

    return "✅ Looks Safe"

if st.button("Check"):
    if user_input.strip() == "":
        st.warning("Please enter something")
    else:
        # If input looks like a URL
        if "http" in user_input:
            result = check_url(user_input)
            if "⚠️" in result:
                st.error(result)
            else:
                st.success(result)

        else:
            data = vectorizer.transform([user_input])
            prediction = model.predict(data)

            if prediction[0] == 1:
                st.error("⚠️ Scam Message!")
            else:
                st.success("✅ Safe Message!")