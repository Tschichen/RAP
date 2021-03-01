library(ggplot2)

cluster_data <- read.csv('~/Desktop/RAP/test_out/Sig_1_peak_sorted_unique_dedup.bed.gz_intersect_cluster.bed_cluster_to_height.csv', header=TRUE, sep="\t")

cluster_data$cluster <- as.character(cluster_data$cluster)
cluster_data$reads <- as.numeric(cluster_data$reads)
cluster_data$height <- as.numeric(cluster_data$height)

plot_cluster <- function(cluster_data){
  plot_x <- ggplot(cluster_data, aes(reads, height)) + geom_point() +
    labs(x="# of seq. in cluster", y="height of peak") + theme_bw(base_size=32)
    #+ xlim(0, 500)
  
  
  ggsave('~/Desktop/RAP/plots_cluster_height/Sig_1_unique_cluster_to_height.pdf', plot_x, height = 8, width = 12)

  print(plot_x)
  
}

plot_cluster(cluster_data)