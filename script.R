data <- read.csv('data_frame.csv', header = TRUE)    # データの読み込み
attach(data)
sapply(data, class)
data$築年数 <- as.integer(data$築年数)
data_0 <- data[立地変数 == 0,]    # 立地で分ける
data_1 <- data[立地変数 == 1,]

hist(data_1$賃料, main = "本厚木の賃料")    # ヒストグラム作成
hist(data_0$賃料, main = "大和、中央林間の賃料")


IQR_0 <- IQR(data_0$賃料)    # 外れ値処理
IQR_1 <- IQR(data_1$賃料)
third_0 <- fivenum(data_0$賃料)[4]
third_1 <- fivenum(data_1$賃料)[4]
outliers_0 <- third_0 + IQR_0 * 1.5
outliers_1 <- third_1 + IQR_1 * 1.5
data_0 <- data_0[data_0$賃料 <= outliers_0,]
data_1 <- data_1[data_1$賃料 <= outliers_1,]

hist(data_0$賃料, main = "大和の賃料", xlim = c(0, 120000))    # 外れ値処理をしたヒストグラム作成
hist(data_1$賃料, main = "本厚木の賃料", breaks = c(0,10000,20000,30000,40000,50000,60000,70000,80000,90000,100000,110000,120000),  xlim = c(0, 120000))
nrow(data_0)
nrow(data_1)


mean(data_0$賃料)    #　賃料における検定
mean(data_1$賃料)
var.test(data_0$賃料, data_1$賃料)
t.test(data_1$賃料, data_0$賃料, var.equal = F)


hist(data_1$専有面積, main = "大和の専有面積", xlim = c(0, 120))    # その他のヒストグラム
hist(data_1$専有面積, main = "本厚木の専有面積", xlim = c(0, 120))
hist(data_0$階, main = "大和の階数")
hist(data_1$階, main = "本厚木の階数")
hist(data_1$築年数, main = "本厚木の築年数")
hist(data_0$築年数, main = "大和の築年数")

install.packages("exactRankTests", dependencies = TRUE)    # 築年数、専有面積における検定の実施
library(exactRankTests)
median(data_0$専有面積)
median(data_1$専有面積)
median(data_0$築年数, na.rm = TRUE)    # 築年数に99年以上という外れ値を無視するために na.rm を使用
median(data_1$築年数,  na.rm = TRUE)
wilcox.exact(x = data_0$築年数, y = data_1$築年数, paired = F)
wilcox.exact(x = data_0$専有面積, y = data_1$専有面積, paired = F)