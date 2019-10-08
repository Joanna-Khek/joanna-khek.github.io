# import library
library(shiny)
library(ggplot2)
library(dplyr)
library(shinydashboard)
library(devtools)
library(dashboardthemes)
library(shinyBS)
library(DT)
library(data.table)
library(plotly)
library(rsconnect)

# import data
data = read.csv("fifa19_final.csv", header= TRUE)

# edit data
data$Club = iconv(data$Club, "latin1", "ASCII", sub="")
data$Jersey = ifelse(data$Jersey.Number >= 40, "Others", data$Jersey.Number)
data$Jersey = factor(data$Jersey, levels = c(seq(from=1, to=39, by=1), "Others"))

# ui
ui = dashboardPage(
         dashboardHeader(title = "FIFA 19 Dashboard"),
         dashboardSidebar(
             sidebarMenu(
                menuItem("Dashboard", tabName = "dashboard", icon = icon("dashboard")),
                
                selectInput(inputId="leagueInput", "League", 
                            choices = sort(unique(data$League))),
                
                menuItem("About Me", icon=icon("send", lib = "glyphicon"),
                         href = "https://linkedin.com/in/joannakhek/")
                 
         )),
         
         dashboardBody(
             shinyDashboardThemes(
                 theme = "blue_gradient"
             ),
             
             tabItems(
                 tabItem(tabName = "dashboard",
                     fluidRow(
                         valueBoxOutput("value1"),
                         valueBoxOutput("value2"),
                         valueBoxOutput("value3")
                     ),
                     
                     fluidRow(
                         box(
                             width = 4,
                             title = "Average Value by Club",
                             status = "primary",
                             solidHeader = TRUE,
                             collapsible = TRUE,
                             plotlyOutput("value", height = 300)
                         ),
                         
                         box(
                             width = 4,
                             title = "Average Wage by Club",
                             status = "success",
                             solidHeader = TRUE,
                             collapsible = TRUE,
                             plotlyOutput("wage", height = 300)
                         ),
                         
                         box(
                             width = 4,
                             title = "Histogram of Age by Club",
                             status = "warning",
                             solidHeader = TRUE,
                             collapsible = TRUE,
                             plotlyOutput("hist_age", height = 300)
                         ),
                         
                         
                         # box(
                         #     width = 4,
                         #     tabsetPanel(
                         #         tabPanel("Average Value",
                         #                  DT::dataTableOutput("value_table")),
                         #         tabPanel("Average Wage",
                         #                  DT::dataTableOutput("wage_table")),
                         #         tabPanel("Average Age",
                         #                  DT::dataTableOutput("age_table"))
                         #     )
                         # ),
                         
                         box(
                             width = 4,
                             title = "Jersey Number V.S Wage",
                             status = "primary",
                             solidHeader = TRUE,
                             collapsible = TRUE,
                             plotlyOutput("jersey_wage", height = 300)

                         ),
                         
                         box(
                             width = 4,
                             title = "Position V.S Wage",
                             status = "success",
                             solidHeader = TRUE,
                             collapsible = TRUE,
                             plotlyOutput("position_wage", height = 300)
                         ),
                         
                         box(
                             width = 4,
                             title = "Age V.S Wage",
                             status = "warning",
                             solidHeader = TRUE,
                             collapsible = TRUE,
                             plotlyOutput("age_wage", height = 300)
                         )
                     )
                 )
             )
         )
)
                 



