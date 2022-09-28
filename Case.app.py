#!/usr/bin/env python
# coding: utf-8

# # Case 2 - Team 12

# * Joey van Alphen
# * Mohamed Garad
# * Nusret Kaya
# * Shereen Macnack

# # 1. Data inladen

# ### Dataset 1: Maandcijfers Nederlandse luchthavens van nationaal belang

# In[1]:


#pip install cbsodata


# In[2]:


import cbsodata
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import statsmodels.api as sm


# In[3]:


data1 = pd.DataFrame(cbsodata.get_data('37478hvv'))


# In[4]:


#data1.shape


# In[5]:


data1.info(verbose=True, show_counts=True)


# In[6]:


data1.head()


# ### Dataset 2: Emissies naar lucht door de Nederlandse economie; nationale rekeningen

# In[7]:


data2 = pd.DataFrame(cbsodata.get_data('83300NED'))


# In[8]:


# data2.shape


# In[9]:


data2.info()


# In[10]:


data2.head()


# # 2. Data filteren

# ### 1. Aviation data filteren

# In[11]:


aviation_data = data1[['ID', 'Luchthavens', 'Perioden', 'Overlandbewegingen_1', 'Terreinbewegingen_2','TotaalAlleVluchten_3', 'TotaalVertrokkenVluchten_9', 'TotaalAantalPassagiers_12','EuropaTotaal_22','EULanden_54','OverigEuropa_55', 'Afrika_57','Amerika_63', 'Azie_67', 'Oceanie_71', 'TotaalGoederenvervoer_43', 'TotalePostvervoer_74']]


# In[ ]:





# In[12]:


#aviation_data die is gefilterd op alleen het totaal van alle luchhavens van nationaal belang
alle_luchthavens = aviation_data[aviation_data['Luchthavens']=='Totaal luchthavens van nationaal belang']


# In[13]:


alle_luchthavens.head(50)


# In[14]:


# alle_luchthavens filteren op volledige jaren ipv maanden voor totaal 
value_list = ['1997', '1998', '1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020']
boolean_series = alle_luchthavens.Perioden.isin(value_list)
alle_luchthavens = alle_luchthavens[boolean_series]
alle_luchthavens_index = alle_luchthavens.reset_index(drop = True)
alle_luchthavens_index.head(50)


# In[ ]:





# In[15]:


#aviation_data die de individuele luchthavens bevat
individuele_luchthavens = aviation_data[aviation_data['Luchthavens']!='Totaal luchthavens van nationaal belang']
individuele_luchthavens_index = individuele_luchthavens.reset_index(drop = True)


# In[ ]:





# In[16]:


#individuele_luchthavens_index gefilterd op volledige jaren ipv maanden voor individuele luchthavens
value_list = ['1997', '1998', '1999', '2000', '2001', '2002', '2003', '2004', '2005','2006', '2007', '2008', '2009', '2010', '2011','2012', '2013', '2014', '2015', '2016','2017', '2018', '2019','2020']
boolean_series = individuele_luchthavens_index.Perioden.isin(value_list)
individuele_luchthavens_index = individuele_luchthavens_index[boolean_series]
individuele_luchthavens_index.head()


# ### 2. Emissies data filteren

# In[17]:


data2.head()


# In[18]:


co2_emissies = data2[['ID','NederlandseEconomie','Perioden', 'CO2_1']]


# In[19]:


co2_emissies_luchtvaart = co2_emissies[co2_emissies['NederlandseEconomie']=='51 Vervoer door de lucht']


# In[20]:


co2_emissies_luchtvaart.head(50)


# In[21]:


#Filteren vanaf 1997 om de andere dataset te matchen
co2_emissies_luchtvaart = co2_emissies_luchtvaart[co2_emissies_luchtvaart['Perioden']>='1997'].reset_index(drop=True)
co2_emissies_luchtvaart = co2_emissies_luchtvaart.drop(['ID'], axis=1) 


# In[22]:


co2_emissies_luchtvaart.head(50)


# In[23]:


co2_emissies_luchtvaart.columns = ['Emissie categorie', 'Perioden', 'CO2 uitstoot (mln kg)']
co2_emissies_luchtvaart.head(30)


# In[24]:


# Dataframes combineren
samengestelde_tabel = alle_luchthavens_index.merge(co2_emissies_luchtvaart, on='Perioden', how='left')

samengestelde_tabel = samengestelde_tabel.drop(['ID', 'Emissie categorie'], axis = 1)


# In[25]:


