####load Momocs
library(Momocs)
library(here)
library(ggplot2)
#load dataset
image_folder <- here("OpenCV--get_coordinates", "coordinates", "coordinates_txt")
lf <- list.files(image_folder, pattern = ".txt", all.files = TRUE,full.names = TRUE)
silver <- import_txt(lf)

#set figures storage directory
dir.create("figures", showWarnings = FALSE)

#load label
label <- read.table(here("Momocs--EFA","label1.txt"), header = TRUE)

#combine dataset and label
silverCom<-Out(silver, fac = label, ldk = list())
silverCom[1] %>% paper %>% draw_outline
silver %>% paper %>% draw_curve
silver %>% paper_chess %>% draw_outline -> x
x

###Fig7(1)all images standardlization
png("figures/fig7_a_stack.png", width = 800, height = 600)
silverCom %>%coo_center %>% coo_scale %>%coo_alignxax() %>% coo_slidedirection("up") %T>%print() %>% stack()
dev.off()
###Fig7(3) curve fitting, x(t) and y(t) positions along the curvilinear 
png("figures/fig7_c_oscillo.png", width = 800, height = 600)
coo_oscillo(silverCom[9], "efourier")
dev.off()
#computes Elliptical Fourier Analysis from a listof (x; y) coordinates. 
silver.f <- efourier(silverCom, nb.h=7,norm=TRUE)

###Fig7(2)Calculates harmonic power
ef <- efourier(silverCom[10], nb.h = 22, norm = TRUE)  
harmonic_power1 <- harm_pow(ef)
png("figures/fig7_b_harmonic_power.png", width = 800, height = 600)
plot(cumsum(harmonic_power1[-1]), type = "o",
     main = "Cumulative Harmonic Power ",
     ylab = "Cumulative Harmonic Power", xlab = "Harmonic Rank")
dev.off()
###Fig7(4)Explores the distribution of coefficient values.
png("figures/fig7_d_efourier_boxplot.png", width = 800, height = 600)
boxplot(silver.f, drop=1)
dev.off()
#perform PCA
silver.p <- PCA(silver.f)
class(silver.p)

###Fig8(b)the proportion of total variance explained by each PC
scree(silver.p)
scree_plot(silver.p)
p_scree <- scree_plot(silver.p)
ggsave("figures/fig8b_scree_plot.png", p_scree, width = 6, height = 4, dpi = 300)
###Fig8(a)the change in shape on the first three axes of the PCA with±2 standard deviations each
png("figures/fig8a_PC_contrib.png", width = 800, height = 600)
PCcontrib(silver.p,nax=1:3)
dev.off()
###Fig9Scatter plot of PC1 against PC2 for all bullions
pc1_range <- range(silver.p$x[, 1])
pc2_range <- range(silver.p$x[, 2])
png("figures/fig9_PC1_PC2_scatter.png", width = 800, height = 600)
plot(silver.p, axes = c(1, 2), xlim = pc1_range, ylim = pc2_range, cex = 1.1)
dev.off()

