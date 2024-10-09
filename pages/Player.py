import streamlit as st
import pandas as pd
from ScoutDatabase import load_data

st.set_page_config(page_title="ScoutDatabase", page_icon="⚽", layout="wide")

performance = load_data()[1]
if 'data' in st.session_state:
    data = st.session_state['data']
else:
    st.write("Os dados não foram carregados. Por favor, volte para a Página 1 para carregar os dados.")

st.subheader('Player👤')

player_name = st.selectbox('Player Name',sorted(list(data['Short Name'].unique())))
data = data[data['Short Name'] == player_name]
performance = pd.merge(left=data, right=performance, how='left', left_on='Player ID', right_on='Player ID')
performance_df = performance[['Season','Tournament','Games','Wins','Draws','Losses','Goal Difference','Minutes','Starting XI','Used Sub','Goals Scored','Assists','Own Goals','Yellow Cards','Double Yellows','Red Cards']]

col1, col2, col3 = st.columns([4,1,1])
with col1:
    st.subheader(data['Full Name'].iloc[0])
    st.write(f"Age: {data['Age'].iloc[0]}")
    # st.write(f"Birth Date: {dados['Birth Date'].iloc[0].strftime('%Y/%m/%d')}")
    st.write(f"Height: {int(data['Height (cm)'].iloc[0])}cm")
    st.write(f"Position: {data['Position'].iloc[0]}")
    st.write(f"Market Value: {data['Market Value'].iloc[0]}")


# Colocar as imagens na terceira coluna (canto superior direito)
with col2:
    st.image(data['Team img url'].iloc[0], use_column_width='auto')

with col3:
    st.html(f'''<div style="text-align: center;">
            <img src="{data['Player img url'].iloc[0]}" 
                 style="max-width:100%; border-radius: 25px; border: 3px solid black; margin-bottom: 10px;">
            <img src="{data['flag_img_url'].iloc[0]}" 
                 style="max-width:50%; border-radius: 5px;">
        </div>''')
st.dataframe(performance_df)
#st.text_area('Scout Report')

# col1, col2, col3 = st.columns([1,4,1])
# with col2:
#    st.video('https://www.youtube.com/watch?v=aONi70TalZ8')