# Kolom namen veranderen van samengestelde tabel
samengestelde_tabel = samengestelde_tabel.rename ({'Perioden': 'Jaar', 'Overlandbewegingen_1':'Overlandbewegingen' , 'Terreinbewegingen_2':'Terreinbewegingen', 'TotaalAlleVluchten_3': 'Totaal aantal vluchten', 'TotaalVertrokkenVluchten_9':'Totaal vertrokken vluchten','TotaalAantalPassagiers_12': 'Totaal aantal passagiers', 'EuropaTotaal_22':'Europa totaal','EULanden_54': 'EU landen', 'OverigEuropa_55':'Overig Europa', 'Afrika_57':'Afrika','Amerika_63': 'Amerika','Azie_67': 'Azie', 'Oceanie_71':'Oceanie', 'TotaalGoederenvervoer_43':'Totaal goederenvervoer','TotalePostvervoer_74':'Totaal postvervoer', 'CO2_1': 'CO2 emissies in jaar'}, axis = 1)
samengestelde_tabel.head(30)


# In[26]:


corr = np.corrcoef(samengestelde_tabel['Totaal aantal vluchten'], samengestelde_tabel['CO2 uitstoot (mln kg)'])


# In[27]:


fig = px.scatter(samengestelde_tabel, x='Totaal aantal vluchten', y ='CO2 uitstoot (mln kg)', trendline="ols", )


# In[28]:


fig1 = px.histogram(individuele_luchthavens_index, x='Perioden', y='TotaalAlleVluchten_3', color = 'Luchthavens')


# In[29]:


fig2 = px.line(samengestelde_tabel, x='Jaar', y='CO2 uitstoot (mln kg)')


# # 3. Maken van de Streamlit app

# In[30]:


header = st.container()


# In[31]:


with header:
    st.title('Aviaition data blog')
    st.markdown('In deze blog gebruiken we data van het CBS over de maandelijkse cijfers van Nederlandse luchthavens. Wij willen inzicht krijgen in welke mate deze cijfers gerelateerd zijn tot de jaarlijkse uitstoot van de luchtvaart industrie met behulp van een tweede dataset')


# In[32]:


aviation_data_streamlit_table = aviation_data[['Luchthavens', 'Perioden', 'TotaalAlleVluchten_3', 'TotaalAantalPassagiers_12','TotaalGoederenvervoer_43', 'TotalePostvervoer_74']]
aviation_data_streamlit_table.columns = ['Luchthavens', 'Perioden', 'Totaal aantal vluchten', 'Totaal aantal passagiers', 'Totale goederenvervoer', 'Totale postvervoer']
value_list = ['1997', '1998', '1999', '2000', '2001', '2002', '2003', '2004', '2005','2006', '2007', '2008', '2009', '2010', '2011','2012', '2013', '2014', '2015', '2016','2017', '2018', '2019','2020']
boolean_series = aviation_data_streamlit_table.Perioden.isin(value_list)
aviation_data_streamlit_table = aviation_data_streamlit_table[boolean_series]
aviation_data_streamlit_table.head(30)


# In[33]:


st.header('Data inladen')
st.markdown("Beide dataset zijn ingeladen door eerst een package can het CBS te downloaden. Vervolgens hebben we de data binnen kunnen halen met een pandas dataframe door de get_data() aan te roepen met de tabelcode van het CBS. als argument de met behulp van ")


# In[35]:


st.subheader('Dataset 1 met de maandelijkse cijfers van Nederlandse luchthavens')
st.markdown("Deze eerste dataset is gefilterd op de belangrijke informatie per luchthaven en alle luchthavens in totaal")


# In[36]:


InputAirport = st.sidebar.selectbox("Select Airport", ("Totaal luchthavens van nationaal belang", "Amsterdam Airport Schiphol", "Rotterdam The Hague Airport", "Eindhoven Airport", "Maastricht Aachen Airport", "Groningen Airport Eelde"))


# In[37]:


AirportSelect = aviation_data_streamlit_table[aviation_data_streamlit_table["Luchthavens"] == InputAirport]


# In[38]:


st.dataframe(AirportSelect)


# ### tweede tabel

# In[39]:


st.subheader('Dataset 2 met emissies')
st.markdown("Deze dataset is gefilterd op de emissies van de categorie 'Vervoer door de lucht' en de bijbehorende CO2 uitstoot ")


# In[40]:


st.dataframe(co2_emissies_luchtvaart)


# In[41]:


st.subheader("De samengestelde dataset")
st.markdown('Met behulp van de .merge() methode hebben we nu één tabel. Hierin kunnen we variabelen toevoegen')


# In[42]:


