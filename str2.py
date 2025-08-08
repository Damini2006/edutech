import streamlit as st
import requests
import google.generativeai as genai

#Set Gemini API key
genai.configure(api_key="")
model = genai.GenerativeModel(model_name="gemini-2.0-flash"
st.title("📚 Edutech Learning Platform")

selection = st.sidebar.selectbox("Choose the page", ["Submit Learning Data", "Recommendation", "Feedback", "Chat Tutor"])

# Submit Learning Data Page
if selection == "Submit Learning Data":
    st.header("📄 Submit Learning Form")
    with st.form("submit_form"):
        user_id = st.number_input("User Id", min_value=1, step=1)
        topic = st.selectbox("Topics", ["Algebra", "Trigonometry", "Probability", "Statistics", "Calculus", "Limits", "Functions", "Derivative", "Linear Equations"])
        e_spent = st.slider("Time Spent (minutes)", 1, 100)  # Changed from time_spent to e_spent
        quiz_score = st.slider("Quiz Score", 0, 100)
        preference = st.selectbox("Learning Preference", ["Visual", "Text", "Audio", "Interactive"])
        feedback = st.text_area("Feedback")
        rating = st.slider("Rating", 1, 5)
        submit = st.form_submit_button("Submit")
        
        if submit:
            datas = {
                "user_id": user_id,
                "topic": topic,
                "e_spent": e_spent,  # FIX: backend expects this key, not time_spent
                "quiz_score": quiz_score,
                "preference": preference,
                "feedback": feedback,
                "rating": rating
            }
            try:
                res = requests.post("http://127.0.0.1:8000/submit", json=datas)
                response = res.json()
                st.write("📡 Response from API:", response)
                st.success(response.get("message", " Submitted successfully."))
            except Exception as e:
                st.error(f"API Error: {e}")

#  Feedback Sentiment Analysis Page
elif selection == "Feedback":
    st.header("🧠 Feedback Sentiment Analysis")
    feedback = st.text_area("Enter your feedback:")
    if st.button("Submit Feedback"):
        try:
            res = requests.post("http://127.0.0.1:8000/feedback", json={"feedback": feedback})
            result = res.json()
            st.write("🧠 Sentiment Result:")
            st.write(result.get("Feedback", "No sentiment found."))
        except Exception as e:
            st.error(f"API Error: {e}")

#  AI Chat Tutor Page
elif selection == "Chat Tutor":
    st.header("🤖 AI Tutor ChatBot")
    prmt = st.text_input("Ask your doubt:")
    chat = model.start_chat(history=[])
    if st.button("Clear the Doubt"):
        if prmt.strip() != "":
            res = chat.send_message(prmt)
            st.write("Tutor Response:")
            st.write(res.text)
        else:
            st.warning("Please enter a question.")

# Recommendation Page
elif selection == "Recommendation":
    user_id = st.number_input("Enter the User Id", min_value=1, step=1)
    if st.button("Get Recommendations"):
        try:
            res = requests.get(f"http://127.0.0.1:8000/get_recommend/{user_id}")
            response = res.json()
            st.write("📡 API Response:", response)

            # Use correct key – assume "recommend" is correct, not "recomand"
            recommendations = response.get("recommend") or response.get("recomand")
            if recommendations:
                st.write("🎯 Recommended Topics:")
                st.write(recommendations)
            else:
                st.warning("No recommendations found or invalid key in API response.")
        except Exception as e:
            st.error(f"API Error: {e}")

