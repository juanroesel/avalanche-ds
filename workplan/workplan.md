# **Workplan**

## **Introduction**

The following document outlines a high level workplan I suggest following to develop a generic analytics dashboard to visualize key statistics, trends, and patterns around survey data.

The proposed workplan is designed to meet the technical and business requirements highlighted in the "DS Exercise for Juan Jose Roesel Interview" document, which were stated as follows:

**Key questions:**

* What kind of visualizations could aid the analyst’s understanding of the language that distinguishes these themes?

* What kind of visualizations will help analysts to communicate their findings with our clients?

**Approaches to discuss:**
* Simple and more complex approaches
* Human interaction and labeling
* Machine learning
* Advanced NLP techniques

**Technical architecture and scalability:**
While this data represents one project, such a dashboard would need to serve many different projects with different themes. 

Please prepare a draft work plan for how you would approach the task of making such a dashboard usable for all of our analysts regardless of the project they are on.

* What data or other information will you need access to?
* Who will you need to coordinate with?
* How will you get feedback?

## Workplan structure
The workplan document contains the following sections:

* EDA and key insights
* Technical approaches
* High-level architecture and scalability
* Timeline


## **EDA and Key Insights**

I conducted an Exploratory Data Analysis process (see `1-exploratory_data_analysis.ipynb`) and found some insights that could help frame the right technical approach to answer the key questions posited in the interview document.

### General insights
* There's a total of 4,608 responses and all have been fully recorded.
* There are no missing values in the dataset.

### Insights on binary features
* All of the features in the dataset are dominated by the `False` value, suggesting a deeper dive into the nature of these responses. 
* However, the features with the least False might shed some light on the kinds of words and topics that might resonate positively with people. Here's the top 5 of such features along with their respective `True` count:
    * *Believes Science And Experts*: 759
    * *Has a plan to protect Americans from COVID*: 725
    * *Cares about Americans*: 454
    * *Cares about all Americans*: 478
    * *Taking COVID Seriously*: 369

### Insights on the open text feature
* There are a total of 50,673 tokens across all documents (open-ended responses).
* The average tokens per document is 11, which suggests that responses are rather short.
* Using SpaCy's `LanguageDetector()` object, an estimated 11% of overall documents (about 516) were found to be in a different language than English. However, after taking a deeper look into the `other_lang_sents` list, most of them were found to be in English but holding one or several of the following characteristics:
    * Tokens without any lexical sense (i.e., "pk")
    * Very short phrases (between 1 and 5 tokens long) or long phrases with repeteative words (i.e., "nonoe none none none none none none none none none none none")
    * Phrases with mispelled words (i.e., "He *hasa* plan" or "*Donal tramp*")
    * Sentences in other languages (i.e., Spanish)
* Digging further into this phenomena, we can see a considerable difference (over 5X) in type/token ratios between both categories (English vs Other)
    * Type-token ratio English: 0.0641
    * Type-token ratio Other: 0.371 
* Hence, documents bucketed into the "Other" category might contain noise and should be looked at in more detail before deciding to incorporate them further into the analysis.
* Lastly, the average lexical density across all documents is 10.7%, which means that the proportion of open-class words to all words is relatively low. This suggests that the open-ended responses recorded are not very expressive.


## **Technical approaches**

Key question to answer: *"What language characteristics distinguish these themes?"*

**Simple and more complex approaches**
* Simple approaches (working primarily with "meaningful" text):
    * Text analytics:
        * Conduct basic text analytics (token frequencies, lexical density, POS tags, etc)
        * Set lexical density threshold to filter "noise" out of responses
    * Topic modeling:
        * Run LDA topic modeling to get initial overview of theme clusters
    * Sentiment analysis:
        * Use Pre-trained BERT models to compute sentiment scores on filtered text
        * Run correlation analysis to find linear relations between features and sentiment labels/scores
    * Feature engineering:
        * Create relevant features that might be useful for uncovering specific language characteristics in these clustered themes
    * Prepare visualizations:
        * 

* More complex approaches:
    * Text preprocessing:
        * Use rule-based methods to identify relevant linguistic phenomena (i.e., word elongation, code-switching, mispellings)
        * Use specialized tools such as [ekphrasis](https://github.com/cbaziotis/ekphrasis) which normalizes and provides annotation for these special features
        * Experiment with fine-tuned Neural Machine Translator to convert non-English text to English
    * Sentiment analysis model fine-tuning
        * Create manually annotated dataset of 500 examples
        * Calculate model accuracy scores
        * Fine-tune BERT sentiment model using Active Learning methods
        * Do fine-grained sentiment analysis with SVM Ranking
        * Test the Pollyanna hypothesis (i.e., natural bias towards positive comments)
    * Apply ML to theme labelling
        * Work with domain experts to label existing theme clusters
        * Explore with semi-supervised, weakly supervised, and active learning methods to automate theme cluster labelling

Taking into account these approaches and the possibilities they enable, I propose the following answers to the key questions posited in the interview document:

*What kind of visualizations could aid the analyst’s understanding of the language that distinguishes these themes?*

* Dashboard of linguistic phenomena
    * 
* Topic modeling dashboard
    * Intertopic Distance Map


*What kind of visualizations will help analysts to communicate their findings with our clients?*
* WordCloud including sentiment dimension
* Sentiment spectrum - Buckets of words that are highly correlated with positive sentiment
* Topic modeling dashboard
    * Intertopic Distance Map
* 


## **High-level architecture and scalability**



## **Timeline**

