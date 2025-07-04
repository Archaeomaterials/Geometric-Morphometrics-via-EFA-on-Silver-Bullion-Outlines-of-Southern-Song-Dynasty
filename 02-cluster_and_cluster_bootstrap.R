## Fig10a-b: Bootstrap Stability Analysis of Clustering
library(fpc)       
library(cluster)   
library(ggplot2)
library(dplyr)
library(here)
library(ggforce)
library(RColorBrewer)
library(viridis)

# data loader
pc_data <- as.data.frame(silver.p$x[, 1:2])  
colnames(pc_data) <- c("PC1", "PC2")  
pc_data$Type <- silver.p$type

# data standardation
normalized_data <- as.data.frame(scale(pc_data[, c("PC1", "PC2")]))
df <- normalized_data
k_values <- 2:6

# configuration
boot_sil_list <- list()
avg_sil <- numeric(length(k_values))
boot_stability <- numeric(length(k_values))

set.seed(123)  

for (i in seq_along(k_values)) {
  k <- k_values[i]
  cb <- clusterboot(df, clustermethod = kmeansCBI, krange = k, B = 100, seed = 123)
  partition <- cb$result$partition
  sil <- silhouette(partition, dist(df))
  boot_sil_list[[as.character(k)]] <- sil[, "sil_width"]
  avg_sil[i] <- mean(sil[, "sil_width"])
  boot_stability[i] <- mean(cb$bootmean)
  cat("For k =", k, "average silhouette width =", round(avg_sil[i], 3),
      "and average bootmean =", round(boot_stability[i], 3), "\n")
}

optimal_k <- k_values[which.max(avg_sil)]
cat("\nOptimal number of clusters:", optimal_k, "\n")

# Fig10asilhouette_boxplot
sil_df <- bind_rows(lapply(names(boot_sil_list), function(k) {
  data.frame(k = factor(k, levels = as.character(k_values)),
             sil_width = boot_sil_list[[k]])
}))

fig10a <- ggplot(sil_df, aes(x = k, y = sil_width, fill=k)) +
  geom_boxplot() +
  stat_boxplot(geom = "errorbar", linetype="dashed", width = 0.4) +
  labs(
    title = "Bootstrapped Silhouette Widths",
    subtitle = "Boxplots for different numbers of clusters",
    x = "Number of Clusters (k)",
    y = "Silhouette Width"
  ) +
  theme_minimal() +
  theme(legend.position = "none")

ggsave("figures/fig10a_silhouette_boxplot.png", fig10a, width = 7, height = 5, dpi = 300)


# Fig10bsummary_metrics
stab_df <- data.frame(k = k_values,
                      avg_silhouette = avg_sil,
                      avg_bootmean = boot_stability)

fig10b <- ggplot(stab_df, aes(x = k)) +
  geom_line(aes(y = avg_silhouette, color = "Avg Silhouette"), size = 1.2) +
  geom_point(aes(y = avg_silhouette, color = "Avg Silhouette"), size = 3) +
  geom_line(aes(y = avg_bootmean, color = "Avg Jaccard similarity"), size = 1.2, linetype = "dashed") +
  geom_point(aes(y = avg_bootmean, color = "Avg Jaccard similarity"), size = 3) +
  labs(title = "Summary Metrics vs. Number of Clusters",
       x = "Number of Clusters (k)",
       y = "Metric Value") +
  scale_color_manual(name = "Metric", values = c("Avg Silhouette" = "blue",
                                                 "Avg Jaccard similarity" = "red")) +
  theme_minimal()

ggsave("figures/fig10b_summary_metrics.png", fig10b, width = 7, height = 5, dpi = 300)


## Fig10c: K-meanscluster_weights

kmeans_res <- kmeans(silver.p$x[, 1:2], centers = 3)
data_label <- pc_data
data_label$Cluster <- as.factor(kmeans_res$cluster)
label2 <- read.table(here("Momocs--EFA", "label2.txt"), header = TRUE, sep = "\t")
data_label$BullionWeights <- label2$BullionWeights
data_label$ProductionLocales <- label2$ProductionLocales
data_label$ProductionProvince <- label2$ProductionProvince
data_label$ProductionCategory <- ifelse(data_label$ProductionLocales == "Gate tax", "Gate tax", "Other")

cluster_counts <- table(data_label$Cluster, data_label$BullionWeights)
cluster_counts_df <- as.data.frame(cluster_counts)
colnames(cluster_counts_df) <- c("Cluster", "Weight", "Count")

fig10c <- ggplot(cluster_counts_df, aes(x = Cluster, y = Count, fill = Weight)) +
  geom_bar(stat = "identity", position = "dodge") +
  labs(
    title = "Distribution of Silver Bullion Weights by Cluster",
    x = "Cluster",
    y = "Count of Bullions"
  ) +
  scale_fill_brewer(palette = "Set2") +
  theme_minimal()

ggsave("figures/fig10c_cluster_weights.png", fig10c, width = 7, height = 5, dpi = 300)


## Fig11: PCA_category_kmeans.
data_label$BullionWeights <- as.factor(data_label$BullionWeights)
shape_palette <- c(16, 17, 15, 18, 8)
color_palette <- c("Gate tax" = "#D55E00", "Other" = "#56B4E9")

