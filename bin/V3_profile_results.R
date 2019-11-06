#!/usr/bin/env Rscript

library(data.table)
library(ggplot2)
library(viridis)
library(dplyr)

#args = commandArgs(trailingOnly = F)
#setwd(args[1])

# Read Profile.csv
df <- read.csv("~/Dropbox/Masters/03_results/out_190925/out_190917/viz/B1_profile_stats.csv", header = T, stringsAsFactors = T)
df <- melt(df,
           id = 1:5,
           variable.name = 'bp_position',
           value.name = 'pval'
           )

df$bp_position <- gsub("X", "", df$bp_position)
df$bp_position <- as.numeric(df$bp_position)

pdf("B1_profile.pdf")
ggplot(data = subset(df, seqLen == 100), aes(bp_position, pval)) +
  geom_point(aes(colour = dualInf), alpha = 0.6) +
  #geom_line(aes(group = seqLen+rep+dualInf)) +
  scale_y_reverse() +
  facet_grid(cols = vars(rec), rows = vars(mut)) +
  geom_hline(yintercept = 0.05, colour = 'red') +
  labs(title = "n = 100") +
  scale_color_viridis() +
  theme_bw()

ggplot(data = subset(df, seqLen == 1000), aes(bp_position, pval)) +
  geom_point(aes(colour = dualInf), alpha = 0.6) +
  #geom_line(aes(group = seqLen+rep+dualInf)) +
  scale_y_reverse() +
  facet_grid(cols = vars(rec), rows = vars(mut)) +
  geom_hline(yintercept = 0.05, colour = 'red') +
  labs(title = "n = 1000") +
  scale_color_viridis() +
  theme_bw()

ggplot(data = subset(df, seqLen == 5000), aes(bp_position, pval)) +
  geom_point(aes(colour = dualInf), alpha = 0.6) +
  #geom_line(aes(group = seqLen+rep+dualInf)) +
  scale_y_reverse() +
  facet_grid(cols = vars(rec), rows = vars(mut)) +
  geom_hline(yintercept = 0.05, colour = 'red') +
  labs(title = "n = 5000") +
  scale_color_viridis() +
  theme_bw()

dev.off()
