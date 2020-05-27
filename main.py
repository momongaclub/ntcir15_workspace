import Data
import sys

from bert_serving.client import BertClient

def bert(data):
    for query, text in data.queryid2texts.items():
        texts = []
        queryid2texts = {}
        all_ = []
        bc = BertClient(ip='localhost')
        query = [query]
        print(query)
        query_embeddings = bc.encode(query)
        all_.append(query_embeddings)
        for t in text:
            t = [t]
            t_embeddings = bc.encode(t)
            texts.append(t_embeddings)
            all_.append(t_embeddings)
        #queryid2texts[query_embeddings] = texts
    #return queryid2texts
    return all_

def main():
    data = Data.Data()
    data.load_query(sys.argv[1])
    data.load_textdata(sys.argv[2])
    data.load_result(sys.argv[3])
    data.convnert_id2text()
    queryid2texts = bert(data)
    print(queryid2texts)

if __name__ == '__main__':
    main()
