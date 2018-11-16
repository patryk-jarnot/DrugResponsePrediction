from optparse import OptionParser
from joblib import Parallel, delayed
import multiprocessing
import src.utils.pubmedutils as pmu
from eutils import Client


def job_get_mesh_terms_for_pmid(pmid, queue):
    ec = Client(api_key="fa081c19a44e9bfe267689cd45c7d31bae08")
    #ec = Client()

    result = ec.efetch(db='pubmed', id=pmid)
    x = iter(result)
    for i in x:
        queue.put([pmid, i.mesh_headings])


def read_pmids(options):
    with pmu.PubmedReader(options.input) as pmr:
        return [pmid for pmid in pmr.read_all()]


def read_mesh_terms(options, queue):
    pmids = read_pmids(options)

    element_information = Parallel(n_jobs=16)(delayed(job_get_mesh_terms_for_pmid)(pmid, queue) for pmid in pmids)

    return queue


def get_options():
    parser = OptionParser()
    parser.add_option("-v", "--version", action="store_true", dest="version", default=False)
    parser.add_option("-i", "--input", dest="input", default=None,
                      help="Path to input database", metavar="PATH")
    parser.add_option("-o", "--output", dest="output", default=None,
                      help="Path to output file", metavar="PATH")
    return parser.parse_args()


def merge_queries(queue):
    mesh_terms_dict = {}
    while not queue.empty():
        terms = queue.get_nowait()
        for term in terms[1]:
            if term not in mesh_terms_dict:
                mesh_terms_dict[term] = [terms[0]]
            else:
                mesh_terms_dict[term].append(terms[0])
    return mesh_terms_dict


def main(options, args):
    m = multiprocessing.Manager()
    queue = m.Queue()
    queue = read_mesh_terms(options, queue)
    statistics = merge_queries(queue)

    for stat_key, stat_val in statistics.items():
        print("{0};{1};{2}".format(stat_key, len(stat_val), str(stat_val)))


if __name__ == '__main__':
    options, args = get_options()
    main(options, args)


