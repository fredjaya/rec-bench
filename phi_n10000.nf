
seq = "$baseDir/data/hcv/FP7_patient_037_allseqs.fasta"
seqFile = file(seq)

input = Channel.fromPath( 'out/santa/*n10000*.fasta')

process phipack_s {

  publishDir 'out/S1_phipack', mode: 'move', saveAs: { filename -> "${seq}_$filename" }

  input:
  file seq from input.flatten()

  output:
  file 'Phi.inf.list'
  file 'Phi.inf.sites'
  file 'Phi.log'
  file 'Phi.poly.unambig.sites'

  script:
  """
  Phi -f $seq -o -p
  """

}
