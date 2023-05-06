import re
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Embedding, LSTM, Dense
import streamlit as st
import pymongo

# function for connecting Database 
def dataConnectivity():
    conn_str = "mongodb://project3343:rsproject@ac-gjl3aea-shard-00-00.sop0wqm.mongodb.net:27017,ac-gjl3aea-shard-00-01.sop0wqm.mongodb.net:27017,ac-gjl3aea-shard-00-02.sop0wqm.mongodb.net:27017/?ssl=true&replicaSet=atlas-xr3bsz-shard-0&authSource=admin&retryWrites=true&w=majority"
    client = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=5000)
    try:
        client.server_info()
    except Exception:
        print("Unable to connect to the server.")
    db = client.resumeDBt
    return db

# define a function to autofill the form fields
def autofill(username_box, email_box, resume_box, user_data):
    username_box.text_input("Username", value=user_data["name"])
    email_box.text_input("Email", value=user_data["emailId"])
    resume_box.text_area("Resume", value=user_data["description"], height=200)

def extract_cgpa(text):
    #CGPA or cgpa 
    cgpa_regex = r'CGPA\s*[:|;]?\s*(\d+(?:\.\d+)?)'
    match = re.search(cgpa_regex, text, re.IGNORECASE)
    if match:
        return float(match.group(1))
    else:
        return None

def extract_degree(text):
    degree_regex = r'B\.Tech|BCA|M\.Tech'
    match = re.search(degree_regex, text, re.IGNORECASE)
    if match:
        return match.group(0)
    else:
        return None

def extract_years_of_experience(text):
    experience_regex = r'(\d+)\s+(?:years?|yrs?)\s+of\s+experience'
    match = re.search(experience_regex, text, re.IGNORECASE)
    if match:
        return int(match.group(1))
    else:
        return None
    
# create a list of dictionaries to store the user data
db = dataConnectivity()
users = list(db.users.find({}))


def app():

    ####Side Bar####

    st.title("Job Application Screening App")
    # create the sidebar with the list of usernames
    st.sidebar.title("Candidates List")
    user_selection = st.sidebar.radio("Select a candidate:", [user["name"] for user in users])
    user_data = next(user for user in users if user["name"] == user_selection)
    # create the form fields and autofill them with the user data
    username_box = st.empty()
    email_box = st.empty()
    resume_box = st.empty()
    autofill(username_box, email_box, resume_box, user_data)

    ####JD dropbox###

    db = dataConnectivity()
    jdList = db.jd.find({})
    dropDisplay = []
    for jds in jdList:
        dropDisplay.append(jds["name"])
    option = st.selectbox("Select Job Description",(dropDisplay))
    st.write(option)
    selectedJD = db.jd.find_one({"name":option})
    job_description = selectedJD["desc"]
    st.write(job_description)
    resume = user_data["description"]

    ####Eligibility Check####
    if st.button("Check Eligibility"):
        resume_cgpa = extract_cgpa(resume)
        job_description_cgpa = extract_cgpa(job_description)
        resume_degree = extract_degree(resume)
        resume_years_of_experience = extract_years_of_experience(resume)

        if not resume_degree:
            st.error("The candidate's degree is not eligible for the selected role position in this company.")
        elif not resume_cgpa or not job_description_cgpa:
            st.warning("CGPA not found in either job description or resume.")
        else:
            job_description_years = int(re.findall(r'\d+', job_description)[0])

            # Check if the candidate has enough experience
            if not resume_years_of_experience:
                st.warning("Years of experience not found in the resume.")
            elif resume_years_of_experience < job_description_years:
                st.warning("The candidate is not qualified because it has less years of experience")
            else:
                # Check if candidate's CGPA is greater than or equal to JD CGPA
                if resume_cgpa >= job_description_cgpa:
                    tokenizer = Tokenizer(num_words=5000)
                    tokenizer.fit_on_texts([job_description, resume])
                    job_description_seq = tokenizer.texts_to_sequences([job_description])
                    resume_seq = tokenizer.texts_to_sequences([resume])
                    job_description_seq = pad_sequences(job_description_seq, maxlen=5)
                    resume_seq = pad_sequences(resume_seq, maxlen=5)

                    labels = np.array([0, 1])
                    X_train = np.concatenate([job_description_seq, resume_seq])
                    y_train = np.repeat(labels, job_description_seq.shape[0])
                    X_test = X_train
                    y_test = y_train

                    model = Sequential()
                    model.add(Embedding(input_dim=5000, output_dim=50, input_length=5))
                    model.add(LSTM(100))
                    model.add(Dense(1, activation='sigmoid'))
                    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
                    model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=15, batch_size=1)
                    loss, accuracy = model.evaluate(X_test, y_test)
                    #st.write(f"Neural Network Model Loss: {loss:.3f}, Accuracy: {accuracy:.3f}")
                    predictions = model.predict(X_test)
                    score = predictions[1] * 100
                    st.write(score)
                    vectorizer = CountVectorizer()
                    job_description_vector = vectorizer.fit_transform([job_description])
                    clean_text_vector = vectorizer.transform([resume])
                    similarity = cosine_similarity(job_description_vector, clean_text_vector)
                    st.write(similarity)
                    if score > 50 and similarity[0][0] >= 0.5:
                        st.success("The candidate is qualified.")
                        st.write(f"{user_data['name']}, resume matches the job description!")
                    else:
                        st.warning("The candidate is not qualified.")
                        st.write(f"Sorry {user_data['name']}, resume does not match the job description.")
                else:
                    st.warning("The candidate has LESS CGPA so tata!")
if __name__ == '__main__':
    app()