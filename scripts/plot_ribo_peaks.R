#!/usr/bin/env Rscript
# Generate bar plot that represents frequence of peaks for single ribozyme types out of Ribozeq experiments

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

if(grepl("ribo_peaks_quantify_count", csv, fixed=TRUE)){
  
  length_height <- read.csv(csv, sep="\t", header=TRUE)
  
  length_height$length <- as.numeric(length_height$length)
  length_height$height <- as.numeric(length_height$height)
  length_height$ribo <- as.character(length_height$hit)
  length_height$ribo <- as.factor(length_height$ribo)
  
  
  plot_ribo_length_height <- function(data, name, path){
  new_path = paste(path, "_length_height.pdf", sep="")
  
  x <- ggplot(data, aes(x = length, y=height)) + theme_bw(base_size=32) + geom_violin() + geom_point() +
    labs(title=name, x='length of peaks', y='peak height') + facet_wrap(~ ribo)
  
  ggsave(new_path, x, width = 18, height = 8)}
  
  plot_ribo_length_height(length_height, name, path)
  
}