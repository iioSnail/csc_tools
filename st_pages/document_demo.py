# -*- coding: UTF-8 -*-

import os
from pathlib import Path
from tempfile import NamedTemporaryFile

import streamlit as st

from utils.str_utils import render_color_for_text, compare_text, split_sentence, pred_token_process, read_pdf_by_page, \
    count_diff_num, read_document

TEMP_DIR = Path("./tmp")
os.makedirs(TEMP_DIR, exist_ok=True)


def document_demo(model, max_length, only_chinese, *args, **kwargs):
    with st.form("csc"):
        uploaded_file = st.file_uploader("请上传要检测的文档", type=['pdf', 'docx'])
        submitted = st.form_submit_button("提交")

    pbar = st.progress(0)

    error_page_st = st.empty()
    error_pages = []

    if submitted:
        if uploaded_file is None:
            st.warning('请选择要纠错的文件！')
            return
        file_type = uploaded_file.name.split(".")[-1]
        with NamedTemporaryFile(dir='./tmp', suffix='.%s' % file_type, delete=False) as f:
            f.write(uploaded_file.getbuffer())
            filepath = f.name

        print("Temp filepath: ", filepath)

        spliter = ''
        if file_type in ['pdf']:
            spliter = '页码'
        if file_type in ['docx']:
            spliter = '章节'

        file_contents = read_document(filepath, file_type)
        for con_i, content in enumerate(file_contents):

            sentences = split_sentence(para=content['text'], max_length=max_length)
            paragraph = ''.join(sentences)

            pred_para = ''
            for i, sentence in enumerate(sentences):
                pred = model.predict(sentence)
                pred = pred_token_process(sentence, pred, only_chinese=only_chinese)
                pred_para += pred

            diff_index = compare_text(paragraph, pred_para)
            error_num = count_diff_num(paragraph, pred_para)

            if error_num:
                error_pages.append(content['index'])

            if len(error_pages) == 0:
                error_page_st.caption('暂未发现错误')
            else:
                error_page_st.caption('包含错字的%s：:red[%s]' % (spliter, ', '.join(error_pages)))

            c1, c2 = st.columns([0.5, 0.5])

            con1 = c1.expander("%s修改前" % content['desc'], expanded=False)
            if error_num > 0:
                con2 = c2.expander("%s修改后（错字数量: :red[**%d**]）" % (content['desc'], error_num), expanded=False)
            else:
                con2 = c2.expander("%s修改后（未发现错误）" % content['desc'], expanded=False)

            con1.markdown(render_color_for_text(paragraph, diff_index, color='red', format='markdown')
                          .replace(" ", "&nbsp;").replace("\n", "<br>"), unsafe_allow_html=True)
            con2.markdown(render_color_for_text(pred_para, diff_index, color='blue', format='markdown')
                          .replace(" ", "&nbsp;").replace("\n", "<br>"), unsafe_allow_html=True)

            pbar.progress(con_i / len(file_contents))

        if len(error_pages) == 0:
            error_page_st.caption('解析完毕！未发现错误')
        else:
            error_page_st.caption('解析完毕！包含错字的%s：:red[%s]' % (spliter, ', '.join(error_pages)))
