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
//  C H A N N E L S  //
//===================//
mutRate = Channel.from(10e-5, 10e-4, 10e-3)
recRate = Channel.from(10e-8, 10e-7)



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
  each mutRate from mutRate
  each recRate from recRate

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
  file 'tree_*.trees' into //treeS3
  file 'msa_*.fasta' into rdmInputS1, rdmInputS2, rdmInputS4//, rdmInputS3

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
  errorStrategy 'ignore' //Too few informative sites to test significance.
  //errorStrategy 'retry'
  //maxRetries 3

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
/*
process cfml_s {

  publishDir 'out/S3_cfml', mode: 'move'

  input:
  file seq from rdmInputS3
  file tree from treeS3

  output:
  file '*.cfml.pdf'
  file '*.em.txt'
  file '*.importation_status.txt'
  file '*labelled_tree.newick'
  file '*.ML_sequence.fasta'
  file '*.position_cross_reference.txt'
  //file '*.emsim.txt' optional true

  script:
  """
  $baseDir/bin/ClonalFrameML $tree $seq $seq
  Rscript $baseDir/bin/cfml_results.R $seq
  """

}
*/

process uchime_s {

  publishDir 'out/S4_uchime', mode: 'move'

  input:
  file seq from rdmInputS4.flatten()

  output:
  file '*_m'
  file '*.rc'
  file '*.nonrc'
  file '*.log'

  script:
  """
  sed 's|'-'|''|g' $seq > ${seq}_m
  $baseDir/bin/vsearch --uchime_denovo ${seq}_m \
                       --chimeras ${seq}_m.rc \
                       --nonchimeras ${seq}_m.nonrc \
                       --log ${seq}_m.log
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

process iqtree {

  publishDir 'out/iqtree', mode: 'copy'

  input:
  file seq from seq

  output:
  file '*.bionj'
  file '*.ckp.gz'
  file '*.iqtree'
  file '*.log'
  file '*.mldist'
  file '*.uniqueseq.phy'
  file '*.treefile' into treeE3

  script:
  """
  $baseDir/bin/iqtree -s $seq -m GTR+I+G -nt AUTO
  """
  //$baseDir/bin/iqtree -s $seq -m GTR+I+G -alrt 1000 -bb 1000 -nt AUTO

}

process cfml_e {

  publishDir 'out/E3_cfml', mode: 'move'

  input:
  file seq from seq
  file tree from treeE3

  output:
  file '*.cfml.pdf'
  file '*.em.txt'
  file '*.importation_status.txt'
  file '*labelled_tree.newick'
  file '*.ML_sequence.fasta'
  file '*.position_cross_reference.txt'
  //file '*.emsim.txt' optional true

  script:
  """
  $baseDir/bin/ClonalFrameML $tree $seq $seq
  Rscript $baseDir/bin/cfml_results.R $seq
  """

}

process uchime_e {

  publishDir 'out/E4_uchime', mode: 'move'

  input:
  file seq from seq

  output:
  file '*_m'
  file '*.rc'
  file '*.nonrc'
  file '*.log'

  script:
  """
  sed 's|'-'|''|g' $seq > ${seq}_m
  $baseDir/bin/vsearch --uchime_denovo ${seq}_m \
                       --chimeras ${seq}_m.rc \
                       --nonchimeras ${seq}_m.nonrc \
                       --log ${seq}_m.log
  """
}
