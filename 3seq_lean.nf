input = Channel.fromPath( 'out/santa/msa_*.fasta' )

process '3seq_s' {

  publishDir 'out/S2_3seq', mode: 'move'

  input:
  file seq from input.flatten()

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
