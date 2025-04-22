#!/usr/bin/python3
"""
Search Modulue
"""
import os
import re
import csv
import time
import pandas as pd
from Bio import Entrez
from lxml import etree
from multiprocessing import Pool, cpu_count

Entrez.email = "jmuindedt@gmail.com"
Entrez.api_key = "314f9774d7bb236f95add6b7c417cceb3709"
def search_pmc(term, max_results=0):
	""" Query the database and return the article ids"""
	query = f'({term}) AND case reports[Publication Type]'
	print("Search Query:", query)
	handle = Entrez.esearch(
			db="pmc",
			term=query,
			retmax=max_results
	)
	record = Entrez.read(handle)
	return record["IdList"]

def fetch_fulltext(pmc_id):
	""" extract content by artciel id"""
	handle = Entrez.efetch(db="pmc", id=pmc_id, rettype="full", retmode="xml")
	return handle.read() 

def extract_narrative(xml_text):
	if isinstance(xml_text, str):
		xml_text = xml_text.encode('utf-8')
	root = etree.fromstring(xml_text)
	body = root.find(".//body")
	if body is not None:
		paragraphs = body.xpath(".//p")
		return "\n\n".join([p.text for p in paragraphs if p.text])
	return None

def extract_demographics(text):
	age_match = re.search(r"\b(\d{1,3})[- ]?(year[- ]old|years old)\b", text, re.IGNORECASE)
	gender_match = re.search(r"\b(male|female|man|woman)\b", text, re.IGNORECASE)
	age = age_match.group(1) if age_match else None
	gender = gender_match.group(1).capitalize() if gender_match else None
	return age, gender

def contains_diagnosis(text):
	diagnoses = ['stress', 'anxiety', 'depression', 'Stress', 'Anxiety', 'Depression']
	for d in diagnoses:
		if re.search(rf"\b{d}\b", text, re.IGNORECASE):
			return d
	return None

def process_article(pmc_id):
	try:
		xml = fetch_fulltext(pmc_id)
		text = extract_narrative(xml)
		if not text:
			return None
		diagnosis = contains_diagnosis(text)
		if diagnosis:
			age, gender = extract_demographics(text)
			return {
				"PMC_ID": pmc_id,
				"Diagnosis": diagnosis.capitalize(),
				"Age": age,
				"Gender": gender,
				"Comments": text[:100]
			}
	except Exception as e:
		print(f"Error processing PMC{pmc_id}: {e}")
	return None


def extract_and_store(subset_term, max_cases=500, output_file="mental_health_cases.csv", batch_size=20):
	ids = search_pmc(subset_term, max_cases)
	print(f"found {len(ids)} artciles, processing...")
	batches = [ids[i:i + batch_size] for i in range(0, len(ids), batch_size)]

	for i, batch in enumerate(batches):
		print(f" Process batch {i + 1}/{len(batches)}...")


		with Pool(processes=min(4, cpu_count())) as pool:
			results = pool.map(process_article, batch)
	
		records = [r for r in results if r is not None]
		if records:
			df = pd.DataFrame(records)
			df.to_csv(output_file, mode='a',header=not os.path.exists(output_file), index = False)
			print(F" Batch {i + 1} saved: len{(records)}")
		else:
			print("Batch {i + 1} had no valid arcticles")
		time.sleep(1.5)

# ---- Run Script ----
if __name__ == "__main__":
	extract_and_store("stress OR depression OR anxiety", max_cases=500)

 
