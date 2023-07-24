# -*- coding: UTF-8 -*-
import streamlit as st
from utils.str_utils import render_color_for_text, compare_text, pred_token_process


def simple_demo(model, only_chinese, *args, **kwargs):
    with st.form("csc"):
        sentence = st.text_area("请输入你要修改的文本", max_chars=500, value="我是练西时长两年办的个人联系生菜徐坤！")

        submitted = st.form_submit_button("提交")

        if submitted:
            pred = model.predict(sentence)
            pred = pred_token_process(sentence, pred, only_chinese=only_chinese)
            diff_index = compare_text(sentence, pred)
            st.text("原句子为：")
            st.markdown(render_color_for_text(sentence, diff_index, color='red', format='markdown'))
            st.text("修改后为：")
            st.markdown(render_color_for_text(pred, diff_index, color='blue', format='markdown'))
