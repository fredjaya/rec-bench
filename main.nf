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

//===================//
// S A N T A - S I M //
//===================//

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

process paramsweep {

  input:
  file hcvXml from hcvXml2
  each mutRate from 10e-5, 10e-4, 10e-3
  each recRate from 10e-8, 10e-7

  output:
  file 'hcvXml_*.xml' into santaInput

  script:
  """
  sed 's|'MUTRATE'|'$mutRate'|g; s|'RECRATE'|'$recRate'|g' $hcvXml > hcvXml_m${mutRate}_r${recRate}.xml
  """

}

process santa {
  errorStrategy 'ignore' //non-viable population

  publishDir 'out/santa', mode: 'copy'

  input:
  file xml from santaInput

  output:
  file 'stats_*.csv'
  file 'tree_*.trees' //into treeInput
  file 'msa_*.fasta' into rdmInputS1, rdmInputS2

  script:
  """
  java -jar $baseDir/bin/santa-ba8733a.jar $xml
  """

}

//===================//
// S I M U L A T E D //
//===================//

process phipack_s {

  publishDir 'out/S1_phipack', mode: 'move', saveAs: { filename -> "${seq}_$filename" }
  //errorStrategy 'ignore' //Too few informative sites to test significance.
  errorStrategy 'retry'
  maxRetries 3

  input:
  file seq from rdmInputS1.flatten()

  output:
  file 'Phi.inf.list'
  file 'Phi.inf.sites'
  file 'Phi.log'
  file 'Phi.poly.unambig.sites'

  script:
  """
  $baseDir/bin/Phi -f $seq -o -p
  """
}


process '3seq_s' {

  publishDir 'out/S2_3seq', mode: 'move'

  input:
  file seq from rdmInputS2.flatten()

  output:
  file '*3s.log'
  file '*3s.pvalHist'
  file '*s.rec'
  file '*3s.longRec' optional true

  script:
  """
  echo "Y" |
  $baseDir/bin/3seq -f $seq -d -id ${seq}
  """
}

//===================//
// E M P I R I C A L //
//===================//

process phipack_e {

  publishDir 'out/E1_phipack', mode: 'move', saveAs: { filename -> "${seq}_$filename" }
  //errorStrategy 'ignore' //Too few informative sites to test significance.

  input:
  file seq from seq

  output:
  file 'Phi.inf.list'
  file 'Phi.inf.sites'
  file 'Phi.log'
  file 'Phi.poly.unambig.sites'

  script:
  """
  $baseDir/bin/Phi -f $seq -o -p
  """
}

process '3seq_e' {

  publishDir 'out/E2_3seq', mode: 'move'

  input:
  file seq from seq

  output:
  file '*3s.log'
  file '*3s.pvalHist'
  file '*s.rec'
  file '*3s.longRec' optional true

  script:
  """
  echo "Y" |
  $baseDir/bin/3seq -f $seq -d -id ${seq}
  """
}
