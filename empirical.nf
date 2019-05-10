#!/usr/local/bin nextflow

/* Dependecies:
 *  Python (biopython)
 *  Java
 *  OpenMPI
 *  R - ape, phangorn
 *
 */

seq = file("$baseDir/data/hcv/alignment_1.fasta")

// PHIPACK //
process phipack_e {

  storeDir 'out/e/1_phipack'

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

  storeDir 'out/e/2_3seq'

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

  storeDir 'out/e/iqtree'

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

  storeDir 'out/e/3_cfml'

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
