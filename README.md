# VarHMMin?


Genome-wide association studies have successfully identified many associated genetic loci with complex traits and disease. However, only a small number of biologically causal variants within these loci have been identified. In order to aid in the discovery process to identify etiological variants, we provide a tool to merge GWAS results with a much larger catalog of variants from whole genome sequencing and provide an annotation layer predicting the pathogenic potential of the regions near significant GWAS hits. 

We hypothesize that there are combinatorial and spatial patterns in the way that variants are distributed thoughout the genome and that this information could be used to infer the pathogenic potential in genomic regions.

As such, we aim to create an annotator which will identify 

## Approach 

In order to identify regions of potential pathogenic interest, we 

We will be using Alzheimer's GWAS data as a test case for this general tool. Variant data from whole-genome-sequencing will be pulled from gnomAD and annotated using Open-CRAVAT. 

### Open-CRAVAT annotators used:
- Vista Enhancer Browser
- VEST
- Repeat Sequences
- Gencode
- GTEX
- ClinVar
- 1000genomes
- gnomAD
- dbSNP
- COSMIC
