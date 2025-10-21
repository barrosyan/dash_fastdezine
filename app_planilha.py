import streamlit as st
import pandas as pd

# ==============================
# CONFIGURAÇÃO INICIAL
# ==============================
st.set_page_config(page_title="Base Unificada", page_icon="📊", layout="wide")

st.title("📊 Visualização e Filtro da Base Unificada")
st.write("Explore, filtre e busque informações facilmente na base consolidada.")

# ==============================
# CARREGAMENTO DA BASE
# ==============================
@st.cache_data
def load_data():
    # Aqui você pode mudar para o caminho real do seu arquivo
    df = pd.read_excel("unificado_final.xlsx")
    # Normaliza colunas que às vezes podem vir com espaços
    df.columns = df.columns.str.strip().str.lower()
    return df

df = load_data()

# ==============================
# BARRA LATERAL DE FILTROS
# ==============================
st.sidebar.header("🔍 Filtros")

# Filtro por categoria
categorias = df["categoria"].dropna().unique().tolist()
categoria_selecionada = st.sidebar.multiselect("Categoria:", categorias, default=categorias)

# Filtro por presença de CRM
crm_status = st.sidebar.selectbox("CRM preenchido:", ["Todos", "Com CRM", "Sem CRM"])
# Filtro por nome
busca_nome = st.sidebar.text_input("Buscar por nome:")

# ==============================
# APLICAÇÃO DOS FILTROS
# ==============================
df_filtrado = df.copy()

if categoria_selecionada:
    df_filtrado = df_filtrado[df_filtrado["categoria"].isin(categoria_selecionada)]

if crm_status == "Com CRM":
    df_filtrado = df_filtrado[df_filtrado["crm"].notna()]
elif crm_status == "Sem CRM":
    df_filtrado = df_filtrado[df_filtrado["crm"].isna()]

if busca_nome:
    busca_lower = busca_nome.lower()
    df_filtrado = df_filtrado[df_filtrado["name"].str.lower().str.contains(busca_lower, na=False)]

# ==============================
# VISUALIZAÇÃO PRINCIPAL
# ==============================
st.markdown("### 📋 Resultados Filtrados")

# Mostra quantidade e preview
st.write(f"**{len(df_filtrado)} registros encontrados**")

st.dataframe(
    df_filtrado,
    use_container_width=True,
    hide_index=True
)

# ==============================
# VISUALIZAÇÕES RESUMIDAS
# ==============================
st.markdown("### 📈 Estatísticas e Insights")

col1, col2, col3 = st.columns(3)

col1.metric("Total de Registros", len(df))
col2.metric("Registros Filtrados", len(df_filtrado))
col3.metric("Categorias Únicas", df["categoria"].nunique())

st.bar_chart(df_filtrado["categoria"].value_counts(), use_container_width=True)

# ==============================
# DOWNLOAD DOS DADOS
# ==============================
st.markdown("### 💾 Exportar Dados Filtrados")
csv = df_filtrado.to_csv(index=False).encode("utf-8")
st.download_button("Baixar CSV Filtrado", data=csv, file_name="base_filtrada.csv", mime="text/csv")
