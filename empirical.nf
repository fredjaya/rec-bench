#!/usr/local/bin nextflow

/* Dependecies:
 *  Python (biopython)
 *  Java
 *  OpenMPI
 *  R - ape, phangorn
 *
 */

seq = file("$baseDir/data/hcv/alignment_m0.001_rep1_.fasta")
tree = file("$baseDir/data/hcv/tree_m0.001_rep1.trees")

publishDir = "$baseDir/out"
// PHIPACK //
process phipack_e {

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

  input:
  file seq from seq
  file tree from tree

  output:
  file{'*'}

  script:
  """
  $baseDir/bin/ClonalFrameML $tree $seq cfml
  """
}

/*
process fas2phy {

  input:
  file seq from seq

  output:
  file '*.phy' into phylip

  script:
  """
  python3 $baseDir/bin/fasta2phylip.py -i $seq -o ${seq}.phy
  """

}

process dualbro {
// Putative recombination must be the last sequence, hence requires prior detction

  input:
  file phylip from phylip

  output:
  file{'*'}

  script:
  """
  java $baseDir/bin/DualBrothers-1.1.jar 12345
  """
}
*/
