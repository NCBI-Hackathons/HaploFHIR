# HaploFHIR
A Prototype to Detect Baseline Haploblocks from Popular SNP Chips and Port them to EMRs

# Using p53 and K562 as examples to define toxic paths in graphs

## It has become apparent that it doesnt make sense to load full haploblock complements into EMRs.  Without context they are meaningless.  What would be much more useful to port to FHIR are discrepacies between patient haploblocks and their population segment.  Now we are preparing the data to look at differences between a CML cell line and a cohort of normals, as a proof of principle.  

## Scroll down

## Possibilities for Phasing and HaploBlock Generators

### Phasing

#### Genipe -- a combination of plink, SHAPEIT and IMPUTE2 **

##### Will try Beagle for multiallelic chips

#### Inputs

Getting data into plink

./plink2 --vcf Gencove_normal_p53_total.vcf --allow-extra-chr 0 --make-bed --out Gencove_normal_p53_total

##### Chips

Nice to have: Find a clever way to feed the tons of MAF info you have into plink!

+ You might be able to use GATK's VariantstoBinaryPed

Currently, chips arent converting well into plink2-readable vcfs and theres also the multiallelic problem (potentially solveable with Beagle)

##### Low coverage WGS (Gencove)

**--> NOTE: You need large enough regions for phasing (i.e. one gene locus with a relatively low mutation rate does NOT cut it<--**

Phasing works with genipe:

e.g. for the beginning of chromosome 1 

```
genipe-launcher \
    --chrom 1 \
    --bfile /home/ben.busby/foo3.test \
    --shapeit-bin /home/ben.busby/genipe_tutorial/bin/shapeit \
    --impute2-bin /home/ben.busby/genipe_tutorial/bin/impute2 \
    --plink-bin /home/ben.busby/genipe_tutorial/bin/plink \
    --reference /home/ben.busby/genipe_tutorial/hg19/hg19.fasta \
    --hap-template /home/ben.busby/genipe_tutorial/1000GP_Phase3/1000GP_Phase3_chr{chrom}.hap.gz \
    --legend-template /home/ben.busby/genipe_tutorial/1000GP_Phase3/1000GP_Phase3_chr{chrom}.legend.gz \
    --map-template /home/ben.busby/genipe_tutorial/1000GP_Phase3/genetic_map_chr{chrom}_combined_b37.txt \
    --sample-file /home/ben.busby/genipe_tutorial/1000GP_Phase3/1000GP_Phase3.sample \
    --filtering-rules 'ALL<0.01' 'ALL>0' \
    --report-title "Tutorial2" \
    --report-number "Test2Report"
```

##### One option at this point in the hackathon: build bcf files with SRA pileup, then phase straight from there!

##### Other options for phasing (not used)

WhatsHap (Marschall)

+ Mostly for read-backed phasing

SHAPE-IT

+ Prephasing imputation with PLINK

BEAGLE 5.1

+ Also requires PLINK



###### If you have to, just use an LD calculator as an approximation?

LDlink (NCI)

ldLookup

### Block Generation

HaploBlocker (Torsten Pook)

+ Learned about this one at the biohackathon!

+ Tested on corn!

## Code framework

![Alt text](https://github.com/NCBI-Hackathons/HaploFHIR/blob/master/2019_Biohackathon_BB.png)

### Overview of Workplan

A. Will use Haploblocker to generate additional input data for graph genomes team (Monday, Tuesday)

B. Will think about how to extract reportable paths ("lava") from graphs, and figure out when they are touched by short and long reads (Wednesday).  **Just start with ClinVar SNPs that are asserted pathogenic and have multiple stars**

C. Will figure out to extract gene level haplotypes from graphs and put them into FHIR (Thursday, Friday)

## Specific workplan details

### HaploBlocker Test Cases

#### Ben Busby is interested in generating Haplotype blocks from Human SNP arrays for clinical studies.  These can be reused as a VGBrowser test case.

#### Based on R Package

##### NOTE: HaploBlocker is NOT recommended to work on macOS.  After two hours of hacking at it, I have confirmed this assertion.  Will put in a github issue as a feature request.  

##### Data: 1,000 individuals x 1 million SNPs (another source of data besides PGP is OpenHumans -- some overlap).

###### From PGP. Much of the data are vcf-type files with GRCh36 or GRCh37 coordinates.  Will need to remap.  

Downloaded standalone remapper from NCBI here: ftp://ftp.ncbi.nlm.nih.gov/pub/remap/stand_alone/

##### Instead of converting, then remapping, used the open-cravat converter.

##### Will import 23 and me and output in GRCh38

##### Now have .vcf prepared for HaploBlocker

###### Cravat command: cravat ./example5 -t vcf --cleanup 

###### Gives a nicely annotated .vcf 

###### List of annotators

Name                          Title                               Type               Version       Data source ver    Size        
23andme-converter             23andMe Converter                   converter          1.0.4                            6.0 GB      
ancestrydna-converter         AncestryDNA Converter               converter          1.0.4                            6.0 GB      
clinvar                       ClinVar                             annotator          2019.08.23    2019.01.02         89.7 MB     
cravat-converter              Cravat Converter                    converter          1.0.4                            13.6 kB     
dbsnp                         dbSNP                               annotator          151.0.9       v151               27.0 GB     
dbsnp-converter               dbSNP Converter                     converter          1.0.1                            30.7 GB     
excelreporter                 Excel Reporter                      reporter           1.0.5                            1.5 MB      
gnomad                        gnomAD                              annotator          2.1.8         v2.1               17.4 GB     
gnomad_gene                   gnomAD Gene                         annotator          2.1.8         v2.1               10.2 MB     
gtex                          GTEx                                annotator          7.0.3         v7                 14.7 MB     
gwas_catalog                  GWAS Catalog                        annotator          1.0.0                            39.0 MB     
hg38                          UCSC hg38 Gene Mapper               mapper             1.2.7                            7.2 GB      
ncbigene                      NCBI Gene                           annotator          2019.08.02    2019.03.23         13.7 MB     
oldcravat-converter           OldCravat Converter                 converter          1.0.2                            12.4 kB     
pubmed                        PubMed                              annotator          1.1.4                            977.3 kB    
tagsampler                    Tag Sampler                         postaggregator     1.1.0                            6.9 kB      
textreporter                  Text Reporter                       reporter           1.0.5                            8.5 kB      
thousandgenomes               1000 Genomes                        annotator          4.0.5         Phase 3            5.3 GB      
thousandgenomes_group         1000 Genomes                        group              3.1.0         Phase 3            17.7 kB     
uk10k_cohort                  UK10k Cohorts                       annotator          3.5.9         dbNSFP v4.0b1      16.4 MB     
uniprot                       UniProt                             annotator          2019.08.22    201809             706.2 kB    
vcf-converter                 VCF Converter                       converter          1.1.6                            44.1 kB     
vcfinfo                       VCF Info                            postaggregator     1.1.4                            8.7 kB      
vcfreporter                   VCF Reporter                        reporter           1.0.8                            40.3 kB     
wgbase                        Base information                    webviewerwidget    1.0.8                            3.4 kB      
wgcircossummary               Circos Summary                      webviewerwidget    1.1.7                            622.8 kB    
wgcodingvsnoncodingsummary    Coding vs Noncoding Summary         webviewerwidget    1.0.6                            3.1 kB      
wggosummary                   Gene Ontology Summary               webviewerwidget    1.0.8                            10.6 MB     
wglollipop                    Protein diagram                     webviewerwidget    1.1.8                            73.2 MB     
wgnote                        Note                                webviewerwidget    1.0.3                            6.0 kB      
wgsosamplesummary             Sequence Ontology Sample Summary    webviewerwidget    1.1.8                            15.6 kB     
wgsosummary                   Sequence Ontology Summary           webviewerwidget    1.1.3                            3.8 kB 

## Phasing

First, convert to plink

``` ./plink2 --vcf foo3.vcf --allow-extra-chr 0 --make-bed --out foo3.test ```

### Actual phasing

Using Genipe, a combination of:

plink, IMPUTE2 and SHAPEIT

```./custom.sh```

``` 
#!/usr/bin/env bash
# Changing directory
cd /home/ben.busby/genipe_tutorial

# Launching the imputation with genipe
genipe-launcher \
    --chrom autosomes \
    --bfile /home/ben.busby/foo3.test \
    --shapeit-bin /home/ben.busby/genipe_tutorial/bin/shapeit \
    --impute2-bin /home/ben.busby/genipe_tutorial/bin/impute2 \
    --plink-bin /home/ben.busby/genipe_tutorial/bin/plink \
    --reference /home/ben.busby/genipe_tutorial/hg19/hg19.fasta \
    --hap-template /home/ben.busby/genipe_tutorial/1000GP_Phase3/1000GP_Phase3_chr{chrom}.hap.gz \
    --legend-template /home/ben.busby/genipe_tutorial/1000GP_Phase3/1000GP_Phase3_chr{chrom}.legend.gz \
    --map-template /home/ben.busby/genipe_tutorial/1000GP_Phase3/genetic_map_chr{chrom}_combined_b37.txt \
    --sample-file /home/ben.busby/genipe_tutorial/1000GP_Phase3/1000GP_Phase3.sample \
    --filtering-rules 'ALL<0.01' 'ALL>0' \
    --report-title "Tutorial2" \
    --report-number "Test2Report"
    
    ```

## HaploBlocker

library(HaploBlocker)

library(vcfR)

###### Import vcfs and Convert to Matrix



###### Calculate Blocks

Arguments for block_calculation:

args(block_calculation)
function (dhm, window_sequence = NULL, window_size = 20, merging_error = 1, 
    node_min = 5, gap = 10, min_share = 0.975, off_lines = 2, 
    min_similarity = 0.99, merge_closeblock = FALSE, max_diff_l = 1, 
    max_diff_i = 1, min_majorblock = 5000, bp_map = NULL, window_anchor_gens = NULL, 
    consider_nodes = TRUE, consider_edge = TRUE, edge_min = 5, 
    subgroups = NULL, min_per_subgroup = 0, subgroup_exception = 0, 
    consider_all = TRUE, save_allblock = TRUE, block_extending = TRUE, 
    max_extending_diff = 1, extending_ratio = 20, min_majorblock_steps = 4, 
    snp_extending = TRUE, max_extending_diff_snp = 0, extending_ratio_snp = Inf, 
    major_snp_calculation = TRUE, off_node_addition = FALSE, 
    off_node_minimum_blocklength = 10, off_node_minimum_blocksize = 5, 
    raster = 5, at_least_one = TRUE, prefilter = FALSE, maf = 0, 
    equal_remove = FALSE, big_output = FALSE, blockinfo_mode = 0, 
    c_dhm_mode = TRUE, intersect_func = TRUE, fast_compiler = TRUE, 
    max_groups = 0, recoding = FALSE, recoding_notneeded = FALSE, 
    consider_multi = FALSE, multi_min = 5, blockinfo_mode_na = FALSE, 
    actual_snp_weight = 5, na_snp_weight = 2, na_seq_weight = 0, 
    weighting_length = 1, weighting_size = 1, recalculate_biggest = TRUE, 
    target_coverage = NULL, max_iteration = 10, min_step_size = 25, 
    target_stop = 0.001, multi_window_mode = FALSE, adaptive_mode = FALSE, 
    developer_mode = FALSE, double_share = 1, early_remove = FALSE, 
    node_min_early = NULL, min_reduction_cross = -Inf, min_reduction_neglet = -Inf, 
    parallel_window = Inf, window_overlap = 0, window_cores = 1) 
    
   

##### Settings: Window Size 20, Differences in Windows Ignored 0, 

###### Window size 20 seems awful small for this purpose.  

##### Capture Intermediate number for test cases

###### Number of starting signatures

###### Signatures present at [1]  [10]  [100]  [1000] [100000]

##### Run simple merge

###### Collect same numbers again

##### Run Split Groups, Simple Merge, Neglect Nodes(5)

###### Collect same numbers again

##### Do Block Identification?

###### How many blocks Identified?

##### Length of first block?

##### Number of individuals in first block?

##### Do Block Filtering.  What is the MCMB setting?

##### How many blocks after Filter?

## Using p53 as an example for toxic paths in graphs

## Using K562 as an example of what a cancer genome looks like in vg?

###### Downloaded phased vcfs from: https://genome.cshlp.org/content/29/3/472.full

###### Building into vg, then will return to phasing and blocking.  

###### Block from vg (explicitly, not with haploblocker?)

##### We now have a simple pipeline to build paths in cancer that are not found in normal cohorts.  In theory we could do this with a lot of cancer samples e.g. 1 cohort from TCGA -- in fact you should try that from dbGaP (loading up from toolkit!)