fig11 <- ggplot(data_label, 
                aes(x = PC1, y = PC2, 
                    shape = BullionWeights, 
                    color = ProductionCategory)) +
  geom_point(size = 3, alpha = 0.8, stroke = 0.5) +  
  scale_shape_manual(values = shape_palette) +     
  scale_color_manual(values = color_palette) +     
  stat_ellipse(aes(group = Cluster),
               type = "norm", 
               linetype = "dashed", 
               color = "black", 
               size = 0.8, 
               alpha = 0.4) +
  labs(
    x = "PC1",
    y = "PC2",
    title = "PCA of all Silver Bullions",
    shape = "BullionWeights"
  ) +
  theme_minimal(base_size = 12) +
  theme(
    legend.position = "bottom",
    legend.box = "horizontal",  
    plot.title = element_text(hjust = 0.5, face = "bold"),
    panel.grid.minor = element_blank()
  ) +
  guides(
    shape = guide_legend(override.aes = list(size = 3)),
    color = guide_legend(title = NULL)  
  )

ggsave("figures/fig11_PCA_category_kmeans.png", fig11, width = 7, height = 5, dpi = 300)
###Fig13 Scatter plot of variations in 50 taels bullion with different production locales
library(ggplot2)
library(dplyr)

#data loader
data_label50 <- data_label %>% 
  filter(BullionWeights == "50 taels") %>%
  mutate(
    ProductionLocales = factor(ProductionLocales)
  )

#define parameters
point_size <- 4  
alpha_val <- 0.8  
stroke_width <- 1.5  
legend_font_size <- 14  
axis_title_size <- 16  
plot_title_size <- 18  

#plot
fig13 <- ggplot(data_label50, 
                aes(x = PC1, y = PC2, 
                    shape = ProductionLocales)) +
  geom_point(size = point_size, color = "#0072B2", alpha = alpha_val, stroke = stroke_width) + 
  scale_shape_manual(values = 1:length(unique(data_label50$ProductionLocales))) + 
  labs(x = "PC1", y = "PC2", 
       title = "50 Taels Bullion by Production Locales",
       shape = "Production Locale") +
  theme_minimal(base_size = 14) +
  theme(
    legend.position = "right",
    legend.text = element_text(size = legend_font_size),
    legend.key = element_blank(),
    axis.title = element_text(size = axis_title_size),
    plot.title = element_text(hjust = 0.5, size = plot_title_size, face = "bold")
  )

ggsave("figures/fig13_50taels_locales.png", fig13, width = 10, height = 6, dpi = 300)

###Fig14 Comparison of 25 taels and 12.5 taels bullions produced by gold and silver shops and local government.
library(ggplot2)
library(dplyr)
library(scales)
data_label_25_12.5 <- data_label %>% 
  filter(BullionWeights %in% c("25 taels", "12.5 taels")) %>%
  mutate(
    ProductionLocales = factor(ProductionLocales),
    BullionWeights = factor(BullionWeights, levels = c("25 taels", "12.5 taels")),
    Cluster = Cluster  
  )
color_palette_production <- hue_pal()(length(unique(data_label_25_12.5$ProductionLocales)))

#define parameters
point_size <- 4            
alpha_val <- 0.8           
stroke_width <- 1.5        
legend_font_size <- 14  
axis_title_size <- 16  
plot_title_size <- 18  
color_palette <- c("25 taels" = "#0072B2", "12.5 taels" = "#D55E00")
hollow_shapes <- c(0,1,2,5,6,7,8,9,10,11,12,13,14)
fig14_left <- ggplot(data_label_25_12.5, 
                     aes(x = PC1, y = PC2,
                         shape = BullionWeights, color = BullionWeights)) +  
  geom_point(size = point_size, alpha = alpha_val, stroke = stroke_width) +
  
  stat_ellipse(data = data_label_25_12.5 %>% filter(Cluster %in% c(1, 3)),  
               aes(x = PC1, y = PC2, group = Cluster), 
               linetype = "dashed", 
               color = "black", 
               size = 0.8, 
               alpha = 0.4,
               inherit.aes = FALSE) +
  
  scale_shape_manual(values = c(2, 1)) +  
  labs(x = "PC1", y = "PC2",
       title = "Bullion Weights with Cluster 1 & 3",
       shape = "Bullion Weight") +
  scale_color_manual(values = color_palette) +  
  theme_minimal(base_size = 14) +
  theme(
    legend.position = "right",
    legend.text = element_text(size = legend_font_size),
    axis.title = element_text(size = axis_title_size),
    plot.title = element_text(hjust = 0.5, size = plot_title_size, face = "bold")
  ) +
  guides(color = "none")  

ggsave("figures/fig14_left_weights_cluster1_3.png", fig14_left, width = 7, height = 5, dpi = 300)

fig14_right <- ggplot(data_label_25_12.5,
                      aes(x = PC1, y = PC2,
                          shape = ProductionLocales, color = ProductionLocales)) +  
  geom_point(size = point_size, alpha = alpha_val, stroke = stroke_width) +
  
  stat_ellipse(data = data_label_25_12.5 %>% filter(Cluster %in% c(1, 3)),
               aes(x = PC1, y = PC2, group = Cluster),
               linetype = "dashed", 
               color = "black", 
               size = 0.8, 
               alpha = 0.4,
               inherit.aes = FALSE) +
  
  scale_shape_manual(values = hollow_shapes) +
  labs(x = "PC1", y = "PC2",
       title = "Production Locales with Cluster 1 & 3",
       shape = "Production Locale") +  
  scale_color_manual(values = color_palette_production) +  
  theme_minimal(base_size = 14) +
  theme(
    legend.position = "right",
    legend.text = element_text(size = legend_font_size),
    axis.title = element_text(size = axis_title_size),
    plot.title = element_text(hjust = 0.5, size = plot_title_size, face = "bold")
  ) +
  guides(color = "none") +  
  guides(shape = guide_legend(ncol = 1))

ggsave("figures/fig14_right_locales_cluster1_3.png", fig14_right, width = 12, height = 7, dpi = 300)
