#!/usr/local/bin nextflow

Channel
    .fromPath("/shared/homes/13444841/rec-bench/data/*.fasta")
    .into { phi_fa; tseq_fa; gc_fa; uc_fa; gmos_fa }

params.out = "/shared/homes/13444841/2105_empirical"

log.info """

===== DIRECTORIES AND PATHS =====
base = ${baseDir}
bin  = ${params.bin}
out  = ${params.out}

"""

process E1_phi_profile {
    
    label "empirical"
    tag "$seq"
    publishDir "${params.out}", mode: 'move', saveAs: { filename -> "${seq}_$filename" }
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

process E2_3seq {

    label "empirical"
    tag "$seq"
    publishDir "${params.out}", mode: 'move'

    input:
        path seq from tseq_fa

    output:
        file '*3s.log'
        file '*3s.pvalHist'
        file '*s.rec'
        file '*3s.longRec' optional true

    script:
    """
    echo "Y" |
    3seq_elf -f ${seq} -d -id ${seq}
    """

}

process E3_geneconv {

    label "empirical"
    tag "$seq"
    publishDir "${params.out}", mode: 'move'
  
    input:
       path seq from gc_fa
  
    output:
        file '*.tab'
  
    script:
    """
    geneconv $seq -nolog -Dumptab -Fancy
    """

}

process E4_filter_fasta {
    
    label "empirical"
    publishDir "${params.out}/E0_filter_fasta"
    conda 'python=3.7.3 matplotlib=3.1.0'

    input:
        path seq from uc_fa

    output:
    	path 'seqLength*.png' optional true
    	path '*_m'
    	path '*_n'
    	path '*_n_filtered' into E4_input_uchime_derep
    	path '*_removed'
    	path '*_log.txt'

    script:
    """
    python3 ${params.bin}/S1_filter_fasta.py $seq
    """

}

process E4_uchime_derep {

    label "empirical"
    tag "$seq"
    publishDir "${params.out}/E4_uchime_derep"
    conda 'bioconda::vsearch=2.14'

    input:
        path seq from E4_input_uchime_derep

    output:
        path 'derep_*' into E4_input_uchime

    script:
    """
    vsearch --derep_fulllength ${seq} \
        --output derep_${seq} \
        --sizeout
    """

}

process E4_uchime {

    label "empirical"
    tag "$seq"
    publishDir "${params.out}", mode: 'move'
    conda "bioconda::vsearch=2.14"

    input:
    	path seq from E4_input_uchime
  
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

process E5_gmos {
    
    label "empirical"
    tag "$seq"
    publishDir "${params.out}", mode: 'move'
  
    input:
    	path seq from gmos_fa
  
    output:
    	path '*.fasta'
    	path '*.len'
    	path '*.txt'
  
    script:
    """
    ${params.bin}/gmos -i ${seq} \
                       -j ${seq} \
                       -o gmos_${seq} \
                       -t   
    """

}
