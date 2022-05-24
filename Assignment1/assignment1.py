import argparse as ap

from Bio import Entrez

if __name__ == "__main__":
    argparser = ap.ArgumentParser(description="Script that downloads (default) 10 articles referenced by the given PubMed ID concurrently.")
    argparser.add_argument("-n", action="store",
                           dest="n", required=False, type=int, default=10,
                           help="Number of references to download concurrently.")
    argparser.add_argument("pubmed_id", action="store", type=str, nargs=1, help="Pubmed ID of the article to harvest for references to download.")
    args = argparser.parse_args()
    print("Getting: ", args.pubmed_id)

    Entrez.email = "pieterdejong812@gmail.com"
    results = Entrez.read(Entrez.elink(dbfrom="pubmed",
                                    db="pmc",
                                    LinkName="pubmed_pmc_refs",
                                    id=args.pubmed_id,
                                    api_key='93d90475a4e8ac57b7a1b71b86a89c611208'))
    references = [f'{link["Id"]}' for link in results[0]["LinkSetDb"][0]["Link"]]

    for refid in references:

        handle = Entrez.efetch(db="pmc", id=refid, rettype="XML", retmode="text",
                            api_key='93d90475a4e8ac57b7a1b71b86a89c611208')
        with open(f'output/{refid}.xml', 'wb') as file:
            file.write(handle.read())
        args.n = args.n-1
        if args.n ==0:
            break
