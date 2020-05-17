
# Define server logic required to draw a histogram
shinyServer(function(input, output, session) {
    
    observeEvent("", {
        showModal(modalDialog(
            includeHTML("intro_page.html"),
            easyClose = TRUE,
        )
        )
    })
    
    
    ###### RANKING #####
    filtered_name = reactive({
                         req(input$name)
        
                         rank_data %>% 
                                select(Name, Updated.Date, Overall_Rank, Latest_Tier) %>%
                                filter(Name %in% input$name)
    })
    
    output$ranking_plot = renderPlotly({
        plot_ly(data = filtered_name(), x = ~Updated.Date, y = ~Overall_Rank, 
                type="scatter",
                mode="lines+markers+text", 
                split= ~Name,
                color = ~Latest_Tier,
                line = list(shape = "linear", width = 5),
                marker = list(size = 15),
                text = ~Name,
                textposition = "middle top",
                hovertemplate = paste("<br>Date</b>: %{x}",
                                      "<br>Name</b>: %{text}",
                                      "<br>Rank</b>: %{y}")
                )  %>%
            layout(title ="Overall Ranking", xaxis = list(title="Date"), 
                   yaxis = list(title="Overall Rank", autorange="reversed")) %>% 
            config(displayModeBar = F)
    })
            
    filtered_ranking_name = reactive({
        data %>% arrange(Rank_Overall) %>% select("Name", "Personality", "Species", "Tier", "Rank_Overall")
    })
    
    
    output$ranking_table = DT::renderDataTable(
        filtered_ranking_name(),
        selection = list(mode = "single", selected = 1),
        filter = "none",
        class = "stripe compact hover",
        style = "default",
        options = list(autoWidth = FALSE)
    )
    
    
    ranking_villager_name = reactive({filtered_ranking_name()[input$ranking_table_rows_selected, 1]})
    
    
    output$display_image_ranking = renderImage({
        filename = paste("www/Image_Large/", ranking_villager_name(), ".png", sep="")
        list(src = filename,
             width = 300,
             height = 400,
             contentType = "image/png")}, deleteFile = FALSE)
    
    ###### GENDER ######
    filtered_gender_tier = reactive({
        data %>% filter(Tier == input$gender_tier_Input) %>% filter(Gender == input$gender_gender_Input) %>% arrange(Rank_Overall) %>%select("Name", "Personality", "Species", "Horoscope", "Tier", "Rank_Overall")
    })
    
    output$gender_plot =  renderHighchart({ 
        hchart(data_gender, "column", hcaes(x = Tier, y = Frequency, group = Gender))  %>%
            hc_colors(c("#ED5F8C", "#7B91F0")) %>%
            hc_title(text = "Count of Gender by Tier")
    })
    
    
    output$gender_table = DT::renderDataTable(
        filtered_gender_tier(),
        selection = list(mode = "single", selected = 1),
        filter = "none",
        class = "stripe compact hover",
        style = "default",
        options = list(autoWidth = FALSE)
    )
    
    
    gender_villager_name = reactive({filtered_gender_tier()[input$gender_table_rows_selected, 1]})
    
    
    output$display_image = renderImage({
        filename = paste("www/Image_Large/", gender_villager_name(), ".png", sep="")
        list(src = filename,
             width = 300,
             height = 400,
             contentType = "image/png")}, deleteFile = FALSE)
    

    
    ###### PERSONALITY ######
    filtered_personality_tier = reactive({
        data %>% filter(Tier == input$personality_tier_Input) %>% filter(Personality == input$personality_personality_Input) %>% arrange(Rank_Overall)%>% select("Name", "Personality", "Species", "Horoscope", "Tier", "Rank_Overall")
    })
    
    output$personality_plot_1 = renderHighchart({
        hchart(data_personality, "column", hcaes(x = Tier, y = Frequency, group = Personality)) %>%
        hc_title(text = "Count of Personality by Tier")
    })
    output$personality_plot_2 = renderHighchart({
        hchart(data_personality, "bar", hcaes(x = Personality, y = Frequency, group = Tier)) %>%
            hc_plotOptions(bar = list(stacking="normal")) %>%
            hc_title(text = "Count of Tier by Personality")
            
    })
    
    
    output$personality_table = DT::renderDataTable(
        filtered_personality_tier(),
        selection = lst(mode="single", selected = 1),
        filter = "none",
        class = "stripe compact hover",
        style = "default",
        options = list(autoWidth = FALSE)
    )
    
    personality_villager_name = reactive({filtered_personality_tier()[input$personality_table_rows_selected, 1]})
    
    output$display_image_personality = renderImage({
        filename = paste("www/Image_Large/", personality_villager_name(), ".png", sep="")
        list(src = filename,
             width = 300,
             height = 400,
             contentType = "image/png")}, deleteFile = FALSE)
    
    ###### SPECIES #####
    filtered_species_tier_1 = reactive({
        data %>% filter(Tier == input$species_tier_Input_1) %>% select("Name", "Tier", "Species")
    })
    
    data_species_2 = reactive({filtered_species_tier_1() %>% group_by(Tier, Species, .drop=FALSE) %>% summarise(n = n()) %>% arrange(-n)
    })
    
    output$species_plot_1 = renderHighchart({
        hchart(data_species_2(), "treemap", hcaes(x = Species, value = n, color = n)) %>%
            hc_colorAxis(stops = color_stops(colors = viridis::viridis(10))) %>%
            hc_title(text = "Count of Species by Tier")
    })
    
    output$species_plot_2 = renderHighchart({
        hchart(data_species_1, "column", hcaes(x = Species, y = Frequency)) %>%
        hc_xAxis(labels = list(rotation = 90)) %>%
        hc_title(text = "Overall Count of Species")
    })
    
    filtered_species_tier_2 = reactive({
        data %>% filter(Tier == input$species_tier_Input_2) %>% filter(Species == input$species_species_Input_2) %>% select("Name", "Personality", "Species", "Horoscope", "Tier", "Rank_Overall")
    })
    
    output$species_table = DT::renderDataTable(
        filtered_species_tier_2(),
        selection = lst(mode="single", selected = 1),
        filter = "none",
        class = "stripe compact hover",
        style = "default",
        options = list(autoWidth = FALSE)
    )
    
    species_villager_name = reactive({filtered_species_tier_2()[input$species_table_rows_selected, 1]})
    
    output$display_image_species = renderImage({
        filename = paste("www/Image_Large/", species_villager_name(), ".png", sep="")
        list(src = filename,
             width = 300,
             height = 400,
             contentType = "image/png")}, deleteFile = FALSE)
    
    ##### HOROSCOPE #####
    filtered_horoscope_tier_1 = reactive({
        data %>% filter(Tier == input$horoscope_tier_Input_1) %>% arrange(Rank_Overall)%>% select("Name", "Tier", "Horoscope")
    })
    
    data_horoscope_2 = reactive({filtered_horoscope_tier_1() %>% group_by(Tier, Horoscope, .drop=FALSE) %>% summarise(n = n()) %>% arrange(-n)
    })
    
    output$horoscope_plot_1 = renderHighchart({
        hchart(data_horoscope_2(), "treemap", hcaes(x = Horoscope, value = n, color = n)) %>%
            hc_colorAxis(stops = color_stops(colors = viridis::viridis(10))) %>%
            hc_title(text = "Count of Horoscope by Tier")
 
    })
    output$horoscope_plot_2 = renderHighchart({
        hchart(data_horoscope_1, "bar", hcaes(x = Horoscope, y = Frequency, group = Tier)) %>%
            hc_plotOptions(bar = list(stacking="normal")) %>%
            hc_title(text = "Count of Tier by Horoscope")
        
    })
    
    filtered_horoscope_tier_2 = reactive({
        data %>% filter(Tier == input$horoscope_tier_Input_2) %>% filter(Horoscope == input$horoscope_horoscope_Input_2) %>% arrange(Rank_Overall)%>% select("Name", "Personality", "Species", "Horoscope", "Tier", "Rank_Overall")
    })
    
    output$horoscope_table = DT::renderDataTable(
        filtered_horoscope_tier_2(),
        selection = lst(mode="single", selected = 1),
        filter = "none",
        class = "stripe compact hover",
        style = "default",
        options = list(autoWidth = FALSE)
    )
    
    horoscope_villager_name = reactive({filtered_horoscope_tier_2()[input$horoscope_table_rows_selected, 1]})
    
    output$display_image_horoscope = renderImage({
        filename = paste("www/Image_Large/", horoscope_villager_name(), ".png", sep="")
        list(src = filename,
             width = 300,
             height = 400,
             contentType = "image/png")}, deleteFile = FALSE)
    
    ##### SKILL #####
    filtered_skill_tier_1 = reactive({
        data %>% filter(Tier == input$radio_skill) %>% select("Name", "Tier", "Skill")
    })
    
    data_skill_2 = reactive({filtered_skill_tier_1() %>% group_by(Tier, Skill, .drop=FALSE) %>% summarise(n = n()) %>% arrange(-n)
    })
    
    output$skill_plot_1 = renderHighchart({
        hchart(data_skill_2(), "treemap", hcaes(x = Skill, value = n, color = n)) %>%
            hc_colorAxis(stops = color_stops(colors = viridis::viridis(10))) %>%
            hc_title(text = "Count of Skill by Tier")
        
    })

    filtered_skill_tier_2 = reactive({
        data %>% filter(Tier == input$skill_tier_Input_2) %>% filter(Skill == input$skill_skill_Input_2) %>% arrange(Rank_Overall)%>% select("Name", "Personality", "Species", "Skill", "Tier", "Rank_Overall")
    })
    
    output$skill_table = DT::renderDataTable(
        filtered_skill_tier_2(),
        selection = lst(mode="single", selected = 1),
        filter = "none",
        class = "stripe compact hover",
        style = "default",
        options = list(autoWidth = FALSE)
    )
    
    skill_villager_name = reactive({filtered_skill_tier_2()[input$skill_table_rows_selected, 1]})
    
    output$display_image_skill = renderImage({
        filename = paste("www/Image_Large/", skill_villager_name(), ".png", sep="")
        list(src = filename,
             width = 300,
             height = 400,
             contentType = "image/png")}, deleteFile = FALSE)

    ###### GOAL ######
    filtered_goal_tier_1 = reactive({
        data %>% filter(Tier == input$radio_goal) %>% select("Name", "Tier", "Goal")
    })
    
    data_goal_2 = reactive({filtered_goal_tier_1() %>% group_by(Tier, Goal, .drop=FALSE) %>% summarise(n = n()) %>% arrange(-n)
    })
    
    output$goal_plot_1 = renderHighchart({
        hchart(data_goal_2(), "treemap", hcaes(x = Goal, value = n, color = n)) %>%
            hc_colorAxis(stops = color_stops(colors = viridis::viridis(10))) %>%
            hc_title(text = "Count of Goal by Tier")
        
    })
    
    filtered_goal_tier_2 = reactive({
        data %>% filter(Tier == input$goal_tier_Input_2) %>% filter(Goal == input$goal_goal_Input_2)%>% arrange(Rank_Overall) %>% select("Name", "Personality", "Species", "Goal", "Tier", "Rank_Overall")
    })
    
    output$goal_table = DT::renderDataTable(
        filtered_goal_tier_2(),
        selection = lst(mode="single", selected = 1),
        filter = "none",
        class = "stripe compact hover",
        style = "default",
        options = list(autoWidth = FALSE)
    )
    
    goal_villager_name = reactive({filtered_goal_tier_2()[input$goal_table_rows_selected, 1]})
    
    output$display_image_goal = renderImage({
        filename = paste("www/Image_Large/", goal_villager_name(), ".png", sep="")
        list(src = filename,
             width = 300,
             height = 400,
             contentType = "image/png")}, deleteFile = FALSE)
    
    ###### STYLE #####
    filtered_style_tier_1 = reactive({
        data %>% filter(Tier == input$style_tier_Input_1) %>% select("Name", "Tier", "Style")
    })
    
    data_style_2 = reactive({filtered_style_tier_1() %>% group_by(Tier, Style, .drop=FALSE) %>% summarise(n = n()) %>% arrange(-n)
    })
    
    output$style_plot_1 = renderHighchart({
        hchart(data_style_2(), "treemap", hcaes(x = Style, value = n, color = n)) %>%
            hc_colorAxis(stops = color_stops(colors = viridis::viridis(10))) %>%
            hc_title(text = "Count of Style by Tier")
        
    })
    output$style_plot_2 = renderHighchart({
        hchart(data_style_1, "bar", hcaes(x = Style, y = Frequency, group = Tier)) %>%
            hc_plotOptions(bar = list(stacking="normal")) %>%
            hc_title(text = "Count of Tier by Style")
        
    })
    
    filtered_style_tier_2 = reactive({
        data %>% filter(Tier == input$style_tier_Input_2) %>% filter(Style == input$style_style_Input_2) %>% arrange(Rank_Overall)%>% select("Name", "Personality", "Species", "Style", "Tier", "Rank_Overall")
    })
    
    output$style_table = DT::renderDataTable(
        filtered_style_tier_2(),
        selection = lst(mode="single", selected = 1),
        filter = "none",
        class = "stripe compact hover",
        style = "default",
        options = list(autoWidth = FALSE)
    )
    
    style_villager_name = reactive({filtered_style_tier_2()[input$style_table_rows_selected, 1]})
    
    output$display_image_style = renderImage({
        filename = paste("www/Image_Large/", style_villager_name(), ".png", sep="")
        list(src = filename,
             width = 300,
             height = 400,
             contentType = "image/png")}, deleteFile = FALSE)
    
    ###### FAVORITE ######
    filtered_favorite_song_tier_1 = reactive({
        data %>% filter(Tier == input$radio_favorite_song) %>% select("Name", "Tier", "Favorite_Song")
    })
    
    data_favorite_song_2 = reactive({filtered_favorite_song_tier_1() %>% group_by(Tier, Favorite_Song, .drop=FALSE) %>% summarise(n = n()) %>% arrange(-n)
    })
    
    output$favorite_song_plot_1 = renderHighchart({
        hchart(data_favorite_song_2(), "treemap", hcaes(x = Favorite_Song, value = n, color = n)) %>%
            hc_colorAxis(stops = color_stops(colors = viridis::viridis(10))) %>%
            hc_title(text = "Count of Favorite Song by Tier")
        
    })
    
    filtered_favorite_song_tier_2 = reactive({
        data %>% filter(Tier == input$favorite_song_tier_Input_2) %>% filter(Favorite_Song == input$favorite_song_song_Input_2) %>% arrange(Rank_Overall)%>% select("Name", "Personality", "Species", "Favorite_Song", "Tier", "Rank_Overall")
    })
    
    output$favorite_song_table = DT::renderDataTable(
        filtered_favorite_song_tier_2(),
        selection = lst(mode="single", selected = 1),
        filter = "none",
        class = "stripe compact hover",
        style = "default",
        options = list(autoWidth = FALSE)
    )
    
    favorite_song_villager_name = reactive({filtered_favorite_song_tier_2()[input$favorite_song_table_rows_selected, 1]})
    
    output$display_image_favorite_song = renderImage({
        filename = paste("www/Image_Large/", favorite_song_villager_name(), ".png", sep="")
        list(src = filename,
             width = 300,
             height = 400,
             contentType = "image/png")}, deleteFile = FALSE)

})

