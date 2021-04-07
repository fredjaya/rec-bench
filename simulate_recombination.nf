#!/usr/local/bin nextflow

/*
 * Simulate one generation of recombination on previously mutated sequences
 * Goal: Find the diversity limit required for recombination to be detected
 */

/*
 * PARAMETERS
 */

params.mutated_fasta = "${params.mutated_fasta}"
params.xml           = "${params.xml}"


/*
 * CHANNELS
 */

fasta_ch = Channel.fromPath(params.mutated_fasta)
recrate  = Channel.from(0, 0.2, 0.4, 0.6, 0.8, 1)

/*
 * PROCESSES
 */

process generate_xml {

    input:
    path xml from params.xml
    val fasta
    
}

process simulate_recombination {

    input:
    path fasta from 
    
}

if (params.mode == 'sim') {


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
