library(tidyverse)

# Set command-line arguments
args <- commandArgs(trailingOnly = T)

# Prepare general santa_bp ----------
# Read V2_santa_bp.csv
santa_bp <- read.csv(args[1], na.strings = c("", NA))

# Amend sci notation to match RDM output file names
santa_bp$mut <- gsub('1e-07', '1.0E-7'   , santa_bp$mut)
santa_bp$mut <- gsub('1e-06', '0.0000010', santa_bp$mut)
santa_bp$mut <- gsub('1e-05', '0.000010' , santa_bp$mut)
santa_bp$mut <- gsub('1e-04', '0.00010'  , santa_bp$mut)
santa_bp$mut <- gsub('0.001', '0.0010'   , santa_bp$mut)
santa_bp$mut <- gsub('0.01' , '0.010'    , santa_bp$mut)

santa_bp$rec <- gsub('1e-07', '1.0E-7'   , santa_bp$rec)
santa_bp$rec <- gsub('1e-06', '0.0000010', santa_bp$rec)
santa_bp$rec <- gsub('1e-05', '0.000010' , santa_bp$rec)
santa_bp$rec <- gsub('1e-04', '0.00010'  , santa_bp$rec)
santa_bp$rec <- gsub('0.001', '0.0010'   , santa_bp$rec)
santa_bp$rec <- gsub('0.01' , '0.010'    , santa_bp$rec)

# Sanity check
paste("Mutation rate: "     , unique(santa_bp$mut   ))
paste("Recombination rates ", unique(santa_bp$rec   ))
paste("Sample sizes "       , unique(santa_bp$seqnum))

# Add file name prefixes
santa_bp$mut     <- paste('msa_m', santa_bp$mut    , sep = '')
santa_bp$rec     <- paste('rc'   , santa_bp$rec    , sep = '')
santa_bp$seqnum  <- paste('n'    , santa_bp$seqnum , sep = '')
santa_bp$dualInf <- paste('dual' , santa_bp$dualInf, sep = '')

# Parse to match PhiPack (Profile) file names ----------
profile_bp     <- santa_bp
profile_bp$rep <- paste('rep', profile_bp$rep, '.fasta_Profile.csv', sep = '')

# Concatenate breakpoints per parameter
profile_bp <- profile_bp %>%
  unite(col = params, mut:rep, sep = '_') %>%
  group_by(params) %>%
  summarize(bps = paste(bps, collapse = ":"))

# Remove NAs in breakpoint column
profile_bp$bps <- gsub('NA:', '', profile_bp$bps)
profile_bp$bps <- gsub(':NA', '', profile_bp$bps)

write.csv(profile_bp, "V3_profile_sim_bp.csv",
          row.names = F)

# Parse to match 3SEQ file names ----------
tseq_bp <- santa_bp
tseq_bp$rep <- paste('rep', tseq_bp$rep, '.fasta.3s.rec', sep = '')

# Concatenate as file name
tseq_bp <- tseq_bp %>%
  unite(col = params, mut:rep, sep = '_')

write.csv(tseq_bp,"V3_3seq_sim_bp.csv",
          row.names = F)

# Parse to match GENECONV file names ----------
gc_bp <- santa_bp
gc_bp$rep <- paste('rep', gc_bp$rep, '.tab', sep = '')

# Concatenate as file name
gc_bp <- gc_bp %>%
  unite(col = params, mut:rep, sep = '_')

write.csv(gc_bp,"V3_gc_sim_bp.csv",
          row.names = F)

