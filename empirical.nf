#!/usr/local/bin nextflow

/* Dependecies:
 *  Python (biopython)
 *  Java
 *  OpenMPI
 *  R - ape, phangorn
 *
 */

seq = file("$baseDir/data/fmdv/FMDV_Kenya_plaques_refs.fas")

// PHIPACK //
process phipack_e {

  publishDir 'out/e/1_phipack', mode: 'move'

  input:
  file seq from seq

  output:
  file{'*'}

  script:
  """
  $baseDir/bin/Phi -f $seq -o -p
  """

}

// 3SEQ //
process '3seq_e' {

  publishDir 'out/e/2_3seq', mode: 'move'

  input:
  file seq from seq

  output:
  file{'*'}

  script:
  """
  echo "Y" |
  $baseDir/bin/3seq -f $seq -d -id 3seq.out
  """

}

// Create tree to initialise ClonalFrameML
process iqtree {

  publishDir 'out/e/iqtree', mode: 'copy'

  input:
  file seq from seq

  output:
  file{'*'}
  file '*.treefile' into tree

  script:
  """
  $baseDir/bin/iqtree -s $seq -m GTR+I+G -nt AUTO
  """
//$baseDir/bin/iqtree -s $seq -m GTR+I+G -alrt 1000 -bb 1000 -nt AUTO
}

// CLONALFRAMEML //
process clonalfml_e {

  publishDir 'out/e/3_cfml', mode: 'move'

  input:
  file seq from seq
  file tree from tree

  output:
  file{'*'}

  script:
  """
  $baseDir/bin/ClonalFrameML $tree $seq $seq
  Rscript $baseDir/bin/cfml_results.R $seq
  """
}

process uchime_e {

  publishDir 'out/e/4_uchime', mode: 'move'

  input:
  file seq from seq

  output:
  file{'*'}

  script:
  """
  $baseDir/bin/vsearch --uchime_denovo $seq \
                       --chimeras ${seq}.rc \
                       --nonchimeras ${seq}.nonrc \
                       --log ${seq}.log
  """

}
