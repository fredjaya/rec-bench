input2 = Channel.fromPath( 'out/santa/n10000/*.fasta' )

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
