from paddlenlp.utils.log import logger
import random
import os
import json
import numpy as np
import paddle


def read_json_lines(file):
    return [json.loads(x) for x in open(file, encoding='utf-8')]


def write_json_lines(lines, out_path):
    with open(out_path, 'w+', encoding='utf-8') as f:
        for line in lines:
            line = json.dumps(line, ensure_ascii=False) + '\n'
            f.write(line)


def sequence_padding(inputs, length=None, value=0, seq_dims=1, mode='post', dtype='int64'):
    """Numpy函数，将序列padding到同一长度
    """
    if length is None:
        length = np.max([np.shape(x)[:seq_dims] for x in inputs], axis=0)
    elif not hasattr(length, '__getitem__'):
        length = [length]

    slices = [np.s_[:length[i]] for i in range(seq_dims)]
    slices = tuple(slices) if len(slices) > 1 else slices[0]
    pad_width = [(0, 0) for _ in np.shape(inputs[0])]

    outputs = []
    for x in inputs:
        x = x[slices]
        for i in range(seq_dims):
            if mode == 'post':
                pad_width[i] = (0, length[i] - np.shape(x)[i])
            elif mode == 'pre':
                pad_width[i] = (length[i] - np.shape(x)[i], 0)
            else:
                raise ValueError('"mode" argument must be "post" or "pre".')
        x = np.pad(x, pad_width, 'constant', constant_values=value)
        outputs.append(x)
    return np.array(outputs, dtype=dtype)


def seed_everything(seed):
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    np.random.seed(seed)
    paddle.seed(seed)


class AverageMeter:
    def __init__(self):
        self.total = 0
        self.n = 0

    def update(self, item):
        self.total += item
        self.n += 1

    def accumulate(self):
        return self.total / self.n

    def reset(self):
        self.total = 0
        self.n = 0


def dict_collate(batch):
    return {k: paddle.to_tensor(sequence_padding(v)) for k, v in batch.items()}

def list_collate(batch):
    return [sequence_padding(x) for x in batch]


def smart_save(model, model_save_path):
    save_dir = os.path.dirname(model_save_path)
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
    paddle.save(model.state_dict(), model_save_path)


def print_item(alist):
    for i in alist:
        print(i)


def stratified_sampling(df, by, test_frac=None, test_num=None, random_state=None):
    df.index = range(len(df))
    test_idx = []
    if test_num:
        test_frac = test_num / df.shape[0]
    for by, df_gp in df.groupby(by):
        test_idx += list(df_gp.sample(frac=test_frac, random_state=random_state).index)
    test = df[df.index.isin(test_idx)]
    train = df[~df.index.isin(test_idx)]
    return train, test


def label2id(alist):
    alist = sorted(set(alist))
    return dict(zip(alist, range(len(alist))))


if __name__ == '__main__':
    x1 = np.random.randn(3, 3)
    x2 = np.random.randn(4, 4)
    x3 = sequence_padding([x1, x2], seq_dims=2)
    print(x3.shape)
