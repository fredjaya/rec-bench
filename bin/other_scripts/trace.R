# Replace tabs with commas in *.tsv:
  # gsed -i s/t/QQQ/g *
  # gsed -i "s/\t/,/g" *
  # gsed -i "s/QQQ/t/g" *

library(ggplot2)
library(tidyr)
library(data.table)
library(dplyr)
library(lubridate)
library(viridis)

#setwd("~/GitHub/rec-bench/out/trace/")

# List of all file names
fileNames <- list.files(pattern = "*.csv")
print(paste(nrow(as.matrix(fileNames)), "files total."))

# Initialise blank dataframe
x <- data.frame(matrix(ncol = 14, nrow = 0))
colnames(x) <- c("task_id", "hash", "native_id", "name", "status", "exit", 
                "submit", "duration", "realtime", "perc_cpu", "peak_rss", 
                "peak_vmem", "rchar", "wchar"
                )

for (i in fileNames) {
  # Read in all files and concatenate to one dataframe
  print(paste("Reading ", i, "...", sep = ''))
  temp <- read.csv(i)
  x <- rbind(x, temp)
}
rm(fileNames, temp, i)

# Parse parameters - separate into individual columns
x <- x %>%
  separate(col = name, into = c('name', 'params'), sep = ' \\(')
x$params <- gsub('[a-z]', '', x$params)
x$params <- gsub('.)', '', x$params) 
x$params <- gsub('^_', '', x$params)
x <- x %>%
  separate(col = params, into = c('mut', 'rc', 'seq_n', 'dual_inf', 'rep'),
           sep = '_', remove = T)

#write.csv(x, "../trace_all.csv")

# The following lines plots the times, but times are incorrectly parsed 
# i.e. 3h 2m 10s is ok, but 3h 10s == 3m 10s
#######

# Subset rows for profile runs
profile <- filter(x, name == 'profile_s')
profile$seq_n <- as.numeric(profile$seq_n)

profile2 <- profile
for (i in 13:14) {
  profile2[,i] <- as.character(profile2[,i])
  profile2[,i] <- parse_date_time(profile2[,i], c("S", "MS", "HMS", "HS"))
}
rm(i)

# Plot
ggplot(profile, aes(seq_n, realtime)) +
  geom_point(aes(colour = mut, shape = rc), size = 4, alpha = 0.5)
