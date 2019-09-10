#!/usr/local/bin nextflow

def helpMessage() {
  log.info"""
  Usage:

  The typical command for running the pipeline is as follows:

  nextflow run fredjaya/rec-bench --mode [sim/rdm/emp]

  Mandatory arguments:
    --mode sim      Generate simulation datasets
    --mode bm       Detect recombination in simulated datasets and benchmark methods
    --mode emp      Detect recombination in empirical sequence alignments
    --seq [.fasta]  Path to input .fasta file

  Optional arguments:
    --out [str]     Name of output folder

  """.stripIndent()
}

/*
 * INPUT OPTIONS / PARAMETERS
 */

// Show help message
if (params.help) {
  helpMessage()
  exit 0
}

// check input seq
if (!params.seq) {
  println "ERROR: No input file specified. Use --seq [.fasta]"
  exit 1
}

// Decide which analysis to run and set channels for input files
if (params.mode == 'sim') {
  println "Running simulation..."

}
else if (params.mode == 'bm') {
  println "Analysing recombination in simulated data..."
}
else if (params.mode == 'emp') {
  println "Analysing recombination in empirical data..."
}
else {
  log.info"""
  ERROR: Run mode not selected. Please specify:
    --mode sim    Generate simulation datasets
    --mode bm     Detect recombination in simulated datasets and benchmark methods
    --mode emp    Detect recombination in empirical sequence alignments

  For all options:

  nextflow run fredjaya/rec-bench --help

  """.stripIndent()
  exit 1
}

/*
 *  Channels for input files
 */


/*
 * [S]IMULATIONS
 */

// Create channel for sim
if (params.mode == 'sim') {

  println "Reading ${params.seq}"
  seqTemp = "${params.seq}"
  seqFile = file(seqTemp)

  process S1_filter_fasta {

    publishDir "${params.out}/fasta", mode: 'copy'

    input:
    file seq from seqFile

    output:
    file 'seqLength*.png' optional true
    file '*_m' //into rdmInput*
    file '*_n' //into seqUchime
    file '*_n_filtered' into seqPath
    file '*_removed'
    file '*_log.txt'

    script:
    """
    python3.7 $baseDir/bin/S1_filter_fasta.py $seq
    """

  }


}

/*
 * 2. RECOMBINATION DETECTION (SIMULATIONS)
 */

/*
 *  Filter sequences for gaps
 */


/*
 * 3. RECOMBINATION DETECTION (EMPIRICAL)
 */
