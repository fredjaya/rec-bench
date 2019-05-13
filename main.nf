#!/usr/local/bin nextflow

/* Dependecies:
 *  Python (biopython)
 *  Java
 *  OpenMPI
 *  R - ape, phangorn
 *
 */

 /*
  * hcvDir = "$baseDir/data/hcv/*"
  * hcvSeq = file(hcvDir)fmdvDir = "$baseDir/data/fmdv/*"
  * fmdvFile = file($fmdvDir)
  * fmdvXml = file('fmdv_santa.xml')
  */

// Set path for empirical sequence data
seq = file("$baseDir/data/hcv/seqment_1.fasta")

// SANTA-SIM
hcvXml = file("$baseDir/hcv_santa.xml")

// Create three input .xml files, iterating over 3 mutation rates
process paramsweep {

  input:
  file hcvXml from hcvXml
  each mutRate from 0.001,0.0001

  output:
  file 'hcvXml_*.xml' into santaInput

  script:
  """
  sed 's|'MUTRATE'|'$mutRate'|g' $hcvXml > hcvXml_${mutRate}.xml
  """

}

process santa {

  publishDir 'out/santa', mode: 'copy'

  input:
  file xml from santaInput

  output:
  file('stats_*.csv')
  file('tree_*.trees')
  file ('seqment_*.fasta') into rdmInput

  script:

  """
  java -jar $baseDir/bin/santa-ba8733a.jar $xml
  """

}

// Run RDMs
process phipack_s {

  publishDir 'out/S1_phipack', mode: 'move'

  input:
  file seq from rdmInput

  output:
  file{'*'}

  script:
  """
  $baseDir/bin/Phi -f $seq -o -p
  """
}

process '3seq_s' {

  publishDir 'out/S2_3seq', mode: 'move'

  input:
  file seq from rdmInput

  output:
  file{'*'}

  script:
  """
  echo "Y" |
  $baseDir/bin/3seq -f $seq -d -id 3seq.out
  """
}

/*
process phipack_e {

  publishDir 'out/E1_phipack', mode: 'move'

  input:
  file hcv from hcvSeq

  output:
  file{'*'}

  script:
  """
  $baseDir/bin/Phi -f $hcv -o -p
  """
}

process '3seq_e' {

  publishDir 'out/E2_3seq', mode: 'move'

  input:
  file hcv from hcvSeq

  output:
  file{'*'}

  script:
  """
  echo "Y" |
  $baseDir/bin/3seq -f $hcv -d -id 3seq.out
  """
}
*/
