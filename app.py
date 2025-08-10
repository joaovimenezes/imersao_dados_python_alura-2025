import streamlit as st
import pandas as pd
import plotly.express as px

# --- Configuração da Página ---
# Define o título da página, o ícone e o layout para ocupar a largura inteira.
st.set_page_config(
    page_title="Dashboard de Salários na Área de Dados",
    page_icon="📊",
    layout="wide",
)
df = pd.read_csv("https://raw.githubusercontent.com/vqrca/dashboard_salarios_dados/refs/heads/main/dados-imersao-final.csv")

#barra
st.sidebar.header('🔎Filtros')

#filtro ano
anos_disp = sorted(df['ano'].unique())
anos_selected = st.sidebar.multiselect('Ano', anos_disp, default= anos_disp)

#filtro senioridade
senioridade_disp = sorted(df['senioridade'].unique())
senioridade_selected = st.sidebar.multiselect('Senioridade', senioridade_disp, default= senioridade_disp)

#filtro contrato
contrato_disp = sorted(df['contrato'].unique())
contrato_selected = st.sidebar.multiselect('Tipo de Contrato', contrato_disp, default= contrato_disp)

#filtro tamanho_empresa
tamempresa_disp = sorted(df['tamanho_empresa'].unique())
tamempresa_selected = st.sidebar.multiselect('Tamanho da Empresa', tamempresa_disp, default= tamempresa_disp)

#filtro funcional

df_filter = df [
    (df['ano'].isin(anos_selected)) &
    (df['senioridade'].isin(senioridade_selected)) &
    (df['contrato'].isin(contrato_selected)) &
    (df['tamanho_empresa'].isin(tamempresa_selected))
]

st.markdown(
    '''
     <style data-emotion="st-emotion-cache" data-s="">
        .st-emotion-cache-1r61a0z {
            background-image: linear-gradient(90deg, rgb(255 75 233), rgb(125 143 255));
        }
    </style>
        ''', unsafe_allow_html=True
)

st.markdown(
    '''
     <style data-emotion="st-emotion-cache" data-s="">
        .st-emotion-cache-1dp5vir {
            background-image: linear-gradient(90deg, rgb(255 75 233), rgb(125 143 255));
        }
    </style>
        ''', unsafe_allow_html=True
)

st.markdown(
    '''
     <style media>
        .st-bq {
            background-color: rgb(239 75 255);
        }
    </style>
        ''', unsafe_allow_html=True
)

#conteúdo do site
st.title('📊🎲Dashboard de Salários na Área de Dados')
st.markdown('Visualize os dados salariais da área de dados ao longo dos anos no mundo todo. Utilize os filtros à esquerda para uma anáalise mais específica.')
st.markdown('---')

#KPI's
st.subheader('KPIs Gerais🧮  (Salário anual em USD💵)')

if not df_filter.empty:
    salario_medio = df_filter['usd'].mean()
    salario_max = df_filter['usd'].max()
    total_register = df_filter.shape[0]
    cargo_mais_frequente = df_filter['cargo'].mode()[0]
    
else:
    salario_medio, salario_max, total_register, cargo_mais_frequente = 0, 0, 0, ""

col1, col2, col3, col4 = st.columns(4)
col1.metric("Salário Médio 💰", f'${salario_medio:,.0f}')
col2.metric("Salário Máximo 🤑", f'${salario_max:,.0f}')
col3.metric('Total de Registros 🔢', f'{total_register:,}')
col4.metric('Cargo Mais Frequente 🧑‍💼', cargo_mais_frequente)
    
st.markdown('---')

#graficos com plotly
st.subheader('Gráficos📊')

col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    if not df_filter.empty:
        top_cargos = df_filter.groupby('cargo')['usd'].mean().nlargest(10).sort_values(ascending = True).reset_index()
        grafico_cargos = px.bar(
            top_cargos,
            x='usd',
            y='cargo',
            orientation='h',
            color_discrete_sequence=["#BA98BA"],
            title = 'Top 10 Cargos por Salário Médio',
            labels ={'usd': 'Média Salárial Anual(USD)', 'cargo': ''}
        )
        grafico_cargos.update_layout(title_x=0.35, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(grafico_cargos, use_container_width= True)
    else:
        st.warning('Nenhum dado para exibir no gráfico cargos.')

with col_graf2:
    if not df_filter.empty:
        grafico_hist = px.histogram(
            df_filter,
            x='usd',
            nbins = 35,
            color_discrete_sequence=["#BA98BA"],
            title = 'Distribuição de Salários Anuais',
            labels = {'usd': 'Faixa Salarial (USD)', 'count':''}
        )
        grafico_hist.update_layout(title_x=0.35)
        st.plotly_chart(grafico_hist, use_container_width=True)
    else:
        st.warning('Nenhum dado para exibir no gráfico de distribuição.')

col_graf3, col_graf4 = st.columns(2)

with col_graf3:
    if not df_filter.empty:
        remoto_contagem = df_filter['remoto'].value_counts().reset_index()
        remoto_contagem.columns = ['tipo_trabalho', 'quantidade']
        grafico_remoto = px.pie(
            remoto_contagem,
            names = 'tipo_trabalho',
            values = 'quantidade',
            title = 'Proporção das Modalidades de Trabalho',
            color_discrete_sequence=["#BA98BA"],
            hole= 0.6
        )
        grafico_remoto.update_traces(textinfo='percent+label')
        grafico_remoto.update_layout(title_x= 0.05)
        st.plotly_chart(grafico_remoto, use_container_width=True)
    else:
        st.warning('Nenhum dado para exibir no gráfico das modalidades de trabalho.')

with col_graf4:
    if not df_filter.empty:
        df_ds = df_filter[df_filter['cargo'] == 'Data Scientist']
        media_ds_pais = df_ds.groupby('residencia_iso3')['usd'].mean().reset_index()
        grafico_pais = px.choropleth(
            media_ds_pais,
            locations='residencia_iso3',
            color='usd',
            color_continuous_scale=["#DEC2DE", "#864286", "#400540" ],
            title='Salário Médio de Cientista de Dados por País',
            labels={'usd': 'Salário Médio (USD)', 'residencia_iso3':'País'}
        )
        grafico_pais.update_layout(title_x=0.05)
        st.plotly_chart(grafico_pais, use_container_width=True)
    else:
        st.warning('Nenhum dado para exibir o gráfico de países')

st.markdown('---')
st.subheader('Dados Completos🎲🔍')

st.dataframe(df_filter)

