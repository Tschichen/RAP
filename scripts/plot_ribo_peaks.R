#!/usr/bin/env Rscript

# Filename: plot_ribo_peaks.R
# Description: Generates bar plots that represents frequence of peaks for single ribozyme types from SCRibo-seq data
# Author: Christiane Gaertner
# Version: 0.1
# Package-Requires: ggplot2


# CODE

# IMPORTS

library("ggplot2")

options(echo=TRUE)
args <- commandArgs(trailingOnly = TRUE)
print(args)

csv <- args[1]
name <- args[2]
path <- args[3]

name <- as.character(name)

if(grepl("ribos_peak_", csv, fixed=TRUE)){

count_data <- read.csv(csv, sep="\t", header=TRUE)

count_data$count <- as.numeric(count_data$count)
count_data$ribo <- as.character(count_data$hit)

plot_ribo_count <- function(data, name, path){
  
  new_path = paste(path, "_count.pdf", sep="")
	
	x <- ggplot(data, aes(x = ribo, y=count, label=count)) + theme_bw(base_size=32) + geom_bar(stat='identity') +
      labs(title=name, x='ribozyme', y='count') + geom_text(aes(label=count), position=position_dodge(width=1), hjust=-0.2, size=3) +
      coord_flip()
      
      ggsave(path, x, width = 15, height = 8)
	
	}

plot_ribo_count(count_data, name, path)}