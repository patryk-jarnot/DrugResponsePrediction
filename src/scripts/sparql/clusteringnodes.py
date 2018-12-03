from SPARQLWrapper import SPARQLWrapper, JSON

from optparse import OptionParser
import pandas as pd
import math
import sys
from collections import OrderedDict
from operator import itemgetter
import pickle

import pickle


def print_query():
    sparql = SPARQLWrapper("http://pgxlod.loria.fr/sparql")
    # sparql.setQuery("select <http://bio2rdf.org/pubchem.compound:129211> ?p ?o ?p2 ?o2 where {<http://bio2rdf.org/pubchem.compound:129211> ?p ?o. ?o ?p2 ?o2.} LIMIT 100")
    sparql.setQuery("select ?p ?o ?p2 ?o2 ?p3 ?o3 where {<http://bio2rdf.org/pubchem.compound:129211> ?p ?o. ?o ?p2 ?o2. ?o2 ?p3 ?o3.} LIMIT 100000")
    # sparql.setQuery("select ?p ?o where {<http://bio2rdf.org/pubchem.compound:%d> ?p ?o.} LIMIT 1000" % (id))
    sparql.setReturnFormat(JSON)
    try:
        results = sparql.query().convert()
    except:
        print("dupa", file=sys.stderr)
        return None

    x = 0
    for result in results["results"]["bindings"]:
        key = "{0}^{1}".format(result["p"]["value"], result["o"]["value"])
        print("p: {0}, o: {1}".format(result["p"]["value"], result["o"]["value"]))
        print("p2: {0}, o2: {1}".format(result["p2"]["value"], result["o2"]["value"]))
        print("p3: {0}, o3: {1}".format(result["p3"]["value"], result["o3"]["value"]))
        x += 1
    print(x)

last_key = ""
last_key2 = ""


def hit_database(id, is_first_layer=True):
    sparql = SPARQLWrapper("http://pgxlod.loria.fr/sparql")
    # sparql.setQuery("select <http://bio2rdf.org/pubchem.compound:%d> ?p ?o ?p2 ?o2 where {<http://bio2rdf.org/pubchem.compound:%d> ?p ?o. ?o ?p2 ?o2.} LIMIT 100" % (id, id))
    if is_first_layer:
        # sparql.setQuery("select ?p ?o where {<http://bio2rdf.org/pubchem.compound:%d> ?p ?o.} LIMIT 1000" % (id))
        # sparql.setQuery("select ?p ?o ?p2 ?o2 ?p3 ?o3 where {<http://bio2rdf.org/pubchem.compound:%d> ?p ?o. ?o ?p2 ?o2. ?o2 ?p3 ?o3.} LIMIT 100000" % (id))
        sparql.setQuery("select ?p ?o ?p2 ?o2 ?p3 ?o3 ?p4 ?o4 where {<http://bio2rdf.org/pubchem.compound:%d> ?p ?o. ?o ?p2 ?o2. ?o2 ?p3 ?o3. ?o3 ?p4 ?o4.} LIMIT 100000" % (id))
    else:
        # print("id: {0}".format(id), file=sys.stderr)
        if not id.startswith("http"):
            return None
        sparql.setQuery("select ?p ?o where {<%s> ?p ?o.} LIMIT 1000" % (id))
    sparql.setReturnFormat(JSON)
    try:
        results = sparql.query().convert()
    except:
        return None
    return results


pharma_neg = pickle.load( open( "/home/pjarnot/tmp/pharma_neg.pkl", "rb" ) )
pharma_pos = pickle.load( open( "/home/pjarnot/tmp/pharma_pos.pkl", "rb" ) )
pickle_nodes = {}

for k,v in pharma_neg.items():
    pickle_nodes[k] = v
for k,v in pharma_pos.items():
    pickle_nodes[k] = v


def hit_pickle(id):
    global pickle_nodes
    return pickle_nodes[id]


