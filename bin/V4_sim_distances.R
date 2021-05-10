# Return the summary stats of sequence distances for a single .fasta
# Loop through bulk .fasta and cat to one sim_distances.txt using
# loop in log.sh

library(seqinr)
args <- commandArgs(trailingOnly = TRUE)
fasta <- read.alignment(args[1], format = 'fasta')
dist <- as.vector(dist.alignment(fasta, matrix = 'identity'))
summary(dist)
