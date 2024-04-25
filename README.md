# csc_tools

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/iioSnail/csc_tools/blob/master/colab.ipynb)



# 项目介绍

csc_tools是一个中文拼写纠错（Chinese Spell Checking / Chinese Spell Correction, CSC）工具箱，帮助人们利用已有模型方便的进行中文拼写纠错。

> 中文拼写纠错仅针对错字进行修改，不处理多字和漏字的情况。

# 页面展示

目前，该工具支持如下功能：

- 简单文本校对：对不超过500字的中文文本进行纠错。
- 长文本校对：对不限文本长度的中文文本进行纠错。
- 文档校对：对文档进行校对。支持PDF和DOCX，其中PDF按页进行划分，DOCX按章节进行划分（以文章中的二级标题为一个单位）。

效果图如下：

![简单文本校对](./images/simple_demo.png)

![长文本校对](./images/longtext_demo.png)

![文档校对](./images/doc_demo.png)


# CSC模型

目前支持的模型如下：

- ChineseBertForCSC(SCOPE)（[Hugging Face](https://huggingface.co/iioSnail/ChineseBERT-for-csc), [Github](https://github.com/jiahaozhenbang/SCOPE), [论文](https://aclanthology.org/2022.emnlp-main.287/) ）：该模型源于对SCOPE论文的复现，几乎可以达到原论文的效果。
- macbert4csc（[Hugging Face](https://huggingface.co/shibing624/macbert4csc-base-chinese), [Github](https://github.com/shibing624/pycorrector) ）: 该模型在Github上虽然关注度较高，但效果相对要差一点。

# 项目部署

1.下载项目并安装依赖：

```
git clone https://github.com/iioSnail/csc_tools.git
cd csc_tools
pip install -r requirements.txt
```

2.运行`streamlit_demo.py`

```
streamlit run streamlit_demo.py
```

运行后会从huggingface下载模型，国内会由于网络问题加载失败，可手动下载后放到项目目录下。下载后的目录如下：

```
├── csc_tools
    ├── iioSnail  # 模型文件
    │   └── ChineseBERT-for-csc
    ├── shibing624  # 模型文件
    │   └── macbert4csc-base-chinese
    ├── images
    ├── models
    ├── st_pages
    ├── tmp
    └── utils
```

