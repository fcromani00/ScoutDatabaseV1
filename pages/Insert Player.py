import pandas as pd
import streamlit as st
from WebScraping import scraping_transfermarkt
from WebScraping import scraping_playmaker
from WebScraping import add_new_player

st.set_page_config('Insert Player', page_icon="⚽")

st.title('Insert Player')
st.write('''Use these sites to insert new players:\n
[Transfermarkt](https://www.transfermarkt.com/)\n
[Playmaker](https://www.playmakerstats.com/)''')

df_player_info = pd.DataFrame()
df_player_performance = pd.DataFrame()

if 'dict_scoutdatabase' not in st.session_state:
    st.session_state['dict_scoutdatabase'] = {
  'Player ID':pd.NA,
  'Short Name': pd.NA,
  'Full Name': pd.NA,
  'Birth Date': pd.NA,
  'Age': pd.NA,
  'Nationality':pd.NA,
  'Citizenship': pd.NA,
  'Team': pd.NA,
  'Position': pd.NA,
  'Market Value': pd.NA,
  'Foot': pd.NA,
  'Height (cm)': pd.NA,
  'Player Agent': pd.NA,
  'Player Agent Link':pd.NA,
  'Contract Expires':pd.NA,
  'On Loan': pd.NA,
  'Loan Contract Expires' : pd.NA,
  'On Loan From': pd.NA,
  'Instagram': pd.NA,
  'Player img url':pd.NA,
  'Team img url':  pd.NA,
  'Transfermarkt Profile': pd.NA,
  'PlaymakerStats Profile': pd.NA
}
dict_scoutdatabase = st.session_state['dict_scoutdatabase']

if 'df_player_performance' not in st.session_state:
  st.session_state['df_player_performance'] = pd.DataFrame()
df_player_performance = st.session_state['df_player_performance']
  
with st.form('form_insert_player'):
  st.write('Use links from the same player in both sites')
  
  link_TF = st.text_input('Player Profile link in Transfermarkt')

  link_PMS = st.text_input('Player Profile link in PlaymakerStats')

  submit = st.form_submit_button("Get Data")
  if submit:
    # try:
      if link_TF != '':
        dict_transfermarkt = scraping_transfermarkt(link_TF)
      if link_PMS != '':
        dict_playmaker, df_player_performance = scraping_playmaker(link_PMS)
        
      dict_scoutdatabase['Player ID'] = dict_playmaker['Player ID']
      
      for key, value in dict_scoutdatabase.items():
        if pd.isna(dict_scoutdatabase[key]) and not pd.isna(dict_transfermarkt[key]):
          dict_scoutdatabase[key] = dict_transfermarkt[key]
        elif pd.isna(dict_scoutdatabase[key]) and not pd.isna(dict_playmaker[key]):
          dict_scoutdatabase[key] = dict_playmaker[key]

      df_player_info = pd.DataFrame([dict_scoutdatabase])

    # except:
    #   st.write('Error: Please check the link and try again')

st.write('---')

st.data_editor(df_player_info,
  column_config={
   "Player img url":st.column_config.ImageColumn("Player", width='small'),
   'Team img url':st.column_config.ImageColumn('Team', width='small'),
   'Player Agent Link':st.column_config.LinkColumn('Player Agent Link',width='small')
},
  hide_index=True)
st.write('---')
st.data_editor(df_player_performance
               ,hide_index=True)

if 'dict_scoutdatabase' in st.session_state:
  st.session_state['dict_scoutdatabase'] = dict_scoutdatabase
  
if 'df_player_performance' in st.session_state:
  st.session_state['df_player_performance'] = df_player_performance

insert = st.button('Insert Player in ScoutDatabase')


if insert:
  add_new_player(st.session_state['dict_scoutdatabase'], st.session_state['df_player_performance'])
  del st.session_state['dict_scoutdatabase']
  del st.session_state['df_player_performance']
  st.cache_data.clear()
  st.success('Player inserted successfully')