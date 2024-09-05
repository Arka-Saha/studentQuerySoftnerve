import streamlit as st
from openai import OpenAI, APIConnectionError

# using llama model via api, as my system doesnt have a gpu for running llm independently 
openai = OpenAI(
    api_key="<api key>", 
    base_url="https://cloud.olakrutrim.com/v1",
)

# function to get response from llm 
def get_resp(q):
    chat_completion = openai.chat.completions.create(
    model="Meta-Llama-3-8B-Instruct",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {'role':"user", 'content':"help me with info about books .. student managemnt "},
        {"role": "user", "content": q}
    ],
    frequency_penalty= 0, # Optional, Defaults to 0. Range: -2 to 2
    logit_bias= {2435: -100, 640: -100},
    logprobs= True, # Optional, Defaults to false
    top_logprobs= 2, # Optional. Range: 0 to 50
    n= 1, # Optional, Defaults to 1
    presence_penalty= 0, # Optional, Defaults to 0. Range: -2 to 2
    response_format= { "type": "text" }, # Optional, Defaults to text
    stop= None, # Optional, Defaults to null. Can take up to 4 sequences where the API will stop generating further tokens.
    stream= False, # Optional, Defaults to false
    temperature= 0, # Optional, Defaults to 1. Range: 0 to 2
    top_p= 1 # Optional, Defaults to 1. We generally recommend altering this or temperature but not both.
)

    # returns the generated answer
    return chat_completion.choices[0].message.content

# setting title heading on the frontend
st.title("Student Query Management System")

# text input box in the frontend page
query = st.text_input("Ask your book or topic-related question:")

if st.button("Submit"):
    if query:
        try:
        with st.spinner("Fetching answer..."):
                answer = get_resp(query)
            st.write(f"Answer: {answer}")
        except APIConnectionError:
            # when internet is not avaialbe it gives api error
            st.write(f"An error occured, check your internet before using.")
        except Exception as e:
            st.write(f"An error occured, please retry or try after sometimes. Error: {e.__cause__}")

    else:
        st.write("Please enter a question.")

