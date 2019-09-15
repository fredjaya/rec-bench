#!/usr/local/bin nextflow

//===============================================================
//===============================================================
// Define parameters for S3_param_sweep. Edit the following:
//mutrate = Channel.from(10e-8, 10e-7, 10e-6, 10e-5, 10e-4, 10e-3)
//recrate = Channel.from(10e-8, 10e-7, 10e-6, 10e-5, 10e-4, 10e-3)
//seqnum = Channel.from(100, 1000, 2500, 5000, 10000)
//dualinf = Channel.from(0.05, 0.1, 0.25, 0.5, 1)
mutrate = Channel.from(10e-7)
recrate = Channel.from(10e-4, 10e-3)
seqnum = Channel.from(100, 1000)
dualinf = Channel.from(0.5, 0.9)
//===============================================================
//===============================================================

/*
 * INPUT OPTIONS / PARAMETERS
 */

 def helpMessage() {
   log.info"""
   Usage:

   The typical command for running the pipeline is as follows:

   nextflow run fredjaya/rec-bench --mode [sim/rdm/emp]

   Mandatory arguments:
     --mode sim      Generate simulation datasets
     --mode bm       Detect recombination in simulated datasets and benchmark methods
     --mode emp      Detect recombination in empirical sequence alignments
     --mode sim_v  Visualise simulation outputs (sequence stats, breakpoints)
     --seq [.fasta]  Path to input .fasta file

   Optional arguments:
     --out [str]     Name of output folder
     --xml [.xml]    SANTA-SIM .xml configuration. Defaults to santa.xml

   """.stripIndent()
 }

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
else if (params.mode == 'sim_v') {
  println "Plotting simulation results..."
}
else {
  log.info"""
  ERROR: '--mode' not selected.
  See all options 'nextflow run fredjaya/rec-bench --help'

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
  seq_temp = "$baseDir/${params.seq}"
  seq_file = file(seq_temp)

  process S1_filter_fasta {
    // Filter the longest, gapless sequence as SANTA-SIM can't analyse gaps.
    // TO DO: Probably need a better way to handle this i.e. generate consensus
    publishDir "${params.out}/S1_filter_fasta", mode: 'copy'

    input:
    file seq_file from seq_file

    output:
    file 'seqLength*.png' optional true
    file '*_m' //into rdmInput*
    file '*_n' //into seqUchime
    file '*_n_filtered' into seq_path
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
    xml_in = file("$baseDir/${params.xml}")

    input:
    file xml_in from xml_in
    val seq_path from seq_path

    output:
    file '*_out.xml' into xml_out

    script:
    """
    sed 's|'SEQPATH'|'${seq_path}'|g' ${xml_in} > ${xml_in}_out.xml
    """

  }

  process S3_param_sweep {
    // Generate .xml files across specified evolutionary parameters
    // TO DO: parameter config file

    input:
    file xml_out from xml_out
    each mutrate from mutrate
    each recrate from recrate
    each seqnum from seqnum
    each dualinf from dualinf

    output:
    file '*.xml' into santa_in

    script:
    """
    sed 's|'MUTRATE'|'$mutrate'|g; s|'RECRATE'|'$recrate'|g; \
    s|'SEQNUM'|'$seqnum'|g; s|'DUALRATE'|'$dualinf'|g' \
    $xml_out > xml_m${mutrate}_rc${recrate}_n${seqnum}_n${dualinf}.xml
    """

  }

  process S4_santa {
    // Simulate sequences over time, based on .xml files generated
    // TO DO: add santa.jar to conda/docker/sing

    publishDir "${params.out}/S4_santa", mode: 'copy'

    input:
    file santa_in from santa_in

    output:
    file 'stats_*.csv'
    file 'tree_*.trees'
    file 'msa_*.fasta' //into rdmInputS1, rdmInputS2, rdmInputS4 //rdmInputS3,
    //set file('tree_*.trees'), file('msa_*.fasta') into rdmInputS3

    script:
    """
    java -jar -Xmx512M -XX:ParallelGCThreads=2 $baseDir/bin/santa_bp.jar \
    $santa_in
    """

  }

}

if (params.mode == 'simv') {
  // Set input; S4_santa output dir

  process V1_santa_stats {
    // Visualise simulation statistics and breakpoints

    v1_temp = ""
    publishDir "${params.out}/viz", mode: 'copy'

    input:
    file

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
