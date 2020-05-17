# import libraries
library(rsconnect)
library(shiny)
library(plotly)
library(argonR)
library(argonDash)
library(dplyr)
library(parcoords)
library(highcharter)
library(viridisLite)
library(viridis)
library(GGally)
library(hrbrthemes)
library(ggplot2)
library(reactable)
library(DT)
library(shinyWidgets)
library(shinymaterial)

# import data

data = read.csv("Animal_Crossing_Full_Data_15_May.csv", header=T)
rank_data = read.csv("Overall_Villager_Data_Rank.csv", header=T)

# data update on
data_text = "Data: 15th May 2020"

# slice gender data
data_gender = data %>% group_by(Tier, Gender, .drop=FALSE) %>% count()
colnames(data_gender) = c("Tier", "Gender", "Frequency")

# slice personality data
data_personality = data %>% group_by(Tier, Personality, .drop=FALSE) %>% count()
colnames(data_personality) = c("Tier", "Personality", "Frequency")

# slice species data
data_species_1 = data %>% group_by(Species, .drop=FALSE) %>% count()
colnames(data_species_1) = c("Species", "Frequency")

# slice horoscope data
data_horoscope_1 = data %>% group_by(Tier, Horoscope, .drop=FALSE) %>% count()
colnames(data_horoscope_1) = c("Tier", "Horoscope", "Frequency")

# slice skills data
data_skill_1 = data %>% group_by(Tier, Skill, .drop=FALSE) %>% count()
colnames(data_skill_1) = c("Tier", "Skill", "Frequency")

# slice goals data
data_goals_1 = data %>% group_by(Tier, Goal, .drop=FALSE) %>% count()
colnames(data_goals_1) = c("Tier", "Goals", "Frequency")

# slice style data
data_style_1 = data %>% group_by(Tier, Style, .drop=FALSE) %>% count()
colnames(data_style_1) = c("Tier", "Style", "Frequency")

# slice style data
data_favorite_song_1 = data %>% group_by(Tier, Favorite_Song, .drop=FALSE) %>% count()
colnames(data_favorite_song_1) = c("Tier", "Favorite_Song", "Frequency")
