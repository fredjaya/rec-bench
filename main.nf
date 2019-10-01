#!/usr/local/bin nextflow

//===============================================================
//===============================================================
// Define parameters for S3_param_sweep. Edit the following:
mutrate = Channel.from(10e-7, 10e-5, 10e-3)
recrate = Channel.from(10e-7, 10e-5, 10e-3)
seqnum = Channel.from(100, 1000, 2500, 5000)
dualinf = Channel.from(0, 0.05, 0.5, 1)
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
     --mode viz      Parse simulation and analysis outputs for analysis
     --mode div      Divide sequence simulations by size for `--mode bm`
     --seq [.fasta]  Path to input .fasta file

   Optional arguments:
     --seqn  [int]     Required for '--mode bm'. Sequence number for benchmark analysis
     --out   [str]     Name of output folder
     --xml   [.xml]    SANTA-SIM .xml configuration. Defaults to santa.xml
     --label ['str']   PBS queue label for '--mode bm' e.g. 'pbs_small' 'pbs_med'
     --trace [t/f]     Enables/disables tracing. Disable for testing and non `--mode bm`
   """.stripIndent()
 }

/*
def processLabel() {
  // Provide PBS queue based on seqnum
  if (seqnum < 5000) {
    params.label = pbs_small
    println "pbs_small"
  }
  else if (seqnum > 1000) {
    println "pbs_med"
  }

}
*/

if (params.help) {
  // Show help message
  helpMessage()
  exit 0
}

// Print parameters
log.info """
=================================================
=================================================
DIRECTORIES / PATHS
base      = ${baseDir}
bin       = ${params.bin}
out       = ${params.out}
trace     = ${params.tracedir}
=================================================
=================================================
"""
/*
PARAMETERS
Mutation rate       = ${mutrate}
Recombination rate  = ${recrate}
Sequence number     = ${seqnum}
Dual infection rate = ${dualinf}
*/

// Decide which analysis to run and set channels for input files
if (params.mode == 'sim') {
  if (!params.seq) {
    println "ERROR: No input file specified. Use --seq [.fasta]"
    exit 1
  }
  else {
    println "Running simulation..."
  }
}
else if (params.mode == 'bm') {
  if (!params.seqn) {
    println "ERROR: Please specify sequence number for analysis"
    exit 1
  }
  else {
  println "Analysing recombination in simulated data..."
  }
}
else if (params.mode == 'emp') {
  println "Analysing recombination in empirical data..."
}
else if (params.mode == 'viz') {
  println "Plotting simulation outputs..."
}
else if (params.mode == 'div') {
  println "Arranging sequences into dirs by size"
}
else {
  log.info"""
  ERROR: '--mode' not selected.
  See all options 'nextflow run fredjaya/rec-bench --help'

  """.stripIndent()
  exit 1
}

/*
 * 1. SEQUENCE SIMULATION
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
    python3.7 ${params.bin}/S1_filter_fasta.py $seq_file
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
    label 'pbs_small'

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
    java -jar -Xmx512M -XX:ParallelGCThreads=2 ${params.bin}/santa_bp.jar \
    $santa_in
    """

  }

}

if (params.mode == 'viz') {
  // Set input; S4_santa output dir

  //V1_fileDir = "${params.out}/S4_santa"

  process parse_outputs {
    // Visualise simulated SANTA-SIM sequence statistics
    // TO DO: implement Rscript (crushingly diminishing returns to softcode plots)
    // TO DO: add output? `mv...` tests the output currently and destroys the purpose of nextflow

    //output:
    //file 'V1_santa_stats.csv'

    script:
    """
    mkdir -p ${params.out}/viz

    python3.7 ${params.bin}/V1_santa_stats.py ${params.out}/S4_santa
    #python3.7 ${params.bin}/V2_santa_bp.py ${params.out}/S4_santa
    python3.7 ${params.bin}/V3_profile_results.py ${params.out}/B1_phi_profile
    python3.7 ${params.bin}/V4_3seq_results.py ${params.out}/B2_3seq
    python3.7 ${params.bin}/V5_geneconv_results.py ${params.out}/B3_geneconv
    #python3.7 ${params.bin}/V6_uchime.py ${params.out}/B4_uchime

    mv ${params.out}/S4_santa/V1_santa_stats.csv ${params.out}/viz
    mv ${params.out}/B1_phi_profile/B1_profile_stats.csv ${params.out}/viz
    mv ${params.out}/B2_3seq/B2_3seq_stats.csv ${params.out}/viz
    mv ${params.out}/B3_geneconv/B3_geneconv_*.csv ${params.out}/viz
    """

  }

}

if (params.mode == 'div') {

  process split_seqnum {
    // Divide files into dirs based on sequence number

    input:
    each seqnum from seqnum

    script:
    """
    mkdir ${params.out}/S4_santa/n${seqnum}
    mv ${params.out}/S4_santa/*_n${seqnum}_*.fasta \
       ${params.out}/S4_santa/n${seqnum}
    """
  }

}
/*
 * 2. RECOMBINATION DETECTION (SIMULATIONS)
 */

if (params.mode == 'bm') {

  // INPUT CHANNELS
  // TO DO: select sequence number -> queue settings for all
  // TO DO: change below to look nicer `Channel.formPath.set{}...`
  B1_input = Channel.fromPath( "${params.out}/S4_santa/n${params.seqn}/*.fasta" )
  B2_input = Channel.fromPath( "${params.out}/S4_santa/n${params.seqn}/*.fasta" )
  B3_input = Channel.fromPath( "${params.out}/S4_santa/n${params.seqn}/*.fasta" )
  B4_input = Channel.fromPath( "${params.out}/S4_santa/n${params.seqn}/*.fasta" )

  process B1_phi_profile {

    label "${params.label}"
    tag "$seq"
    publishDir "${params.out}/B1_phi_profile", mode: 'move', saveAs: { filename -> "${seq}_$filename" }

    input:
    file seq from B1_input.flatten()

    output:
    file 'Profile.csv'
    file 'Profile.log'

    script:
    """
    Profile -f ${seq}
    """

  }

  process B2_3seq {
    // TO DO: add to bioconda

    label "${params.label}"
    tag "$seq"
    publishDir "${params.out}/B2_3seq", mode: 'move'

    input:
    file seq from B2_input.flatten()

    output:
    file '*3s.log'
    file '*3s.pvalHist' optional true
    file '*s.rec' optional true
    file '*3s.longRec' optional true

    script:
    """
    echo "Y" |
    ${params.bin}/3seq_elf -f $seq -d -id ${seq}
    """

  }

  process B3_geneconv {
    // TO DO: add to bioconda

    errorStrategy 'ignore'
    label "${params.label}"
    tag "$seq"
    publishDir "${params.out}/B3_geneconv", mode: 'move'

    input:
    file seq from B3_input.flatten()

    output:
    file '*.tab'

    script:
    """
    ${params.bin}/geneconv $seq -inputpath=${params.out}/S4_santa/n${params.seqn}/ -nolog -Dumptab -Fancy
    """

   }

  process B4_uchime {

    label "${params.label}"
    tag "$seq"
    publishDir "${params.out}/B4_uchime", mode: 'move'

    input:
    file seq from B4_input.flatten()

    output:
    file '*.rc'
    file '*.nonrc'
    file '*.log'

    script:
    """
    vsearch --uchime_denovo ${seq} \
            --chimeras ${seq}.rc \
            --nonchimeras ${seq}.nonrc \
            --log ${seq}.log
    """

  }

}

/*
 * 3. RECOMBINATION DETECTION (EMPIRICAL)
 */
