# Return the summary stats of sequence distances for a single .fasta
# Loop through bulk .fasta and cat to one sim_distances.txt using
# /Users/13444841/Dropbox/Masters/02_working/2101_diverse/7_sim_dist.sh

library(seqinr)
args <- commandArgs(trailingOnly = TRUE)
fasta <- read.alignment(args[1], format = 'fasta')
dist <- as.vector(dist.alignment(fasta, matrix = 'identity'))
summary(dist)
