#!/usr/local/bin nextflow

seq = file("$baseDir/FMD_recomb_final.fas")

//===================//
// E M P I R I C A L //
//===================//

process phipack_e {

  publishDir 'out/E1_phipack', mode: 'move'

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
  file 'Profile.log'

  script:
  """
  $baseDir/bin/Profile -f $seq
  Rscript $baseDir/bin/phi_profile.R
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

// Create tree to initialise ClonalFrameML
process iqtree {

  publishDir 'out/Eiqtree', mode: 'copy'

  input:
  file seq from seq

  output:
  file '*.bionj'
  file '*.ckp.gz'
  file '*.iqtree'
  file '*.log'
  file '*.mldist'
  file '*.uniqueseq.phy'
  file '*.treefile' into tree

  script:
  """
  $baseDir/bin/iqtree -s $seq -m GTR+I+G -nt AUTO
  """
//$baseDir/bin/iqtree -s $seq -m GTR+I+G -alrt 1000 -bb 1000 -nt AUTO
}

process clonalfml_e {

  publishDir 'out/E3_cfml', mode: 'move'

  input:
  file seq from seq
  file tree from tree

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
