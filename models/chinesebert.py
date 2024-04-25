import os.path

from transformers import AutoTokenizer, AutoModel

from models.base import CSCBaseModel
from utils.str_utils import convert_sentence_to_tokens, pred_token_process


class ChineseBertForCSC(CSCBaseModel):

    model_name = "ChineseBertForCSC(SCOPE)"

    def __init__(self, model_path="iioSnail/ChineseBERT-for-csc", device='cpu', *args, **kwargs):
        super(ChineseBertForCSC, self).__init__()

        self.device = device
        self.tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
        self.model = AutoModel.from_pretrained(model_path, trust_remote_code=True).to(self.device)

    def predict(self, sentence):
        src_tokens = convert_sentence_to_tokens(sentence, self.tokenizer.get_vocab())
        inputs = self.tokenizer([src_tokens], return_tensors='pt', is_split_into_words=True).to(self.device)
        outputs = self.model(**inputs).logits

        pred_tokens = self.tokenizer.convert_ids_to_tokens(outputs.argmax(-1)[0, 1:-1])
        return pred_token_process(list(sentence), pred_tokens)
