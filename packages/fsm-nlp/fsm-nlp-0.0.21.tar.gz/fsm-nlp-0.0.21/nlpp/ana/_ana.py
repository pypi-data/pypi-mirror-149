import pandas as pd
import numpy as np

from spacy.language import Language
from spacy.tokens import Doc, Token

Doc.set_extension("keyword_found", default=False)
Doc.set_extension("res", default={})
Token.set_extension("contains_keyword", default=False)


@Language.component("keyword_search")
def keyword_search(corpus, keyword):
    for doc in corpus:
        method = "keyword_search"
        doc._.keyword_found = True
        for token in doc:
            if keyword in token.text:
                token._.contains_keyword = True

        if method in doc._.analysis:
            doc._.analysis["keyword_search"].append(keyword)
        else:
            doc._.analysis[method] = [keyword]
        doc._.res = create_doc_dataframe(doc)
    # return doc
    res = create_res_dataframe(corpus)
    return res

def create_res_dataframe(corpus):

    dfs = []

    max_time = max([value for doc in corpus for value in doc._.res.timestamp])
    for i, doc in enumerate(corpus):
        df = corpus[i]._.res
        df['str'] = df.timestamp.apply(lambda x: x.isoformat())
        df['datetime'] = pd.to_datetime(df['str'], infer_datetime_format=True)
        max_datetime = pd.to_datetime(max_time.isoformat())
        df[doc._.title] = 1
        res = df.groupby(pd.Grouper(key='datetime', freq="1s")).count()
        res[doc._.title] = res[doc._.title].cumsum()
        res = res[[doc._.title]]
        res.loc[res.index[0].floor('d')] = 0
        res.sort_index(inplace=True)
        # res.reindex(method='ffill')
        # max_time = max(df.datetime)
        seconds = (max_datetime - max_datetime.floor('d')).seconds
        date_index = pd.date_range(max_datetime.floor('d'), periods=seconds, freq='s')
        print(len(date_index))
        res = res.reindex(date_index)
        dfs.append(res)

    # df = dfs[0].append(dfs[1:])
    df = pd.concat(dfs, axis=1)
    # date_index = pd.date_range(dfs[0].index[0], periods=max([len(df) for df in dfs]), freq='s')
    # df.reindex(date_index)
    df.fillna(method='ffill', inplace=True)
    df.fillna(0, inplace=True)
    return df

def create_doc_dataframe(doc):
    words = [token.text for token in doc if token._.contains_keyword]
    timestamps = [token._.timestamp for token in doc if token._.contains_keyword]

    df = pd.DataFrame(list(zip(words, timestamps)),
            columns = ["word", "timestamp"]
    )

    df.index +=1
    return df
