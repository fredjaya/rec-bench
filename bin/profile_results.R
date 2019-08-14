#!/usr/bin/env Rscript

library(data.table)
library(ggplot2)
library(viridis)
library(dplyr)

#setwd("GitHub/rec-bench/")

# Read Profile.csv
df <- read.csv("out/profile_s_stats.csv", header = T, stringsAsFactors = T)
df <- melt(df,
           id = 1:5,
           variable.name = 'bp_position',
           value.name = 'pval'
           )

df$bp_position <- gsub("X", "", df$bp_position)
df$bp_position <- as.numeric(df$bp_position)

pdf("out/profile.pdf")
ggplot(data = subset(df, seqLen == 100), aes(bp_position, pval)) +
  geom_point(alpha = 0.9, size = 2, shape = 18) +
  geom_line(aes(group = rep+seqLen)) +
  scale_y_reverse() +
  facet_grid(cols = vars(rec), rows = vars(mut)) +
  geom_hline(yintercept = 0.05, colour = 'red') +
  labs(title = "n = 100")

ggplot(data = subset(df, seqLen == 1000), aes(bp_position, pval)) +
  geom_point(alpha = 0.9, size = 2, shape = 18) +
  geom_line(aes(group = rep+seqLen)) +
  scale_y_reverse() +
  facet_grid(cols = vars(rec), rows = vars(mut)) +
  geom_hline(yintercept = 0.05, colour = 'red') +
  labs(title = "n = 1000")

ggplot(data = subset(df, seqLen == 2500), aes(bp_position, pval)) +
  geom_point(alpha = 0.9, size = 2, shape = 18) +
  geom_line(aes(group = rep+seqLen)) +
  scale_y_reverse() +
  facet_grid(cols = vars(rec), rows = vars(mut)) +
  geom_hline(yintercept = 0.05, colour = 'red') +
  labs(title = "n = 2500")

ggplot(data = subset(df, seqLen == 5000), aes(bp_position, pval)) +
  geom_point(alpha = 0.9, size = 2, shape = 18) +
  geom_line(aes(group = rep+seqLen)) +
  scale_y_reverse() +
  facet_grid(cols = vars(rec), rows = vars(mut)) +
  geom_hline(yintercept = 0.05, colour = 'red') +
  labs(title = "n = 5000")

ggplot(data = subset(df, seqLen == 10000), aes(bp_position, pval)) +
  geom_point(alpha = 0.9, size = 2, shape = 18) +
  geom_line(aes(group = rep+seqLen)) +
  scale_y_reverse() +
  facet_grid(cols = vars(rec), rows = vars(mut)) +
  geom_hline(yintercept = 0.05, colour = 'red') +
  labs(title = "n = 10000")

dev.off()
#fail
##### 
seqnum <- unique(df$seqLen)
pdf("profile_test.pdf", onefile = F)
par(mfrow = c(5,1))
for (i in seqnum) {
p <- ggplot(df, aes(bp_position, pval)) +
  geom_point(data = subset(df, seqLen == i), aes(colour = as.factor(seqLen)), alpha = 0.7, size = 2) +
  scale_y_reverse() +
  scale_colour_viridis(discrete = T) +
  facet_grid(cols = vars(rec), rows = vars(mut)) +
  geom_hline(yintercept = 0.05, colour = 'red')
p
}
dev.off()
