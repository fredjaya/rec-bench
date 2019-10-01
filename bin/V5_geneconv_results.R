library(ggplot2)
library(viridis)
library(dplyr)

setwd("~/GitHub/rec-bench/")
x <- read.csv("out/geneconv_s_stats_long.csv")

# Plot all start and end breakpoints
x100 <- filter(x, seqLen == 100)
x1000 <- filter(x, seqLen == 1000)
x2500 <- filter(x, seqLen == 2500)
x5000 <- filter(x, seqLen == 5000)

ggplot(x100) +
  geom_histogram(aes(aligned_start), bins = 168, fill = "#440154FF", alpha = 0.9) +
  geom_histogram(aes(aligned_end), bins = 168, fill = "#FDE725FF", alpha = 0.9) +
  facet_grid(rows = vars(mut),
             cols = vars(rec)) +
  labs(title = 'n100')

ggplot(x1000) +
  geom_histogram(aes(aligned_start), bins = 168, fill = "#440154FF", alpha = 0.9) +
  geom_histogram(aes(aligned_end), bins = 168, fill = "#FDE725FF", alpha = 0.9) +
  facet_grid(rows = vars(mut),
             cols = vars(rec)) +
  labs(title = 'n1000')

ggplot(x2500) +
  geom_histogram(aes(aligned_start), bins = 168, fill = "#440154FF", alpha = 0.9) +
  geom_histogram(aes(aligned_end), bins = 168, fill = "#FDE725FF", alpha = 0.9) +
  facet_grid(rows = vars(mut),
             cols = vars(rec)) +
  labs(title = 'n2500')

ggplot(x5000) +
  geom_histogram(aes(aligned_start), bins = 168, fill = "#440154FF", alpha = 0.9) +
  geom_histogram(aes(aligned_end), bins = 168, fill = "#FDE725FF", alpha = 0.9) +
  facet_grid(rows = vars(mut),
             cols = vars(rec)) +
  labs(title = 'n5000')
