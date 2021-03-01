count_data <- read.csv("~/Desktop/RAP/3prime_other_peaks_csv/others_peak_AtRNL2_peak_sorted_dedup.bed.gz_intersect_othe.csv", sep="\t", header=TRUE)


count_data$count <- as.numeric(count_data$count)
count_data$ribo <- as.character(count_data$hit)

plot_ribo_count <- function(data, path){
  
  x <- ggplot(data, aes(x = ribo, y=count, label=count)) + theme_bw(base_size=32) + geom_bar(stat='identity') +
    labs(x='hit name', y='count') + geom_text(aes(label=count), position=position_dodge(width=1), hjust=-0.2, size=3) +
    coord_flip()
  
  ggsave("~/Desktop/RAP/test_out/3prime_AtRNL2_other_peaks.pdf", x, width = 15, height = 8)
  
  print(x)
  
}

plot_ribo_count(count_data)