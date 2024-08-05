import streamlit as st

# st.title('🎈 App Name')

# st.write('Hello world!')
import zipfile
import os
import shutil

def save_uploadedfile(uploadedfile):
    with open(os.path.join("tempDir",uploadedfile.name),"wb") as f:
        f.write(uploadedfile.getbuffer())
    return st.success("Saved File:{} to tempDir".format(uploadedfile.name))

st.title("Aplicativo de Descompactação de Arquivos Zip")
uploaded_file = st.file_uploader("Escolha um arquivo zip", type="zip")
if uploaded_file is not None:
    if not os.path.exists('tempDir'):
        os.makedirs('tempDir')
    save_uploadedfile(uploaded_file)
    with zipfile.ZipFile(uploaded_file, 'r') as zip_ref:
        zip_ref.extractall("tempDir")
    st.write("Arquivos e subpastas no arquivo zip:")
    for root, dirs, files in os.walk("tempDir"):
        for filename in files:
            st.text(os.path.join(root, filename))
    shutil.rmtree('tempDir')
