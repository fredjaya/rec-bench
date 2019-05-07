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

  publishDir 'out/1_santa'

  input:
  file xml from santaInput

  output:
  file('stats_*.csv')
  file('tree_*.trees')
  file 'alignment_*.fasta' into rdmInput

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
/*
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
*/
