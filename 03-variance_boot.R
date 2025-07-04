###Fig15 bootstrap about 25tales and 12.5taels producted in linan and jinghunanlu
#load data
data_boot <- data_label_25_12.5[data_label_25_12.5$ProductionProvince %in% c("Jing Hu Nan Lu", "Gold and silver shop"), ]
locales <- c("Gold and silver shop", "Jing Hu Nan Lu")

#Initialize a bootstrap results data frame for both PC1 and PC2
boot_df <- data.frame(Locale = character(0),
                      SampleSize = numeric(0),
                      PC = character(0),
                      Range1 = numeric(0),
                      stringsAsFactors = FALSE)

set.seed(123)

#Loop over each locale and for each principal component (PC1 and PC2),this loop will cost 5 minutes
for (loc in locales) {
  for (pc in c("PC1", "PC2")) {
    # Extract values for the current locale and PC
    values <- data_boot[[pc]][data_boot$ProductionProvince == loc]
    N <- length(values)
    if (N == 0) next  # Skip if no data available for this locale
    sample_sizes <- seq(1, N, by = 1)
    
    # For each sample size, perform 500 bootstrap iterations
    for (n in sample_sizes) {
      for (iter in 1:500) {
        sample_vals <- sample(values, size = n, replace = TRUE)
        # Compute the total range: (max - min)
        boot_range <- (max(sample_vals) - min(sample_vals))
        boot_df <- rbind(boot_df, data.frame(Locale = loc,
                                             SampleSize = n,
                                             PC = pc,
                                             Range1 = boot_range,
                                             stringsAsFactors = FALSE))
      }
    }
  }
}

# Compute summary statistics (mean Range and 95% CI) for each Locale, SampleSize, and PC
library(dplyr)
summary_df <- boot_df %>%
  group_by(Locale, SampleSize, PC) %>%
  summarize(mean_Range = mean(Range1, na.rm = TRUE),
            lower = quantile(Range1, 0.025, na.rm = TRUE),
            upper = quantile(Range1, 0.975, na.rm = TRUE)) %>%
  ungroup()

# Plot the results using ggplot2, with separate facets for PC1 and PC2
library(ggplot2)
fig15 <- ggplot(summary_df, aes(x = SampleSize, y = mean_Range, color = Locale)) +
  geom_line(size = 1) +
  geom_ribbon(aes(ymin = lower, ymax = upper, fill = Locale), alpha = 0.2, color = NA) +
  facet_wrap(~PC, scales = "free_y") +
  labs(x = "Sample Size",
       y = "Mean Range",
       title = "Bootstrap Analysis: Mean Total Range vs. Sample Size (95% CI)") +
  theme_minimal()

ggsave("figures/fig15.png", fig15, width = 7, height = 5, dpi = 300)