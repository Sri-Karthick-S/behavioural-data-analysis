---
title: "Music, Mood & Misconceptions"
output:
  flexdashboard::flex_dashboard:
    orientation: rows
    vertical_layout: fill
runtime: shiny
---

```{r setup, include=FALSE}
library(tidyverse)
library(plotly)
library(flexdashboard)
library(htmltools)

df <- read_csv("mxmh_cleaned.csv")
```

# Understanding the Audience

**How are music listening habits (genre, platform, time, perception) related to self-reported mental health conditions (anxiety, depression, insomnia, OCD, distress)?**

## Listener Demographics {.columns}

### Which age groups are listening the most?

```{r}
p_age <- df %>%
  count(AgeGroup) %>%
  ggplot(aes(x = AgeGroup, y = n, fill = AgeGroup)) +
  geom_col() +
  labs(x = "Age Group", y = "Count") +
  theme_minimal(base_size = 10) +
  theme(legend.position = "none")

ggplotly(p_age) %>% layout(height = 200)
```

### What music do people love the most?

```{r}
top_genres_plot <- df %>%
  count(`Fav genre`) %>%
  top_n(5, n) %>%
  arrange(desc(n)) %>%
  ggplot(aes(x = reorder(`Fav genre`, n), y = n, fill = `Fav genre`)) +
  geom_col() +
  coord_flip() +
  labs(x = "Genre", y = "Count") +
  theme_minimal(base_size = 10) +
  theme(legend.position = "none")

ggplotly(top_genres_plot) %>% layout(height = 250)
```

### Where do listeners get their music from?

```{r}
p_stream <- df %>%
  count(`Primary streaming service`, sort = TRUE) %>%
  plot_ly(
    labels = ~`Primary streaming service`,
    values = ~n,
    type = "pie",
    textinfo = "label+percent",
    insidetextorientation = "auto"
  ) %>%
  layout(showlegend = FALSE)

p_stream
```

## Listening Behavior {.columns}

### Do younger people spend more time listening?

```{r}
p_hours_age <- df %>%
  ggplot(aes(x = AgeGroup, y = `Hours per day`, fill = AgeGroup)) +
  geom_boxplot(alpha = 0.6) +
  labs(x = "Age Group", y = "Hours") +
  theme_minimal(base_size = 10) +
  theme(legend.position = "none")

ggplotly(p_hours_age) %>% layout(height = 250)
```

### Are people listening to music during work?

```{r}
p_work <- df %>%
  mutate(WorkListener = ifelse(`While working` == 1, "Yes", "No")) %>%
  count(WorkListener, AgeGroup) %>%
  ggplot(aes(x = AgeGroup, y = n, fill = WorkListener)) +
  geom_col(position = "fill") +
  labs(x = "Age Group", y = "Proportion") +
  theme_minimal(base_size = 10)

ggplotly(p_work) %>% layout(height = 250)
```

# Genre and Wellness Patterns

### How do Genres relate to Distress or Wellbeing? {.columns}

```{r}
selectInput("mh_metric", "Choose Mental Health Indicator",
  choices = c(
    "Total Distress Score" = "`Total Distress Score`",
    "Anxiety"             = "Anxiety",
    "Depression"          = "Depression",
    "Insomnia"            = "Insomnia",
    "OCD"                 = "OCD"
  ),
  selected = "`Total Distress Score`"
)
```

#### Mental Health Metric by Genre

```{r}
renderPlotly({
  req(input$mh_metric)

  p_box <- df %>%
    ggplot(aes_string(x = "`Fav genre`", y = input$mh_metric, fill = "`Fav genre`")) +
    geom_boxplot(alpha = 0.7, outlier.shape = NA) +
    labs(x = "Genre", y = gsub("_", " ", input$mh_metric)) +
    theme_minimal(base_size = 10) +
    theme(legend.position = "none") +
    coord_flip()

  ggplotly(p_box)
})
```

### Emotional Patterns {.columns}

#### How is Mental Health distributed among listeners?

```{r}
renderPlotly({
  req(input$mh_metric)

  p_hist <- df %>%
    ggplot(aes_string(x = input$mh_metric)) +
    geom_histogram(binwidth = 1, fill = "#66C2A5", color = "white") +
    labs(x = gsub("_", " ", input$mh_metric), y = "Count") +
    theme_minimal(base_size = 10)

  ggplotly(p_hist) %>% layout(height = 250)
})
```

#### Does more listening time mean more (or less) distress?

