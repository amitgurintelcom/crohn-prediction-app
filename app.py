import streamlit as st
from streamlit_option_menu import option_menu
import http.client
import base64
import json
import re
import os
###################################
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid.shared import JsCode
from moviepy.editor import VideoFileClip
###################################
from PIL import Image
import io


def _max_width_():
    max_width_str = f"max-width: 1800px;"
    st.markdown(
        f"""
    <style>
    .reportview-container .main .block-container{{
        {max_width_str}
    }}
    </style>    
    """,
        unsafe_allow_html=True,
    )

def load_pre_defined_video():
    try:
        if os.path.exists("myvideo.mp4"):
            with open('myvideo.mp4', 'rb') as f:
                vid = f.read()
            return vid
    except:
        return None

def present_video(content):
    try:
        if not os.path.exists("myvideo.mp4"):
            videoClip = VideoFileClip(content).subclip(0,60)
            clip_resized = videoClip.resize(height=360)
            clip_resized.write_videofile("myvideo.mp4", fps=25)

        with open('myvideo.mp4', 'rb') as f:
            vid = f.read()
        return vid
    except:
        return None 


def send_request(video, conn_req, conn_addr, api_key):
    video_url="https://libhub-readme.s3.us-west-2.amazonaws.com/crohns-app-cvbock/video.mpeg"
    request_dict =  {"video":video} # {"video":video_url}
    payload = '{"input_params":' + json.dumps(request_dict) + "}"
    headers = {
            'Cnvrg-Api-Key': api_key,
            'Content-Type': "application/json"
            }
    vid = present_video(video)
    send_to_endpoint(payload, headers, conn_req, conn_addr, vid=vid)


def send_pre_defined(conn_req, conn_addr, api_key):
    video_url="https://libhub-readme.s3.us-west-2.amazonaws.com/crohns-app-cvbock/video.mpeg"
    request_dict =  {"video":''} # {"video":video_url}
    payload = '{"input_params":' + json.dumps(request_dict) + "}"
    headers = {
            'Cnvrg-Api-Key': api_key,
            'Content-Type': "application/json"
            }
    vid = load_pre_defined_video()
    send_to_endpoint(payload, headers, conn_req, conn_addr)


def send_to_endpoint(payload, headers, conn_req, conn_addr, vid=None):
    is_exception_raised = False
    output = None
    with st.spinner('This might take few seconds ... '):
        try:
            conn = http.client.HTTPSConnection(conn_addr)
            st.info('Sending File to the server')
            conn.request("POST", conn_req, payload, headers)
            st.info('Got server POST response')
            res = conn.getresponse()
            data = res.read()
            output = data.decode("utf-8")
        except:
            st.error('Cant connect to server. Try to disable VPN!')
            is_exception_raised = True
            output = None

    if not is_exception_raised and output is not None:
        #print(output)
        #print("@@@ \n", json.loads(output))
        prediction = float(json.loads(output)['prediction'][0])
        confidence = json.loads(output)['prediction'][1]
        if prediction==1:
            pred_str='Yes'
            conf_win= float(confidence[1])*100
        else:
            pred_str='No'
            conf_win= float(confidence[0])*100
        print("prediction:", prediction)
        images = json.loads(output)['prediction'][2]['images']
    
        c1, c2 = st.columns([3,5])
        with c1:
            if vid:
                with st.spinner('Preview input video ...'):
                    st.video(vid)
        with c2:
            st.metric(label="Diseases treatment success Prediction:", value=f"{pred_str}")
            st.metric(label=f'confidence level', value=f"{conf_win}%")
            for i,image_1 in enumerate(images):
                image_data = base64.b64decode(image_1) 
                image_2 = Image.open(io.BytesIO(image_data))
                st.image(image_2, width=500)
    else:
        st.info(f"""???? Please upload a .mpg Capsule Endoscopy video first""")


def select_host(selected):
    if selected=="AWS":
        api_key=os.getenv('api_key_aws')
        conn_addr=os.getenv('conn_addr_aws')
        conn_req=os.getenv('conn_req_aws')
        # api_key="dm32GHs3S9eojhMm5SsV9FbG"
        # conn_addr="gastro-web-4-1.am22ensuxenodo5ihblszm8.cloud.cnvrg.io"
        # conn_req="/api/v1/endpoints/cukczelw3sytfuga7byy"
    elif selected=="Intel DevCloud":
        api_key=os.getenv('api_key_intel')
        conn_addr=os.getenv('conn_addr_intel')
        conn_req=os.getenv('conn_req_intel')        
        # api_key="WeaN8QbbKmhWZHJryoJzuUM1"
        # conn_addr="ecg-web-dev-cloud-1.aaorm9bej4xwhihmdknjw5e.cloud.cnvrg.io"
        # conn_req="/api/v1/endpoints/q6wmgijl7mqesrqneoau"
    else:
        api_key=os.getenv('api_key_aws')
        conn_addr=os.getenv('conn_addr_aws')
        conn_req=os.getenv('conn_req_aws')
        # api_key="dm32GHs3S9eojhMm5SsV9FbG"
        # conn_addr="gastro-web-4-1.am22ensuxenodo5ihblszm8.cloud.cnvrg.io"
        # conn_req="/api/v1/endpoints/cukczelw3sytfuga7byy"
    return api_key, conn_addr, conn_req


st.set_page_config(page_icon="??????", page_title="Crohn's Treatment Outcome Prediction", layout="wide")

with st.sidebar:
        st.image('./intel.png', width=90)
        st.subheader('Developer Cloud')
        st.image("footer.png")
        st.write("")
        st.write("")
        selected = option_menu(
            menu_title="Choose web host",  # required
            options=["Intel DevCloud", "AWS (Future)", "Azure (Future)"],  # required
            icons=["snow2", "bank2", "microsoft"],  # optional
            menu_icon="heart-pulse",  # optional
            default_index=0,  # optional
                )
        st.info(f'web host is {selected}', icon="??????")


st.title("Crohn's Treatment Outcome Prediction")
c1, _, c2 = st.columns([1,1,5])
with c1:
    st.image('CE_basic.jpg', width=200)
with c2:
    st.write('''
        Capsule endoscopy (CE) is a prime modality for diagnosing and monitoring Crohn's disease (CD). 
        However, CE's video wasn't utilized for predicting the success of biologic therapy.
        This demo runs the Timesformer model trained on Sheba data by Intel's New AI technologies group.
        The model reaches a 20% improvement over the best existing biomarker (fecal calprotectin) while providing decision explainability and confidence level
        ''')

api_key, conn_addr, conn_req = select_host(selected)

pre_defined_video_demo, upload_your_own = st.tabs(["Run Example", "Upload Your Own"])

with pre_defined_video_demo:
    send_pre_defined(conn_req, conn_addr, api_key)

with upload_your_own:
    print('in upload your own')
    uploaded_file = st.file_uploader("", type="mpg", key="1")
    if uploaded_file is not None:
        content = uploaded_file.read()
        encoded_string = base64.b64encode(content).decode("utf-8")
        send_request(encoded_string, conn_req, conn_addr, api_key)


        