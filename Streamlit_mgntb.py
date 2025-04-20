import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from io import StringIO


# Load token from Streamlit secrets
token = st.secrets["github"]["token"]

# Github connection info
owner = "SausanCantik"
repo = "data"
file_path = "lpdp_awardee_ntb.csv"

# GitHub API URL
url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}"

# API headers
headers = {
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github.v3.raw"
}

# Get file
response = requests.get(url, headers=headers)

if response.status_code == 200:
    csv_content = response.text
    df = pd.read_csv(StringIO(csv_content))
    
else:
    st.error(f"Failed to fetch file: {response.status_code}")


# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv(StringIO(csv_content))
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    return df

df = load_data(df)

st.title("📊 LPDP NTB Awardee Dashboard")

# Sidebar Filters
st.sidebar.header("Filter Data")
year_filter = st.sidebar.multiselect("Tahun Diterima", sorted(df['tahun_diterima_lpdp'].dropna().unique()))
beasiswa_filter = st.sidebar.multiselect("Jenis Beasiswa", df['jenis_beasiswa'].dropna().unique())
jenjang_filter = st.sidebar.multiselect("Jenjang", df['jenjang'].dropna().unique())
kabupaten_filter = st.sidebar.multiselect("Kabupaten/Kota", df['kabupaten/kota'].dropna().unique())
gender_filter = st.sidebar.multiselect("Jenis Kelamin", df['jenis_kelamin'].dropna().unique())

# Apply Filters
filtered_df = df.copy()
if year_filter:
    filtered_df = filtered_df[filtered_df['tahun_diterima_lpdp'].isin(year_filter)]
if beasiswa_filter:
    filtered_df = filtered_df[filtered_df['jenis_beasiswa'].isin(beasiswa_filter)]
if jenjang_filter:
    filtered_df = filtered_df[filtered_df['jenjang'].isin(jenjang_filter)]
if kabupaten_filter:
    filtered_df = filtered_df[filtered_df['kabupaten/kota'].isin(kabupaten_filter)]
if gender_filter:
    filtered_df = filtered_df[filtered_df['jenis_kelamin'].isin(gender_filter)]

st.markdown("### Jumlah Penerima: {}".format(len(filtered_df)))

# Plot 1: Tahun Diterima
st.subheader("Penerima per Tahun")
tahun_counts = filtered_df['tahun_diterima_lpdp'].value_counts().sort_index().reset_index()
tahun_counts.columns = ['Tahun', 'Jumlah']
fig1 = px.bar(tahun_counts, x='Tahun', y='Jumlah', title='Jumlah Penerima Beasiswa per Tahun')
st.plotly_chart(fig1)

# Plot 2: Jenis Beasiswa
st.subheader("Distribusi Jenis Beasiswa")
fig2 = px.histogram(filtered_df, x='jenis_beasiswa', title='Distribusi Jenis Beasiswa')
st.plotly_chart(fig2)

# Plot 3: Jenjang Pendidikan
st.subheader("Distribusi Jenjang Pendidikan")
fig3 = px.histogram(filtered_df, x='jenjang', title='Distribusi Jenjang Pendidikan')
st.plotly_chart(fig3)

# Plot 4: Status Beasiswa
st.subheader("Status Beasiswa")
fig4 = px.histogram(filtered_df, x='status_beasiswa', title='Status Beasiswa')
st.plotly_chart(fig4)

# Plot 5: Tujuan Studi
st.subheader("Tujuan Studi")
fig5 = px.histogram(filtered_df, x='tujuan_studi', title='Tujuan Studi')
st.plotly_chart(fig5)

# Optional raw data display
#if st.checkbox("Tampilkan Data Mentah"):
#    st.dataframe(filtered_df.reset_index(drop=True))
