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
    --xml [.xml]    SANTA-SIM .xml configuration. Defaults to santa.xml

  """.stripIndent()
}

/*
 * INPUT OPTIONS / PARAMETERS
 */

if (params.help) {
  // Show help message
  helpMessage()
  exit 0
}

if (!params.seq) {
  // check input seq
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

  See all options: nextflow run fredjaya/rec-bench --help

  """.stripIndent()
  exit 1
}

/*
 *  Channels for input files
 */


/*
 * [S]IMULATIONS
 */

if (params.mode == 'sim') {
  // Set input for SANTA-SIM
  println "Reading ${params.seq}"
  seq_path = "${params.seq}"
  seq_file = file(seq_path)

  process S1_filter_fasta {
    // Filter the longest, gapless sequence as SANTA-SIM can't analyse gaps.
    // TO DO: Probably need a better way to handle this i.e. generate consensus
    publishDir "${params.out}/fasta", mode: 'copy'

    input:
    file seq_file from seq_file

    output:
    file 'seqLength*.png' optional true
    file '*_m' //into rdmInput*
    file '*_n' //into seqUchime
    file '*_n_filtered' //into seqPath
    file '*_removed'
    file '*_log.txt'

    script:
    """
    python3.7 $baseDir/bin/S1_filter_fasta.py $seq_file
    """

  }

  process S2_santa_xml {
    // Add path of input .fasta to santa.xml
    // TO DO: Add final sequence length from S1
    publishDir "${params.out}/fasta", mode: 'copy'
    xml_in = file("$baseDir/${params.xml}")

    input:
    file xml_in from xml_in
    val seq_path from seq_path

    output:
    file '*_out.xml' //into xml_out

    script:
    """
    sed 's|'SEQPATH'|'${seq_path}'|g' ${xml_in} > ${xml_in}_out.xml
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
