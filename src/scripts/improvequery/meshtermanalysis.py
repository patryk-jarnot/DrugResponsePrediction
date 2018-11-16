from optparse import OptionParser
import src.utils.meshtermutils as mtu
from operator import itemgetter
from collections import OrderedDict


def read_mesh_terms(file_name):
    mesh_terms = {}
    with mtu.MeshTermReader(file_name) as mtr:
        for item in mtr.read_all():
            mesh_terms[item[0]] = int(item[1])
    return mesh_terms


def get_bad_terms_not_in_good(mesh_terms_good, mesh_terms_bad, ratio_min):
    retval = {}

    for bad_key, bad_val in mesh_terms_bad.items():
        try:
            ratio = bad_val / mesh_terms_good[bad_key]
        except:
            ratio = 1000000

        if ratio > ratio_min:
            retval[bad_key] = bad_val
        # if bad_key not in mesh_terms_good:
        #     retval[bad_key] = bad_val

    return retval


def sort_mesh_terms(bad_terms_only):
    return OrderedDict(sorted(bad_terms_only.items(), key=itemgetter(1), reverse=True))


def write_mesh_terms(file_name, bad_terms_only):
    with mtu.MeshTermWriter(file_name) as mtw:
        mtw.write_all(bad_terms_only)


def main(options, args):

    if options.sort:
        result = read_mesh_terms(options.input)
        result = sort_mesh_terms(result)
        write_mesh_terms(options.output, result)

    else:
        mesh_terms_good = read_mesh_terms(options.input_good)
        mesh_terms_bad = read_mesh_terms(options.input_bad)

        bad_terms_only = get_bad_terms_not_in_good(mesh_terms_good, mesh_terms_bad, options.ratio)

        bad_terms_only = sort_mesh_terms(bad_terms_only)

        write_mesh_terms(options.output, bad_terms_only)


def get_options():
    parser = OptionParser()
    parser.add_option("-v", "--version", action="store_true", dest="version", default=False)
    parser.add_option("-s", "--sort", action="store_true", dest="sort", default=False)
    parser.add_option("-r", "--ratio", dest="ratio", default=8, type="float",
                      help="Path to input database", metavar="VALUE")
    parser.add_option("-i", "--input", dest="input", default=None,
                      help="Path to input database", metavar="PATH")
    parser.add_option("-g", "--input-good", dest="input_good", default=None,
                      help="Path to input database", metavar="PATH")
    parser.add_option("-b", "--input-bad", dest="input_bad", default=None,
                      help="Path to input database", metavar="PATH")
    parser.add_option("-o", "--output", dest="output", default=None,
                      help="Path to output file", metavar="PATH")
    return parser.parse_args()


if __name__ == '__main__':
    options, args = get_options()
    main(options, args)

