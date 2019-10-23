import json


def dump_inverse_file(filename, inverse_file):
    json_data = json.dumps(inverse_file)
    try:
        f = open(filename, "w")
        f.write(json_data)
    except:
        print("An error has occuring serializing the inverse file")


def load_inverse_file(filename):
    try:
        f = open(filename)
        inverse_file = json.loads(f.read())
        return inverse_file
    except:
        print("An error has ocurring retrieving the inverse file")


def print_inverse_file(inverse_file):
    to_print = ""
    for term in inverse_file:
        to_print += "Term: " + term + " IDF: " + str(inverse_file[term]["idf"]) + " Post-list: "
        for document in inverse_file[term]["post_list"]:
            to_print += "\n\t* Doc_ID: " + document["doc_id"] + " TF: " + str(document["tf"])
        to_print += "\n"
    print(to_print)
