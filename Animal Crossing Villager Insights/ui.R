
# set working directory

source("data_loader.R")


# UI Design
ui = argonDashPage(
    
    
    title = "Animal Crossing Villager Insights",
    sidebar = argonDashSidebar(
        vertical = TRUE,
        skin = "light",
        background = "white",
        size = "md",
        side = "left",
        id = "sidebar",
        img(src = "AC_Logo.png", height=150),
        br(),
        argonSidebarMenu(
            argonSidebarItem(
                tabName = "Ranking",
                icon = argonIcon("trophy"),
                "Ranking"
            ),
            
            argonSidebarItem(
                tabName = "Gender",
                icon = argonIcon("circle-08"),
                "Gender"
            ),
            
            argonSidebarItem(
                tabName = "Personality",
                icon = argonIcon("single-02"),
                "Personality"
            ),
            
            argonSidebarItem(
                tabName = "Species",
                icon = argonIcon("planet"),
                "Species"
            ),
            
            argonSidebarItem(
                tabName = "Horoscope",
                icon = argonIcon("calendar-grid-58"),
                "Horoscope"
            ),
            
            argonSidebarItem(
                tabName = "Skill",
                icon = argonIcon("palette"),
                "Skill"
            ),
            
            argonSidebarItem(
                tabName = "Goal",
                icon = argonIcon("diamond"),
                "Goal"
            ),
            
            argonSidebarItem(
                tabName = "Style",
                icon = argonIcon("glasses-2"),
                "Style"
            ),
            
            argonSidebarItem(
                tabName = "Song",
                icon = argonIcon("note-03"),
                "Song"
            ),
            
            br(),
            br(),
            br(),
            br(),
            br(),
            br(),
            
            argonSidebarItem(
                tabName = "About",
                icon = argonIcon("circle-08"),
                "About"
            )
        )
    ),
    
    header = argonDashHeader(
        gradient= FALSE,
        separator = FALSE,
        bottom_padding = 4,
        background_img = "AC_Banner_Words_2.jpg",
        height = 300
    ),
    
    body = argonDashBody(
        tags$head(
            tags$link(rel = "stylesheet", type = "text/css", href = "AC_style.css"),
            tags$style(type = "text/css",
            "display_image_ranking img {max-width: 100%; width: 100%; height: auto}"
        )),
        
        argonTabItems(
            argonTabItem(
                tabName = "Ranking",  
                active = TRUE,
                argonRow(
                    argonTabSet(
                        id = "tabset0",
                        card_wrapper = FALSE,
                        horizontal = TRUE,
                        circle = FALSE,
                        size = "md",
                        width = 12,
                        iconList = list(
                            argonIcon("chart-bar-32"),
                            argonIcon("badge")
                        ),
                        argonTab(
                            tabName = "Overview",
                            active = TRUE,
                            argonRow(
                                argonCard(
                                    title = "Last Updated: 15 May 2020",
                                    width = 12,
                                    selectInput("name", strong("Select multiple villagers you would like to see: "), multiple = T, width = "100%",
                                                selected = c("Raymond", "Audie", "Beau", "Sherb", "Merengue", "Marshal", "Ankha"), choices = sort(unique(rank_data$Name))),
                                    h5(span("Double click on the legend (right side of the plot) to zoom in on the selected villager", style="color:blue")),
                                    h5(strong(span("Hover over to view rank of each villager", style="color:blue"))),
                                    plotlyOutput("ranking_plot", height = "800px"),
                                    br(),
                                    h5("Data obtained from: https://www.animalcrossingportal.com/games/new-horizons/guides/villager-popularity-list.php#/")
                                )
                            )
                        ),
                        
                        argonTab(
                            tabName = "Villagers",
                            active = FALSE,
                            argonRow(
                                argonCard(
                                    width = 7,
                                    argonColumn(DT::dataTableOutput("ranking_table"), inline=TRUE),
                                    h5("*Based on Latest Tier")
                                ),
   
                                argonCard(
                                    width = 5,
                                    argonColumn(
                                        argonCard(
                                            imageOutput("display_image_ranking", inline=TRUE)
                                        )
                                    )
                                )
                            )
                        )
                    )
                )
            ),
            argonTabItem(
                tabName = "Gender",
                active = FALSE,
                argonRow(
                    width = 12,
                    argonTabSet(
                        id = "tabset1",
                        card_wrapper = FALSE,
                        horizontal = TRUE,
                        circle = FALSE,
                        size = "md",
                        width = 12,
                        iconList = list(
                            argonIcon("chart-bar-32"),
                            argonIcon("badge")
                        ),
                        argonTab(
                            tabName = "Overview",
                            active = TRUE,
                            argonRow(
                                argonCard(
                                    width = 12,
                                    h5(strong(span("Hover over to view count of each category", style="color:blue"))),
                                    argonColumn(highchartOutput("gender_plot", height = "500px")),
                                    h5(data_text)
                                )
                            )
                        ),

                        
                        argonTab(
                            tabName = "Villagers",
                            active = FALSE,
                            argonRow(
                                argonCard(
                                    width = 7,
                                    argonColumn(
                                            width = 6,
                                            selectInput(inputId = "gender_tier_Input", "Tier", choices = sort(unique(data$Tier)), width="300px",
                                                        selected = "Tier 1")
                                            ),
                                    argonColumn(
                                            width = 6,
                                            selectInput(inputId = "gender_gender_Input", "Gender", choices = sort(unique(data$Gender)), width="300px",
                                                            selected = "Male")
                                            ),
                                            argonColumn(DT::dataTableOutput("gender_table"), inline=TRUE)
                                ),
                                argonCard(
                                    width = 5,
                                    argonColumn(
                                        argonCard(
                                            imageOutput("display_image", inline=TRUE)
                                        )
                                    )
                                )
                            )
                        )
                    )
                )
            ),
            argonTabItem(
                tabName = "Personality",
                active = FALSE,
                argonRow(
                        width = 12,
                        argonTabSet(
                            id = "tabset2",
                            card_wrapper = FALSE,
                            horizontal = TRUE,
                            circle = FALSE,
                            size = "md",
                            width = 12,
                            iconList = list(
                                argonIcon("chart-bar-32"),
                                argonIcon("badge")
                            ),
                            argonTab(
                                tabName = "Overview",
                                active = TRUE,
                                argonRow(
                                    argonCard(
                                        width = 7,
                                        argonColumn(
                                                h5(strong(span("Hover over to view count of each category", style="color:blue"))),
                                                highchartOutput("personality_plot_1", height = "500px"),
                                                h5(data_text)
                                        )
                                    ),
                                    argonCard(
                                        width = 5,
                                        argonColumn(
                                                h5(strong(span("Hover over to view count of each category", style="color:blue"))),
                                                highchartOutput("personality_plot_2", height = "500px"),
                                                h5(data_text)
                                        )
                                    )
                                )
                            ),
                            
                            argonTab(
                                tabName = "Villagers",
                                active = FALSE,
                                argonRow(
                                    argonCard(
                                        width = 8,
                                        argonColumn(
                                            width = 6,
                                            selectInput(inputId = "personality_tier_Input", "Tier", choices = sort(unique(data$Tier)), width="300px",
                                                        selected = "Tier 1")
                                        ),
                                        argonColumn(
                                            width = 6,
                                            selectInput(inputId = "personality_personality_Input", "Personality", choices = sort(unique(data$Personality)), width="300px",
                                                        selected = "Smug")
                                        ),
                                        argonColumn(DT::dataTableOutput("personality_table"), inline=TRUE)
                                    ),
                                    argonCard(
                                        width = 4,
                                        argonColumn(
                                                imageOutput("display_image_personality",inline=TRUE)
                                        )
                                    )
                                )
                            )
                        )
                )
            ),
            
            argonTabItem(
                tabName = "Species",
                active  = FALSE,
                argonRow(
                        width = 12,
                        argonTabSet(
                            id = "tabset3",
                            card_wrapper = FALSE,
                            horizontal = TRUE,
                            circle = FALSE,
                            size = "md",
                            width = 12,
                            iconList = list(
                                argonIcon("chart-bar-32"),
                                argonIcon("badge")
                            ),
                            argonTab(
                                tabName = "Overview",
                                active = TRUE,
                                argonRow(
                                    argonCard(
                                        width = 5,
                                        h5(strong(span("Hover over to view count of each category", style="color:blue"))),
                                        selectInput(inputId = "species_tier_Input_1", "Select a tier", choices = sort(unique(data$Tier)), width="300px"),
                                        highchartOutput("species_plot_1", height = "500px"),
                                        h5(data_text)
                                    ),
                                    
                                    argonCard(
                                        width = 7,
                                        h5(strong(span("Hover over to view count of each category", style="color:blue"))),
                                        highchartOutput("species_plot_2", height = "600px"),
                                        h5(data_text)
                                    )
                                )
                            ),
       
                            argonTab(
                                tabName = "Villagers",
                                active = FALSE,
                                argonRow(
                                    argonCard(
                                        width = 8,
                                        argonColumn(
                                                width = 6,
                                                selectInput(inputId = "species_tier_Input_2", "Tier", choices = sort(unique(data$Tier)), width="300px",
                                                                 selected = "Tier 1")
                                                ),
                                        argonColumn(
                                                width = 6,
                                                selectInput(inputId = "species_species_Input_2", "Species", choices = sort(unique(data$Species)), width="300px",
                                                                 selected = "Cat")
                                                ),
                                                argonColumn(DT::dataTableOutput("species_table"),inline=TRUE)
                                    ),
                                    argonCard(
                                        width = 4,
                                        argonColumn(
                                                imageOutput("display_image_species",inline=TRUE)
                                            )
                                    )
                                )
                            )
                        )
                )
            ),
            argonTabItem(
                tabName = "Horoscope",
                active  = FALSE,
                argonRow(
                    width = 12,
                    argonTabSet(
                        id = "tabset4",
                        card_wrapper = FALSE,
                        horizontal = TRUE,
                        circle = FALSE,
                        size = "md",
                        width = 12,
                        iconList = list(
                            argonIcon("chart-bar-32"),
                            argonIcon("badge")
                        ),
                        argonTab(
                            tabName = "Overview",
                            active = TRUE,
                            argonRow(
                                argonCard(
                                    width = 6,
                                    argonColumn(
                                            h5(strong(span("Hover over to view count of each category", style="color:blue"))),
                                            selectInput(inputId = "horoscope_tier_Input_1", "Select a tier", choices = sort(unique(data$Tier)), width="300px",
                                                        selected = "Tier 1"),
                                            highchartOutput("horoscope_plot_1", height = "500px"),
                                            h5(data_text)
                                    )
                                ),
                                    
                                argonCard(
                                    width = 6,
                                    argonColumn(
                                            h5(strong(span("Hover over to view count of each category", style="color:blue"))),
                                            highchartOutput("horoscope_plot_2", height = "700px"),
                                            h5(data_text)
                                    )
                                )
                            )
                        ),
                        
                        argonTab(
                            tabName = "Villagers",
                            active = FALSE,
                            argonRow(
                                argonCard(
                                    width = 8,
                                    argonColumn(
                                            width = 6,
                                            selectInput(inputId = "horoscope_tier_Input_2", "Tier", choices = sort(unique(data$Tier)), width="300px",
                                                            selected = "Tier 1")
                                            ),
                                    argonColumn(
                                            width = 6,
                                            selectInput(inputId = "horoscope_horoscope_Input_2", "Horoscope", choices = sort(unique(data$Horoscope)), width="300px",
                                                            selected = "Aquarius")
                                            ),
                                    argonColumn(DT::dataTableOutput("horoscope_table"),inline=TRUE)
                                ),
                                argonCard(
                                    width = 4,
                                    argonColumn(
                                            imageOutput("display_image_horoscope",inline=TRUE)
                                    )
                                )
                            )
                        )
                    )
                )
            ),
            
            argonTabItem(
                tabName = "Skill",
                active  = FALSE,
                argonRow(
                    width = 12,
                    argonTabSet(
                        id = "tabset5",
                        card_wrapper = FALSE,
                        horizontal = TRUE,
                        circle = FALSE,
                        size = "md",
                        width = 12,
                        iconList = list(
                            argonIcon("chart-bar-32"),
                            argonIcon("badge")
                        ),
                        argonTab(
                            tabName = "Overview",
                            active = TRUE,
                            argonRow(
                                argonCard(
                                    width = 12,
                                    argonColumn(
                                        argonCard(
                                            width = 2,
                                            argonColumn(
                                                radioButtons("radio_skill", label = h3("Select a Tier"),
                                                        choices = list("Tier 1" = "Tier 1", 
                                                                       "Tier 2" = "Tier 2", 
                                                                       "Tier 3" = "Tier 3", 
                                                                       "Tier 4" = "Tier 4", 
                                                                       "Tier 5" = "Tier 5", 
                                                                       "Tier 6" = "Tier 6"),
                                                        selected = "Tier 1")
                                            )
                                        ),
                                        
                                        argonCard(
                                            width = 10,
                                            #selectInput(inputId = "skill_tier_Input_1", "Tier", choices = sort(unique(data$Tier)), width="300px"),
                                            argonColumn(
                                                width = 12,
                                                h5(strong(span("Hover over to view count of each category", style="color:blue"))),
                                                highchartOutput("skill_plot_1", height = "700px"),
                                                h5(data_text)
                                            )
                                        )
                                    )
                                )
                            )
                        ),
                        argonTab(
                            tabName = "Villagers",
                            active = FALSE,
                            argonRow(
                                argonCard(
                                    width = 8,
                                    argonColumn(
                                        width = 6,
                                        selectInput(inputId = "skill_tier_Input_2", "Tier", choices = sort(unique(data$Tier)), width="300px",
                                                    selected = "Tier 1")
                                    ),
                                    argonColumn(
                                        width = 6,
                                        selectInput(inputId = "skill_skill_Input_2", "Skill", choices = sort(unique(data$Skill)), width="300px",
                                                    selected = "Air Guitar")
                                    ),
                                    argonColumn(DT::dataTableOutput("skill_table"),inline=TRUE)
                                ),

                                argonCard(
                                    width = 4,
                                    argonColumn(
                                            imageOutput("display_image_skill",inline=TRUE)
                                    )
                                )
                            )
                        )
                    )
                )
            ),
            argonTabItem(
                tabName = "Goal",
                active  = FALSE,
                argonRow(
                    width = 12,
                    argonTabSet(
                        id = "tabset6",
                        card_wrapper = FALSE,
                        horizontal = TRUE,
                        circle = FALSE,
                        size = "md",
                        width = 12,
                        iconList = list(
                            argonIcon("chart-bar-32"),
                            argonIcon("badge")
                        ),
                        argonTab(
                            tabName = "Overview",
                            active = TRUE,
                            argonRow(
                                argonCard(
                                    width = 12,
                                    argonColumn(
                                        argonCard(
                                            width = 2,
                                            argonColumn(
                                                radioButtons("radio_goal", label = h3("Select a Tier"),
                                                             choices = list("Tier 1" = "Tier 1", 
                                                                            "Tier 2" = "Tier 2", 
                                                                            "Tier 3" = "Tier 3", 
                                                                            "Tier 4" = "Tier 4", 
                                                                            "Tier 5" = "Tier 5", 
                                                                            "Tier 6" = "Tier 6"),
                                                             selected = "Tier 1")
                                            )
                                        ),
                                        
                                        argonCard(
                                            width = 10,
                                            #selectInput(inputId = "skill_tier_Input_1", "Tier", choices = sort(unique(data$Tier)), width="300px"),
                                            argonColumn(
                                                width = 12,
                                                h5(strong(span("Hover over to view count of each category", style="color:blue"))),
                                                highchartOutput("goal_plot_1", height = "700px"),
                                                h5(data_text)
                                            )
                                        )
                                    )
                                )
                            )
                        ),
                        argonTab(
                            tabName = "Villagers",
                            active = FALSE,
                            argonRow(
                                argonCard(
                                    width = 8,
                                    argonColumn(
                                            width = 6,
                                            selectInput(inputId = "goal_tier_Input_2", "Tier", choices = sort(unique(data$Tier)), width="300px",
                                                             selected = "Tier 1")
                                            ),
                                    argonColumn(
                                            width = 6,
                                            selectInput(inputId = "goal_goal_Input_2", "Skill", choices = sort(unique(data$Goal)), width="300px",
                                                             selected = "Actor")
                                            ),
                                    argonColumn(DT::dataTableOutput("goal_table"),inline=TRUE)
                                ),
                                argonCard(
                                    width = 4,
                                    argonColumn(
                                            imageOutput("display_image_goal",inline=TRUE)
                                    )
                                )
                            )
                        )
                    )
                )
            ),
            argonTabItem(
                tabName = "Style",
                active  = FALSE,
                argonRow(
                    width = 12,
                    argonTabSet(
                        id = "tabset7",
                        card_wrapper = FALSE,
                        horizontal = TRUE,
                        circle = FALSE,
                        size = "md",
                        width = 12,
                        iconList = list(
                            argonIcon("chart-bar-32"),
                            argonIcon("badge")
                        ),
                        argonTab(
                            tabName = "Overview",
                            active = TRUE,
                            argonRow(
                                argonCard(
                                    width = 6,
                                    argonColumn(
                                            h5(strong(span("Hover over to view count of each category", style="color:blue"))),
                                            selectInput(inputId = "style_tier_Input_1", "Select a tier", choices = sort(unique(data$Tier)), width="300px",
                                                         selected = "Tier 1"),
                                            highchartOutput("style_plot_1", height = "500px"),
                                            h5(data_text)
                                    )
                                ),
                                
                                argonCard(
                                    width = 6,
                                    argonColumn(
                                            h5(strong(span("Hover over to view count of each category", style="color:blue"))),
                                            highchartOutput("style_plot_2", height = "600px"),
                                            h5(data_text)
                                    )
                                )
                            )
                        ),
                        
                        argonTab(
                            tabName = "Villagers",
                            active = FALSE,
                            argonRow(
                                argonCard(
                                    width = 8,
                                    argonColumn(
                                            width = 6,
                                            selectInput(inputId = "style_tier_Input_2", "Tier", choices = sort(unique(data$Tier)), width="300px",
                                                             selected = "Tier 1")
                                            ),
                                    argonColumn(
                                            width = 6,
                                            selectInput(inputId = "style_style_Input_2", "Style", choices = sort(unique(data$Style)), width="300px",
                                                             selected = "Basic")
                                            ),
                                    h5(strong(span("Hover over to view count of each category", style="color:blue"))),
                                    argonColumn(DT::dataTableOutput("style_table"),inline=TRUE)
                                ),
                                argonCard(
                                    width = 4,
                                    argonColumn(
                                            imageOutput("display_image_style",inline=TRUE)
                                    )
                                )
                            )
                        )
                    )
                )
            ),
            
            argonTabItem(
                tabName = "Song",
                active  = FALSE,
                argonRow(
                    width = 12,
                    argonTabSet(
                        id = "tabset8",
                        card_wrapper = FALSE,
                        horizontal = TRUE,
                        circle = FALSE,
                        size = "md",
                        width = 12,
                        iconList = list(
                            argonIcon("chart-bar-32"),
                            argonIcon("badge")
                        ),
                        argonTab(
                            tabName = "Overview",
                            active = TRUE,
                            argonRow(
                                argonCard(
                                    width = 12,
                                    argonColumn(
                                        argonCard(
                                            width = 2,
                                            argonColumn(
                                                radioButtons("radio_favorite_song", label = h3("Select a Tier"),
                                                             choices = list("Tier 1" = "Tier 1", 
                                                                            "Tier 2" = "Tier 2", 
                                                                            "Tier 3" = "Tier 3", 
                                                                            "Tier 4" = "Tier 4", 
                                                                            "Tier 5" = "Tier 5", 
                                                                            "Tier 6" = "Tier 6"),
                                                             selected = "Tier 1")
                                            )
                                        ),
                                        
                                        argonCard(
                                            width = 10,
                                            #selectInput(inputId = "skill_tier_Input_1", "Tier", choices = sort(unique(data$Tier)), width="300px"),
                                            argonColumn(
                                                width = 12,
                                                h5(strong(span("Hover over to view count of each category", style="color:blue"))),
                                                highchartOutput("favorite_song_plot_1", height = "700px"),
                                                h5(data_text)
                                            )
                                        )
                                    )
                                )
                            )
                        ),
                        argonTab(
                            tabName = "Villagers",
                            active = FALSE,
                            argonRow(
                                argonCard(
                                    width = 8,
                                    argonColumn(
                                            width = 6,
                                            selectInput(inputId = "favorite_song_tier_Input_2", "Tier", choices = sort(unique(data$Tier)), width="300px",
                                                             selected = "Tier 1")
                                            ),
                                    argonColumn(
                                            width = 6,
                                            selectInput(inputId = "favorite_song_song_Input_2", "Favorite Song", choices = sort(unique(data$Favorite_Song)), width="300px",
                                                             selected = "Agent K.K." )
                                            ),
                                    argonColumn(DT::dataTableOutput("favorite_song_table"),inline=TRUE)
                                ),
                                argonCard(
                                    width = 4,
                                    argonColumn(
                                            imageOutput("display_image_favorite_song",inline=TRUE)
                                    )
                                )
                            )
                        )
                    )
                )
            ),
            
            argonTabItem(
                tabName ="About",
                active = FALSE,
                argonRow(
                    argonCard(
                        width = 12,
                        h1("About this Dashboard"),
                        p(strong("Hi I'm Joanna and I have an announcement to make. Yes, I am officially hooked on Animal Crossing New Horizon.
                           My first Animal Crossing game was New Leaf on the 3DS and I'll be honest, I didn't 
                           spend as much time playing it compared to New Horizon. (perhaps it's due to the hype on 
                           social media and that I have a sister to play ACNH with everyday)")),
                        p(strong("A few months into the game, a", 
                          span('Villager Popularity List', style = "color:blue"),
                          "was being circulated online", span("https://www.animalcrossingportal.com/games/new-horizons/guides/villager-popularity-list.php#/", style = "color:blue"),
                          "As I was looking through, I wondered about the factors contributing to their popularity. As there were no readily available data, 
                          I had to first write some Python script to scrape the website,", span("https://animalcrossing.fandom.com/wiki/Villager_list_(New_Horizons)", style = "color:blue"),
                                 "in order to obtain the raw data needed.")),
                        p(strong("Finally, I've put together some interesting villager insights in the form of a dashboard! The dashboard will be updated every
                                 month as the new popularity list comes in. I hope you will find this dashboard as interesting as I have found it to be. 
                                 You can contact me at", span("joannakhek@gmail.com", style = "color:blue")))
                    )
                )
            )
        )
    )
)
