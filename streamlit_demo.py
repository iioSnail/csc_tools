# -*- coding: UTF-8 -*-
import streamlit as st
import torch

from st_pages.document_demo import document_demo
from st_pages.longtext_demo import longtext_demo
from st_pages.simple_demo import simple_demo
from utils.reflect_utils import get_model_names, load_model

st.set_page_config(layout="wide")


def intro(*args, **kwargs):
    st.markdown(
        """
        # 中文拼写纠错（Chinese Spell Correction）工具
        
        本项目是一个中文拼写纠错集工具箱，方便用户对自己的文章、文档等进行改错。
        """
    )


pages_names_to_funcs = {
    "-": intro,
    "简单文本校对": simple_demo,
    "长文本校对": longtext_demo,
    "文档校对": document_demo,
}

demo_name = st.sidebar.selectbox("选择工具", pages_names_to_funcs.keys())

st.sidebar.write("设置")


device_list = ['cpu']
if torch.cuda.is_available():
    device_list.append('cuda')
st_device = st.sidebar.selectbox("请选择推理设备:", options=device_list)

st_model_name = st.sidebar.selectbox("请选择您要使用的模型:", options=get_model_names())
max_length = st.sidebar.number_input("max length:", min_value=32, max_value=512, value=256,
                                     help="输入模型的最大文本长度。若文本超过该长度，则将会按照该长度进行截取。注意：若长度太长会导致OOM")
only_chinese = st.sidebar.checkbox("仅修改汉字", value=True)


@st.cache_resource
def _load_model(model_name, device):
    print("model_name:", model_name)
    print("device:", device)
    return load_model(model_name, device)


model = _load_model(st_model_name, st_device)
if model is None:
    st.error("加载模型失败!")
    st.cache_resource.clear()
    exit(0)

pages_names_to_funcs[demo_name](model=model, max_length=max_length, only_chinese=only_chinese)
