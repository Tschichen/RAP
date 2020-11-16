#!/usr/bin/env Rscript
library("ggplot2")

options(echo=TRUE)
args <- commandArgs(trailingOnly = TRUE)
print(args)

csv <- args[1]
name <- args[2]
path <- args[3]

name <- as.character(name)

length_data <- read.csv(csv, sep="\t", header=TRUE)

length_data$length <- as.numeric(length_data$length)
length_data$ribo <- as.character(length_data$ribozyme)

plot_ribo_length <- function(data, name, path){

x <- ggplot(data, aes(x = ribo, y=length)) + theme_bw(base_size=32) + geom_boxplot() + 
labs(title=name, x='ribozyme', y='length') + ggpubr::rotate_x_text()

ggsave(path, x, width = 13, height = 10)

}

plot_ribo_length(length_data, name, path)