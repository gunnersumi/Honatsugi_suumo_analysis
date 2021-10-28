data <- read.csv('data_frame.csv', header = TRUE)    # ƒf[ƒ^‚Ì“Ç‚İ‚İ
attach(data)
sapply(data, class)
data$’z”N” <- as.integer(data$’z”N”)
data_0 <- data[—§’n•Ï” == 0,]    # —§’n‚Å•ª‚¯‚é
data_1 <- data[—§’n•Ï” == 1,]

hist(data_1$’À—¿, main = "–{Œú–Ø‚Ì’À—¿")    # ƒqƒXƒgƒOƒ‰ƒ€ì¬
hist(data_0$’À—¿, main = "‘å˜aA’†‰›—ÑŠÔ‚Ì’À—¿")


IQR_0 <- IQR(data_0$’À—¿)    # ŠO‚ê’lˆ—
IQR_1 <- IQR(data_1$’À—¿)
third_0 <- fivenum(data_0$’À—¿)[4]
third_1 <- fivenum(data_1$’À—¿)[4]
outliers_0 <- third_0 + IQR_0 * 1.5
outliers_1 <- third_1 + IQR_1 * 1.5
data_0 <- data_0[data_0$’À—¿ <= outliers_0,]
data_1 <- data_1[data_1$’À—¿ <= outliers_1,]

hist(data_0$’À—¿, main = "‘å˜a‚Ì’À—¿", xlim = c(0, 120000))    # ŠO‚ê’lˆ—‚ğ‚µ‚½ƒqƒXƒgƒOƒ‰ƒ€ì¬
hist(data_1$’À—¿, main = "–{Œú–Ø‚Ì’À—¿", breaks = c(0,10000,20000,30000,40000,50000,60000,70000,80000,90000,100000,110000,120000),  xlim = c(0, 120000))
nrow(data_0)
nrow(data_1)


mean(data_0$’À—¿)    #@’À—¿‚É‚¨‚¯‚éŒŸ’è
mean(data_1$’À—¿)
var.test(data_0$’À—¿, data_1$’À—¿)
t.test(data_1$’À—¿, data_0$’À—¿, var.equal = F)


hist(data_1$ê—L–ÊÏ, main = "‘å˜a‚Ìê—L–ÊÏ", xlim = c(0, 120))    # ‚»‚Ì‘¼‚ÌƒqƒXƒgƒOƒ‰ƒ€
hist(data_1$ê—L–ÊÏ, main = "–{Œú–Ø‚Ìê—L–ÊÏ", xlim = c(0, 120))
hist(data_0$ŠK, main = "‘å˜a‚ÌŠK”")
hist(data_1$ŠK, main = "–{Œú–Ø‚ÌŠK”")
hist(data_1$’z”N”, main = "–{Œú–Ø‚Ì’z”N”")
hist(data_0$’z”N”, main = "‘å˜a‚Ì’z”N”")

install.packages("exactRankTests", dependencies = TRUE)    # ’z”N”Aê—L–ÊÏ‚É‚¨‚¯‚éŒŸ’è‚ÌÀ{
library(exactRankTests)
median(data_0$ê—L–ÊÏ)
median(data_1$ê—L–ÊÏ)
median(data_0$’z”N”, na.rm = TRUE)    # ’z”N”‚É99”NˆÈã‚Æ‚¢‚¤ŠO‚ê’l‚ğ–³‹‚·‚é‚½‚ß‚É na.rm ‚ğg—p
median(data_1$’z”N”,  na.rm = TRUE)
wilcox.exact(x = data_0$’z”N”, y = data_1$’z”N”, paired = F)
wilcox.exact(x = data_0$ê—L–ÊÏ, y = data_1$ê—L–ÊÏ, paired = F)