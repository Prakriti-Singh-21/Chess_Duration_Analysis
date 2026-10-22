# Decoding Chess Game Duration & Chess Opening family Dynamics

**CMSE 830-001 Midterm Project**  
**Student:** Prakriti Singh 
**Instructor:** Dr. Jie Hou  
**Institution:** Michigan State University  

## 📋 Table of Contents
1. [Project Overview & Narrative Context](#-project-overview--narrative-context)
2. [Dataset Quality Assessment & Variable Specifications](#-dataset-Quality--variable-specifications)
3. [Data Preparation & Transformation ](#-data-preparation--transformation)
4. [Exploratory Data Analysis & Statistical Findings](#-exploratory-data-analysis--statistical-findings)
5. [Interactive Streamlit Application](#-interactive-streamlit-application)
6. [Repository Organization & Directory Structure](#-repository-organization--directory-structure)
7. [Environment Setup & Reproduction Guide](#-environment-setup--reproduction-guide)
8. [Generative AI Disclosure](#-generative-ai-disclosure)

---

## 📌 Project Overview & Narrative Context

In competitive chess, players dedicate significant preparation to memorizing "opening book theory"— and have established, optimal move sequences analyzed over centuries. A central debate among coaches, analysts, and players is whether committing to deep opening theory translates into longer, structurally stable games, or if game duration is predominantly dictated by player tactical competence and blunder avoidance. My maian question of analysis is 'What affects duration of chess game?'

### Core Research Questions 
1. **EDA 1**
Does memorizing and playing deeper opening theory (`opening_ply`) prolong actual game duration (`turns`)?
2. **EDA 2**
 Is game duration primarily driven by opening selection or by player skill level (avg_rating / skill_tier)?


 ### Intended Audience
* **Chess Coaches & Instructors:** To guide recommendation based on player of the Elo tiers rather than overemphasizing deep opening memorization for beginners.
* **Competitive Players:** To provide empirical expectations on game length and blunder dynamics across rating classes.
* **Sports & Gaming Data Analysts:** Demonstrating interactive exploratory data visuaulisation for comparison.


---

## 📊 Dataset Quality Assessment & Variable Specifications

* **Data Source:** Lichess Open Dataset (Chess data set).(https://www.kaggle.com/datasets/datasnaek/chess)
* **Sample Size:** $n = 8,946$ total filtered games ($7,524$ matches categorized across the three core skill tiers).
* **Observation Unit:** Individual completed online chess match.

### Key Variable Definitions
| Variable Name | Data Type | Domain / Analytical Definition | Transformation Status |
| :--- | :--- | :--- | :--- |
| `id` | Categorical / String | Unique alphanumeric hash for each match observation. | Raw Metadata |
| `turns` | Numerical (Integer) | Total count of individual player half-moves (**plies**). | Raw Target Variable |
| `full_rounds` | Numerical (Float) | Total full chess rounds calculated as $\text{turns} / 2$. | Derived Feature |
| `opening_ply` | Numerical (Integer) | Number of initial moves following strict "book" theory. | Primary Predictor |
| `white_rating` | Numerical (Integer) | Elo rating score of the White player. | Raw Feature |
| `black_rating` | Numerical (Integer) | Elo rating score of the Black player. | Raw Feature |
| `avg_rating` | Numerical (Float) | Mean rating of both players: $(\text{white\_rating} + \text{black\_rating}) / 2$. | Derived Feature |
| `skill_tier` | Categorical | Binned rating class: **Beginner** ($<1400$), **Intermediate** ($1400-1800$), **Advanced** ($1800+$). | Engineered Category |
| `opening_family` | Categorical | Standardized top-level opening system (*Ruy Lopez*, *Sicilian Defense*, etc.). | Grouped / Standardized |
| `victory_status` | Categorical | Match outcome termination method (`Mate`, `Resign`, `Out of Time`, `Draw`). | Raw Feature |
| `rated` | Boolean | Match status flag (`True` = Competitive Rated, `False` = Casual). | Core Filter |

---

## 🧹 Data Preparation & Transformation 

The data is transformed from raw match telemetry into clean tabular structures suitable for statistical aggregation and interactive rendering. All transformations and detailed analysis and Explanation about the code and visulisation are recorded in `Chess_Prakriti_Singh.ipynb`.

The final file name of cleaned data set is `chess_cleaned.csv`

```
┌────────────────────────┐     ┌──────────────────────────┐     ┌─────────────────────────┐
│ Raw Lichess CSV        │ ──> │ Feature Engineering      │ ──> │ Final Cleaned Dataset   │
│ (20,000+ Raw Rows)     │     │ - Ply-to-Turn Ratio      │     │ (n = 8,946 Filtered)    │
│                        │     │ - Avg Rating Calculation │     │ (n = 7,524 Skilled)     │
│                        │     │ - Skill Tier Binning     │     │                         │
│                        │     │ - Family Standardization │     │                         │
└────────────────────────┘     └──────────────────────────┘     └─────────────────────────┘
```

---

## 📈 Exploratory Data Analysis & Statistical Findings

### Finding 1: Bivariate Correlation Analysis ($r = 0.047$)
* **Method:** Computed Pearson correlation coefficient between theoretical depth (`opening_ply`) and game length (`turns`).
* **Result:** $r = 0.047$ across all filtered matches.
* **Interpretation:** Weak linear relationship; theoretical opening depth does not dictate total match duration. Instead, game length is driven by the pawn structure and tactical nature of the specific opening family—as demonstrated by the contrast between the Ruy Lopez (long games) and Italian Game (short games) despite both sharing similar theory depths.

### Finding 2: Skill Tier Dominates Across Opening Families
* **Method:** Faceted multi-panel bar chart comparing mean turn counts per opening family across the three engineered skill tiers.
* **Result:**
  * Beginner matches average **$48-52$ plies** (~$25$ rounds) across all openings.
  * Advanced matches average **$68-74$ plies** (~$35-37$ rounds) across all openings.
* **Interpretation:** Beginner games are significantly shorter due to early blunder-induced resignations, while advanced games are systematically longer due to positional defense and endgame maneuvering. Hence, player rating level is a far stronger predictor of game duration than the opening choice itself.​

---

## 💻 Interactive Streamlit Application

The web dashboard (`app.py`) is organized in a  format that enables the user with multi-dimensional data exploration:

* **Sidebar Filtering Engine:** Dynamic toggles for Rated vs. Casual status, Skill Tier subsetting, and Opening Family focus.
* **Performance Caching:** Utilizes Streamlit `@st.cache_data` decorators to store dataset transformations in memory, providing sub-second re-rendering during filter updates.
* **Interactive Visualization Layer:** Built with Altair and Plotly Express to support interactive hover tooltips, zoom/pan functionality, and dynamic legend toggling.

## 🔗 Live Application & Resources

* **Live Streamlit App:** [Chess Opening & Duration Explorer](https://chessdurationanalysis-kdqt3drbtpxemauv92rmwj.streamlit.app/)*
* **GitHub Repository:** [Prakriti-Singh-21/Chess_Duration_Analysis](https://github.com/Prakriti-Singh-21/Chess_Duration_Analysis)

## 📂 Repository Organization & Directory Structure

```text
Chess_Duration_Analysis/
├── Chess_Prakriti_Singh.ipynb  # Exploratory Data Analysis & statistical modeling
├── README.md                   # Comprehensive project documentation & live links
├── app.py                      # Production Streamlit multi-tab dashboard app
├── chess_cleaned.csv           # Preprocessed dataset with engineered features
├── games.csv                   # Raw Lichess source telemetry dataset
└── requirements.txt            # Python operational dependencies & versions
```

----

## 🚀 Environment Setup & Reproduction Guide


### Prerequisites
* Python 3.9+
* `pip` package manager

### 1. Clone the Repository
```bash
git clone [https://github.com/Prakriti-Singh-21/Chess_Duration_Analysis.git](https://github.com/Prakriti-Singh-21/Chess_Duration_Analysis.git)
cd Chess_Duration_Analysis
```

### 2. Configure Virtual Environment
```bash
# macOS / Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Launch the Local Application
```bash
streamlit run app.py
```
The application will open automatically at `http://localhost:8501`.

---
## 🤖 Generative AI Disclosure 

**Tool / version:** Gemini 4.0 

**What I asked it to help with:** I asked AI, to help me build and strucure of the README document, and construct Github repsitory

**How I checked or verified the response:** I gave mutiple promt in diffrent ways 

**My own contribution / interpretation:** I brainstromed to understand what it was conveying and build my understanding and made the project accordingly