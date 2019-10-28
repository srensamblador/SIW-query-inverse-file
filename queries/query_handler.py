from queries.index_persistence import load_inverse_file, print_inverse_file
from nltk import PorterStemmer, word_tokenize
from nltk.corpus import stopwords
import string, math
import heapq as hp


def query(index, input_query, documents): 
    ''' Makes a query against an inverse file

    Parameters:
    - index: TF-IDF inverse file, as seen in the 5th assignment
    - input_query: query to match against the index
    - documents: dictionary used to match documents_id from the inverse file with the documents' text when generating the returned value

    Returns:
    - Dictionary of the form:
        {"hits": {
            "DOC1": {
                "similarity": double,
                "text": string
            },
            "DOC2"...
        }}

    '''
    # Get terms from the query
    query_terms, query_term_count = extract_terms(input_query)

    # If a term was not in the index it's added with an empty post_list
    for term in query_terms:
        if term not in index:
            index[term] = {"idf": 0, "post_list": []}

    doc_similarity = {} # To store the partial calculations of cosine similarity
    module_query = 0

    # Calculates components of cosine similarity by iterating through the query terms and the documents in their post_lists
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
    for document in doc_similarity:
        data = doc_similarity[document]
        cosine_sim = data["dot_product"] / (math.sqrt(data["module_doc"])*math.sqrt(module_query))
        # Priority heap to sort the documents by cosine_similarity. Built-in heap in Python is a min heap, that's why I inverted the cosine_sim when pushing
        hp.heappush(results, (-cosine_sim, document)) 

    # Prepares returned dictionary
    data = {"hits": {}}
    for _ in range(len(results)):
        r = hp.heappop(results)
        data["hits"][r[1]] = {"similarity": -r[0], "text": documents[r[1]]}
    return data


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


