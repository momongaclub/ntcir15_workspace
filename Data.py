import sys
import json

class Data():

    def __init__(self):
        self.query_sentences = []
        self.result_queryid2texts = {}
        self.queryid2query = {}
        self.textid2text = {}
        self.queryid2texts = {}

    def load_textdata(self, fname):
        decoder = json.JSONDecoder()
        with open(fname, 'r') as fp:
            for line in fp:
                data = json.loads(line)
                self.textid2text[data['id']] = data['title']
                # TODO \u3000 全角空白がタイトルに含まれている

    def load_query(self, fname):
        with open(fname, 'r') as fp:
            for line in fp:
                line = line.rstrip('\n')
                line = line.split('\t')
                queryid = line[0]
                query = line[1]
                self.queryid2query[queryid] = query

    def load_result(self, fname):
        with open(fname, 'r') as fp:
            for line in fp:
                line = line.rstrip('\n')
                line = line.split(' ')
                queryid = line[0]
                textid = line[2]
                # 結果のテキストidをテキストへ
                # 結果のクエリidをクエリ文へ
                if self.result_queryid2texts.get(queryid) == None:
                    self.result_queryid2texts[queryid] = []
                else:
                    self.result_queryid2texts[queryid].append(textid)

    def convnert_id2text(self):
        for key, value in self.result_queryid2texts.items():
            v_list = []
            for v in value:
                v_list.append(self.textid2text[v])
            query = self.queryid2query[key]
            self.queryid2texts[query] = v_list

def main():
    data = Data()
    data.load_query(sys.argv[1])
    data.load_textdata(sys.argv[2])
    data.load_result(sys.argv[3])
    data.convnert_id2text()
# 元データ読み込み
# 元データからresultファイルのクエリ文とテキストデータを引っ張って来る
# それを格納して返す

if __name__ == '__main__':
    main()
