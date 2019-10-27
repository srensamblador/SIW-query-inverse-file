import json


def dump_inverse_file(filename, inverse_file):
    json_data = json.dumps(inverse_file)
    with open(filename, "w") as f:
        f.write(json_data)


def load_inverse_file(filename):
    with open(filename, "r") as f:
        inverse_file = json.loads(f.read())
        return inverse_file


def load_documents(filename):
    with open(filename, "r") as f:
        dict_documents = {}
        for line in f:
            split_line = line.split(" ")
            doc_id, text = split_line[:1][0], " ".join(split_line[1:])
            dict_documents[doc_id] = text.strip()
        return dict_documents


def print_inverse_file(inverse_file):
    to_print = ""
    for term in inverse_file:
        to_print += "Term: " + term + " IDF: " + str(inverse_file[term]["idf"]) + " Post-list: "
        for document in inverse_file[term]["post_list"]:
            to_print += "\n\t* Doc_ID: " + document["doc_id"] + " TF: " + str(document["tf"])
        to_print += "\n"
    print(to_print)
