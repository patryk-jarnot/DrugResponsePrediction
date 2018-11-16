import src.utils.pubmedutils as pmu


if __name__ == '__main__':
    with pmu.PubmedReader("../../data/pubmed_list/good/labeled.txt") as pr:
        good_pmids = [pmid for pmid in pr.read_all()]

    bad_pmids = []
    with pmu.PubmedReader("../../data/pubmed_list/reviewed/list_pmid") as pr:
        for pmid in pr.read_all():
            if pmid not in good_pmids:
                bad_pmids.append(pmid)

    with pmu.PubmedWriter("../../data/pubmed_list/bad/labeled.txt") as pw:
        pw.write_all(bad_pmids)


