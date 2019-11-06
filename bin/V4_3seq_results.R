#!/usr/bin/env Rscript

# Install github tidyr for pivot functions
#devtools::install_github("tidyverse/tidyr")
library(tidyr)
library(dplyr)
library(ggplot2)

setwd("Dropbox/FMDV_Kenya/03_results/230519_fmdv_recbench/2_3seq/")

# Read in .rec output
df <- read.delim("FMDV_Kenya_4refs_alg_m.fasta.3s_tsStripped.rec", header = F, sep = "\t",
                 stringsAsFactors = F)
#df <- df[, c(1:3, 7, 13:ncol(df))]

seqLength = 7035
# Gather breakpoint columns into rows
df <- df %>%
  # Remove "header" row
  .[-1,] %>% 
  # Pivot double bp columns into one
  pivot_longer(cols = 13:ncol(df)) %>% 
  # Remove "name" column created by pivot
  select(-name) %>% 
  # Remove all rows that have blank fields in new bp col
  .[!(.$value == ""),] %>% 
  # Separate breakpoints into start and end columns
  separate(col = value, into = c("bp_start", "bp_end"), sep = "-\\d+\\s&\\s\\d+-")

# Rename columns
colnames(df) <- c("P_ACCNUM", "Q_ACCNUM", "C_ACCNUM", "m", "n", "k", "p", 
                   "HS?", "log(p)", "DS(p)", "DS(p)2", "min_rec_length",
                   "bp_start", "bp_end")

write.csv(df, "3seq_results.csv")
# Change plot info to numeric
df[,4:14] <- sapply(df[,4:14], as.numeric)

# Inverse p values
df2 <- df
df2$p <- sapply((df2$p), function(x) 1-x)

numUniqueSeq <- n_distinct(df2[,1:3])

# Plot individual recombinants
pdf("3seq_rc_plot.pdf")
df2 %>% 
  group_by(P_ACCNUM, Q_ACCNUM, C_ACCNUM) %>%
  ggplot(data = .) + 
  theme(strip.text   = element_blank(),
        axis.text.y  = element_blank(),
        axis.ticks.y = element_blank(),
        legend.position = "none",
        plot.margin = unit(c(1,1,1,10), "lines")) +
  coord_cartesian(xlim = c(0, seqLength),
                  ylim = c(0, 1),
                  clip ='off') +
  facet_wrap(~P_ACCNUM+Q_ACCNUM+C_ACCNUM,
             nrow = numUniqueSeq,
             ncol = 1) +
  geom_rect(aes(xmin = bp_start, xmax = bp_end, 
                ymin = 0, ymax = p, 
                alpha = 0), colour = "red", fill = NA) +
  geom_text(aes(x = -0, y = p, label = C_ACCNUM),
            size = 2.5, vjust = 1, hjust = 1)
dev.off()
