#!/usr/local/bin Rscript

library(dplyr)
library(ggplot2)
library(gridExtra)
library(viridis)

#setwd("~/GitHub/rec-bench/")
x <- read.csv("out/phipack_s_stats.csv")
#x <- arrange(x, seqLen, rec, mut, rep)

# Set parameters as factors for plotting 
x[,1:5] <- sapply(x[,1:5], as.factor)

#try facet_wrap per thing
x$x <- "x" # add arbitrary column

p1 <- ggplot(data = x, aes(x, NSS)) +
  scale_y_reverse() +
  geom_jitter(aes(col = seqLen), size = 5, alpha = 0.5) +
  facet_grid(rows = vars(rec), cols = vars(mut))

p2 <- ggplot(data = x, aes(x, MaxChi)) +
  scale_y_reverse() +
  geom_jitter(aes(col = seqLen), size = 5, alpha = 0.5) +
  facet_grid(rows = vars(rec), cols = vars(mut))

p3 <- ggplot(data = x, aes(x, PhiPerm)) +
  scale_y_reverse() +
  geom_jitter(aes(col = seqLen), size = 5, alpha = 0.5) +
  facet_grid(rows = vars(rec), cols = vars(mut))

p4 <- ggplot(data = x, aes(x, PhiNorm)) +
  scale_y_reverse() +
  geom_jitter(aes(col = seqLen), size = 5, alpha = 0.5) +
  facet_grid(rows = vars(rec), cols = vars(mut))

# Plot to pdf
pdf("out/phipack.pdf")
grid.arrange(p1, p2, p3, p4)
dev.off()

rm(x, p1, p2, p3, p4)

print("Plotting to out/phipack.pdf")
# print("Writing to 'out/phipack_s_stats_sorted.csv'...")
# write.csv(x, "out/phipack_s_stats_sorted.csv")
