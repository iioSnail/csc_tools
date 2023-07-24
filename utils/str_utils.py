# -*- coding: UTF-8 -*-

import re
import traceback

import docx
import fitz

special_tokens = ['[MASK]', '[PAD]', '[UNK]']
pad_tokens = [' ', '\n']


def is_chinese(uchar):
    return '\u4e00' <= uchar <= '\u9fa5'


def convert_sentence_to_tokens(sentence, vocab):
    src_tokens = list(sentence)
    for i in range(len(src_tokens)):
        if src_tokens[i] in pad_tokens:
            src_tokens[i] = '[PAD]'
            continue

        if src_tokens[i] not in vocab:
            src_tokens[i] = '[UNK]'

    return src_tokens


def pred_token_process(src_tokens, pred_tokens, only_chinese=False, ignore_token: list = None, output_sentence=True):
    if type(src_tokens) == str:
        src_tokens = list(src_tokens)

    if type(pred_tokens) == str:
        pred_tokens = list(pred_tokens)

    if len(src_tokens) != len(pred_tokens):
        print("[ERROR]输入输出长度不相等")
        print("src:", ''.join(src_tokens))
        print("pred:", ''.join(pred_tokens))
        if output_sentence:
            return ''.join(src_tokens)
        return src_tokens

    for i in range(len(src_tokens)):
        if src_tokens[i] in pad_tokens:
            pred_tokens[i] = src_tokens[i]

        if pred_tokens[i] in special_tokens:
            pred_tokens[i] = src_tokens[i]
            continue

        if only_chinese and not is_chinese(src_tokens[i]) \
                or len(pred_tokens[i]) > 1 \
                or len(pred_tokens[i]) <= 0:
            pred_tokens[i] = src_tokens[i]
            continue

        if ignore_token:
            if src_tokens[i] in ignore_token:
                pred_tokens[i] = src_tokens[i]
                continue

    if output_sentence:
        return ''.join(pred_tokens)

    return pred_tokens


def render_color_for_text(text, indices, color='red', format='console'):
    color_indices = {
        'black': '30',
        'red': '31',
        'green': '32',
        'yellow': '33'
    }

    char_list = list(text)
    for i in range(len(indices)):
        if indices[i]:
            if format in ['console', "sh", "shell"]:
                char_list[i] = "\033[" + color_indices.get(color, '30') + "m" + text[i] + "\033[0m"
            elif format in ['markdown', "md"]:
                char_list[i] = ":%s[**%s**]" % (color, char_list[i])

    return ''.join(char_list)


def compare_text(src: str, tgt: str):
    src_char_list = list(src)
    tgt_char_list = list(tgt)

    result = [False] * max(len(src_char_list), len(tgt_char_list))

    for i in range(min(len(src_char_list), len(tgt_char_list))):
        if src_char_list[i] != tgt_char_list[i]:
            result[i] = True

    return result


def count_diff_num(src: str, tgt: str):
    diff_indices = compare_text(src, tgt)
    return sum(diff_indices)


def split_sentence(para, max_length: int = None):
    """
    将中文段落分句。
    :param para 长段落
    :param max_length: 句子最大长度。若给出句子最大长度，则会合并多句，让其尽可能达到但不超过句子最大长度。若单句长度超过max_length，则会进行截取，将其拆分成多句。
    """
    separator = "[!@#]"

    para = re.sub('([。！？\?])([^”’])', r"\1%s\2" % separator, para)  # 单字符断句符
    para = re.sub('(\.{6})([^”’])', r"\1%s\2" % separator, para)  # 英文省略号
    para = re.sub('(\…{2})([^”’])', r"\1%s\2" % separator, para)  # 中文省略号
    para = re.sub('([。！？\?][”’])([^，。！？\?])', r'\1%s\2' % separator, para)

    sentences = para.split(separator)

    if max_length is None or max_length <= 0:
        return sentences

    final_sentences = []
    last_sentence = ''
    for i, sentence in enumerate(sentences):
        if len(sentence) > max_length:
            if last_sentence != '':
                final_sentences.append(last_sentence)
                last_sentence = ''

            # 拆分句子
            items = [sentence[i:i + max_length] for i in range(0, len(sentence), max_length)]
            final_sentences.extend(items[:-1])

            sentence = items[-1]

        if len(last_sentence) + len(sentence) > max_length:
            final_sentences.append(last_sentence)
            last_sentence = ''

        last_sentence += sentence

    if last_sentence != '':
        final_sentences.append(last_sentence)

    return final_sentences


def read_pdf_by_page(pdf_path):
    pages_contents = []
    with fitz.open(pdf_path) as doc:
        for page_num in range(doc.page_count):
            try:
                page = doc.load_page(page_num)
                pages_contents.append({
                    "index": str(page_num + 1),
                    "desc": "第 %d 页" % (page_num + 1),
                    "text": page.get_text(),
                })
            except Exception as e:
                traceback.print_exc()
                pages_contents.append("[ERROR]")
                print("解析第%d页出现异常" % (page_num + 1))

    return pages_contents


def read_docx_by_section(docx_file):
    """
    按章节返回内容。以2级标题为一个单位
    """
    doc = docx.Document(docx_file)

    sections = []
    current_section = ""
    current_heading = ""
    heading_1 = ""

    for paragraph in doc.paragraphs:
        if paragraph.style.name.startswith("Heading 1") \
                or paragraph.style.name.startswith("Heading 2"):  # Assuming heading styles are used to mark sections
            # Save the last section text when a new section is appeared.
            if current_section:
                if len(current_heading) > 20:
                    current_heading = current_heading[:17] + "..."

                sections.append({
                    "index": current_heading,
                    "desc": "章节“%s”" % current_heading,
                    "text": current_section.strip(),
                })
                current_heading = ""

            # If the text is heading 1, record the heading text for heading 2 section.
            if paragraph.style.name.startswith("Heading 1"):
                heading_1 = paragraph.text
                current_heading = heading_1

            current_section = paragraph.text

            if paragraph.style.name.startswith("Heading 2"):
                current_section = heading_1 + " " + current_section
                current_heading = current_section
        else:
            current_section += "\n" + paragraph.text

    if current_section:
        sections.append({
            "index": current_heading,
            "desc": "章节“%s”" % current_heading,
            "text": current_section.strip(),
        })

    return sections


def read_document(filepath, file_type: str):
    if file_type == 'pdf':
        return read_pdf_by_page(filepath)

    if file_type == 'docx':
        return read_docx_by_section(filepath)

    raise RuntimeError("暂不支持 %s 类型文件" % file_type)


if __name__ == '__main__':
    contents = read_document("../test.docx", file_type='docx')
    print(contents)
