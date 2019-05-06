#!/usr/local/bin nextflow

 /* fmdvDir = "$baseDir/data/fmdv/*"
  * fmdvFile = file($fmdvDir)
  * fmdvXml = file('fmdv_santa.xml')
  */

// Set path for empirical sequence data
hcvDir = "$baseDir/data/hcv/*"
hcvSeq = file(hcvDir)

// SANTA-SIM
hcvXml = file("$baseDir/hcv_santa.xml")

process santa {

  publishDir 'out/1_santa'
  seqInput = hcvXml

  input:
  file xml from hcvXml

  output:
  file('stats_1.csv')
  file('tree_1.trees')
  file 'alignment_1_O.fasta' into rdmInput

  script:

  """
  java -jar $baseDir/rdm/santa-ba8733a.jar $xml
  """

}

// Run RDMs
process phipack_s {

  publishDir 'out/S2_phipack'

  input:
  file align from rdmInput

  output:
  file{'*'}

  script:
  """
  $baseDir/rdm/Phi -f $align -o -p
  """
}

process '3seq_s' {

  publishDir 'out/S3_3seq'

  input:
  file align from rdmInput

  output:
  file{'*'}

  script:
  """
  echo "Y" |
  $baseDir/rdm/3seq -f $align -d -id 3seq.out
  """
}

process phipack_e {

  publishDir 'out/E2_phipack'

  input:
  file hcv from hcvSeq

  output:
  file{'*'}

  script:
  """
  $baseDir/rdm/Phi -f $hcv -o -p
  """
}

process '3seq_e' {

  publishDir 'out/E3_3seq'

  input:
  file hcv from hcvSeq

  output:
  file{'*'}

  script:
  """
  echo "Y" |
  $baseDir/rdm/3seq -f $hcv -d -id 3seq.out
  """
}
