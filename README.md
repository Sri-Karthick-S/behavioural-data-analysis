# Music, Mood and Misconceptions

A data analysis project that explores how music listening habits relate to self-reported mental health conditions including anxiety, depression, insomnia, and OCD.

The project uses survey data from Kaggle and presents findings through an interactive dashboard built with R Shiny and flexdashboard.

Live app: https://r9o3o0-sri0karthick-selvam.shinyapps.io/Music_mood_misconception/

---

## Project Overview

The central question this project tries to answer is: do music listening habits (genre, platform, hours, and perception) have any measurable relationship with mental health outcomes?

To answer this, the project goes through three stages. First, the raw survey data is cleaned and prepared using Python. Then exploratory data analysis is performed to find patterns. Finally, the findings are presented in an interactive R Shiny dashboard with three sections.

---

## Dashboard Sections

**Understanding the Audience**
Covers who the listeners are, which age groups listen the most, what genres they prefer, which streaming platforms they use, and whether they listen while working.

**Genre and Wellness Patterns**
Explores how different music genres relate to mental health indicators. Users can switch between anxiety, depression, insomnia, OCD, and a combined distress score to see how each metric varies by genre and listening duration.

**Perception vs Reality**
Looks at whether people accurately assess how music affects their mental health. The key finding here is that 28.4% of respondents show a mismatch between their belief about music's effect and their actual distress level.

---

## Key Finding

28.4% of listeners either believed music improved their mental health while showing high distress scores, or believed it worsened their health while showing low distress scores. This suggests a notable gap between perception and reality when it comes to music and mental wellbeing.

---

## Project Structure

```
Music_mood_misconception/
|-- app.R                    # R Shiny dashboard (flexdashboard)
|-- eda_music_mental_health.py  # Python EDA and preprocessing script
|-- data/
|   |-- mxmh_survey_results.csv   # Original dataset from Kaggle
|   |-- mxmh_cleaned.csv          # Cleaned dataset used by the dashboard
|-- screenshots/
|   |-- understanding_audience.png
|   |-- genre_wellness.png
|   |-- perception_reality.png
|-- README.md
```

---

## How to Run Locally

**Prerequisites**

R packages required:
- tidyverse
- plotly
- flexdashboard
- shiny
- htmltools

Python packages required (for preprocessing):
- pandas
- numpy
- matplotlib
- seaborn
- scipy

**Steps**

1. Clone the repository
2. Place `mxmh_survey_results.csv` inside the `data/` folder
3. Run the Python script to generate the cleaned dataset:
   ```
   python eda_music_mental_health.py
   ```
4. Open `app.R` in RStudio and click Run App, or run from the terminal:
   ```
   Rscript -e "rmarkdown::run('app.R')"
   ```

---

## Dataset

The dataset is the Music and Mental Health Survey Results collected by Catherine Rasgaitis and published on Kaggle. It contains responses from 736 participants covering their music preferences, listening habits, and self-reported scores for anxiety, depression, insomnia, and OCD.

Source: https://www.kaggle.com/datasets/catherinerasgaitis/mxmh-survey-results

---

## Screenshots

**Understanding the Audience**
![Understanding the Audience](screenshots/understanding_audience.png)

**Genre and Wellness Patterns**
![Genre and Wellness](screenshots/genre_wellness.png)

**Perception vs Reality**
![Perception vs Reality](screenshots/perception_reality.png)

---

## References

Rasgaitis, C. (2022). Music and Mental Health Survey Results [Dataset]. Kaggle.
https://www.kaggle.com/datasets/catherinerasgaitis/mxmh-survey-results

Rasgaitis, C. (2022). Music and Mental Health EDA Notebook. Kaggle.
https://www.kaggle.com/code/catherinerasgaitis/music-mental-health-eda

Monfared, M. (2022). Mental Health and Music Relationship Analysis EDA Notebook. Kaggle.
https://www.kaggle.com/code/melissamonfared/mental-health-music-relationship-analysis-eda
