import streamlit as st
from WebScraping import remove_player


st.set_page_config('Remove Player', page_icon="⚽")

st.title('Remove Player')

player_name = st.selectbox('Choose the player to remove', st.session_state['data']['Short Name'].unique())

df_player_info = st.session_state.data[st.session_state.data['Short Name']==player_name]

st.subheader(f"{df_player_info['Full Name'].iloc[0]} - {df_player_info['Team'].iloc[0]}")
st.write(f"Position: {df_player_info['Position'].iloc[0]}")
st.image([df_player_info['Player img url'].iloc[0],df_player_info['Team img url'].iloc[0]], use_column_width='auto')

st.dataframe(df_player_info)

st.session_state['player_id'] = df_player_info['Player ID'].iloc[0]

remove = st.button('Remove Player')
if remove:
  remove_player(st.session_state.player_id)
  del st.session_state.player_id
  st.cache_data.clear()
  st.success('Player removed successfully')