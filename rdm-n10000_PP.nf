input1 = Channel.fromPath( 'out/santa/n10000/*.fasta' )
input2 = Channel.fromPath( 'out/santa/n10000/*.fasta' )

process phipack_s {

  label 'med'
  tag "$seq"
  publishDir 'out/S1_phipack', mode: 'move', saveAs: { filename -> "${seq}_$filename" }

  input:
  file seq from input1.flatten()

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

process profile_s {

  label 'med'
  tag "$seq"
  publishDir 'out/S2_profile', mode: 'move', saveAs: { filename -> "${seq}_$filename" }

  input:
  file seq from input2.flatten()

  output:
  file 'Profile.csv'
  file 'Profile.log'

  script:
  """
  $baseDir/bin/Profile_elf -f $seq -o -p
  """

}
