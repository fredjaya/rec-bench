# TO DO: Add dualInf to plots 
# TO DO: Way to measure co-variance and plot informative info?
# TO DO: softcode input df
# TO DO: resolve warnings when cowplot calls custom theme from quartsFonts()
# Load dependencies
library(tidyverse)
library(data.table)
library(viridis)
library(cowplot)
library(svglite)
#library(ggfortify)

# Data prep -------------------------------------------------------------------
x <- read.csv("~/GitHub/rec-bench/out/viz/V1_santa_stats.csv")
# Remove non-variable columns
x <- x %>%
  select(-generation, -population_size)
# Melt df for plotting
x_melt <- melt(x, id = 1:4)

# Generate dfs of individual variables
meandiv <- filter(x_melt, variable == 'mean_diversity')
meanfit <- filter(x_melt, variable == 'mean_fitness')
maxfreq <- filter(x_melt, variable == 'max_frequency')
meandis <- filter(x_melt, variable == 'mean_distance')
rm(x, x_melt)

# Define font family
#quartzFonts(helvetica_thin = c("Helvetica Neue Light", "Helvetica Neue Regular",
#                               "Helvetica Neue Light Italic", 
#                               "Helvetica Neue Bold Italic"))
theme_set(theme_bw(
          #base_family = "helvetica_thin", 
          base_size = 5)
          )

# Prep plots (SANTA-SIM stats) ------------------------------------------------
# mean diversity
p1_legend <- ggplot(meandiv, aes(as.factor(seqLen), value)) + 
  geom_point(aes(col = as.factor(mut)), size = 1, alpha = 0.6) +
  facet_grid(cols = vars(rec)) +
  scale_color_viridis(discrete = T) +
  theme(axis.text.x = element_text(angle = 45, hjust = 1)) +
  labs(title = "Diversity", 
       subtitle = "Mean nucleotide sequence diversity (estimated from n = 10 random samples)", 
       x = "Sequence Number", y = element_blank(), 
       colour = "Mutation Rate")
# ^ and v are for calling the legend for a cowplot
p1 <- p1_legend + theme(legend.position = 'none')
rm(meandiv)
# mean fit
p2 <- ggplot(meanfit, aes(as.factor(seqLen), value)) + 
  geom_point(aes(col = as.factor(mut)), size = 1, alpha = 0.6) +
  facet_grid(cols = vars(rec)) +
  scale_color_viridis(discrete = T) +
  theme(axis.text.x = element_text(angle = 45, hjust = 1), legend.position = 'none') +
  labs(title = "Fitness", 
       subtitle = "Mean fitness of population",
       x = "Sequence Number", y = element_blank(), 
       colour = "Mutation Rate")
rm(meanfit)
# mean distance
p3 <- ggplot(meandis, aes(as.factor(seqLen), value)) + 
  geom_point(aes(col = as.factor(mut)), size = 1, alpha = 0.6) +
  facet_grid(cols = vars(rec)) +
  scale_color_viridis(discrete = T) +
  theme(axis.text.x = element_text(angle = 45, hjust = 1), legend.position = 'none') +
  labs(title = "Distance", 
       subtitle = "Mean sequence distance of population from initial population (ignoring mutation saturation, thus an overestimate)", 
       x = "Sequence Number", y = element_blank(), 
       colour = "Mutation Rate")
rm(meandis)
# max freq 
p4 <- ggplot(maxfreq, aes(as.factor(seqLen), value)) + 
  geom_point(aes(col = as.factor(mut)), size = 1, alpha = 0.6) +
  facet_grid(cols = vars(rec)) +
  scale_color_viridis(discrete = T) +
  theme(axis.text.x = element_text(angle = 45, hjust = 1), legend.position = "none") +
  labs(title = "Frequency", 
       subtitle = "Max frequency of the most common genome in the population", 
       x = "Sequence Number", y = element_blank(), 
       colour = "Mutation Rate")
rm(maxfreq)
# extract legend
legend <- get_legend(
  p1_legend + theme(legend.box.margin = margin(0, 0, 0, 12))
)
rm(p1_legend)

# Cowplot
pgrid <- plot_grid(p1, p2, p3, p4,
                   align = "hv",
                   #labels = c('a)', 'b)', 'c)', 'd)'),
                   labels = "AUTO",
                   nrow = 2)
rm(p1, p2, p3, p4)

# Output
out <- plot_grid(pgrid, legend, rel_widths = c(15, 1))
rm(pgrid, legend)
ggsave(filename = "V1_santa_stats.svg", plot = out, device = 'svg',
       # A4 with 25.4mm margins
       width = 184.6, height = 135.8, units = 'mm', dpi = 320)

# PCAs ------------------------------------------------------------------------
#logx <- log(x)
##pc <- prcomp(logx)
#pc <- prcomp(x)
#c1 <- autoplot(pc, data = x, colour = 'mean_fitness', size = 'mut',
#               alpha = 0.7,
#               loadings = TRUE, loadings.colour = 'blue',
#               loadings.label = TRUE, loadings.label.size = 3) +
#  scale_color_viridis() + 
#  scale_size_continuous(range = c(1,3))
#
#c2 <- autoplot(prcomp(logx), data = x, colour = 'mean_fitness', size = 'rec',
#               alpha = 0.7,
#               loadings = TRUE, loadings.colour = 'blue',
#               loadings.label = TRUE, loadings.label.size = 3) +
#  scale_color_viridis() 
#
#c3 <- autoplot(prcomp(logx), data = x, colour = 'mean_fitness', size = 'seqLen',
#               alpha = 0.7,
#               loadings = TRUE, loadings.colour = 'blue',
#               loadings.label = TRUE, loadings.label.size = 3) +
#  scale_color_viridis()
#