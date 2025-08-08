import streamlit as st
import requests
import google.generativeai as genai

genai.configure(api_key="AIzaSyDwenD_N4-FX6DA-eDufGsTBT-4XT3ujdE")
model=genai.GenerativeModel(model_name="gemini-2.0-flash")

st.title("Edutech Learning Platform")
selection=st.sidebar.selectbox("Choose the page",["Submit Learning Data","Recommendation","Feedback","chat tutor"])

if selection=="Submit Learning Data":
    st.header("Submit Learning Form")
    with st.form("submit form"):
        user_id=st.number_input("User Id")
        topic=st.selectbox("Topics",["Algebra","Trigonometry","Probability","Statistics","Calculus","Limits","Functions","Derivative","Linear Equations"])
        time_spent=st.slider("Time Spend",1,100)
        quiz_score=st.slider("Quiz_score",0,100)
        preference=st.selectbox("Preference",["Visual","Text","Audio","Interactive"])
        feedback=st.text_area("Feedback")
        rating=st.slider("Ratings",1,5)
        submit=st.form_submit_button("submit")
        if submit:
            datas={
                "user_id":user_id,
                "topic":topic,
                "time_spent":time_spent,
                "quiz_score":quiz_score,
                "preference":preference,
                "feedback":feedback,
                "rating":rating
            }
            res=requests.post("http://127.0.0.1:8000/submit",json=datas)
            st.success(res.json()["message"])

elif(selection=="Feedback"):
    st.header("Feedback Sentiment Analysis")
    feedback=st.text_area("Feedback: ")
    if st.button("submit Feedback"):
        res=requests.post("http://127.0.0.1:8000/feedback",json={"feedback":feedback})
        st.write(res.json()["Feedback"])

elif(selection=="chat tutor"):
    st.header("AI Tutor ChatBot")
    prmt=st.text_input("Ask Your Doubts:")
    chat=model.start_chat(history=[])
    if st.button("Clear The Doubt"):
        res=chat.send_message(prmt)
        st.write("Tutor Response")
        st.write(res.text)

elif selection == "Recommendation":
    userid = st.number_input("Enter the User Id", min_value=1, step=1)
    
    if st.button("Recomand"):
        try:
            res = requests.get(f"http://127.0.0.1:8000/get_recomend/{userid}")
            if res.status_code == 200:
                response = res.json()
                if "recomand" in response:
                    st.write("✅ Recommended Topics:")
                    st.write(response["recomand"])
                else:
                    st.error("❌ Key 'recomand' not found in the API response.")
                    st.json(response)
            else:
                st.error(f"❌ API returned status code: {res.status_code}")
                st.json(res.json())
        except Exception as e:
            st.error(f"🚫 Error: {e}")

