
Channel
    .fromPath(params.fa)
    .into { rdp_fa, maxchi_fa, chimaera_fa } 
    
process rdp {

    label "rev_scale"
    tag "$seq"
    publishDir "${params.out}/rdp"

    input:
        path fa from rdp_fa

    output:
        path "$fa.baseName" 

    script:
    """
    openrdp $fa -o $fa.baseName -m rdp
    """

}

process maxchi {

    label "rev_scale"
    tag "$seq"
    publishDir "${params.out}/maxchi"

    input:
        path fa from maxchi_fa

    output:
        path "$fa.baseName" 

    script:
    """
    openrdp $fa -o $fa.baseName -m maxchi
    """

}

process chimaera {

    label "rev_scale"
    tag "$seq"
    publishDir "${params.out}/chimaera"

    input:
        path fa from chimaera_fa

    output:
        path "$fa.baseName" 

    script:
    """
    openrdp $fa -o $fa.baseName -m chimaera
    """

}
