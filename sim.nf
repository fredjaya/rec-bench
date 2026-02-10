#!/usr/local/bin nextflow


/*
 * INPUT OPTIONS AND PARAMETERS
 */

// Print parameters
log.info """

===== DIRECTORIES AND PATHS =====
base      = ${baseDir}
bin       = ${params.bin}
out       = ${params.out}
trace     = ${params.trace}
mode      = ${params.mode}
seq       = ${params.seq}
xml       = ${params.xml}

"""

// Define parameters for S3_param_sweep
if (params.mode == 'performance') {
    mutrate = Channel.from(0, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1)
    recrate = Channel.from(0, 0.001, 0.005, 0.01, 0.05, 0.1)
    dualinf = Channel.from(0, 1)
    seqnum = Channel.from(100) 
}

else if (params.mode == 'scalability') {
    mutrate = Channel.from(0, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1)
    recrate = Channel.from(0, 0.1)
    dualinf = Channel.from(1)
    seqnum = Channel.from(1000)
}

else {
    println "ERROR: Please specify either --mode 'performance' or 'scalability'"
}

def helpMessage() {
    log.info"""
    ===== GENERATING SIMULATION DATASETS =====
    
    Simulate .fasta files across different evolutionary parameters using SANTA-SIM
    
    Usage:
        nextflow run sim.nf [options]
    
    Options:
        --mode [str]    'performance' or 'scalability' 
        --seq [.fasta]  Path to input .fasta file
        --xml [.xml]    SANTA-SIM configuration file 
        --out [path]    Path to working directory
    """.stripIndent()
 }

if (params.help) {
  // Show help message
  helpMessage()
  exit 0
}

/*
 * SEQUENCE SIMULATION
 */

process S1_filter_fasta {
    
    // Retain full-length sequences only as SANTA-SIM can't handle gaps
    
    conda 'python=3.7.3 matplotlib=3.1.0'
    publishDir "${params.out}/S1_filter_fasta"
    
    input:
        path seq from params.seq
    
    output:
        path 'seqLength*.png' optional true
        path '*_m'
        path '*_n'
        path '*_n_filtered' into seq_path
        path '*_removed'
        path '*_log.txt'
    
    script:
    """
    python3 ${params.bin}/S1_filter_fasta.py $seq
    """
    
}

process S2_santa_xml {
    
    // Add path of input .fasta to santa.xml
    
    input:
        path xml_in from params.xml
        val seq_path from seq_path
    
    output:
        path '*_out.xml' into xml_out
    
    script:
    """
    sed 's|'SEQPATH'|'${seq_path}'|g' ${xml_in} > ${xml_in}_out.xml
    """
    
  }

process S3_param_sweep {
    
    // Generate .xml files across specified evolutionary parameters
    
    publishDir "${params.out}/S3_param_sweep"
    
    input:
        path xml_out from xml_out
        each mutrate from mutrate
        each recrate from recrate
        each seqnum from seqnum 
        each dualinf from dualinf

    output:
        path '*.xml' into santa_in
    
    script:
    """
    sed 's|'MUTRATE'|'$mutrate'|g; s|'RECRATE'|'$recrate'|g; \
    s|'SEQNUM'|'$seqnum'|g; s|'DUALRATE'|'$dualinf'|g' \
    $xml_out > xml_m${mutrate}_rc${recrate}_n${seqnum}_n${dualinf}.xml
    """

}

process S4_santa {

    // Simulate sequences over time, based on .xml files generated
    
    executor 'slurm'
    cpus 2
    memory { 8.GB * task.attempt }
    time '24h'
    errorStrategy 'retry'

    conda 'bioconda::java-jdk=8.0.92'

    publishDir "${params.out}/S4_santa", mode: 'copy'

    input:
        path santa_in from santa_in

    output:
        path 'stats_*.csv'
        path 'tree_*.trees'
        path 'msa_*.fasta' into fasta_ch

    script:
    """
    java -jar -Xmx512M -XX:ParallelGCThreads=2 ${params.bin}/santa_bp.jar \
    $santa_in
    """

}

fasta_ch
    .flatten()
    .into { phi_fa; tseq_fa; gc_fa; uchime_fa; gmos_fa; rdp_fa; maxchi_fa; chimaera_fa }


process B1_phi_profile {

    label "sim_benchmark"
    tag "$seq"
    publishDir "${params.out}/B1_phi_profile",
        saveAs: { filename -> "${seq}_$filename" }
    conda 'bioconda::phipack=1.1'

    input:
        path seq from phi_fa

    output:
        path 'Profile.csv'
        path 'Profile.log'

    script:
    """
    Profile -f ${seq}
    """

}

process B2_3seq {

    label "sim_benchmark"
    tag "$seq"
    publishDir "${params.out}/B2_3seq"
    
    input:
        path seq from tseq_fa

    output:
        path '*.3s.log'
        path '*3s.pvalHist' optional true
        path '*s.rec' optional true
        path '*3s.longRec' optional true


    script:
    """
    echo "Y" |
    3seq_elf -f ${seq} -d -id ${seq}
    """
    
}

process B3_geneconv {

    label "sim_benchmark"                           
    tag "$seq"                                      
    publishDir "${params.out}/B3_geneconv"

    input:
        path seq from gc_fa

    output:
        path '*.tab'

    script:
    """
    geneconv ${seq} -inputpath=${params.out}/S4_santa \
    -nolog -Dumptab -Fancy
    """

}

process B4_uchime_derep {

    label "sim_benchmark"                               
    tag "$seq"                                          
    publishDir "${params.out}/B4_uchime/derep"
    conda 'bioconda::vsearch=2.14'

    input:
        path seq from uchime_fa

    output:
        path 'derep_*' into uchime_in

    script:
    """
    vsearch --derep_fulllength ${seq} \
            --output derep_${seq} \
            --sizeout
    """

}

process B4_uchime {

    label "sim_benchmark"                               
    tag "$seq"                                          
    publishDir "${params.out}/B4_uchime"
    conda 'bioconda::vsearch=2.14'

    input:
        path seq from uchime_in

    output:
        path '*.rc'
        path '*.nonrc'
        path '*.log'

    script:
    """
    vsearch --uchime_denovo ${seq} \
            --chimeras ${seq}.rc \
            --nonchimeras ${seq}.nonrc \
            --log ${seq}.log
    """

}

process B5_gmos {

    label "sim_benchmark"                             
    tag "$seq"                                        
    publishDir "${params.out}/B5_gmos",
        saveAs: { filename -> "${seq}_$filename" }

    input:
        path seq from gmos_fa

    output:
        path '*.fasta'
        path '*.len'
        path '*.txt'

    script:
    """
    gmos -i ${seq} -j ${seq} -o gmos.txt -t
    """
}

process rdp {

    label "slurm"                             
    tag "$seq"                                        
    publishDir "${params.out}/rdp"

    input:
        path seq from rdp_fa

    output:
        path "$seq.baseName"

    script:
    """
    openrdp $seq -o $seq.baseName -m rdp
    """

}

process maxchi {

    label "slurm"                             
    tag "$seq"                                        
    publishDir "${params.out}/maxchi"

    input:
        path seq from maxchi_fa

    output:
        path "$seq.baseName"

    script:
    """
    openrdp $seq -o $seq.baseName -m maxchi
    """

}

process chimaera {

    label "slurm"                             
    tag "$seq"                                        
    publishDir "${params.out}/chimaera"

    input:
        path seq from chimaera_fa

    output:
        path "$seq.baseName"

    script:
    """
    openrdp $seq -o $seq.baseName -m chimaera
    """

}
