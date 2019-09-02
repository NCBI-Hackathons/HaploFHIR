# HaploFHIR
A Prototype to Detect Baseline Haploblocks from Popular SNP Chips and Port them to EMRs

## Possibilities for LD Calculators

LDlookup (Purcell)

WhatsHap (Marschall)

LDlink (NCI) 

HaploBlocker (Torsten Pook)

+ Learned about this one at the biohackathon!

+ Tested on corn!

## Code framework

![Alt text](https://github.com/NCBI-Hackathons/HaploFHIR/blob/master/2019_Biohackathon_BB.png)

### Overview of Workplan

A. Will use Haploblocker to generate additional input data for graph genomes team (Monday, Tuesday)

B. Will think about how to extract reportable paths ("lava") from graphs, and figure out when they are touched by short and long reads (Wednesday)

C. Will figure out to extract gene level haplotypes from graphs and put them into FHIR (Thursday, Friday)

## Specific workplan details

### HaploBlocker Test Cases

#### Ben Busby is interested in generating Haplotype blocks from Human SNP arrays for clinical studies.  These can be reused as a VGBrowser test case.

#### Based on R Package

##### Data: 1,000 individuals x 1 million SNPs

##### Settings: Window Size 20, Differences in Windows Ignored 0, 

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



