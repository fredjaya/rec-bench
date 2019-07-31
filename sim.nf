#!/usr/local/bin nextflow

// From hcv_minimal_hpc.nf

// Set path for empirical sequence data

seq = "$baseDir/data/hcv_raghwani/FP7_patient_037_allseqs.fasta"
seqFile = file(seq)

//===================//
//  C H A N N E L S  //
//===================//

mutRate = Channel.from(10e-5, 10e-4, 10e-3) //  "Error rate", mutation/nt/rep cycle (Bartenschlager and Lohmann, 2000; Ribeiro et al., 2012)
recRate = Channel.from(10e-8, 10e-7) // recombination/site/day (Raghwani et al., 2019) "average normalised recombination frequency" (Reiter, 2011)
seqNum = Channel.from(100, 1000, 2500, 5000, 10000)
dualInf = Channel.from(0.05)

//====================//
// I N P U T  P R E P //
//====================//

process prepro {

  publishDir 'out/fasta', mode: 'copy'

  input:
  file seq from seqFile

  output:
  file 'seqLength*.png' optional true
  file '*_m' //into rdmInput*
  file '*_n' //into seqUchime
  file '*_n_filtered' into seqPath
  file '*_removed'
  file '*_log.txt'

  script:
  """
  python3.7 $baseDir/bin/fasta_preprocess.py $seq
  """
}

//===================//
// S A N T A - S I M //
//===================//

//xml1 = file("$baseDir/hcv_santa.xml")
xml1 = file("$baseDir/hcv_santa.xml")

process xmlPath {

  input:
  file xml from xml1
  val seqPath from seqPath

  output:
  //file 'hcv_santa2.xml' into xml2
  file '*2.xml' into xml2

  script:
  """
  sed 's|'SEQPATH'|'$seqPath'|g' $xml > ${xml}2.xml
  """

}

process paramsweep {

  input:
  file xml from xml2
  each mutRate from mutRate
  each recRate from recRate
  each seqNum from seqNum
  each dualInf from dualInf

  output:
  file '*.xml' into santaInput

  script:
  """
  sed 's|'MUTRATE'|'$mutRate'|g; s|'RECRATE'|'$recRate'|g; s|'SEQNUM'|'$seqNum'|g; s|'DUALRATE'|'$dualInf'|g' $xml > xml_m${mutRate}_rc${recRate}_n${seqNum}_n${dualInf}.xml
  """

}

process santa {
  //errorStrategy 'ignore' //non-viable population

  publishDir 'out/santa', mode: 'copy'

  input:
  file xml from santaInput

  output:
  file 'stats_*.csv'
  //file 'tree_*.trees'
  file 'msa_*.fasta' into rdmInputS1, rdmInputS2, rdmInputS4 //rdmInputS3,
  set file('tree_*.trees'), file('msa_*.fasta') into rdmInputS3

  script:
  """
  java -jar -Xmx512M -XX:ParallelGCThreads=2 $baseDir/bin/santa_bp.jar $xml
  """

}

process divy {

  input:
  each seqNum from seqNum

  script:
  """
  mkdir $baseDir/out/santa/n${seqNum}
  mv $baseDir/out/santa/*${seqNum}_*.fasta $baseDir/out/santa/n${seqNum}
  """


}
