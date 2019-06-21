#!/usr/bin/env nextflow
params.name   = "AlzML"


log.info "AlzML"
log.info "====================================="
log.info "name                   : ${params.name}"
log.info "\n"



process download_vcf {

  publishDir 'data/gnomad'
  errorStrategy 'retry'


  output:
  set file("*.vcf.bgz") into gnomad_vcf


  script:
  """
  gsutil -o "GSUtil:parallel_process_count=12" \
         -o "GSUtil:parallel_thread_count=2" \
         -m cp -r \
         gs://gnomad-public/release/2.1.1/vcf/genomes/gnomad.genomes.r2.1.1.sites.vcf.bgz \
         .
  """
}
