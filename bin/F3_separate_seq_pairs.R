library(dplyr)
library(tidyr)

# Set command-line arguments
args <- commandArgs(trailingOnly =T)

# Read concatenated gc outputs (F3_geneconv_summarised.csv)
gc <- read.csv(args[1])

# Separate outer sequence fragments
outer <- gc %>%
  filter(frag_type == "GO")

# Transform inner sequence frags
gc <- gc %>%
  filter(frag_type != "GO") %>%
  separate(seq_names, c('seq1', 'seq2'), sep = ';')

# Clean and separate sequence pairs
seq1 <- gc %>%
  select(-seq2, -seq2_begin, -seq2_end, -seq2_length) %>%
  rename(seq_name = seq1, start_bp = seq1_begin, end_bp = seq1_end, bp_length = seq1_length)

seq2 <- gc %>%
  select(-seq1, -seq1_begin, -seq1_end, -seq1_length) %>%
  rename(seq_name = seq2, start_bp = seq2_begin, end_bp = seq2_end, bp_length = seq2_length)

gc_out <- rbind(seq1, seq2)
gc_out <- gc_out %>%
  select(-frag_type, -num_dif, -mismatch_penalty)

gc_out$seq_name <- gsub(":\\d+", "", gc_out$seq_name)
write.csv(gc_out, "F3_geneconv_unpaired.csv", row.names = F)

