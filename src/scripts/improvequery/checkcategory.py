import src.utils.pubmedutils as pmu
import os


def compare_labeled_with_categories():
    categories_dir = "/home/pjarnot/polsl/conference/biohackathon/Pharmacology/data/pubmed_list/categories/"
    results_dir = "/home/pjarnot/polsl/conference/biohackathon/Pharmacology/data/pubmed_list/results/"
    with pmu.PubmedReader("../../data/pubmed_list/good/labeled.txt") as pr:
        good_pmids = [pmid for pmid in pr.read_all()]

    with pmu.PubmedReader("../../data/pubmed_list/bad/labeled.txt") as pr:
        bad_pmids = [pmid for pmid in pr.read_all()]

    for category in os.listdir(categories_dir):
        good_pmids_result = []
        bad_pmids_result = []
        other_pmids_result = []
        with pmu.PubmedReader("{0}{1}".format(categories_dir, category)) as pr:
            for pmid in pr.read_all():
                if pmid in good_pmids:
                    good_pmids_result.append(pmid)
                elif pmid in bad_pmids:
                    bad_pmids_result.append(pmid)
                else:
                    other_pmids_result.append(pmid)


        with pmu.PubmedWriter("{0}{1}_good".format(results_dir, category)) as pw:
            pw.write_all(good_pmids_result)

        with pmu.PubmedWriter("{0}{1}_bad".format(results_dir, category)) as pw:
            pw.write_all(bad_pmids_result)

        with pmu.PubmedWriter("{0}{1}_other".format(results_dir, category)) as pw:
            pw.write_all(other_pmids_result)


def create_dir(dir_name):
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)


def init_results_bad_categories_dict(bad_categories_dir, groups_dir, results_bad_categories):

    for bad_category in os.listdir(bad_categories_dir):
        results_bad_categories[bad_category] = {}

    for group in os.listdir(groups_dir):
        for key, value in results_bad_categories.items():
            results_bad_categories[key][group] = []


def init_groups_dict(groups_dir, groups):
    for group in os.listdir(groups_dir):
        with pmu.PubmedReader("{0}{1}".format(groups_dir, group)) as pr:
            groups[group] = [pmid for pmid in pr.read_all()]


def compare_categories_with_bad_categories():
    bad_categories_dir = "/home/pjarnot/polsl/conference/biohackathon/Pharmacology/data/pubmed_list/bad_categories/"
    groups_dir = "/home/pjarnot/polsl/conference/biohackathon/Pharmacology/data/pubmed_list/results/"
    results_bad_categories_dir = "/home/pjarnot/polsl/conference/biohackathon/Pharmacology/data/pubmed_list/results_bad_categories/"

    groups = {}
    results_bad_categories = {}

    init_results_bad_categories_dict(bad_categories_dir, groups_dir, results_bad_categories)

    init_groups_dict(groups_dir, groups)

    create_dir("{0}".format(results_bad_categories_dir))
    for bad_category in os.listdir(bad_categories_dir):
        create_dir("{0}{1}".format(results_bad_categories_dir, bad_category))

        with pmu.PubmedReader("{0}{1}".format(bad_categories_dir, bad_category)) as pr:
            for pmid in pr.read_all():
                for group_key, group_value in groups.items():
                    if pmid in group_value:
                        results_bad_categories[bad_category][group_key].append(pmid)

    for bad_category_key, bad_category_value in results_bad_categories.items():
        for group_key, group_value in results_bad_categories[bad_category_key].items():
            with pmu.PubmedWriter("{0}{1}/{2}".format(results_bad_categories_dir, bad_category_key, group_key)) as pr:
                pr.write_all(results_bad_categories[bad_category_key][group_key])


def compare_categories_with_bad_and_good():
    bad_dir = "/home/pjarnot/polsl/conference/biohackathon/Pharmacology/data/pubmed_list/bad/"
    good_dir = "/home/pjarnot/polsl/conference/biohackathon/Pharmacology/data/pubmed_list/good/"
    rest_dir = "/home/pjarnot/polsl/conference/biohackathon/Pharmacology/data/pubmed_list/rest/"
    bad_categories_dir = "/home/pjarnot/polsl/conference/biohackathon/Pharmacology/data/pubmed_list/bad_categories/"
    results_good_dir = "/home/pjarnot/polsl/conference/biohackathon/Pharmacology/data/pubmed_list/results_labeled_categories/good/"
    results_bad_dir = "/home/pjarnot/polsl/conference/biohackathon/Pharmacology/data/pubmed_list/results_labeled_categories/bad/"
    results_rest_dir = "/home/pjarnot/polsl/conference/biohackathon/Pharmacology/data/pubmed_list/results_labeled_categories/rest/"
    results_other_dir = "/home/pjarnot/polsl/conference/biohackathon/Pharmacology/data/pubmed_list/results_labeled_categories/other/"

    with pmu.PubmedReader("{0}{1}".format(good_dir, "labeled.txt")) as pr:
        good_list = [pmid for pmid in pr.read_all()]

    with pmu.PubmedReader("{0}{1}".format(bad_dir, "labeled.txt")) as pr:
        bad_list = [pmid for pmid in pr.read_all()]

    with pmu.PubmedReader("{0}{1}".format(rest_dir, "all")) as pr:
        rest_list = [pmid for pmid in pr.read_all()]

    good_results = {}
    bad_results = {}
    rest_results = {}
    other_results = {}

    for bad_category in os.listdir(bad_categories_dir):
        good_results[bad_category] = []
        bad_results[bad_category] = []
        rest_results[bad_category] = []
        other_results[bad_category] = []
        with pmu.PubmedReader("{0}{1}".format(bad_categories_dir, bad_category)) as pr:
            for pmid in pr.read_all():
                if pmid in good_list:
                    good_results[bad_category].append(pmid)
                elif pmid in bad_list:
                    bad_results[bad_category].append(pmid)
                elif pmid in rest_list:
                    rest_results[bad_category].append(pmid)
                else:
                    other_results[bad_category].append(pmid)

    create_dir(results_good_dir)
    for good_key, good_value in good_results.items():
        with pmu.PubmedWriter("{0}{1}".format(results_good_dir, good_key)) as pr:
            pr.write_all(good_value)

    create_dir(results_bad_dir)
    for bad_key, bad_value in bad_results.items():
        with pmu.PubmedWriter("{0}{1}".format(results_bad_dir, bad_key)) as pr:
            pr.write_all(bad_value)

    create_dir(results_rest_dir)
    for rest_key, rest_value in rest_results.items():
        with pmu.PubmedWriter("{0}{1}".format(results_rest_dir, rest_key)) as pr:
            pr.write_all(rest_value)

    create_dir(results_other_dir)
    for other_key, other_value in other_results.items():
        with pmu.PubmedWriter("{0}{1}".format(results_other_dir, other_key)) as pr:
            pr.write_all(other_value)


if __name__ == '__main__':
    compare_categories_with_bad_and_good()