def query_drug(id, result_dict, is_first_layer=True):
    global last_key
    global last_key2

    node = "http://bio2rdf.org/drugbank:DB00201"

    results = hit_database(id)
    # results = hit_pickle(id)

    visited_set = {None}

    for result in results["results"]["bindings"]:
        # if result["o"]["value"] == node or result["o2"]["value"] == node or result["o3"]["value"] == node:
        #     print("id: {0}".format(id), file=sys.stderr)

        key = "{0}^{1}".format(result["p"]["value"], result["o"]["value"])
        if key not in visited_set:
            if key in result_dict:
                result_dict[key] += 1
            else:
                result_dict[key] = 1
            visited_set.add(key)

        key = "{0}^{1}".format(result["p2"]["value"], result["o2"]["value"])
        if key not in visited_set:
            if key in result_dict:
                result_dict[key] += 1
            else:
                result_dict[key] = 1
            visited_set.add(key)

        key = "{0}^{1}".format(result["p3"]["value"], result["o3"]["value"])
        if key not in visited_set:
            if key in result_dict:
                result_dict[key] += 1
            else:
                result_dict[key] = 1
            visited_set.add(key)

    return results


def read_data(file_path):
    retval = {}
    data = pd.read_csv(file_path, header=0, sep=";")

    for row in data.values:
        if not math.isnan(row[0]):
            retval[int(row[0])] = int(row[-1])

    return retval


def should_search_more(dictionary):
    for key, value in dictionary.items():    # for name, age in dictionary.iteritems():  (for Python 2.x)
        if value == 1:
            return True
    return False


def go_deeper(dict_of_interest):
    rounds = 1
    new_dict = {}
    iterate_dict = dict(dict_of_interest)

    while rounds < 3:# and (should_search_more(iterate_dict)): #todo: uncomment
        # print("(1) dict_of_interest: {0}".format(len(dict_of_interest)), file=sys.stderr)
        for drug_key, drug_val in iterate_dict.items():
            # if drug_val == 1: # todo: uncomment
            query_drug(drug_key.split("^")[1], new_dict, False)

        for drug_key, drug_val in new_dict.items():
            if drug_key in dict_of_interest:
                dict_of_interest[drug_key] += 1
            else:
                dict_of_interest[drug_key] = 1

        # print("(2) dict_of_interest: {0}".format(len(dict_of_interest)), file=sys.stderr)
        iterate_dict = new_dict
        new_dict = {}
        rounds += 1


def sort_results(results):
    return OrderedDict(sorted(results.items(), key=itemgetter(1), reverse=True))


def print_results(dict_of_interest):
    for neg_key, neg_val in dict_of_interest.items():
        print("{0};{1}".format(neg_key, neg_val))


def print_first_only(first, second):
    for key, val in first.items():
        if key not in second:
            print("{0};{1}".format(key, val))


def get_options():
    parser = OptionParser()
    parser.add_option("-v", "--version", action="store_true", dest="version", default=False)
    parser.add_option("-i", "--input", dest="input", default=None,
                      help="Path to input database", metavar="PATH")
    parser.add_option("-o", "--output", dest="output", default="/dev/stdout",
                      help="Path to output file", metavar="PATH")
    return parser.parse_args()


def main(options, args):
    drugs = read_data(options.input)
    negative_dict = {}
    positive_dict = {}

    x = 0
    results_neg = {}
    results_pos = {}
    for drug_key, drug_val in drugs.items():
        if drug_val == 0:
            results_neg[drug_key] = query_drug(drug_key, negative_dict)
        else:
            results_pos[drug_key] = query_drug(drug_key, positive_dict)
        x += 1
        print("x: {0}".format(x), file=sys.stderr)

    # go_deeper(negative_dict)
    # go_deeper(positive_dict)

    sort_results(negative_dict)
    sort_results(positive_dict)

    # print_first_only(negative_dict, positive_dict)
    # print_first_only(positive_dict, negative_dict)

    print_results(negative_dict)
    print("------------------------------------")
    print_results(positive_dict)

    # Pickle to file
    f = open("/home/pjarnot/tmp/pharma_neg_4_round.pkl","wb")
    pickle.dump(results_neg,f)
    f.close()

    f = open("/home/pjarnot/tmp/pharma_pos_4_round.pkl","wb")
    pickle.dump(results_pos,f)
    f.close()


if __name__ == '__main__':
    options, args = get_options()
    # options.input = "../../../data/dili/DILI-biohackathon (most-less-no).csv"
    main(options, args)


