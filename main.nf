#!/usr/local/bin nextflow

//===============================================================
//===============================================================
// Define parameters for S3_param_sweep. Edit the following:
mutrate = Channel.from(10e-8, 10e-7, 10e-6, 10e-5, 10e-4, 10e-3)
recrate = Channel.from(10e-8, 10e-7, 10e-6, 10e-5, 10e-4, 10e-3)
seqnum = Channel.from(100, 1000, 5000)
dualinf = Channel.from(0, 0.05)
//===============================================================
//===============================================================


/*
 * INPUT OPTIONS / PARAMETERS
 */

def helpMessage() {
  log.info"""
  Usage:

  The typical command for running the pipeline is as follows:

  nextflow run main.nf --mode [sim/rdm/emp...] --other_options

  Example scripts can be found in rec-bench/example_runscripts

  Process arguments:
    --out   [str]     Name of output folder. Default 'baseDir/out'
    --label [str]     PBS queue label for '--mode bm' e.g. 'pbs_small' 'pbs_med'

    Recommended --label options (based on seq length < 2000 nt):
    --label pbs_small for sample size < 1001
    --label pbs_med   for sample size > 1000

  1. Generate simulation datasets:
    * Please define evolutionary parameters in main.nf *
    --mode sim
    --seq [.fasta]    Path to input .fasta file
    --xml [.xml]      SANTA-SIM .xml configuration. Defaults to ./santa.xml

  2. Visualise/summarise simulation outputs (sequence stats, breakpoints):
    --mode sim_v      Summarise output simulation files for sim_bp
    --simdir [str]    Path to dir which contains folder for simulation files (S4_santa). Default 'baseDir/out'

  3. Benchmark recombination detection methods using simulated data:
    --mode div        Move simulated .fasta into subdirs by size. * Use prior to `--mode bm`*

    --mode bm         Detect recombination in simulated datasets and benchmark methods
    --seqn   [int]    Sample size (number of sequences in alignment) to analyse. * Required for `--mode bm` *
    --simdir [str]    Path to dir which contains folder for simulation files (S4_santa). Default 'baseDir/out'

  4. Detect recombination in empirical sequence alignments:
    --mode emp
    --seq [.fasta]    Path to input .fasta file

  5. Calculating classification metrics:
    --mode class       Determine conditions of simulations vs detected recombination
    --simbp    [.csv]  Path to .csv containing simulated breakpoints per rep
    --rec_path [str]   Path to folder where output for --mode bm is
    --out      [str]   Path to write files to

   """.stripIndent()
 }

/*
def processLabel() {
  // Provide PBS queue based on seqnum
  if (seqnum < 1001) {
    println "pbs_smallq"
  }
  else if (seqnum > 1000) {
    println "pbs_medq"
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
in        = ${params.in}
out       = ${params.out}
trace     = ${params.tracedir}
xml       = ${params.xml}
=================================================
=================================================
"""

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
else if (params.mode == 'sim_v') {
  println "Plotting simulation outputs..."
}
else if (params.mode == 'div') {
  println "Arranging sequences into dirs by size"
}
else if (params.mode == 'class') {
  println "Calculating classification metrics of detected recombination"
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

/*
PARAMETERS
Mutation rate       = ${mutrate}
Recombination rate  = ${recrate}
Sequence number     = ${seqnum}
Dual infection rate = ${dualinf}
=================================================
=================================================
"""
=======
*/

  // Set input for SANTA-SIM
  println "Reading ${params.seq}"
  seq_temp = "${params.seq}"
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
    println "${params.xml}"
    xml_in = file("${params.xml}")

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
    publishDir "${params.out}/S3_param_sweep", mode: 'copy'

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

