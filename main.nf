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
seqPath = "$baseDir/data/hcv/alignment_1n.fasta"
seq = file(seqPath)

// SANTA-SIM
hcvXml1 = file("$baseDir/hcv_santa.xml")

process xmlPath {

  input:
  file hcvXml from hcvXml1
  val seqPath

  output:
  file 'hcv_santa2.xml' into hcvXml2

  script:
  """
  sed 's|'SEQPATH'|'$seqPath'|g' $hcvXml > hcv_santa2.xml
  """
}

// Create three input with 2 reps .xml files, iterating over 3 mutation rates
process paramsweep {

  input:
  file hcvXml from hcvXml2
  each mutRate from 0.01,0.001,0.0001

  output:
  file 'hcvXml_*.xml' into santaInput

  script:
  """
  sed 's|'MUTRATE'|'$mutRate'|g' $hcvXml > hcvXml_m${mutRate}.xml
  """

}

process santa {
  errorStrategy 'ignore' //non-viable population

  publishDir 'out/santa', mode: 'copy'

  input:
  file xml from santaInput

  output:
  file 'stats_*.csv'
  file 'tree_*.trees'
  file 'alignment_*.fasta' into rdmInput1, rdmInput2

  script:
  """
  java -jar $baseDir/bin/santa-ba8733a.jar $xml
  """

}

// Run RDMs
process phipack_s {

  publishDir 'out/S1_phipack', mode: 'move'

  input:
  file seq from rdmInput1

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
  file seq from rdmInput2

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
