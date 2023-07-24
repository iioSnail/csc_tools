# -*- coding: UTF-8 -*-

from transformers import BertTokenizer, BertForMaskedLM

from models.base import CSCBaseModel
from utils.str_utils import convert_sentence_to_tokens, pred_token_process


class MacBert4CSC(CSCBaseModel):

    model_name = 'macbert4csc'

    def __init__(self, model_path="shibing624/macbert4csc-base-chinese", device='cpu', *args, **kwargs):
        super(MacBert4CSC, self).__init__()

        self.device = device
        print("self.device:", self.device)
        self.tokenizer = BertTokenizer.from_pretrained(model_path)
        self.model = BertForMaskedLM.from_pretrained(model_path).to(device)

    def predict(self, sentence):
        src_tokens = convert_sentence_to_tokens(sentence, self.tokenizer.get_vocab())
        inputs = self.tokenizer([src_tokens], return_tensors='pt', is_split_into_words=True).to(self.device)
        outputs = self.model(**inputs).logits

        pred_tokens = self.tokenizer.convert_ids_to_tokens(outputs.argmax(-1)[0, 1:-1])
        return pred_token_process(list(sentence), pred_tokens)


if __name__ == '__main__':
    model = MacBert4CSC()
    print(model.predict("我喜欢吃平果"))
    print(model.predict("我喜欢吃“平果”※"))
    print(model.predict("我喜欢吃平 果"))
    print(model.predict("我喜欢吃 平 果"))
    print(model.predict("我喜欢吃 平 果，嬹"))