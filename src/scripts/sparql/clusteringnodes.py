from SPARQLWrapper import SPARQLWrapper, JSON

from optparse import OptionParser
import pandas as pd
import math


def query_drug(id, result_dict, is_first_layer=True):
    sparql = SPARQLWrapper("http://pgxlod.loria.fr/sparql")
    # sparql.setQuery("select <http://bio2rdf.org/pubchem.compound:%d> ?p ?o ?p2 ?o2 where {<http://bio2rdf.org/pubchem.compound:%d> ?p ?o. ?o ?p2 ?o2.} LIMIT 100" % (id, id))
    if is_first_layer:
        sparql.setQuery("select ?p ?o where {<http://bio2rdf.org/pubchem.compound:%d> ?p ?o.} LIMIT 1000" % (id))
    else:
        sparql.setQuery("select ?p ?o where {<%s> ?p ?o.} LIMIT 1000" % (id))
    sparql.setReturnFormat(JSON)
    print(id)
    try:
        results = sparql.query().convert()
    except:
        return None

    # print(results)
    for result in results["results"]["bindings"]:
        # print("callret-0: {0}".format(result["callret-0"]["value"]))
        # print("p: {0}".format(result["p"]["value"]))
        # print("o: {0}".format(result["o"]["value"]))
        key = "{0}^{1}".format(result["p"]["value"], result["o"]["value"])
        if key in result_dict:
            result_dict[key] += 1
        else:
            result_dict[key] = 1


def read_data(file_path):
    retval = {}
    data = pd.read_csv(file_path, header=0, sep=";")

    # print("{0}".format(data.values[0][0]))
    for row in data.values:
        if not math.isnan(row[0]):
            retval[int(row[0])] = int(row[-1])

    # print(str(retval))

    return retval


def get_options():
    parser = OptionParser()
    parser.add_option("-v", "--version", action="store_true", dest="version", default=False)
    parser.add_option("-i", "--input", dest="input", default=None,
                      help="Path to input database", metavar="PATH")
    parser.add_option("-o", "--output", dest="output", default="/dev/stdout",
                      help="Path to output file", metavar="PATH")
    return parser.parse_args()


def should_search_more(dictionary):
    for key, value in dictionary.items():    # for name, age in dictionary.iteritems():  (for Python 2.x)
        if value == 1:
            return True
    return False


def main(options, args):
    drugs = read_data(options.input)
    negative_dict = {}
    positive_dict = {}

    for drug_key, drug_val in drugs.items():
        # print(str(drug_key))
        if drug_val == 0:
            query_drug(drug_key, negative_dict)

        else:
            query_drug(drug_key, positive_dict)

    rounds = 1
    new_dict = {}
    iterate_dict = negative_dict
    while rounds < 4 and (should_search_more(iterate_dict)):
        for drug_key, drug_val in iterate_dict.items():
            if drug_val == 1:
                query_drug(drug_key.split("^")[1], new_dict, False)

        for drug_key, drug_val in new_dict.items():
            if drug_key in negative_dict:
                negative_dict[drug_key] += 1
            else:
                negative_dict[drug_key] = 1

        iterate_dict = new_dict
        new_dict = {}
        rounds += 1

    rounds = 1
    new_dict = {}
    iterate_dict = positive_dict
    while rounds < 4 and (should_search_more(iterate_dict)):
        for drug_key, drug_val in iterate_dict.items():
            if drug_val == 1:
                query_drug(drug_key.split("^")[1], new_dict, False)

        for drug_key, drug_val in new_dict.items():
            if drug_key in positive_dict:
                positive_dict[drug_key] += 1
            else:
                positive_dict[drug_key] = 1

        iterate_dict = new_dict
        new_dict = {}
        rounds += 1

    for neg_key, neg_val in negative_dict.items():
        print("{0};{1}".format(neg_key, neg_val))

    print("------------------------------------")

    for pos_key, pos_val in positive_dict.items():
        print("{0};{1}".format(pos_key, pos_val))


if __name__ == '__main__':
    options, args = get_options()
    main(options, args)


