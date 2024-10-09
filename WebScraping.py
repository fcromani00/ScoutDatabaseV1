def scraping_transfermarkt(link_TF):
  import re
  import requests
  from bs4 import BeautifulSoup
  import pandas as pd

  dict_transfermarkt = { # Criando dict pra armazenar as informações
    'Player ID':'000000',
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
    'On Loan': "False",
    'Loan Contract Expires' : pd.NA,
    'On Loan From': pd.NA,
    'Instagram': pd.NA,
    'Player img url':pd.NA,
    'Team img url':  pd.NA,
    'Transfermarkt Profile': link_TF,
    'PlaymakerStats Profile': pd.NA
  }
  
  response = requests.get(link_TF, headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}) # Acessando link
  soup = BeautifulSoup(response.content, "html.parser") # Pegando o código fonte do link
  ###########################################################################################  
  try:
    dict_transfermarkt['Player ID'] = link_TF.split('/')[-1] # Coletando o ID do jogador no Transfermarkt
  except:
    dict_transfermarkt['Player ID'] = '000000'

  #Market Value---------------------------------------------------------------------------------------------------------------------------------------------------------
  try:
      dict_transfermarkt['Market Value'] = re.match(r'(€\d+(\.\d+)?[a-zA-Z]+)(?=Last update)',soup.find('a', class_='data-header__market-value-wrapper').get_text(strip=True)).group(1)
  except AttributeError:
      dict_transfermarkt['Market Value'] = pd.NA

  # Birth Date and Age---------------------------------------------------------------------------------------------------------------------------------------------------------
  try:
    label_element = soup.find('span', class_='info-table__content info-table__content--regular', string="Date of birth/Age:") # Encontrando o elemento que contém "Date of birth/Age:"
    date_of_birth_element = re.match(r'([A-Za-z]{3} \d{1,2}, \d{4}) \((\d{1,3})\)',label_element.find_next_sibling('span', class_='info-table__content info-table__content--bold').get_text(strip=True)) # Encontrando o elemento que contém a data de nascimento e a idade

    dict_transfermarkt['Age'] = int(date_of_birth_element.group(2))
    dict_transfermarkt['Birth Date'] = pd.to_datetime(date_of_birth_element.group(1), format="%b %d, %Y").strftime("%Y-%m-%d")
  except:
    dict_transfermarkt['Age'] = pd.NA
    dict_transfermarkt['Birth Date'] = pd.NA

  # Position---------------------------------------------------------------------------------------------------------------------------------------------------------
  try:
    label_element = soup.find('span', class_='info-table__content info-table__content--regular', string="Position:") # Encontrando o elemento que contém "Position:"
    position_element = label_element.find_next_sibling('span', class_='info-table__content info-table__content--bold') # Encontrando o elemento que contém a data de nascimento e a idade
    dict_transfermarkt['Position'] = position_element.get_text(strip=True).split(' - ')[-1]
  except:
    dict_transfermarkt['Position'] = pd.NA

  # Team---------------------------------------------------------------------------------------------------------------------------------------------------------
  try:
    dict_transfermarkt['Team'] = soup.find('div', class_='data-header__club-info').find('a').get_text(strip=True)
  except:
    dict_transfermarkt['Team'] = pd.NA

  # Player Name---------------------------------------------------------------------------------------------------------------------------------------------------------
  try:
    dict_transfermarkt['Short Name'] = re.sub(r'^\s*#?\d*\s*', '', ' '.join(soup.find('h1', class_="data-header__headline-wrapper").stripped_strings))
  except:
    dict_transfermarkt['Short Name'] = pd.NA

  # Foot---------------------------------------------------------------------------------------------------------------------------------------------------------
  try:
    label_element = soup.find('span', class_='info-table__content info-table__content--regular', string="Foot:") # Encontrando o elemento que contém "Foot:"
    foot_element = label_element.find_next_sibling('span', class_='info-table__content info-table__content--bold') # Encontrando o elemento que contém o pé

    if label_element and foot_element: # Verificando se os elementos existem
        dict_transfermarkt['Foot'] = foot_element.get_text(strip=True)
  except:
    dict_transfermarkt['Foot'] = pd.NA

  # Height--------------------------------------------------------------------------------------------------------------------------------------------------------
  try:
    label_element = soup.find('span', class_='info-table__content info-table__content--regular', string="Height:")# Encontrando a tag <span> que contem o texto Height:
    height_element = label_element.find_next_sibling('span', class_='info-table__content info-table__content--bold') # Coletando os dados que estão no irmao da tag que tem Height:

    if label_element and height_element: # Verificando se os elementos existem
        dict_transfermarkt['Height (cm)'] = int(height_element.get_text(strip=True)[:4].replace(',',''))# Coletando apenas os primeiros 4 caracteres na tag em que tem o a altura
  except:
    dict_transfermarkt['Height (cm)'] = pd.NA

  #Contract expires--------------------------------------------------------------------------------------------------------------------------------------------------------
  try:
    label_element = soup.find('span', class_='info-table__content info-table__content--regular', string="Contract expires:") # Encontrando o elemento que contém "Position:"
    contract_element = label_element.find_next_sibling('span', class_='info-table__content info-table__content--bold') # Encontrando o elemento que contém a data de nascimento e a idade

    if label_element and contract_element:
      dict_transfermarkt['Contract Expires'] = pd.to_datetime(contract_element.get_text(strip=True), format="%b %d, %Y").strftime("%Y-%m-%d")
  except:
    dict_transfermarkt['Contract Expires'] = pd.NA

  #Player Agent--------------------------------------------------------------------------------------------------------------------------------------------------------
  try:
    label_element = soup.find('span', class_='info-table__content info-table__content--regular', string="Player agent:") # Encontrando o elemento que contém "Player agent:"
    agent_element = label_element.find_next_sibling('span', class_='info-table__content info-table__content--bold info-table__content--flex') # Encontrando o elemento que contém o Player agent

    if label_element and agent_element:
      dict_transfermarkt['Player Agent'] = agent_element.get_text(strip=True)
  except:
    dict_transfermarkt['Player Agent'] = pd.NA

  try:
    dict_transfermarkt['Player Agent Link'] = f'https://www.transfermarkt.com{agent_element.find("a")["href"]}'
  except:
    dict_transfermarkt['Player Agent Link'] = pd.NA

  # Citizenship--------------------------------------------------------------------------------------------------------------------------------------------------------
  try:
    label_element = soup.find('span', class_='info-table__content info-table__content--regular', string="Citizenship:")
    citizenship_element = label_element.find_next_sibling('span', class_='info-table__content info-table__content--bold')

    if label_element and citizenship_element:
      dict_transfermarkt['Citizenship'] = re.findall('[A-Z][^A-Z]*',citizenship_element.get_text(strip=True))[-1]
      dict_transfermarkt['Nationality'] = re.findall('[A-Z][^A-Z]*',citizenship_element.get_text(strip=True))[0]
  except:
    dict_transfermarkt['Citizenship'] = pd.NA
    dict_transfermarkt['Nationality'] = pd.NA

  # On Loan--------------------------------------------------------------------------------------------------------------------------------------------------------
  try:
    label_element = soup.find('span', class_='info-table__content info-table__content--regular', string="On loan from:")
    loan_element = label_element.find_next_sibling('span', class_='info-table__content info-table__content--bold')


    if label_element and loan_element:
      dict_transfermarkt['On Loan'] = "True"
      dict_transfermarkt['On Loan From'] = loan_element.get_text(strip=True)

  except:
    dict_transfermarkt['On Loan'] = "False"
    dict_transfermarkt['On Loan From'] = pd.NA

  try:
    label_element = soup.find('span', class_='info-table__content info-table__content--regular', string="Contract there expires:")
    loan_contract_element = label_element.find_next_sibling('span', class_='info-table__content info-table__content--bold')

    dict_transfermarkt['Contract Expires'] = pd.to_datetime(loan_contract_element.get_text(strip=True), format="%b %d, %Y").strftime("%Y-%m-%d")
    dict_transfermarkt['Loan Contract Expires'] = pd.to_datetime(contract_element.get_text(strip=True), format="%b %d, %Y").strftime("%Y-%m-%d")

  except:
    dict_transfermarkt['Loan Contract Expires'] = pd.NA

  #Instagram------------------------------------------------------------------------------------------------------------------------------------------------------
  try:
    dict_transfermarkt['Instagram'] = "@" + soup.find('a', title="Instagram")['href'].split("/")[-2]
    if dict_transfermarkt['Instagram'] == '@www.instagram.com':
      dict_transfermarkt['Instagram'] = pd.NA
  except:
    dict_transfermarkt['Instagram'] = pd.NA

  #Full Name ------------------------------------------------------------------------------------------------------------------------------------------------------
  try:
    label_element = soup.find('span', class_='info-table__content info-table__content--regular', string="Full name:")
    full_name_element = label_element.find_next_sibling('span', class_='info-table__content info-table__content--bold')

    if label_element and full_name_element:
      dict_transfermarkt['Full Name'] = full_name_element.get_text(strip=True)
  except:
    try:
      label_element = soup.find('span', class_='info-table__content info-table__content--regular', string="Name in home country:")
      full_name_element = label_element.find_next_sibling('span', class_='info-table__content info-table__content--bold')

      if label_element and full_name_element:
        dict_transfermarkt['Full Name'] = full_name_element.get_text(strip=True)
    except:
      dict_transfermarkt['Full Name'] = dict_transfermarkt['Short Name']

  #Player photo----------------------------------------------------------------------------------------------------------------------------------------------------------
  try:
    img_element = soup.find('img', class_='data-header__profile-image')
    dict_transfermarkt['Player img url'] = img_element.get('src')

    if dict_transfermarkt['Player img url'] == 'https://img.a.transfermarkt.technology/portrait/header/default.jpg?lm=1':
      dict_transfermarkt['Player img url'] = pd.NA

  except:
    dict_transfermarkt['Player img url'] = pd.NA

  #Team photo----------------------------------------------------------------------------------------------------------------------------------------------------------
  try:
    img_tag = soup.find('a', class_='data-header__box__club-link').find('img')['srcset']

    dict_transfermarkt['Team img url'] = img_tag.split(',')[1].split()[0]# Extrair o link da imagem no formato 2x
  except:
    dict_transfermarkt['Team img url'] = pd.NA
  print(dict_transfermarkt)
  return dict_transfermarkt

