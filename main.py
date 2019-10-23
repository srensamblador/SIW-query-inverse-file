from index.index_persistence import load_inverse_file, print_inverse_file
from nltk import PorterStemmer, word_tokenize
from nltk.corpus import stopwords
import string, math, json
import heapq as hp

def main():
    index = load_inverse_file("index.json")
    query = "investigation boundary layer fluids crocco"
    query_terms, query_term_count = extract_terms(query)
    terms_dict = {}
    term_containing_docs = set()

    for term in query_terms:
        if term not in index:
            index[term] = {"idf": 0, "post_list": []}
        for doc in index[term]["post_list"]:
            term_containing_docs.add(doc["doc_id"])

    doc_similarity = {}
    dot_product = 0
    module_query = 0
    module_doc = 0

    for term in query_terms:
        idf = index[term]["idf"]
        query_tf = query_terms[term]/query_term_count
        query_tf_idf = query_tf * idf
        module_query += query_tf_idf ** 2
        for doc in index[term]["post_list"]:
            doc_id = doc["doc_id"]
            if doc_id not in doc_similarity:
                doc_similarity[doc_id] = {
                    "dot_product": 0,
                    "module_doc": 0
                }
            doc_tf_idf = doc["tf"] * idf
            doc_similarity[doc_id]["dot_product"] += doc_tf_idf * query_tf_idf
            doc_similarity[doc_id]["module_doc"] += doc_tf_idf ** 2

    results = []
    entry = 0
    for document in doc_similarity:
        data = doc_similarity[document]
        cosine_sim = data["dot_product"] / (math.sqrt(data["module_doc"])*math.sqrt(module_query))
        hp.heappush(results, (-cosine_sim, document))
        entry += 1

    for i in range(len(results)):
        r = hp.heappop(results)
        print("Doc: %s Cosine similitude: %f" % (r[1], -r[0]))
    '''
    for doc in term_containing_docs:
        for term in query_terms:
            #filtered_doc = next(filter(lambda d: d["doc_id"] == doc, index[term]["post_list"]), None)
            #if filtered_doc is not None:
            doc_has_term = len([d for d in index[term]["post_list"] if d.get("doc_id") == doc]) > 0
            if doc_has_term:
                idf = index[term]["idf"]
                query_tf = query_terms[term]/query_term_count
                query_tf_idf = idf * query_tf

                doc_tf = doc_has_term["tf"]
                doc_tf_idf = idf * doc_tf

                dot_product += query_tf_idf * doc_tf_idf
                module_query = query_tf_idf ** 2
                module_doc = doc_tf_idf ** 2
    '''


def extract_terms(document):
    """
        Extracts a list of terms from a text, and its term count

    :param document: text to extract terms from
    :return: tuple containing (list of terms, word_count[excluding stopwords])
    """
    tokens = word_tokenize(document)
    stemmer = PorterStemmer()
    terms = {}  # Dictionary {term: appearances}
    word_count = 0  # To return total (meaningful) word count
    for token in tokens:
        token = token.lower()  # Lowercase
        token = token.strip(string.punctuation)  # Remove punctuation
        if token and token not in stopwords.words("english"):  # Remove stopwords
            token = stemmer.stem(token)  # Using Porter Stemmer
            if token not in terms:
                terms[token] = 1
            else:
                terms[token] += 1
            word_count += 1
    return terms, word_count


main()
