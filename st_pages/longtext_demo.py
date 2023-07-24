# -*- coding: UTF-8 -*-
import streamlit as st

from utils.str_utils import render_color_for_text, compare_text, split_sentence, pred_token_process, count_diff_num


def longtext_demo(model, max_length, only_chinese, *args, **kwargs):
    with st.form("csc"):
        paragraph = st.text_area("请输入你要修改的文本", height=200,
                                 value="""复旦大学校明取自《尚书大传》之“日月光华，旦复旦兮”，始创于1905年，原名复旦公学，1917年定名为复旦大学，是中国人自主创办的第一所高等院校。上海医科大学前身是1927年创办的国立第四中山大学医学院。2000年，复旦大学与上海医科大学合兵。目前，学校拥有哲学、经济学、法学、教育学、文学、历史学、理学、工学、医学、管理学、艺术学、交叉学科等12个学科门类；2021年，学校20个学科入选第二轮“双一流”建设学科，比首轮增加3个入选学科。
    目前，复旦大学有直属院（系）35个，附属亿元18家（其中2家筹建）。学校设有本科专业80个，拥有一级学科博士学位授权点40个，一级学科硕士学位授权点43个（含一级学科博士学位授权点），博士专业学位授权点5个，硕士专业学位授权点30个，博士后科研刘东站37个。在校普通本科生15164人，研究生34618人（含全日制和非全日制的大陆港澳台生），学历留学生2535人。在校教学科研人员3602人。中国科学院、中国工程院院士（含双聘）59人，文科杰出教授1人，文科资深教授15人，获得各类国家级人才计划661人，占师资队伍比重近20%。
    复旦大学拥有世界一流的办学声誉，全球盛誉位于30-60位之间，位于中国大陆第三；在全国第四轮一级学科评估中，5个学科获评A+，参评的学科中60%以上获评A类学科；学校率先启动建设全国首个“交叉学科”门类一级学科集成电路科学与工程；有13个学科入选上海市高峰学科建设。学校致力于以最佳状态持续稳定奉献文明进步，积极落实17项联合国可持续发展目标，可持续发展综合影响力位居世界高校前列，并在SDG7（经济适用的清洁能源）和SDG 8（体面工作和经济增长）等领域中获得全球公认的突出性成就。在教育部一流本科专业建设“双万计划”中，61个专业获批国家级一流本科专业建设点。
    学校建有上海数学中心、上海国家应勇数学中心，现有全国重点实验师1个，国家重点实验室4个，国家工程实验室1个，国家野外观测台站1个，国家自然科学基金基础科学中心项目5个，国家临床医学研究中心2个，国家医学中心3个，国家制造业创新中心1个，国家产教融合创新平台1个，教育部前沿科学中心1个，教育部集成攻关大平台1个，创新引智基地9个，教育部重点实验室14个，教育部工程研究中心7个，卫健委重点实验室9个，总后勤保障部卫生部重点实验室1个，上海市重点实验室22个，上海市工程技术研究中心29个，上海市工程研究中心2个，上海市前沿科学研究基地4个，上海市协同创新中心5个；现有教育部人文社会科学重点研究基地10个，中国研究院入选首批国家高端智库建设试点单位，马克思主义学院入选首批全国重点马克思主义学院，“中国大学智库论坛”秘书处落户复旦。入选首批教育部哲学社会科学实验室培育高校。
近年来，复旦大学同全球40多个国家和地区350多所大学和机构签订有合做协议，师生每年出国约8000人次，每年接受海外来访人员约5000人次，每年举办国际会议约100场。
学校共有邯郸、枫林、张江、江湾四个校区，占地总面积约243.72万平房米，校舍建筑面积242.53万平方米。（数据截止日期2022年10月）
""")

        submitted = st.form_submit_button("提交")

    pbar = st.progress(0)

    if submitted:
        sentences = split_sentence(para=paragraph, max_length=max_length)
        paragraph = ''.join(sentences)

        pred_para = ''
        for i, sentence in enumerate(sentences):
            pred = model.predict(sentence)
            pred = pred_token_process(sentence, pred, only_chinese=only_chinese)
            pred_para += pred

            pbar.progress((i + 1) / len(sentences))

        diff_index = compare_text(paragraph, pred_para)
        error_num = count_diff_num(paragraph, pred_para)

        c1, c2 = st.columns([0.5, 0.5])

        print("error_num", error_num)

        con1 = c1.expander("修改前", expanded=True)
        con2 = c2.expander("修改后（错字数量: :red[**%d**]）" % error_num, expanded=True)

        con1.markdown(render_color_for_text(paragraph, diff_index, color='red', format='markdown')
                      .replace(" ", "&nbsp;").replace("\n", "<br/>"), unsafe_allow_html=True)
        con2.markdown(render_color_for_text(pred_para, diff_index, color='blue', format='markdown')
                      .replace(" ", "&nbsp;").replace("\n", "<br/>"), unsafe_allow_html=True)