def scraping_playmaker(link_PMS):
  import re
  import requests
  from bs4 import BeautifulSoup
  import pandas as pd
  from io import StringIO
  from urllib.parse import urljoin
  import time

  dict_playmaker = { # Criando dict pra armazenar as informações
      'Player ID':'000000',
      'Short Name': pd.NA,
      'Team':pd.NA,
      'Age':pd.NA,
      'Nationality':pd.NA,
      'Position':pd.NA,
      'Foot':pd.NA,
      'On Loan':pd.NA,
      'Birth Date': pd.NA,
      'Height (cm)':pd.NA,
      'Market Value':pd.NA,
      'Contract Expires':pd.NA,
      'Full Name': pd.NA,
      'On Loan From':pd.NA,
      'Loan Contract Expires' : pd.NA,
      'Citizenship':pd.NA,
      'Player Agent': pd.NA,
      'Player Agent Link':pd.NA,
      'Player img url':pd.NA,
      'Team img url':pd.NA,
      'Instagram':pd.NA,
      'Transfermarkt Profile': pd.NA,
      'PlaymakerStats Profile': link_PMS
  }


  response = requests.get(link_PMS, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})
  soup = BeautifulSoup(response.content, "html.parser")
  
  try:
    profile_soup = soup.find('div', class_='rbbox nofooter')  # Extraindo a div do PROFILE
    divs_bio_half = profile_soup.find_all('div', class_='bio_half')
    divs_bio = profile_soup.find_all('div', class_='bio')
  except:
    print("Erro ao extrair o div do PROFILE")

  #Player ID
  try:
    dict_playmaker['Player ID'] = re.compile(r'/player/[^/]+/(\d+)').search(link_PMS).group(1)
  except:
    dict_playmaker['Player ID'] = '000000'

  #Short Name
  try:
    name_element = soup.find('div', class_='player_name').find('span')# Encontrando a tag <span> com a classe "name"
    if name_element:
      dict_playmaker['Short Name'] = name_element.get_text(strip=True)
  except:
      dict_playmaker['Short Name'] = pd.NA

  #Birth Date
  try:
    # Encontrando a tag que contém "Born/Age"
    bio_half_div = soup.find('div', class_='bio_half')
    born_age_element = bio_half_div.find('span', string='Born/Age')

    if born_age_element:
        # A data de nascimento está logo após o elemento <span> "Born/Age"
        birth_date = born_age_element.find_next_sibling(string=True).strip()
        if birth_date:
            dict_playmaker['Birth Date'] = birth_date
  except:
    dict_playmaker['Birth Date'] = pd.NA

  #foot
  try:
    for div in divs_bio_half:
      span = div.find('span')
      preferred_foot = pd.NA
      if span and 'Preferred foot' in span.text:
          dict_playmaker['Foot'] = div.text.split('Preferred foot')[1].strip().lower()
          break
  except:
    dict_playmaker['Foot'] = pd.NA

  try:
    # Encontrando a tag que contém a idade
    age_element = soup.find('div', class_='bio_half').find('span', class_='small').get_text(strip=True)
    if age_element:
        age = re.search(r'\((\d+) -yrs-old\)', age_element).group(1)
        dict_playmaker['Age'] = age
  except:
    dict_playmaker['Age'] = pd.NA

  try:
    # Encontrando a tag que contém o país de nascimento
    country_element = soup.find('div', class_='bio_half').find('div', class_='micrologo_and_text').find('div', class_='text').get_text(strip=True)
    if country_element:
        dict_playmaker['Nationality'] = country_element
  except:
    dict_playmaker['Nationality'] = pd.NA

  try:
    # Encontrando a tag que contém o país de nascimento
    country_element = soup.find('div', class_='bio_half').find('div', class_='micrologo_and_text').find('div', class_='text').get_text(strip=True)
    if country_element:
      dict_playmaker['Nationality'] = country_element
      dict_playmaker['Citizenship'] = country_element
  except:
     dict_playmaker['Nationality'] = pd.NA
     dict_playmaker['Citizenship'] = pd.NA

  try:
   title = soup.find("title").get_text(strip=True)
   dict_playmaker['Team'] = re.search(r' - ([^-]+) - ', title).group(1).strip()
  except:
    dict_playmaker['Team'] =pd.NA

  try:
    meta_tag = soup.find("meta", {"name": "description"})['content']
    dict_playmaker['Full Name'] = re.search(r'^(.+?) is a \d+-year-old Football player', meta_tag).group(1).strip()
  except:
    dict_playmaker['Full Name'] = pd.NA

  try:
    position_td = soup.find('span', string='Position').find_next_sibling('tr').find_all('td')[1]
    dict_playmaker['Position'] = position_td.get_text(strip=True)
  except:
    dict_playmaker['Position'] = pd.NA

  #player image and height
  try:
    script_tag = soup.find("script", type="application/ld+json").string
    dict_playmaker['Player img url'] = re.search(r'"image"\s*:\s*"([^"]+)"', script_tag).group(1)
  except:
    dict_playmaker['Player img url'] = pd.NA

  try:
    script_tag = soup.find("script", type="application/ld+json").string
    dict_playmaker['Height (cm)'] = int(re.search(r'"height"\s*:\s*"(\d+)', script_tag).group(1))
    if dict_playmaker['Height (cm)'] == 0:
      dict_playmaker['Height (cm)'] = pd.NA
  except:
    dict_playmaker['Height (cm)'] = pd.NA

  try:
    # Encontrar a tag <img> onde o title corresponde ao nome do time usando regex
    img_tag = soup.find("img", {"title": re.compile(re.escape(dict_playmaker['Team']))})
    dict_playmaker['Team img url'] = "https://www.playmakerstats.com" + img_tag['src']
  except:
    dict_playmaker['Team img url'] = pd.NA

  # Instagram
  try:
    for div in divs_bio:
      if 'Other connections' in div.text:
        try:
          instagram_link = div.find('a', href=re.compile(r'https://www.instagram.com/'))['href']
          dict_playmaker['Instagram'] = "@" + re.search(r'https://www.instagram.com/([^/]+)', instagram_link).group(1)
          break  # Se encontrar o Instagram, saia do loop
        except:
          dict_playmaker['Instagram'] = pd.NA
  except:
    dict_playmaker['Instagram'] = pd.NA
  #Extracting seasons data
  try:
    season = soup.find("h2",class_='header').get_text(strip=True)
    current_season = int(re.search(r'Summary\s+(\d{4}(?:/\d{4})?)', season).group(1).strip())
    results_current_season_link = urljoin(link_PMS, soup.find('div', class_='footer').find('a').get('href'))

    # Extrai o epoca_id
    epoca_id = int(re.search(r'epoca_id=(\d+)', results_current_season_link).group(1))

    # Gera a lista de links com epoca_id decrementado
    results_links = [
        results_current_season_link
  ] + [
        re.sub(r'epoca_id=\d+', f'epoca_id={epoca_id - i}', results_current_season_link)
        for i in range(1, 3)
    ]

    seasons_results = pd.DataFrame()
    season_year = current_season

    for result_link in results_links:
      try:
        response = requests.get(result_link, headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}) # Acessando link
        soup = BeautifulSoup(response.content, "html.parser")
        table = StringIO(str(soup.find('table', {'class': 'zztable stats'})))
        season_result = pd.read_html(table)[0]

        if 'GC' not in season_result.columns:
          season_result['GC'] = 0

        if 'GS' not in season_result.columns:
          season_result['GS'] = 0

        del season_result['Unnamed: 15']
        season_result['Season'] = current_season
        season_result = season_result.rename(columns={
          'Unnamed: 0': 'Tournament',
          'G': 'Games',
          'W': 'Wins',
          'D': 'Draws',
          'L': 'Losses',
          'GD': 'Goal Difference',
          'M': 'Minutes',
          'S': 'Starting XI',
          'US': 'Used Sub',
          'GS': 'Goals Scored',
          'AST':'Assists',
          'OG': 'Own Goals',
          'YC': 'Yellow Cards',
          '2Y': 'Double Yellows',
          'RC': 'Red Cards',
          'GC': 'Goals Conceded'})
        season_result = season_result.dropna(subset=['Tournament'])
        seasons_results = pd.concat([seasons_results, season_result], ignore_index=True)
        current_season = current_season -1
      except:
        season_result = pd.NA
    seasons_results['Player ID'] = dict_playmaker['Player ID']
  except:
    seasons_results = pd.DataFrame()

  print(dict_playmaker, seasons_results)
  return dict_playmaker, seasons_results

