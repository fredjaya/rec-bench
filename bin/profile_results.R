#!/usr/bin/env Rscript

library(data.table)
library(ggplot2)
library(viridis)

#setwd("GitHub/rec-bench/")

# Read Profile.csv
df <- read.csv("out/profile_s_stats.csv", header = T, stringsAsFactors = T)
df <- melt(df,
           id = 1:5,
           variable.name = 'bp_position',
           value.name = 'pval'
           )
df$bp_position <- gsub("X", "", df$bp_position)
#df$bp_position <- sapply(df$bp_position, as.factor)

pdf("profile_test.pdf", onefile = F)
df %>% 
  group_by(mut, rec, seqLen) %>%
  ggplot(.) +
  facet_grid(cols = vars(rec), rows = vars(mut)) +
  geom_point(aes(bp_position, pval))
  
  ggplot() +
    geom_point(aes(bp_position, pval), alpha = 0.7, size = 3) +
    scale_y_reverse() +
    scale_colour_viridis(discrete = T) +
    facet_grid(cols = vars(rec), rows = vars(mut))
dev.off()

  geom_point(alpha = 0.7, size = 3) +
  scale_y_reverse() +
  scale_colour_viridis(discrete = T) +
  facet_grid(cols = vars(rec), rows = vars(mut))


ggplot(df, aes(bp_position, pval)) +
  geom_boxplot(aes(colour = as.factor(seqLen)), alpha = 0.7, size = 2) +
  scale_y_reverse() +
  scale_colour_viridis(discrete = T) +
  facet_grid(cols = vars(rec), rows = vars(mut)) +
  geom_hline(yintercept = 0.05, colour = 'red')

