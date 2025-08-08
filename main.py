from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import random 
from transformers import pipeline


app=FastAPI()

df=pd.read_csv("D:\\PROJECTS\\edutech\\edtech_adaptive_learning_dataset.csv")

class form_inp(BaseModel):
    user_id:int
    topic:str
    time_spent:int
    quiz_score:int
    preference:str
    feedback:str
    rating:int

class feedback(BaseModel):
    feedback:str

@app.post("/sumbit")
def form_submit(data:form_inp):
    global df
    new_data=pd.DataFrame([data.dict()])
    df=pd.concat([df,new_data],ignore_index=True)
    df.to_csv("D:\PROJECTS\edutech\edtech_adaptive_learning_dataset.csv",index=False)
    return {"Message":"Data Submitted"}

@app.get("/get_recommend")
def recommend(userid:int):
    user=df[df["user_id"]==userid]
    if user.empty:
        return {"message":"User Not Found"}
    visited_topics=user["topic"].unique().tolist()
    All_topics=df["topic"].unique().tolist()
    Notvisited=list(set(All_topics)-set(visited_topics))

    rec=random.sample(Notvisited,k=min(3,len(Notvisited)))
    return {"recommend",rec}

@app.post("/feedback")
def feedback_analysis(fb:feedback):
    ml=pipeline("sentiment-analysis")
    res=ml(fb.feedback)
    return {"Feedback":res[0]}