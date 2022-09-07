import ast

import pandas as pd
import requests
import streamlit as st

"""
# Sentiment Analysis
"""

sentence = st.text_input('Type text inside the box', "This is awesome!")


def format_response(response: str) -> pd.DataFrame:
    # Convert text to dictionary object
    response_dict = ast.literal_eval(response)

    df = pd.DataFrame.from_dict(response_dict.items())
    df.columns = ["sentiment", "sentiment score"]
    df.replace("neg", "Negative", inplace=True)
    df.replace("pos", "Positive", inplace=True)
    df.replace("neu", "Neutral", inplace=True)
    df.replace("compound", "Compound", inplace=True)
    df.set_index('sentiment', inplace=True)

    return df


def get_response(query: str) -> pd.DataFrame:
    """
    Snychronous call to REST Api
    :param query:
    :return dictionary:
    """
    protocol = "http://"
    url = "sentiment-server-alb-171396013.eu-west-1.elb.amazonaws.com"
    path = "/predict"
    param = "?q="
    api_url = protocol + url + path + param + query

    return format_response(requests.get(api_url).text)


st.bar_chart(get_response(sentence))
st.write("The compound score is the sum of positive, negative & neutral scores. It is then normalized between"
         " -1 (most extreme negative) and +1 (most extreme positive).")


"#### Contact Developer"

st.markdown("Programmed with ❤️ by [Muhammad Ahsan](https://www.linkedin.com/in/muhammad-ahsan/)")
