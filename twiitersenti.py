import streamlit as st
from textblob import TextBlob
import streamlit as st
import pandas as pd
import tweepy
import sys
import pandas as pd

from htbuilder import HtmlElement, div, ul, li, br, hr, a, p, img, styles, classes, fonts
from htbuilder.units import percent, px
from htbuilder.funcs import rgba, rgb


Year_List=[2,3,4,5,6,7,8,9,10]
api_key = "VBvDXjTtyn327kL08S6FiqD0t"
api_key_secret = "U38KIeEZSbzGsis9i46GwaDV4NazoYP0PaRy3P3pr8hk0TE7jy"
access_token = "1404705774400540674-ls6I5Nswv5u8WeBYUltil1fOWgi2iM"
access_token_secret = "SN1c2B85t5FwKWLnvNrkZvuVpokUlhnojblBa3myXhHOB"

st.write("""

# Twitter Sentiment Analysis

""")

st.write("")


def percentage(part, whole):
    return 100 * float(part)/float(whole)

st.sidebar.write("""## Enter values here""")
searchterm = st.sidebar.text_input("Enter the Search Term","Life")
Amount = st.sidebar.number_input("Enter the number",min_value=0,max_value=1000,value=10,step=1)

st.write("""### Tweets: """)
st.write("")
def tweetanalysis(term, amount):
    auth_handler = tweepy.OAuthHandler(consumer_key=api_key, consumer_secret=api_key_secret)
    auth_handler.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth_handler)

    search_term = term
    tweet_amount = amount

    tweets = tweepy.Cursor(api.search, q = search_term, lang = 'en').items(tweet_amount)

    polarity = 0

    positive = 0
    negative = 0
    neutral = 0
    c = 0
    flag = "POSITIVE"

    for tweet in tweets:
        final_text = tweet.text.replace('RT', '')
    
    
        if final_text.startswith(' @'):
            position = final_text.index(':')
            final_text = final_text[position+2:]
        if final_text.startswith('@'):
            position = final_text.index(' ')
            final_text = final_text[position+2:]
        if final_text.startswith('http'):
            position = final_text.index(' ')
            final_text = final_text[position+2:]
            c += 1
        
        st.text(final_text)
        
        
        analysis = TextBlob(final_text)
        tweet_polarity = analysis.polarity

        if tweet_polarity > 0.00:
            positive += 1
        elif tweet_polarity < 0.00:
            negative += 1
        elif tweet_polarity == 0.00:
            neutral += 1
    
        polarity += tweet_polarity
        
    if polarity <= 0.15:
        flag = "NEGATIVE"

    print(polarity)

    print(f'Amount of Positive tweets: {positive}')
    print(f'Amount of Neutral tweets: {neutral}')
    print(f'Amount of Negative tweets: {negative}')
    print(c)
    return(positive,negative,neutral, flag)
    




positive, negative, neutral,flag = tweetanalysis(searchterm, Amount)

st.sidebar.text(f"The polarity of the tweets is: {flag}")


if st.sidebar.checkbox('Show Statistics'):
    st.sidebar.text(f"Positive Tweets: {positive}")
    st.sidebar.text(f"Neutral Tweets: {neutral}")
    st.sidebar.text(f"Negative Tweets: {negative}")




#Footer settings below:
def image(src_as_string, **style):
    return img(src=src_as_string, style=styles(**style))


def link(link, text, **style):
    return a(_href=link, _target="_blank", style=styles(**style))(text)


def layout(*args):

    style = """
    <style>
      # MainMenu {visibility: hidden;}
      footer {visibility: hidden;}
     .stApp { bottom: 105px; }
    </style>
    """

    style_div = styles(
        position="fixed",
        left=0,
        bottom=0,
        margin=px(0, 0, 0, 0),
        width=percent(100),
        color="white",
        text_align="center",
        height="auto",
        opacity=1
    )

    style_hr = styles(
        display="block",
        margin=px(8, 8, "auto", "auto"),
        border_style="inset",
        border_width=px(2)
    )

    body = p()
    foot = div(
        style=style_div
    )(
        hr(
            style=style_hr
        ),
        body
    )

    st.markdown(style, unsafe_allow_html=True)

    for arg in args:
        if isinstance(arg, str):
            body(arg)

        elif isinstance(arg, HtmlElement):
            body(arg)

    st.markdown(str(foot), unsafe_allow_html=True)


def footer():
    myargs = [
        "Made By - Ishan Achinta & Ninad Dekate"
    ]
    layout(*myargs)


if __name__ == "__main__":
    footer()