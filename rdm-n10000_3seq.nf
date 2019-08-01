input3 = Channel.fromPath( 'out/santa/n10000/*.fasta' )

process '3seq_s' {

  label 'med'
  tag "$seq"
  publishDir 'out/S3_3seq', mode: 'move'

  input:
  file seq from input3.flatten()

  output:
  file '*3s.log'
  file '*3s.pvalHist'
  file '*s.rec'
  file '*3s.longRec' optional true

  script:
  """
  echo "Y" |
  $baseDir/bin/3seq_elf -f $seq -d -id ${seq}
  """

}
