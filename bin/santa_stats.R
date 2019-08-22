library(data.table)
library(ggplot2)
library(dplyr)
library(viridis)
library(gridExtra)
setwd("~/GitHub/rec-bench/")

x <- read.csv("out/santa_stats.csv")
# Remove columns (popsize, generation, dualInf)
x <- x[, -c(4, 6, 7)]

# Melt df for plotting
x2 <- melt(x, id = 1:4)

# Generate dfs of individual variables
meandiv <- filter(x2, variable == 'mean_diversity')
maxdiv <- filter(x2, variable == 'max_diversity')
minfit <- filter(x2, variable == 'min_fitness')
meanfit <- filter(x2, variable == 'mean_fitness')
maxfit <- filter(x2, variable == 'max_fitness')
maxfreq <- filter(x2, variable == 'max_frequency')
meandis <- filter(x2, variable == 'mean_distance')

# mean diversity
p1 <- ggplot(meandiv, aes(as.factor(seqLen), value)) + 
  labs(title = "mean_diversity") +
  geom_point(aes(col = as.factor(mut)), size = 4, alpha = 0.8) +
  facet_grid(cols = vars(rec)) +
  scale_color_viridis(discrete = T) +
  theme(legend.position = 'none')

# mean fit
p2 <- ggplot(meanfit, aes(as.factor(seqLen), value)) + 
  labs(title = "mean_fit") +
  geom_point(aes(col = as.factor(mut)), size = 4, alpha = 0.8) +
  facet_grid(cols = vars(rec)) +
  scale_color_viridis(discrete = T) +
  theme(legend.position = 'none')
  
# mean distance
p3 <- ggplot(meandis, aes(as.factor(seqLen), value)) + 
  labs(title = "mean_distance") +
  geom_point(aes(col = as.factor(mut)), size = 4, alpha = 0.8) +
  facet_grid(cols = vars(rec)) +
  scale_color_viridis(discrete = T) +
  theme(legend.position = 'none')

# max freq 
p4 <- ggplot(maxfreq, aes(as.factor(seqLen), value)) + 
  labs(title = "max_frequency") +
  geom_point(aes(col = as.factor(mut)), size = 4, alpha = 0.8) +
  facet_grid(cols = vars(rec)) +
  scale_color_viridis(discrete = T) +
  theme(legend.position = 'none')

pdf("out/santa_stats.pdf")
grid.arrange(p1, p2, p3, p4)
dev.off()

# PCA to explore variation in sim data, based on santa stats output
logx <- log(x[,5:ncol(x)])
pc <- prcomp(logx)

c4 <- plot(pc) # PC1 explains pretty much all the variation
c1 <- autoplot(prcomp(logx), data = x, colour = 'mean_fitness', size = 'mut',
         alpha = 0.7,
         loadings = TRUE, loadings.colour = 'blue',
         loadings.label = TRUE, loadings.label.size = 3) +
  scale_color_viridis() +
  labs(title = )

c2 <- autoplot(prcomp(logx), data = x, colour = 'mean_fitness', size = 'rec',
               alpha = 0.7,
               loadings = TRUE, loadings.colour = 'blue',
               loadings.label = TRUE, loadings.label.size = 3) +
  scale_color_viridis()

c3 <- autoplot(prcomp(logx), data = x, colour = 'mean_fitness', size = 'seqLen',
         alpha = 0.7,
         loadings = TRUE, loadings.colour = 'blue',
         loadings.label = TRUE, loadings.label.size = 3) +
  scale_color_viridis()

pdf("out/santa_pca.pdf")
grid.arrange(c1, c2, c3, nrow = 2)
dev.off()

# Check correlation of mut Rate with fitness?
lr <- lm(mean_fitness ~ mut, data = log(x))
summary(lr)

ggplot(log(x), aes(x = mut, y = mean_fitness)) + 
  geom_point(size = 4, alpha = 0.7) +
  stat_smooth(method = "lm", col = "red") + 
  scale_colour_viridis()

# no logging
halflog <- cbind(x[,1:4],logx)

ggplot(halflog, aes(x = mut, y = mean_fitness)) + 
  geom_point(size = 4, alpha = 0.7) +
  stat_smooth(method = "lm", col = "red") + 
  scale_colour_viridis()

# Check for skew in data
ggplot(x, aes(mean_fitness)) +
  geom_histogram(bins = 50) # looks bimodal?
