#!/usr/local/bin nextflow

def helpMessage() {
  log.info"""
  Usage:

  The typical command for running the pipeline is as follows:

  nextflow run fredjaya/rec-bench --mode [sim/rdm]

  Mandatory arguments:
    --mode              Specify to run simulations (--mode sim) or RDMs (--mode rdm)

  Simulation arguments:
    --seq               Path to input .fasta file

  Recombination detection arguments:
    --path              Path to sim outputs
  """.stripIndent()
}

// Show help message
if (params.help) {
  helpMessage()
  exit 0
}

// Decide which analysis to run
if (params.mode == 'sim') {
  println "Running simulation..."
}
else if (params.mode == 'rdm') {
  println "Analysing recombination..."
}
else {
  log.info"""
  ERROR: please specify:
    --mode sim    Generate simulation datasets
    --mode rdm    Analyse simulated datasets with RDMs

  For all options:
  nextflow run fredjaya/rec-bench --help
  """.stripIndent()
  exit 1
}
