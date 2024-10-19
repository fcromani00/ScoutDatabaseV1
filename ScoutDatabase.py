import streamlit as st
import pandas as pd
from WebScraping import refresh_database
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="ScoutDatabase", page_icon="⚽", layout="wide")#🌎

@st.cache_data
def load_data():
    import pandas as pd
    import streamlit as st
    from streamlit_gsheets import GSheetsConnection

    conn = st.connection("gsheets", type=GSheetsConnection)
    
    flags_df = conn.read(worksheet="flags")
    players_df = conn.read(worksheet="players")
    performance_seasons_df = conn.read(worksheet="performance_seasons")

    
    scoutdatabase_df = pd.merge(left=players_df, right=flags_df, how='left', left_on='Nationality', right_on='country')
    scoutdatabase_df = scoutdatabase_df[
        ['Position','Player img url', 'Short Name','Age','Team img url', 'flag_img_url',  'Team',  'Nationality',
         'Foot', 'On Loan', 'Height (cm)', 'Market Value', 'Birth Date', 'Contract Expires', 'Full Name',
         'On Loan From','Loan Contract Expires', 'Citizenship', 'Player Agent', 'Player Agent Link', 'Instagram', 'Player ID','Transfermarkt Profile', 'PlaymakerStats Profile']]
    return scoutdatabase_df, performance_seasons_df

data, performance_seasons_df = load_data()
raw_data = data.copy()

st.session_state['data'] = data
st.session_state['performance_seasons_df'] = performance_seasons_df

with st.container():

    st.title('ScoutDatabase🌎')
    st.subheader(f'{len(raw_data)} Players under monitoring')
    st.write('Data Sources:')
    col1, col2 = st.columns([0.1, 1])  # Ajustando o tamanho das colunas para melhor proporção
    col3, col4 = st.columns([0.1, 1])

    # Transfermarkt
    with col1:
        transfermarkt_html = """
        <a href="https://www.transfermarkt.com/" target="_blank">
            <img src="https://i0.wp.com/pressfut.com/wp-content/uploads/2021/01/Transfermarkt_logo.png?fit=1020%2C680&ssl=1" width="60">
        </a>
        """
        st.markdown(transfermarkt_html, unsafe_allow_html=True)
    with col2:
        st.markdown("[Transfermarkt](https://www.transfermarkt.com/)")

    # PlaymakerStats
    with col3:
        playmaker_html = """
        <a href="https://www.playmakerstats.com/" target="_blank">
            <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Zerozero-logo.svg/165px-Zerozero-logo.svg.png" width="60">
        </a>
        """
        st.markdown(playmaker_html, unsafe_allow_html=True)
    with col4:
        st.markdown("[PlaymakerStats](https://www.playmakerstats.com/)")        

with st.sidebar:
    st.title('Filter Conditions🔍')
    nationality = st.multiselect('Nationality', ['Any'] + sorted(list(data['Nationality'].unique())), default=['Any'])
    if 'Any' not in nationality:
        data = data[data['Nationality'].isin(nationality)]

    age_min, age_max = st.slider(
        "Age",
        min_value=int(raw_data['Age'].min()),
        max_value=int(raw_data['Age'].max()),
        value=[int(data['Age'].min()), int(data['Age'].max())]
    )
    data = data[(data['Age'] >= age_min) & (data['Age'] <= age_max)]

    height_min, height_max = st.slider(
        "Height (cm)",
        min_value=int(raw_data['Height (cm)'].min()),
        max_value=int(raw_data['Height (cm)'].max()),
        value=[int(data['Height (cm)'].min()), int(data['Height (cm)'].max())]
    )
    data = data[
        (data['Height (cm)'].isna()) | ((data['Height (cm)'] >= height_min) & (data['Height (cm)'] <= height_max))]

    foot = st.selectbox('Preferred Foot', ['Any'] + list(data['Foot'].unique()))
    if foot != 'Any':
        data = data[data['Foot'] == foot]

    position = st.multiselect('Main Position', ['Any'] + sorted(list(data['Position'].unique())), default=['Any'])
    if 'Any' not in position:
        data = data[data['Position'].isin(position)]

with st.container():
    st.write('---')

    scoutdatabase = st.data_editor(data,
                        column_config={
                            "Player ID": None,
                            "Player img url": st.column_config.ImageColumn("Player", width='small'),
                            'Team img url': st.column_config.ImageColumn('Team', width='small'),
                            'flag_img_url': st.column_config.ImageColumn('Flag', width='small'),
                            'Birth Date': st.column_config.DateColumn('Birth Date', width='small', format="YYYY-MM-DD"),
                            'Contract Expires': st.column_config.DateColumn('Contract Expires', width='small',format="YYYY-MM-DD"),
                            'Loan Contract Expires': st.column_config.DateColumn('Loan Contract Expires',width='small',format="YYYY-MM-DD"),
                            'Player Agent Link': st.column_config.LinkColumn('Player Agent Link', width='small'),
                            'Transfermarkt Profile': st.column_config.LinkColumn('Transfermarkt Profile', width='large'),
                            'PlaymakerStats Profile': st.column_config.LinkColumn('PlaymakerStats Profile', width='large'),
                            'On Loan': st.column_config.CheckboxColumn('On Loan', width='small')
                        },
                        hide_index=True,
                        disabled=data.columns
                    )

refresh = st.button('Refresh Database')
if refresh:
    with st.spinner('Updating the database...'):
        refresh_database()
        st.cache_data.clear()
        st.success('Database refreshed successfully!')