def refresh_database():  
  import pandas as pd
  import streamlit as st
  from streamlit_gsheets import GSheetsConnection
  
  conn = st.connection("gsheets", type=GSheetsConnection)

  players_df = conn.read(worksheet="players")
  performance_seasons_df = conn.read(worksheet="performance_seasons")
  
  refresh_players = pd.DataFrame()
  refresh_performance = pd.DataFrame()

  for index,row in players_df[['Transfermarkt Profile', 'PlaymakerStats Profile']].iterrows():
      dict_scoutdatabase = {
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
    
      dict_playmaker = dict_scoutdatabase
      dict_transfermarkt = dict_scoutdatabase
    
      seasons_results_df = pd.DataFrame()
      df_player_info = pd.DataFrame()
    
      link_TF = row.iloc[0] # Pegando o link na base_links['LINK Transfermarkt']
      if pd.notna(link_TF) and link_TF.strip() != '':
        dict_transfermarkt = scraping_transfermarkt(link_TF) # Fazendo scraping utilizando o link

      link_PMS = row.iloc[1] # Pegando o link na base_links['LINK Playmaker']
      if pd.notna(link_PMS) and link_PMS.strip() != '':
        dict_playmaker, seasons_results_df = scraping_playmaker(link_PMS) # Fazendo scraping utilizando o link
      refresh_performance = pd.concat([refresh_performance, seasons_results_df], ignore_index=True)


      dict_scoutdatabase['Player ID'] = dict_playmaker['Player ID']

      for key, value in dict_scoutdatabase.items():
        if pd.isna(dict_scoutdatabase[key]) and not pd.isna(dict_transfermarkt[key]):
          dict_scoutdatabase[key] = dict_transfermarkt[key]
        elif pd.isna(dict_scoutdatabase[key]) and not pd.isna(dict_playmaker[key]):
          dict_scoutdatabase[key] = dict_playmaker[key]

        df_player_info = pd.DataFrame([dict_scoutdatabase])

      refresh_players = pd.concat([refresh_players, df_player_info], ignore_index=True)
    
  conn.update(worksheet="players", data=refresh_players)
  conn.update(worksheet="performance_seasons", data=refresh_performance)

def add_new_player(dict_scoutdatabase,df_player_performance):
  import pandas as pd
  import streamlit as st
  from streamlit_gsheets import GSheetsConnection

  df_player_info = pd.DataFrame(dict_scoutdatabase, index=[0])

  conn = st.connection("gsheets", type=GSheetsConnection)
   
  players_df = conn.read(worksheet="players")
  performance_seasons_df = conn.read(worksheet="performance_seasons")

  players_df = pd.concat([players_df, df_player_info], ignore_index=True)
  performance_seasons_df = pd.concat([performance_seasons_df,df_player_performance], ignore_index=True)

  conn.update(worksheet="players", data=players_df)
  conn.update(worksheet="performance_seasons", data=performance_seasons_df)

def remove_player(player_id):
  import pandas as pd
  from streamlit_gsheets import GSheetsConnection
  import streamlit as st

  conn = st.connection("gsheets", type=GSheetsConnection)
   
  players_df = conn.read(worksheet="players")
  performance_seasons_df = conn.read(worksheet="performance_seasons")

  players_df = players_df[players_df['Player ID']!=player_id] 
  performance_seasons_df = performance_seasons_df[performance_seasons_df['Player ID']!=player_id]
  
  conn.update(worksheet="players", data=players_df)
  conn.update(worksheet="performance_seasons", data=performance_seasons_df)
  
  
#   import sqlite3
#   import pandas as pd
  
#   test_conn = sqlite3.connect(db, check_same_thread=False)
#   test_cur = test_conn.cursor()

#   dict_scoutdatabase = {
#       key: value if not pd.isna(value) else (None if isinstance(value, (int, float)) else '')
#       for key, value in dict_scoutdatabase.items()
#   }

#   test_cur.execute(f'''
#     INSERT INTO "players" (
#       "Player ID",
#       "Short Name",
#       "Full Name",
#       "Birth Date",
#       "Age" ,
#       "Nationality",
#       "Citizenship",
#       "Team",
#       "Position",
#       "Market Value",
#       "Foot" ,
#       "Height (cm)",
#       "Player Agent",
#       "Player Agent Link",
#       "Contract Expires",
#       "On Loan",
#       "Loan Contract Expires",
#       "On Loan From",
#       "Instagram",
#       "Flag img url",
#       "Player img url",
#       "Team img url",
#       "Transfermarkt Profile",
#       "PlaymakerStats Profile"
#     )
#     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
#      (dict_scoutdatabase['Player ID'],
#       dict_scoutdatabase['Short Name'],
#       dict_scoutdatabase['Full Name'],
#       dict_scoutdatabase['Birth Date'],
#       dict_scoutdatabase['Age'],
#       dict_scoutdatabase['Nationality'],
#       dict_scoutdatabase['Citizenship'],
#       dict_scoutdatabase['Team'],
#       dict_scoutdatabase['Position'],
#       dict_scoutdatabase['Market Value'],
#       dict_scoutdatabase['Foot'],
#       dict_scoutdatabase['Height (cm)'],
#       dict_scoutdatabase['Player Agent'],
#       dict_scoutdatabase['Player Agent Link'],
#       dict_scoutdatabase['Contract Expires'],
#       dict_scoutdatabase['On Loan'],
#       dict_scoutdatabase['Loan Contract Expires'],
#       dict_scoutdatabase['On Loan From'],
#       dict_scoutdatabase['Instagram'],
#       dict_scoutdatabase['Flag img url'],
#       dict_scoutdatabase['Player img url'],
#       dict_scoutdatabase['Team img url'],
#       dict_scoutdatabase['Transfermarkt Profile'],
#       dict_scoutdatabase['PlaymakerStats Profile']
#     ))
#   # test_conn.commit()

#   for index, row in df_player_performance.iterrows():
#     test_cur.execute("""
#         INSERT INTO "performance_seasons" (
#           "Tournament"
#         , "Games"
#         , "Wins"
#         , "Draws"
#         , "Losses"
#         , "Goal Difference"
#         , "Minutes"
#         , "Starting XI"
#         , "Used Sub"
#         , "Goals Scored"
#         , "Assists"
#         , "Own Goals"
#         , "Yellow Cards"
#         , "Double Yellows"
#         , "Red Cards"
#         , "Goals Conceded"
#         , "Season"
#         , "Player ID"
#         )
#         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
#            (row['Tournament'],
#             row['Games'],
#             row['Wins'],
#             row['Draws'],
#             row['Losses'],
#             row['Goal Difference'],
#             row['Minutes'],
#             row['Starting XI'],
#             row['Used Sub'],
#             row['Goals Scored'],
#             row['Assists'],
#             row['Own Goals'],
#             row['Yellow Cards'],
#             row['Double Yellows'],
#             row['Red Cards'],
#             row['Goals Conceded'],
#             row['Season'],
#             row['Player ID']
#         )
#     )
#     print(row)
#     # test_conn.commit()
  
#   test_conn.commit()
#   test_conn.close()

# def remove_player(player_id, db):
#   import sqlite3

#   conn = sqlite3.connect(db, check_same_thread=False)
#   cur = conn.cursor()
  
#   cur.execute("""DELETE FROM players WHERE "Player ID" = ?""", (player_id,))
  
#   conn.commit()
#   conn.close()