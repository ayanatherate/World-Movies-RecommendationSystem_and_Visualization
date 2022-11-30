import pandas as pd
import numpy as np
import streamlit as st
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
from streamlit_extras.no_default_selectbox import selectbox
import tmdbsimple as tmdb



tmdb.API_KEY = '8265bd1679663a7ea12ac168da84d2e8'
tmdb.REQUESTS_SESSION = requests.Session()
search = tmdb.Search()

st.set_page_config(page_title='Movie Recommendation App', page_icon="https://cdn-icons-png.flaticon.com/512/1038/1038100.png", layout="centered", initial_sidebar_state="auto", menu_items=None)
hide_streamlit_style2= '''
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.css-1rs6os {visibility: hidden;}
.css-17ziqus {visibility: hidden;}
</style>

'''
st.markdown(hide_streamlit_style2, unsafe_allow_html=True) 


page_bg_img = '''
<style>
.stApp {
background-image: url("https://i.ibb.co/t869zV7/istockphoto-1124347647-170667a.jpg");
background-size: cover;
}
</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)
st.title('Movies Recommender')
st.subheader('Let AI decide for you, what to watch next!')

def take_inp():
    inp=st.text_input(label='Enter a movie name, you just watched:')
    num_movies=st.select_slider('Select number of recommendations you want',options=[i for i in range(16)])
    inp=inp.lower()
    inp=re.sub('[^a-zA-Z0-9 ]','',inp)
    return inp,num_movies



data=pd.read_csv(r"https://raw.githubusercontent.com/ayanatherate/World-Movies-RecommendationSystem-and-Visualization/main/Recommendation_Database/Recommendations_data.csv")

#print(data['recommendaions'])

match_names=[data['normalized_names'][i] for i in range(len(data))]

def map_names(name):
    movie_index=''
    
    for i in range(len(match_names)):
        if name==match_names[i]:
            movie_index=i
            break        
    return movie_index

inp,num_movies=take_inp()

if len(inp)==0 and num_movies==0:
    st.stop()
else:
    movie_index_=map_names(inp)

recommendation=[]

try:
    for i in data['recommendaions'][movie_index_].split(','):
        recommendation.append(int(i))
except:
    st.write('Oops! Seems like this movie is not listed on our Database. You can also try checking out the official name of the movie from Google and try again!')
    selected_movie=selectbox('You can also choose a movie from the list below', match_names)
    movie_index_=map_names(selected_movie)
    for i in data['recommendaions'][movie_index_].split(','):
        recommendation.append(int(i))
    
  
    
st.caption('Here are your recommended movie lists:')   
num_made_recommends=0

#randomize_imgs=['data:image/png;base64,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','
                
for i in recommendation:
    if num_made_recommends<num_movies:
        temp= data[data['id']==i]
        st.write('----------------------')
        time.sleep(1)
        st.title(temp['title'].values[0])
        
        #scraping from tmdb web
        to_search_str='+'.join(temp['title'].values[0].split(' '))
        url=f'https://www.themoviedb.org/search?query={to_search_str}'
        r=requests.get(url)
        src=r.content
        soup = BeautifulSoup(src, 'lxml')
        thumb = soup.find("img", class_ = "poster")
        try:
            movie_srch=' '.join(temp['title'].values[0].split(' '))
            response = search.movie(query=movie_srch)
            path=f"https://image.tmdb.org/t/p/original/{search.results[0]['poster_path']}"
                                
            
            st.image(path,width=200)
        except:
            st.image('data:image/png;base64,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')
            #st.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')
        
        #st.image+AGb32huPHb/Rqp9MNlepMh9knnP96o3cjxsdykMvDKfz5VXll8wpeWVAQWgy0OVptOj3n20JRs+nH9MVKtW8SxR7VXGSTxX2sVlHO4iWUDIBKnK5qjc6Pp1zO01xYwSSuu1nZASR8a0c18dlRGZvqqM5od/DaDSWVjZ3bxWsEUCDA2ouM1ptphNgyqAJgxdD/aq+iwi5vJbphkFs5NaOt30mn2El3FD4qxDc6g87fMj89s0dtPXReOPtL/AEpWMi31iCvJA2stcBBcxZWFQVzkb/KsPS9VNuwvIjuif94oGPnii2012zniDRtG3xPIrcmSpQbRQhs3kl3zjLfyjtXTUrlLOHZuG48sfSvOrdSWNlEWeVQfIDuaBbrVLjV52lMvgQg5we5qpMfiwzyvZ16xDy6I88hxuddq+mawtPsbqTS40to5Hd7l/aX6oG1DnPka0b/NzHsMjug4UH/FGHQcNq1hNEihJQ2HXdksMcH0FBLL6xJ5fhyxr36gJt41t3IYLkD+LzPvo16FiVVnYAkFtoY+eK93nRVtPdtNlsMckBsCt+ysY9NtRHEANowAKzyn7IxOSqi7lR3YD4mpXNIF25cbmPJJqUvQB4rL6kneLT9qHG9gp+FfalXD+ka5cLulxrDYxCPjIyasTIskMiOMqyEEHzBFSpUfS4/BPadI65COVBXHH+Ky7m6lds52H7HFfalbI8Otmirbo5xZZgzMWOfM5rZtUGwseSO1SpVSH+MlReWNVzj+Fc15tLmayuEuLZykq85B7+h94qVKA1pJ2mHOla5d3MNmZRETKpLEL7jit+47fMVKlIl08l5MVHLJL9PtSpUoBB//2Q==')
        st.caption(f'Released on : {temp.release_date.values[0]}, Rating: {temp.vote_average.values[0]}')
        print()
        st.write(temp['overview'].values[0])
        print()
        print()
        print()
        
        num_made_recommends+=1

    


    
    

    
    



    
    
    