if (params.mode == 'sim_v') {
  
  println "Reading files from ${params.simdir}/S4_santa"
  sim_path = "${params.simdir}/S4_santa"

  process V1_santa_stats {
    // Summarise population stats

    label 'pbs_small' 
    publishDir "${params.out}", mode: 'copy'

    input:
    val sim_path from sim_path

    output:
    file 'V1_santa_stats.csv'

    script:
    """
    python3.7 ${params.bin}/V1_santa_stats.py ${sim_path}
    """

  }

  process V2_santa_bp {
    // Summarise simulated breakpoints per output .fasta    
    
    label 'pbs_small' 
    publishDir "${params.out}", mode: 'copy'

    input:
    val sim_path from sim_path

    output:
    file 'V2_santa_bp.csv'

    script:
    """
    python3.7 ${params.bin}/V2_santa_bp.py ${sim_path}
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
  // TO DO: change below to look nicer `Channel.fromPath.set{}...`
  B1_input = Channel.fromPath( "${params.simdir}/S4_santa/n${params.seqn}/*.fasta" )
  B2_input = Channel.fromPath( "${params.simdir}/S4_santa/n${params.seqn}/*.fasta" )
  B3_input = Channel.fromPath( "${params.simdir}/S4_santa/n${params.seqn}/*.fasta" )
  B4_input = Channel.fromPath( "${params.simdir}/S4_santa/n${params.seqn}/*.fasta" )
  B5_input = Channel.fromPath( "${params.simdir}/S4_santa/n${params.seqn}/*.fasta" )
/*
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

    errorStrategy 'ignore'
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
    script:
    """
    echo "Y" |
    ${params.bin}/3seq_elf -f $seq -d -id ${seq}
    """

  }
*/
  process B3_geneconv {

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
/*
  process B4_uchime_derep {

    label "${params.label}"
    tag "$seq"
    publishDir "${params.out}/B4_uchime/derep", mode: 'symlink'

    input:
    file seq from B4_input.flatten()

    output:
    file 'derep_*' into B4_input_uchime

    script:
    """
    vsearch --derep_fulllength ${seq} \
            --output derep_${seq} \
            --sizeout
    """

  }

  process B4_uchime {

    label "${params.label}"
    tag "$seq"
    publishDir "${params.out}/B4_uchime", mode: 'move'

    input:
    file seq from B4_input_uchime.flatten()

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

  process B5_gmos {

    label "${params.label}"
    tag "$seq"
    publishDir "${params.out}/B5_gmos", mode: 'move', saveAs: { filename -> "${seq}_$filename" }

    input:
    file seq from B5_input.flatten()

    output:
    file '*.fasta'
    file '*.len'
    file '*.txt'

    script:
    """
    ${params.bin}/gmos -i ${seq} \
                       -j ${seq} \
                       -o gmos.txt \
                       -t   
    """

  }
*/
}

/*
 *  3. RECOMBINATION DETECTION (EMPIRICAL)
 */

if (params.mode == 'emp') {

  println "Reading ${params.seq}"
  seq_temp = "${params.seq}"
  seq_file = file(seq_temp)

  process E1_phi_profile {

    errorStrategy 'ignore'
    label "${params.label}"
    tag "$seq"
    publishDir "${params.out}/empirical", mode: 'move'

    input:
    file seq from seq_file

    output:
    file 'Profile.csv'

    script:
    """
    Profile -f $seq
    """

  }

  process E2_3seq {

    errorStrategy 'ignore'
    label "${params.label}"
    tag "$seq"
    publishDir "${params.out}/empirical", mode: 'move'

    input:
    file seq from seq_file

    output:
    file '*3s.log'
    file '*3s.pvalHist'
    file '*s.rec'
    file '*3s.longRec' optional true

    script:
    """
    echo "Y" |
    ${params.bin}/3seq_elf -f $seq -d -id ${seq}
    """

  }

  process E3_geneconv {

    errorStrategy 'ignore'
    label "${params.label}"
    tag "$seq"
    publishDir "${params.out}/empirical", mode: 'move'

    input:
    file seq from seq_file

    output:
    file '*.tab'

    script:
    """
    ${params.bin}/geneconv $seq -nolog -Dumptab -Fancy
    """

  }

  process E4_filter_fasta {
    // TO DO: Derep this process with S1_filter_fasta
     publishDir "${params.out}/empirical/E0_filter_fasta", mode: 'copy'

    input:
    file seq from seq_file

    output:
    file 'seqLength*.png' optional true
    file '*_m'
    file '*_n'
    file '*_n_filtered' into E4_input_uchime_derep
    file '*_removed'
    file '*_log.txt'

    script:
    """
    python3.7 ${params.bin}/S1_filter_fasta.py $seq
    """

  }

  process E4_uchime_derep {

    label "${params.label}"
    tag "$seq"
    publishDir "${params.out}/empirical/E4_uchime_derep", mode: 'symlink'

    input:
    file seq from E4_input_uchime_derep

    output:
    file 'derep_*' into E4_input_uchime

    script:
    """
    vsearch --derep_fulllength ${seq} \
            --output derep_${seq} \
            --sizeout
    """

  }

  process E4_uchime {

    label "${params.label}"
    tag "$seq"
    publishDir "${params.out}/empirical", mode: 'move'

    input:
    file seq from E4_input_uchime

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

  process E5_gmos {

    label "${params.label}"
    tag "$seq"
    publishDir "${params.out}/empirical", mode: 'move'

    input:
    file seq from seq_file

    output:
    file '*.fasta'
    file '*.len'
    file '*.txt'

    script:
    """
    ${params.bin}/gmos -i ${seq} \
                       -j ${seq} \
                       -o gmos_${seq} \
                       -t   
    """

  }

}

/*
 * 4. CALCULATE CLASSIFICATION METRICS
 */

// Create simulated breakpoints with *.R

if (params.mode == 'class') {

  sim_bp = "${params.sim_bp}"
  rec_path = "${params.rec_path}"
/*
  log.info """
  simbp   = ${params.simbp}
  """.stripIndent()

  Channel
      .fromPath(params.simbp)
      .splitCsv(header:true)
      .map { row -> tuple(file(row.params), row.bps) }
      .set { F1_input }
      .set { F5_input }

  process F1_phi_profile {
    // For some reason, params.bin and params.out don't work???
    // https://github.com/fredjaya/rec-bench/issues/22

    label "${params.label}"
    publishDir "/Users/13444841/Dropbox/Masters/02_working/2001_precision_recall/2001_profile_nf/F1_phi_profile", mode: 'move'

    input:
    set file(params), bps from F1_input

    output:
    file 'condition_*'
    file '*.log'

    script:
    """
    python3.7 ${baseDir}/bin/F1_addCondition_phiProfile.py ${params} ${bps}
    """

    }
*/

  process F2_3seq {

  label "pbs_small" 
  publishDir "${params.out}/F2_3seq"
 
  input:
  val sim_bp from sim_bp
  val rec_path from rec_path

  output:
  file "F2_3seq_conditions.csv"
  
  script:
  """
  python3.7 ${baseDir}/bin/other_scripts/F2_addCondition_3SEQ.py \
            ${sim_bp} \
            ${rec_path}/B2_3seq
  """
  }

/*
  process F5_gmos_parse {
  
    Channel
      .fromPath("/shared/homes/13444841/2001_gmos_sim2/B5_gmos/*_gmos.txt")
      .set{ gmos_out_parse }

    label "${params.label}"
    publishDir "/shared/homes/13444841/2001_gmos_sim2/parsed_out", mode: 'move'

    input:
    file gmos_out_parse from gmos_out_parse

    output:
    file '*.csv' 
  
    script:
    """
    python3.7 ${baseDir}/bin/F5_parse_gmos.py ${gmos_out_parse} 
    """
  
  }

  process F5_gmos_conditions { 

    label "${params.label}"
    publishDir "${params.out}/F5_gmos/conditions", mode: 'move'

    input:
    set file(params), bps from F5_input

    output:
    file '*.csv'

    script:
    """
    python3.7 ${params.bin}/F5_addConditions_gmos.py ${params} ${bps}
    """ 
    
  }
*/
}