aviation_data_streamlit_table = aviation_data_streamlit_table[aviation_data_streamlit_table['Luchthavens']=='Totaal luchthavens van nationaal belang']
samengestelde_tabel_streamlit = aviation_data_streamlit_table.merge(co2_emissies_luchtvaart, on='Perioden', how='left')
samengestelde_tabel_streamlit = samengestelde_tabel_streamlit.drop(['Emissie categorie'], axis = 1)
samengestelde_tabel_streamlit.head(50)


# In[43]:


st.dataframe(samengestelde_tabel_streamlit)


# In[44]:


samengestelde_tabel_streamlit['Totale uitstoot sinds meting'] = samengestelde_tabel_streamlit['CO2 uitstoot (mln kg)'].cumsum()
samengestelde_tabel_streamlit['vulgraad'] = (samengestelde_tabel_streamlit['Totaal aantal passagiers'] + samengestelde_tabel_streamlit['Totale goederenvervoer']) / samengestelde_tabel_streamlit['Totaal aantal vluchten']


# In[45]:


samengestelde_tabel_streamlit.head()


# ## Plots

# In[46]:


st.header("Visualisaties")
st.markdown("Met behulp van visualisaties gaan we nu bepalen wat de correlatie is tussen verschillende variabelen en de totale uitstoot van CO2")
st.markdown("Als eerst bekijken we de CO2 uitstoot door de jaren heen. Hieruit valt dirtect op dat in tijden van crisis (2008 - 2009), maar vooral de coronacrisis (2020) de uitstoot heeft doen verlagen")


# In[47]:


fig1 = px.line(samengestelde_tabel_streamlit, x='Perioden', y='CO2 uitstoot (mln kg)', title = 'CO2 emissie verloop')  
fig.update_xaxes(title_text='Jaren')


# In[48]:


st.plotly_chart(fig1)


# In[49]:


st.markdown("De regressielijn geeft de formule CO2 utstoot (mln kg) = 0,0142941*Totaal aantal vluchten + 4917,18. We kunnen hier dus mee de CO2 uitstoot van een jaar voorspellen op basis van het aantal verwachte vluchten in dat jaar")


# In[50]:


fig2 = go.Figure(data=[go.Scatter(
    x=samengestelde_tabel_streamlit['Perioden'],
    y=samengestelde_tabel_streamlit['CO2 uitstoot (mln kg)'],
    mode='markers',)
])
  
# Add dropdown
fig2.update_layout(
    updatemenus=[
        dict(
            buttons=list([
                dict(
                    args=["type", "scatter"],
                    label="Scatter Plot",
                    method="restyle"               
                ),
                dict(
                    args=["type", "bar"],
                    label="Bar Chart",
                    method="restyle"
                )
            ]),
            direction="down",
        ),
    ]
)

fig2.update_xaxes(title_text = 'Jaar')
fig2.update_yaxes(title_text = 'CO2 emissie')


# In[51]:


st.plotly_chart(fig2)


# In[52]:


st.markdown("Nu bekijken we de relatie tussen het totale aantal vluchten in een jaar tegenover de CO2 uitstoot in dat jaar.")


# In[53]:


fig3 = px.scatter(samengestelde_tabel_streamlit, x='Totaal aantal vluchten', y ='CO2 uitstoot (mln kg)', trendline="ols", )


# In[54]:


st.plotly_chart(fig3)


# In[55]:


st.markdown("Er lijk hier inderdaad sprake van een sterke correlatie. We checheken dit met een correlatie matrix")


# In[56]:


fig, ax = plt.subplots()
sns.heatmap(corr, ax = ax, annot = True)
st.write(fig)


# In[57]:


st.markdown("De correlatie is met 0,77 sterk")


# In[58]:


fig4 = px.scatter(samengestelde_tabel_streamlit, y='CO2 uitstoot (mln kg)', x ='vulgraad', color = 'Perioden', trendline="ols", )


# In[59]:


st.plotly_chart(fig4)


# In[60]:


fig5 = px.line(samengestelde_tabel_streamlit, x='Perioden', y = 'Totale uitstoot sinds meting')
fig5.update_xaxes(title_text='')
fig5.update_yaxes(title_text='')


# In[61]:


st.plotly_chart(fig5)


# In[62]:


fig6 = px.histogram(individuele_luchthavens_index, x='Luchthavens', y='TotaalAlleVluchten_3', color = 'Luchthavens', animation_frame = 'Perioden', animation_group = 'Luchthavens' )


# In[63]:


st.plotly_chart(fig6)


# In[ ]:





# In[ ]:





# In[ ]:




