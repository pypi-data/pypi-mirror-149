#!/usr/bin/env python

__author__ = "Tom Zastrow"
__copyright__ = "Copyright 2022, Tom Zastrow"
__credits__ = ["Tom Zastrow"]
__license__ = "GPL"
__version__ = "3"
__maintainer__ = "Tom Zastrow"
__email__ = "thomas.zastrow@mpcdf.mpg.de"
__status__ = "Development"

from elasticsearch import Elasticsearch
from elasticsearch import RequestsHttpConnection
import lateco.Items as WP

class Queries(object):
    def __init__(self, url, port, user, pwd):
        self.cursor = Elasticsearch([url + ":" + str(port)], http_auth=(user, pwd), timeout=300, connection_class=RequestsHttpConnection,use_ssl=True, verify_certs=False)

    def match(self, ind, layer, query, size, source):
        q = {
            "query": {
                "match": {
                    layer: query,
                }
            },
            "size": size,
            "_source": source
        }
        res = self.cursor.search(index=ind, body=q)
        results = []
        for record in res["hits"]["hits"]:
            results.append(record["_source"]["subcorpus"])
        return results

    def matchPhrase(self, ind, layer, query, slop, size, source):
        q = {
            "query": {
                "match_phrase": {
                    layer: {
                        "query": query,
                        "slop": slop
                    }
                },                
            },
            
            "size": size,
            "_source": source,
            "track_total_hits": True
        }

        res = self.cursor.search(index=ind, body=q)

        return res

    def matchPhraseScroll(self, ind, layer, query, slop):
        q = {
            "query": {
                "match_phrase": {
                    layer: {
                        "query": query,
                        "slop": slop
                    }
                },                
            },
            "_source": True,
            "track_total_hits": True
        }

        res = self.cursor.search(index=ind, body=q, scroll = '2m', size=1000)
        sid = res['_scroll_id']
        scroll_size = res['hits']['total']['value']        
        
        pages = []
        for p in res["hits"]["hits"]:
                pages.append(p)
        
        while (scroll_size > 0):
            page = self.cursor.scroll(scroll_id = sid, scroll = '2m')
            for p in page["hits"]["hits"]:
                pages.append(p)

            sid = page['_scroll_id']
            scroll_size = len(page['hits']['hits'])

        return pages

class Result():
    def __init__(self, result):
        #self, id, score, subcorpus, articleId, token, lemma, pos
        
        self.id = result["_id"]
        self.score = result["_score"]
        self.subcorpus = result["_source"]["subcorpus"]
        self.articleId = result["_source"]["article"]

        self.sentence = WP.Sentence()
        token = result["_source"]["token"].split(" ")
        lemma = result["_source"]["lemma"].split(" ")
        pos = result["_source"]["pos"].split(" ")

        for i in range(0, len(token)):
            t = WP.Token(token[i], lemma[i], pos[i], "", "")
            self.sentence.tokens.append(t)

if __name__ == "__main__":
    print("These are objects for the lateco framework, call them from your own applications!")
