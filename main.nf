#!/usr/local/bin nextflow

/* Dependecies:
 *  Python (biopython)
 *  Java
 *  OpenMPI
 *  R - ape, phangorn
 *
 */

// Set path for empirical sequence data
  // _m: characters in fasta names [m]odified for cfml
  // _n: [n]o gaps ('-') in sequences for santa and uchime

seqPath_m = "$baseDir/data/fmdv/FMDV_Kenya_4refs_alg_m.fasta"
seqPath_n = "$baseDir/data/fmdv/FMDV_Kenya_4refs_alg_n2.fasta"
seq = file(seqPath_m)
seq_n = file(seqPath_n)

//===================//
//  C H A N N E L S  //
//===================//
mutRate = Channel.from(10e-5, 10e-4, 10e-3)
recRate = Channel.from(10e-5, 10e-3)

//===================//
// S A N T A - S I M //
//===================//

//xml1 = file("$baseDir/hcv_santa.xml")
xml1 = file("$baseDir/fmdv_kenya_n.xml")

process xmlPath {

  input:
  file xml from xml1
  val seqPath_n

  output:
  //file 'hcv_santa2.xml' into xml2
  file '*2.xml' into xml2

  script:
  """
  sed 's|'SEQPATH'|'$seqPath_n'|g' $xml > ${xml}2.xml
  """

}

process paramsweep {

  input:
  file xml from xml2
  each mutRate from mutRate
  each recRate from recRate

  output:
  file '*.xml' into santaInput

  script:
  """
  sed 's|'MUTRATE'|'$mutRate'|g; s|'RECRATE'|'$recRate'|g' $xml > xml_m${mutRate}_r${recRate}.xml
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
  java -jar $baseDir/bin/santa-ba8733a.jar $xml
  """

}

/*
process iqtree_s {

  publishDir 'out/iqtree_S', mode: 'copy'

  input:
  file seq from seq_n

  output:
  file '*.bionj'
  file '*.ckp.gz'
  file '*.iqtree'
  file '*.log'
  file '*.mldist'
  file '*.uniqueseq.phy'
  file '*.treefile' into treeS3

  script:
  """
  $baseDir/bin/iqtree -s $seq -m GTR+I+G -nt AUTO
  """
  //$baseDir/bin/iqtree -s $seq -m GTR+I+G -alrt 1000 -bb 1000 -nt AUTO

}
*/

process iqtree_e {

  publishDir 'out/iqtree_E', mode: 'copy'

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

process phipack_profile_s {

  publishDir 'out/S1_phipack', mode: 'move', saveAs: { filename -> "${seq}_$filename" }

  input:
  file seq from seq

  output:
  file 'Profile.csv'

  script:
  """
  $baseDir/bin/Profile -f $seq
  """
  //Rscript $baseDir/bin/phi_profile.R

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

process cfml_s {

  errorStrategy 'ignore' //

  publishDir 'out/S3_cfml', mode: 'move'

  input:
  //file seq from rdmInputS3.flatten()
  //file tree from treeS3
  set file(tree), file(seq) from rdmInputS3.flatten()

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

process phipack_profile_e {

  publishDir 'out/E1_phipack', mode: 'move'

  input:
  file seq from seq

  output:
  file 'Profile.csv'

  script:
  """
  $baseDir/bin/Profile -f $seq
  """
    //Rscript $baseDir/bin/phi_profile.R
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
