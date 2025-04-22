#!/usr/bin/python3
"""
search_pubmed
"""
import sys
 
if __name__ == '__main__':
	search_pmc = __import__('search_pubmed').search_pmc
	fetch_fulltext = __import__('search_pubmed').fetch_fulltext
	extract_narrative = __import__('search_pubmed').extract_narrative
	if len(sys.argv) < 3:
		print("Please pass an argument for the search term in the database and number of articles")
	else:
		ids = search_pmc(sys.argv[1],  sys.argv[2])
		for pmc_id in ids:
			xml = fetch_fulltext(pmc_id)
			case_text = extract_narrative(xml)
			print("\n" + "=" * 40)
			print(f"PMC ID: {pmc_id}\n")
			print(case_text[:1000], "...")  # prints a preview of the text


