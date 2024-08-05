import streamlit as st

# st.title('🎈 App Name')

# st.write('Hello world!')
import zipfile
import os
import shutil


def upload_myfile(content, token, repo_name, username = 'jrhumberto'):
    # Cria o repositório
    url = 'https://api.github.com/user/repos'
    headers = {'Authorization': f'token {token}'}
    payload = {'name': repo_name}
    response = requests.post(url, headers=headers, json=payload)

    # Cria um blob para o arquivo
    url = f'https://api.github.com/repos/{username}/{repo_name}/git/blobs'
    headers = {'Authorization': f'token {token}'}
    payload = {'content': file_content, 'encoding': 'utf-8'}
    response = requests.post(url, headers=headers, json=payload)
    blob_sha = response.json()['sha']

    # Cria uma árvore com o blob
    url = f'https://api.github.com/repos/{username}/{repo_name}/git/trees'
    headers = {'Authorization': f'token {token}'}
    payload = {'tree': [{'path': file_path, 'mode': '100644', 'type': 'blob', 'sha': blob_sha}]}
    response = requests.post(url, headers=headers, json=payload)
    tree_sha = response.json()['sha']

    # Cria um commit
    url = f'https://api.github.com/repos/{username}/{repo_name}/git/commits'
    headers = {'Authorization': f'token {token}'}
    payload = {'message': 'Seu commit message', 'tree': tree_sha}
    response = requests.post(url, headers=headers, json=payload)
    commit_sha = response.json()['sha']

    # Atualiza a referência do branch
    url = f'https://api.github.com/repos/{username}/{repo_name}/git/refs/heads/main'
    headers = {'Authorization': f'token {token}'}
    payload = {'sha': commit_sha}
    response = requests.patch(url, headers=headers, json=payload)

def save_uploadedfile(uploadedfile):
    with open(os.path.join("tempDir",uploadedfile.name),"wb") as f:
        f.write(uploadedfile.getbuffer())
    return st.success("Saved File:{} to tempDir".format(uploadedfile.name))

st.title("Aplicativo de Descompactação de Arquivos Zip")
chave = st.text_input("Digite um valor suficiente para o upload")
repositorio = st.text_input("Coloque um repositorio para o upload")
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
            # st.text(os.path.join(root, filename))
            content = filename.getvalue()
            upload_myfile(content=content, token=chave, repo_name=repositorio)
            st.text(f'{filename}')
            
    shutil.rmtree('tempDir')
#
if st.button("upload"):
    st.write('Conseguimos')
    st.text('E agora?')
#
