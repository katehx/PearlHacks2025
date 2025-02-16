import pandas as pd
import random
from openai import OpenAI
import os
import streamlit as st
import pyautogui
#from dotenv import load_dotenv

df = pd.DataFrame(pd.read_csv('questions.csv'))
if 'count' not in st.session_state:
   st.session_state.count = 0
score_file = open("score.txt", "r+")
score = score_file.read()
def get_question():
    q = random.randint(0, 1379)
    prompt = df.iloc[q]["prompt"]
    A = df.iloc[q]["A"]
    B = df.iloc[q]["B"]
    C = df.iloc[q]["C"]
    D = df.iloc[q]["D"]
    E = df.iloc[q]["E"]
    ra = df.iloc[q]["answer"]
    return prompt, A, B, C, D, E, ra

@st.dialog("Explaination")
def get_explanation(question):
    client = OpenAI(api_key = os.environ.get('OPENAI-KEY'))
    completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a tutor who is very good at explaining history questions, you will be given a question, the answer choices, and the correct answer. Explain why this is the right answer."},
                {"role": "user",
                "content": "Question: " + question}])
    st.write(completion.choices[0].message.content)

@st.dialog("Answer")
def show_answer(answer):
    st.write("The Correct Answer is: " + st.session_state.messages[6])
    if answer[0] == st.session_state.messages[6]:
        st.write("You Answered Correctly! Sprout has more courage!")
        score+=1
        with open("score.txt", "w") as file:
            file.write(score)
    else:
        st.write("Oh no! You Answered Incorrectly. Sprout has lost some courage.")
        score-=1
        with open("score.txt", "w") as file:
            file.write(score)


def main():
    st.title("SproutSmart")
    st.write("Sprout's current courage: " + score)
    if ("messages" not in st.session_state) or (st.session_state.messages == None):
        q=get_question()
        st.session_state.messages = [q[0], q[1], q[2], q[3], q[4], q[5], q[6]]
    form = st.form("Question")
    form.selectbox(st.session_state.messages[0], ("A. " +st.session_state.messages[1], "B. "+st.session_state.messages[2], "C. "+st.session_state.messages[3], "D. "+st.session_state.messages[4], "E. "+st.session_state.messages[5]), index=None,)
    if form.form_submit_button("Check"):
        show_answer()
    if st.button("Explain this Answer"):
        get_explanation(st.session_state.messages[0] + " A. " + st.session_state.messages[1] + " B. " + st.session_state.messages[2] + " C. " + st.session_state.messages[3] + " D. " + st.session_state.messages[4] + " E. " + st.session_state.messages[5] + " Answer: " + st.session_state.messages[6])
    if st.button("Next"):
        pyautogui.hotkey('command', 'r')
        print(st.session_state.messages)


    
    
        

main()

