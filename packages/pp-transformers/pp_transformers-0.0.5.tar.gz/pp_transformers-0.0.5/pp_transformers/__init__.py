from .bert import *
from .roformer2 import *
from .roberta import *
from .nezha import *
from .t5 import *
from .ernie import *
from .roformer import RoFormerModel as RoFormerModelV1
from .roformer import RoFormerForPretraining as RoFormerForPretrainingV1
from paddlenlp.transformers import BertTokenizer, AutoTokenizer, AutoModel
from .tokenizer import ErnieTokenizer
from .utils import logger


def create_mlm_model(args):
    model_path = args.model_path
    if 'roformer_v2' in model_path:
        model_class = RoFormerForPretraining
    elif 'roformer' in model_path:
        model_class = RoFormerForPretrainingV1
    elif 'nezha' in model_path:
        model_class = NeZhaForPretraining
    elif 'roberta' in model_path:
        model_class = RobertaForMaskedLM
    elif 'ernie' in model_path:
        model_class = ErnieForMaskedLM
    else:
        model_class = BertForMaskedLM
    model = model_class.from_pretrained(args.model_path)
    setattr(getattr(model, model.base_model_prefix), 'recompute', args.recompute)
    if args.recompute:
        logger.info('Using recompute')
    return model


def create_base_model(args):
    model_path = args.model_path
    if 'roformer_v2' in model_path:
        model_class = RoFormerModel
    elif 'roformer' in model_path:
        model_class = RoFormerModelV1
    elif 'nezha' in model_path:
        model_class = NeZhaModel
    elif 'roberta' in model_path:
        model_class = RobertaModel
    elif 'ernie' in model_path:
        model_class = ErnieModel
    else:
        model_class = BertModel
    model = model_class.from_pretrained(model_path)
    model.recompute = args.recompute
    if args.recompute:
        logger.info('Using recompute')
    return model


def create_tokenizer(args):
    model_path = args.model_path
    if 'ernie' in model_path:
        tokenizer = ErnieTokenizer.from_pretrained(model_path)
    else:
        try:
            tokenizer = BertTokenizer.from_pretrained(model_path)
        except:
            tokenizer = AutoTokenizer.from_pretrained(model_path)
    return tokenizer
