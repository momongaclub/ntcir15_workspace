import Data
import sys
import numpy as np
from numpy.linalg import norm
import sklearn.metrics.pairwise
from pyknp import Juman
from bert_serving.client import BertClient
import tokenization

CLS = '[CLS]'
SEP = '[SEP]'

def bert(data):
    jumanpp = Juman()
    tokenizer = tokenization.FullTokenizer(vocab_file='/home/mibayashi/programs/ntcir2020/bert/Japanese_L-12_H-768_A-12_E-30_BPE/vocab.txt',do_lower_case=False)
    for query, text in data.queryid2texts.items():
        texts = []
        queryid2texts = {}
        all_ = []
        bc = BertClient(ip='localhost')
        #tokenized_text = tokenizer.tokenize(query)
        #print('tokenized_text(not replace):',tokenized_text)
        #query = query.replace(' ', '')
        #q = jumanpp.analysis(query)
        tokenized_text = tokenizer.tokenize(query)
        tokenized_text.insert(0, CLS)
        tokenized_text.append(SEP)
        #print('tokenized_text(replaced):',tokenized_text)
        #query = [mrph.midasi for mrph in q.mrph_list()]
        print(tokenized_text)
        query_embeddings = bc.encode(tokenized_text)
        all_.append(query_embeddings)
        for t in text:
            #t = [t]
            # t = t.split(' ')
            #t = t.replace(' ', '')
            #te = jumanpp.analysis(t)
            tokenized_text = tokenizer.tokenize(t)
            tokenized_text.insert(0, CLS)
            tokenized_text.append(SEP)
            #t = [mrph.midasi for mrph in te.mrph_list()]
            print(tokenized_text)
            t_embeddings = bc.encode(tokenized_text)
            print('cls_sum:', np.sum(t_embeddings[0][0]))
            print('vec_sum:', np.sum(t_embeddings[0]))
            texts.append(t_embeddings)
            all_.append(t_embeddings)
        #queryid2texts[query_embeddings] = texts
    #return queryid2texts
    return all_

def cosine_similarity(vec):
    cos_sims = []
    #print('vec',vec)
    print('vec_len',len(vec))
    print('vec[0]_len', len(vec[0]))
    print('cls_vec', len(vec[0][0]))
    query_cls = vec[0][0]
    query_cls = np.array([query_cls])
    for v in vec:
        v_cls = v[0]
        print(len(v_cls),len(query_cls))
        #print(cosine_similarity(query,v))
        #print(cosine_similarity(query[0]))
        #print(numpy.sum(v[0]))
        #print(query[0], v[0])
        v_cls = np.array([v_cls])
        cos_sim = sklearn.metrics.pairwise.cosine_similarity(query_cls, v_cls)
        cos_sims.append(cos_sim)
    return cos_sims

def main():
    data = Data.Data()
    data.load_query(sys.argv[1])
    data.load_textdata(sys.argv[2])
    data.load_result(sys.argv[3])
    data.convnert_id2text()
    all_ = bert(data)
    #print(all_)
    cos_sims = cosine_similarity(all_)
    print(cos_sims)
    bc = BertClient(ip='localhost')
    t_embeddings = bc.encode([CLS, '秋田', SEP])
    print(np.sum(t_embeddings[0][0]))
    t_embeddings = bc.encode([CLS, '長野', SEP])
    print(np.sum(t_embeddings[0][0]))
if __name__ == '__main__':
    main()
