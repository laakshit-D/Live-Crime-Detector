
import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, RTCConfiguration
import av
import threading

RTC_CONFIGURATION = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)

st.set_page_config(page_title="Streamlit WebRTC Demo", page_icon="🤖")
task_list = ["Video Stream"]

with st.sidebar:
    st.title('Task Selection')
    task_name = st.selectbox("Select your tasks:", task_list)
st.title(task_name)

framezz=[]

def convert(framezz):
    import numpy as np
    import cv2

    print("hi",len(framezz))
    output_file = 'output_video.mp4'
    codec = cv2.VideoWriter_fourcc(*'mp4v')
    fps = 30.0
    frame_size = (640, 480)
    video_writer = cv2.VideoWriter(output_file, codec, fps, frame_size)

            # Assume frames is a list of frames
    for frame in framezz:
        video_writer.write(frame)

    video_writer.release()

if task_name == task_list[0]:
    style_list = ['color', 'black and white']

    st.sidebar.header('Style Selection')
    style_selection = st.sidebar.selectbox("Choose your style:", style_list)



    class VideoProcessor(VideoProcessorBase):
        def __init__(self):
            self.model_lock = threading.Lock()
            self.style = style_list[0]

        def update_style(self, new_style):
            if self.style != new_style:
                with self.model_lock:
                    self.style = new_style

        def recv(self, frame):
            # img = frame.to_ndarray(format="bgr24")
            img = frame.to_image() 
            framezz.append(frame)
            print(len(framezz))
            if len(framezz)==200:
                convert(framezz)
            if self.style == style_list[1]:
                img = img.convert("L")

            # return av.VideoFrame.from_ndarray(img, format="bgr24")
            return av.VideoFrame.from_image(img)

    ctx = webrtc_streamer(
        key="example",
        video_processor_factory=VideoProcessor,
        rtc_configuration=RTC_CONFIGURATION,
        media_stream_constraints={
            "video": True,
            "audio": False
        }
    )

    if ctx.video_processor:
        ctx.video_transformer.update_style(style_selection)
        



        

        
    