# server
server = function(session,input, output){

    
    # some data manipulation to derive the values of boxes
    average_value = data %>% group_by(League) %>% summarise(value = mean(Value))
    average_wage = data %>% group_by(League) %>% summarise(value = mean(Wage))
    average_age = data %>% group_by(League) %>% summarise(value = mean(Age))
    
    # creating the valueBoxOutput content
    output$value1 = renderValueBox({
        valueBox(
            formatC(average_value %>% filter(League == input$leagueInput) %>% select("value"), format="d", big.mark=","),
            "Average Value",
            icon = icon("stats", lib="glyphicon"),
            color = "purple")
    })

    output$value2 = renderValueBox({
        valueBox(
            formatC(average_wage %>% filter(League == input$leagueInput) %>% select("value"), format="d", big.mark=","), 
            "Average Wage",
            icon = icon("gbp", lib="glyphicon"),
            color = "green")
    })
    
    output$value3 = renderValueBox({
        valueBox(
            formatC(average_age %>% filter(League == input$leagueInput) %>% select("value"), format="d", big.mark=","),
            "Average Age",
            icon = icon("menu-hamburger", lib="glyphicon"),
            color = "yellow")
    })
    
    
    # creating the plotOutput content

    output$value = renderPlotly({
        filtered = data %>% filter(League == input$leagueInput) %>% group_by(Club) %>% summarise(value = mean(Value))
        
        p = ggplot(data=as.data.frame(filtered), aes(x=Club, y=value)) +
            geom_bar(position = "dodge", stat = "identity") + ylab("Value") +
            xlab("Club") + theme(legend.position = "bottom",
                                    plot.title = element_text(size=15, face="bold")) + 
            theme(axis.text.x = element_text(angle=90, hjust=1))
        
        ggplotly(p)

    })

    output$wage = renderPlotly({
        filtered = data %>% filter(League == input$leagueInput) %>% group_by(Club) %>% summarise(value = mean(Wage))
        
        p = ggplot(data = as.data.frame(filtered), aes(x=Club, y=value)) +
            geom_bar(position = "dodge", stat = "identity") + ylab("Wage") +
            xlab("Club") + theme(legend.position="bottom", plot.title = element_text(size=15, face="bold")) +
            theme(axis.text.x = element_text(angle=90, hjust=1))
        
        ggplotly(p)
    })
    
    output$hist_age = renderPlotly({
        filtered = data %>% filter(League == input$leagueInput)
        
        p = ggplot(data = as.data.frame(filtered)) + geom_boxplot(aes(x=Club, y=Age)) + ylab("Age") + xlab("Club") +
            theme(legend.position="bottom", plot.title = element_text(size=15, face="bold")) +
            theme(axis.text.x = element_text(angle=90, hjust=1))
        
        ggplotly(p)
    })
    

    # output$value_table = DT::renderDataTable({
    #     filtered = data %>% filter(League == input$leagueInput) %>% group_by(Club) %>% summarise(value = mean(Value))
    #     data.table(filtered)
    # }, options = list(lengthMenu = c(5, 10, -1), pageLength = 5))
    # 
    # output$wage_table = DT::renderDataTable({
    #     filtered = data %>% filter(League == input$leagueInput) %>% group_by(Club) %>% summarise(value = mean(Wage))
    #     data.table(filtered)
    # }, options = list(lengthMenu = c(5, 10, -1), pageLength = 5))
    # 
    # output$age_table = DT::renderDataTable({
    #     filtered = data %>% filter(League == input$leagueInput) %>% group_by(Club) %>% summarise(value = mean(Age))
    #     data.table(filtered)
    # }, options = list(lengthMenu = c(5, 10, -1), pageLength = 5))
    
    output$jersey_wage = renderPlotly({
        filtered = na.omit(data) %>% filter(League == input$leagueInput) %>% group_by(Jersey, Preferred.Foot) %>% summarise(value = mean(Wage))
        
        p = ggplot(data = as.data.frame(filtered), aes(x=Jersey, y=value)) + geom_bar(stat="identity") + 
            ylab("Wage") + theme(legend.position="bottom", plot.title = element_text(size=15, face="bold")) + 
            theme(axis.text.x = element_text(angle=90, hjust=1))
        
        ggplotly(p)
    })
    
    output$position_wage = renderPlotly({
        filtered = na.omit(data) %>% filter(League == input$leagueInput) %>% group_by(Position, Preferred.Foot) %>% summarise(value = mean(Wage))
        
        p = ggplot(data = as.data.frame(filtered), aes(x=Position, y=value)) + geom_bar(stat = "identity") +
            ylab("Wage") + theme(legend.position = "bottom", plot.title = element_text(size=15, face="bold")) +
            theme(axis.text.x = element_text(angle=90, hjust=1))
        
        ggplotly(p)
        
    })
    
    output$age_wage = renderPlotly({
        filtered = na.omit(data) %>% filter(League == input$leagueInput)
        
        p = ggplot(data = as.data.frame(filtered)) + geom_point(aes(x=Age, y=Wage, text=paste("Name", Name)), size = 2) + ylab("Wage") +
            xlab("Age") + theme(legend.position = "bottom", plot.title = element_text(size=15, face="bold"))
        
        ggplotly(p, tooltip = c("text", "x", "y"))
    })

}

shinyApp(ui, server)

