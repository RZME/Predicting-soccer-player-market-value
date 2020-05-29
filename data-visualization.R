dataset <- read.csv2('C:/Users/frank/OneDrive/Bureaublad/Predicting soccer-player market value/dataset.csv', sep = ",", stringsAsFactors = FALSE)
library(ggplot2)
dev.off()

dataset <- dataset[dataset$club_league != 'relegation ligue 1',]
dataset <- dataset[dataset$club_league != 'serie b',]

dataset$market_value <- as.numeric(dataset$market_value)
dataset$transfer_fee <- as.numeric(dataset$transfer_fee)
dataset$player_rating <- as.numeric(dataset$player_rating)
dataset$player_potential <- as.numeric(dataset$player_potential)

mynamestheme <- theme(plot.title = element_text(family = "Helvetica", face = "bold", size = (15)), 
                      legend.title = element_text(colour = "azure4",  face = "bold", size = (15), family = "Helvetica"), 
                      legend.text = element_text(face = "italic", colour="azure3", size = (15), family = "Helvetica"), 
                      axis.title = element_text(family = "Helvetica", face = "bold", size = (16), colour = "azure4"),
                      axis.text = element_text(family = "Courier", colour = "azure3", size = (15)))

p1 <- ggplot(dataset, aes(x = club_league, y=market_value))
p1 <- p1 + geom_boxplot(method = "auto", na.rm = TRUE, aes(group = club_league, col = club_league))
p1 <- p1 + labs(colour ='League') 
p1 <- p1 + labs(y="Market value", x = "League")
print(p1)
dev.off()
ggsave("data-visualization/p1.pdf", scale = 1.7, dpi=600)


p2 <- ggplot(dataset, aes(x=player_position_category, y=market_value))
p2 <- p2 + geom_boxplot(method = "auto", na.rm = TRUE, 
                        aes(col = player_position_category))
p2 <- p2 + labs(colour ='Player position') 
p2 <- p2 + labs(y="Market value (million £)", x = "Player position")
print(p2 + mynamestheme)
ggsave("data-visualization/p2.pdf")


p3 <- ggplot(dataset, aes(x = player_rating, y=transfer_fee))
p3 <- p3 + labs(y="Transfer fee (million £)", x = "FIFA Overall rating", fill = "player position category")
p3 <- p3 + scale_x_continuous(breaks=seq(40, 100, by = 5))
p3 <- p3 + geom_point(method = "auto",  na.rm = TRUE, aes(group = player_age, col = player_age))
p3 <- p3 + labs(colour ='Player age') 
p3 <- p3 + geom_smooth(method = 'auto')
print(p3 + mynamestheme)
ggsave("data-visualization/p3.pdf")


p4 <- ggplot(dataset, aes(x = player_rating, y=market_value))
p4 <- p4 + labs(y="Market value (million £)", x = "FIFA Overall rating", fill = "player position category")
p4 <- p4 + scale_x_continuous(breaks=seq(40, 100, by = 5))
p4 <- p4 + geom_point(method = "auto",  na.rm = TRUE, aes(group = player_age, col = player_age))
p4 <- p4 + labs(colour ='Player age') 
p4 <- p4 + geom_smooth(method = 'auto')
print(p4 + mynamestheme)
ggsave("data-visualization/p4.pdf")


p5 <- ggplot(dataset, aes(x = season, y=transfer_fee))
p5 <- p5 + geom_boxplot(method = "auto",  na.rm = TRUE, 
                        aes(col = season))
p5 <- p5 + labs(y="Transfer fee (million £)",
                x = "Season",
                fill = "player position category")
p5 <- p5 + labs(colour ='Season') 
p5 <- p5 + geom_smooth(method = 'auto')
print(p5 + mynamestheme)
ggsave("data-visualization/p5.pdf", scale = 1.5, dpi=600)


p6 <- ggplot(dataset, aes(x = season, y=market_value))
p6 <- p6 + geom_boxplot(method = "auto",  na.rm = TRUE, 
                        aes(col = season))
p6 <- p6 + labs(y="Market value (million £)",
                x = "Season",
                fill = "player position category")
p6 <- p6 + labs(colour ='Season') 
p6 <- p6 + geom_smooth(method = 'auto')
print(p6 + mynamestheme)
ggsave("data-visualization/p6.pdf", scale = 1.5, dpi=600)



dataset <- dataset[dataset$player_nationality == 'brazil' | 
                     dataset$player_nationality == 'italy'|
                     dataset$player_nationality == 'germany'|
                     dataset$player_nationality == 'france'|
                     dataset$player_nationality == 'netherlands'|
                     dataset$player_nationality == 'spain'|
                     dataset$player_nationality == 'england',]

p7 <- ggplot(dataset,insta aes(x=player_nationality, y=market_value))
p7 <- p7 + geom_boxplot(method = "auto", na.rm = TRUE, 
                        aes(col = player_nationality))
p7 <- p7 + labs(colour ='Country of origin') 
p7 <- p7 + labs(y="Market value (million £)", x = "Country of origin")
print(p7 + mynamestheme)
ggsave("data-visualization/p7.pdf")


