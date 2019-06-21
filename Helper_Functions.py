# This file contains the fucntions to import gwas data, filter variants, make bed, and pull gNOMAD data

import sys
import subprocess
import tempfile 

# Function 1: Get significant SNPS from GWAS import
# Default p-val = p<5E-8
# Make P-val adjustable
# Input: GWAS table (should define default)  
# Output: array of sig SNPs
# Output: number of significant SNPs


def get_intervals(GWAS_infile, Interval_outfile, gNOMAD_outfile,  pval_thresh, window_size, gNOMAD_db):

	# Args
	# GWAS infile is a tab delimited text file
	# Expected format:
	# Chromosome    Position    MarkerName    Effect_allele    Non_Effect_allele    Beta    SE    Pvalue
	# Inerval_outfile: merged bedfile with regions containing the significant GWAS calls (can be fixed)
	# gNOMAD_oufile: vcf containing gnomAD database information for the significan intervals, user downloads his file
	# pval_thresh: float, pval cuffoff, set by user, defaults value to be set
	# window_size: interger, determines the total window size around each significant GWAS variant, can be set by user
	# gNOMAD_db: fixed file, the gnomAD database. 
	
	# read in GWAS file and select the significant genomic loci
	infile = open(GWAS_infile, 'r')
	header = infile.readline()
	GWAS_sig = []
	for line in infile:
		line = line.strip('\n').split('\t')
		chrom = int(line[0])
		position = int(line[1])
		marker_name = str(line[2])
		pval = float(line[7])
		if pval < pval_thresh:
			GWAS_sig.append([chrom,position,marker_name,pval])
	infile.close()

	# This section makes a bedfile of all the significant SNPs with a specified window size, overlapping regions are collapsed

	window_interval = int(int(window_size)/2)
	bedfile_tmp = tempfile.NamedTemporaryFile(mode='w')
	for marker in GWAS_sig:
		chrom = str(marker[0])
		start_pos = str(marker[1]-window_interval)
		stop_pos = str(marker[1]+window_interval)
		name = marker[2]
		score = str(marker[3])
		line = [chrom,start_pos,stop_pos,name+','+score]
		newline = '\t'.join(line)+'\n'
		bedfile_tmp.write(newline)
	interval_file=open(Interval_outfile,'w')
	merged_intervals=subprocess.run(["bedtools","merge", "-i",bedfile_tmp.name, "-c", "4","-o","collapse","-delim",";"], capture_output=True)
	output = merged_intervals.stdout
	interval_file.write(output.decode('utf-8'))
	interval_file.close()
	
	# This section takes in the bedfile regions and outputs a vcf of all gnomAF within those regions.
	# For some reason tabix did not want to run with a bedfile input, so we do each region one at time.
	intervals_input=open(Interval_outfile,'r')
	gNOMAD_outfile=open(gNOMAD_outfile,'w')	
	for line in intervals_input:
		line = line.strip().split()
		location = line[0]+':'+line[1]+'-'+line[2]
		gNOMAD_call=subprocess.run(["tabix",gNOMAD_db,location],capture_output=True)
		gNOMAD_stdout=gNOMAD_call.stdout
		gNOMAD_outfile.write(gNOMAD_stdout.decode('utf-8'))
	gNOMAD_outfile.close()
	

def main():
	infile = sys.argv[1]
	outfile = sys.argv[2]
	gNOMAD_outfile =sys.argv[3]
	#pval = sys.argv[3]
	#window = sys.argv[4]
	pval_default=float(5e-12)
	window = 10000
	gNOMAD_db='/filestore/gnomad/gnomad.genomes.r2.1.1.sites.vcf.bgz'
	get_intervals(infile, outfile, gNOMAD_outfile, pval_default, window, gNOMAD_db)


if __name__ == '__main__':
	main()
		



# Function 2: Make bedfile from significant SNPs
# Default region size: 
# Make region size adjustable 
# output bedfile
# output region count?

# Function 3: 
# 