```{r}
renderPlotly({
  req(input$mh_metric)

  p_time_health <- df %>%
    ggplot(aes_string(x = "`Hours per day`", y = input$mh_metric)) +
    geom_jitter(alpha = 0.3, color = "#FC8D62") +
    geom_smooth(method = "lm", se = FALSE, color = "black") +
    labs(x = "Hours Listening/Day", y = gsub("_", " ", input$mh_metric)) +
    theme_minimal(base_size = 10)

  ggplotly(p_time_health) %>% layout(height = 250)
})
```

# Perception Vs Reality

## Tab 1 {.columns}

### How do people think music affects their mental health?

```{r}
p_effects <- df %>%
  count(`Music effects`) %>%
  plot_ly(
    labels = ~`Music effects`,
    values = ~n,
    type = "pie",
    textinfo = "label+percent",
    insidetextorientation = "radial"
  ) %>%
  layout(showlegend = FALSE)

p_effects
```

### Do self-reported beliefs match mental health scores?

```{r}
p_effect_score <- df %>%
  ggplot(aes(x = `Music effects`, y = `Total Distress Score`, fill = `Music effects`)) +
  geom_boxplot(alpha = 0.7) +
  labs(x = "Music Impact Perception", y = "Total Distress Score") +
  theme_minimal(base_size = 10) +
  theme(legend.position = "none")

ggplotly(p_effect_score) %>% layout(height = 250)
```

### What music do believers of 'help' or 'hurt' listen to?

```{r}
top_genres_by_effect <- df %>%
  count(`Fav genre`, `Music effects`) %>%
  group_by(`Music effects`) %>%
  top_n(5, n) %>%
  ungroup() %>%
  ggplot(aes(x = reorder(`Fav genre`, n), y = n, fill = `Music effects`)) +
  geom_col(position = "dodge") +
  coord_flip() +
  labs(x = "Top Genres", y = "Count", fill = "Perception Group") +
  theme_minimal(base_size = 10)

ggplotly(top_genres_by_effect) %>% layout(height = 250)
```

## Tab 2 {.columns}

### Do long listening hours influence beliefs about music?

```{r}
p_hours_perception <- df %>%
  filter(!is.na(`Music effects`)) %>%
  ggplot(aes(x = `Music effects`, y = `Hours per day`, fill = `Music effects`)) +
  geom_boxplot(alpha = 0.6) +
  labs(x = "Perceived Effect of Music", y = "Hours of Listening per Day") +
  theme_minimal(base_size = 10) +
  theme(legend.position = "none")

ggplotly(p_hours_perception) %>% layout(height = 250)
```

### How many people misjudge music's impact on their health?

```{r}
df <- df %>%
  mutate(
    MH_Category = case_when(
      `Total Distress Score` <= 10 ~ "Low",
      `Total Distress Score` <= 20 ~ "Moderate",
      TRUE                         ~ "High"
    ),
    mismatch = case_when(
      `Music effects` == "Improve" & MH_Category == "High" ~ 1,
      `Music effects` == "Worsen"  & MH_Category == "Low"  ~ 1,
      TRUE                                                  ~ 0
    )
  )

mismatch_rate <- df %>%
  summarise(Mismatch_Percent = round(mean(mismatch, na.rm = TRUE) * 100, 1)) %>%
  pull(Mismatch_Percent)

div(
  style = "background-color:#FFE082; border-left: 5px solid #F57C00; padding: 20px; border-radius: 5px;",
  h3("Mismatch Between Belief and Score"),
  h2(paste0(mismatch_rate, "%")),
  p("Percentage of people whose perceived music impact does not match their actual distress level.")
)
```

### References

```{r}
div(
  p("Rasgaitis, C. (2022). Music and Mental Health Survey Results [Dataset]. Kaggle.",
    tags$a(href = "https://www.kaggle.com/datasets/catherinerasgaitis/mxmh-survey-results",
           "https://www.kaggle.com/datasets/catherinerasgaitis/mxmh-survey-results")),
  p("Rasgaitis, C. (2022). Music and Mental Health EDA Notebook. Kaggle.",
    tags$a(href = "https://www.kaggle.com/code/catherinerasgaitis/music-mental-health-eda",
           "https://www.kaggle.com/code/catherinerasgaitis/music-mental-health-eda")),
  p("Monfared, M. (2022). Mental Health and Music Relationship Analysis EDA Notebook. Kaggle.",
    tags$a(href = "https://www.kaggle.com/code/melissamonfared/mental-health-music-relationship-analysis-eda",
           "https://www.kaggle.com/code/melissamonfared/mental-health-music-relationship-analysis-eda"))
)
```
