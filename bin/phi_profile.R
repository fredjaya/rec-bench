#!/usr/bin/env Rscript

library(ggplot2)

#setwd("GitHub/rec-bench/")
help = paste(
  "phi_profile.R summarizes the results of a PhiPack 'Profile' analysis",
  "Usage: Rscript phi_profile.R",
  sep="\n")

path = "out/e/1_phipack/"

# Read Profile.csv
df <- read.csv(paste(path, 'Profile.csv', sep = ''), header = F)
names(df) <- c('mid_bp', 'pvalue')

# Plot pvalues against putative breakpoint regions
pdf(paste(path, 'Profile.pdf', sep = ''))
ggplot(df, aes(mid_bp, pvalue)) +
  geom_line() +
  geom_hline(yintercept = 0.05, color = 'red') +
  theme_minimal()
dev.off()

