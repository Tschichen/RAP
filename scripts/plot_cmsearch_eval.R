#!/usr/bin/env Rscript
library("ggplot2")

options(echo=TRUE)
args <- commandArgs(trailingOnly = TRUE)
print(args)

csv <- args[1]
name <- args[2]
path <- args[3]

name <- as.character(name)

eval_data <- read.csv(csv, sep="\t", header=TRUE)

eval_data$eval <- as.numeric(eval_data$eval)
eval_data$ribo <- as.character(eval_data$ribozyme)

plot_ribo_eval <- function(data, name, path){
	
	x <- ggplot(data, aes(x = ribo, y=eval)) + theme_bw(base_size=32) + geom_boxplot() +
      labs(title=name, x='ribozyme', y='e-value') + ggpubr::rotate_x_text()
      
      ggsave(path, x, width = 13, height = 10)
	
	}

plot_ribo_eval(eval_data, name, path)