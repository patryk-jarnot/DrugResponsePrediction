from SPARQLWrapper import SPARQLWrapper, JSON

from optparse import OptionParser


def sample_query():
    sparql = SPARQLWrapper("http://pgxlod.loria.fr/sparql")
    sparql.setQuery("""
        select <http://bio2rdf.org/pubchem.compound:18381> ?p ?o ?p2 ?o2 where {<http://bio2rdf.org/pubchem.compound:18381> ?p ?o. ?o ?p2 ?o2.} LIMIT 100
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    print(results)
    for result in results["results"]["bindings"]:
        print("callret-0: {0}".format(result["callret-0"]["value"]))
        print("p: {0}".format(result["p"]["value"]))
        print("o: {0}".format(result["o"]["value"]))


def get_options():
    parser = OptionParser()
    parser.add_option("-v", "--version", action="store_true", dest="version", default=False)
    parser.add_option("-i", "--input", dest="input", default=None,
                      help="Path to input database", metavar="PATH")
    parser.add_option("-o", "--output", dest="output", default=None,
                      help="Path to output file", metavar="PATH")
    return parser.parse_args()


def main(options, args):
    sample_query()


if __name__ == '__main__':
    options, args = get_options()
    main(options, args)

