#!/usr/local/bin Rscript

library(dplyr)
library(ggplot2)
library(gridExtra)
library(viridis)

x <- read.csv("out/phipack_s_stats.csv")
#x <- arrange(x, seqLen, rec, mut, rep)

# Set parameters as factors for plotting 
x[,1:5] <- sapply(x[,1:5], as.factor)

# Note: calling X stat for y aesthetic via for loop and function fails as it 
# calls "X" rather than unquoted X. Plotting individually.

# NSS
p1 <- ggplot(x) +
  theme_minimal() +
  scale_y_reverse() +
  coord_cartesian(ylim = c(1, 0)) +
  ylab("p-value") +
  ggtitle("NSS") +
  geom_hline(yintercept = 0.05, col = "red", alpha = 0.5) +
  geom_point(aes(mut, NSS), size = 4, col = "#107896", alpha = 0.5, stroke = 0) +
  facet_wrap(vars(rec, seqLen), nrow = 1, strip.position = "bottom", scales = "free_x") +
  theme(panel.spacing = unit(0, "lines"),
        strip.background = element_blank(),
        strip.placement = "outside")

# MaxChi
p2 <- ggplot(x) +
  theme_minimal() +
  scale_y_reverse() +
  coord_cartesian(ylim = c(1, 0)) +
  ylab("p-value") +
  ggtitle("MaxChi") +
  geom_hline(yintercept = 0.05, col = "red", alpha = 0.5) +
  geom_point(aes(mut, MaxChi), size = 4, col = "#107896", alpha = 0.5, stroke = 0) +
  facet_wrap(vars(rec, seqLen), nrow = 1, strip.position = "bottom", scales = "free_x") +
  theme(panel.spacing = unit(0, "lines"),
        strip.background = element_blank(),
        strip.placement = "outside")

# PhiPerm
p3 <- ggplot(x) +
  theme_minimal() +
  scale_y_reverse() +
  coord_cartesian(ylim = c(1, 0)) +
  ylab("p-value") +
  ggtitle("PhiPerm") +
  geom_hline(yintercept = 0.05, col = "red", alpha = 0.5) +
  geom_point(aes(mut, PhiPerm), size = 4, col = "#107896", alpha = 0.5, stroke = 0) +
  facet_wrap(vars(rec, seqLen), nrow = 1, strip.position = "bottom", scales = "free_x") +
  theme(panel.spacing = unit(0, "lines"),
        strip.background = element_blank(),
        strip.placement = "outside")

# PhiNorm
p4 <- ggplot(x) +
  theme_minimal() +
  scale_y_reverse() +
  coord_cartesian(ylim = c(1, 0)) +
  ylab("p-value") +
  ggtitle("PhiNorm") +
  geom_hline(yintercept = 0.05, col = "red", alpha = 0.5) +
  geom_point(aes(mut, PhiNorm), size = 4, col = "#107896", alpha = 0.5, stroke = 0) +
  facet_wrap(vars(rec, seqLen), nrow = 1, strip.position = "bottom", scales = "free_x") +
  theme(panel.spacing = unit(0, "lines"),
        strip.background = element_blank(),
        strip.placement = "outside")

# Plot to pdf
pdf("out/phipack.pdf")
grid.arrange(p1, p2, p3, p4)
dev.off()

rm(x, p1, p2, p3, p4)

print("Plotting to out/phipack.pdf")
# print("Writing to 'out/phipack_s_stats_sorted.csv'...")
# write.csv(x, "out/phipack_s_stats_sorted.csv")


#try facet_wrap per thing
x$x <- "x"
ggplot(data = x, aes(x, PhiPerm)) +
  geom_point(aes(col = viridis(seqLen)), size = 5, alpha = 0.5) +
  facet_grid(rows = vars(rec), cols = vars(mut))
