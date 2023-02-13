import streamlit as st
from constants import (MODELS_LIST, FILE_TYPES_LIST , LANGUAGES_SMALL,
                       INPUT_HELP_TEXT , help_dict)
from streamlit_ace import st_ace
from pygments.lexers import guess_lexer
from extra_func import read_up_file, snippets_dict_get
from openai_func import ai_answers
from ya_api import ya_translate
import os

app_path = os.getenv("APP_PATH")


st.set_page_config(
     page_title = "Open AI",
     page_icon = ":robot_face:",
     layout = 'wide',
     initial_sidebar_state = "auto",
     menu_items = {
         'Get Help': 'https://github.com/sham-sr/',
         'Report a bug': 'https://github.com/sham-sr/',
         'About': 'GPT model test'
     }
)    
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

def update_state():
    del st.session_state['ext_input']
    del st.session_state['final_out']
    if 'st.instruct' in st.session_state:
        st.session_state['st.instruct']=''


snippets_dict = snippets_dict_get(app_path+'/snippets.txt')
s11,s12 = st.columns([1,1])
select_snippets = s11.selectbox('Snippets',['']+list(snippets_dict.keys()),
                                 index=0,
                                 format_func = snippets_dict.get,
                                 on_change=update_state)
uploaded_files = s12.file_uploader('Upload file', type=FILE_TYPES_LIST, on_change=update_state)
uploaded_text = read_up_file(uploaded_files,ftype='string_data')

# очистка вывода
if 'ai_out' not in st.session_state:
    st.session_state['ai_out']=''

# перелючаю между снипетами и загрузкой файлов
if 'final_out' not in st.session_state:
    st.session_state['final_out'] = None
if select_snippets != '' and  uploaded_text is None and st.session_state['final_out'] is None:
    st.session_state['ext_input'] = select_snippets
elif uploaded_text is not None and st.session_state['final_out'] is None:
    st.session_state['ext_input'] = uploaded_text
elif st.session_state['final_out']:
    st.session_state['ext_input'] = st.session_state['final_out']
else:
    st.session_state['ext_input'] = None 


with st.sidebar:
    model = st.selectbox('Модель:', MODELS_LIST)
    if model=="text-davinci-003":
        pre_temp = 0.7
        pre_max= 512
    else:
        pre_max = 128
        pre_temp = 0.05
    temperature = st.slider('Температура:', min_value=0.0, max_value=1.0, value=pre_temp,step=0.01,help=help_dict('temperature'))
    max_tokens = st.slider('Max токенов:', min_value=1, max_value=2048, value=pre_max,step=1,help=help_dict('max_tokens'))
    top_p = st.slider('Top P:', min_value=0.0, max_value=1.0, value=1.0,step=0.1,help=help_dict('top_p'))
    frequency_penalty = st.slider('Frequency penalty:', min_value=0.0, max_value=2.0, value=0.0,step=0.01,help=help_dict('frequency_penalty'))
    presence_penalty = st.slider('Presence penalty:', min_value=0.0, max_value=2.0, value=0.0,step=0.01,help=help_dict('presence_penalty'))
    best_of = st.slider('Best of:', min_value=1, max_value=3, value=1,step=1,help=help_dict('best_of'))
    st.checkbox('Использовать ответ ИИ', value=False)

s21,s22,s23,s24,s25 = st.columns([1.5,2.1,.4,2,2])
s21.markdown('## ')
s21.markdown('**F5** сбросить всё')

s23.markdown('## ')
out_lang = s24.radio('Язык вывода', ['en','ru'], horizontal=True, key ='st.p_lang')
select_lang = s25.selectbox('Язык программирования', ['text']+LANGUAGES_SMALL) 
    
inp,out = st.columns([1,1])
with inp:
    if st.session_state['ext_input'] is not None or st.session_state['ext_input'] !='':
        in_text = st_ace(value=st.session_state['ext_input'],
                        placeholder='',
                        auto_update=True,
                        language=select_lang)
    else:
        in_text = st_ace(value='',
                        placeholder=INPUT_HELP_TEXT,
                        auto_update=True,
                        language=select_lang)
    instruct = st.text_input('Инструкции:', help=None, key='st.instruct')

def sent_to_ai(in_text,instruct,model,temperature,max_tokens,top_p,best_of,frequency_penalty,presence_penalty,kep_first):
    try:
        eng_in_text = ya_translate(in_text,target_language='en')
        st.session_state['eng_in_text']  = eng_in_text
    except:
        eng_in_text = 'Ошибка автоперевода на en'
        st.session_state['eng_in_text'] = eng_in_text
    try:
        instruct_eng = ya_translate(instruct,target_language='en')
    except:
        instruct_eng = ''
    eng_in_text = f'{eng_in_text}\n{instruct_eng}'
    if  eng_in_text != 'Ошибка автоперевода на en' or eng_in_text != f'Ошибка автоперевода на en\n{instruct_eng}':
        try:
            ai_out = ai_answers(os.getenv("ORGANIZATION"),
                            os.getenv("OPENAI_API_KEY"),
                            prompt=eng_in_text,
                            model=model,              
                            temperature=temperature,
                            max_tokens=max_tokens,
                            top_p=top_p,
                            best_of =best_of,
                            frequency_penalty=frequency_penalty,
                            presence_penalty=presence_penalty,
                            kep_first=kep_first)['text'] 
        except:
            ai_out = 'Ошибка ответа AI'
    else:
        ai_out = eng_in_text
    st.session_state['ai_out']=ai_out
    st.session_state['st.instruct']=''


if 'ai_out' not in st.session_state:
    st.session_state['ai_out']=''

with out:
    st_ace(value=''+st.session_state['ai_out'],
                   auto_update=True,
                   language=select_lang,
                   key='out_ace')


def copy_out(final_out):
    if final_out is not None or final_out !='':
        st.session_state['st.instruct']=''
        st.session_state['final_out'] = final_out


s23.button('<',help='Вставиь ответ ИИ. Можно использовать для итеративного програмиирования',
             on_click=copy_out,args=(st.session_state['final_out'],))

#st.write(f'Вероятный язык ввода:{guess_lexer(in_text).name}')    
st.button('Отправить ИИ', type='primary',on_click=sent_to_ai,args=(in_text,
                                                                   instruct,
                                                                   model,
                                                                   temperature,
                                                                   max_tokens,
                                                                   top_p,best_of,
                                                                   frequency_penalty,
                                                                   presence_penalty,
                                                                   True)) 


       

with st.expander('Инструкции по OpenAI', expanded=False):
    with open(app_path+'/help.md','r') as f:
        help_text = f.read()
    st.markdown(help_text)
