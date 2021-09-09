# **Workplan**

## **Introduction**

The following document outlines a high level workplan I suggest following to develop a generic analytics dashboard to visualize key statistics, trends, and patterns around survey data.

The proposed workplan is designed to meet the technical and business requirements highlighted in the "DS Exercise for Juan Jose Roesel Interview" document and to answer the following questions:

* *What language characteristics distinguish these themes?*

* *What kind of visualizations could aid the analyst’s understanding of the language that distinguishes these themes?*

* *What kind of visualizations will help analysts to communicate their findings with our clients?*


## **Workplan structure**
The workplan document contains the following sections:

* EDA and key insights
* Technical approaches
* High-level architecture
* Timeline


## **EDA and Key Insights**

I conducted an Exploratory Data Analysis (EDA) process (see `1-exploratory_data_analysis.ipynb`) and found some insights that could help frame the right technical approach to answer the key questions posited in the interview document.

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

In this section, we will discuss different technical approaches that could provide a compelling answer to the general question: *"What language characteristics distinguish these themes?"*, as well as to the more specific questions:

* *What kind of visualizations could aid the analyst’s understanding of the language that distinguishes these themes?*

* *What kind of visualizations will help analysts to communicate their findings with our clients?*

### **Simple and more complex approaches**

* Simple approaches (working primarily to get enough meaningful insights):
    * Text analytics:
        * Conduct basic text analytics (token frequencies, lexical density, POS tags, etc)
        * Set lexical density threshold to filter "noise" out of responses
    * Topic modeling:
        * Run LDA topic modeling to get initial overview of theme clusters
    * Sentiment analysis:
        * Use Pre-trained BERT models to compute sentiment scores on filtered text
        * Identify highest performing documents based on sentiment
    * Prepare visualizations: (Audiences: internal / external / both)
        * Text analytics - Internal
        * Intertopic Distance MAP (LDA) - Both
        * Theme distributions across documents - Both
        * Ranking of dominant themes - Both

* More complex approaches (work aimed at reducing noise in data and optimizing model performance):
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
        * Run correlation analysis to find linear relations between features and sentiment labels/scores
    * Feature engineering:
        * Create relevant features that might be useful for uncovering specific language characteristics in these clustered themes
    * Apply ML to theme labelling
        * Work with domain experts to label existing theme clusters
        * Explore with semi-supervised, weakly supervised, and active learning methods to automate theme cluster labelling

Three separate notebooks were developed to explore some of these technical approaches within the scope of this exercise:

* Text analytics: `1-exploratory_data_analysis.ipynb`
* Topic Modeling: `2-topic_modeling.ipynb`
* Sentiment analysis: `3-sentiment_analysis.ipynb`

## **High-level architecture**

While this data represents one project, such a dashboard would need to serve many different projects with different themes. 

With this request in mind, I've designed the following high-level technical architecture, combining AWS Elastic Beanstalk with serverless capabilities, NoSQL databases, and Kubernetes.

[!image architecture]("../images/architecture.png")

* *What data or other information will you need access to?*
    * IT/Engineering -  I would need access to company-wide data such as:
        * Databases contaning data from past projects
        * Data regarding platform usage and logs
    * Marketing / Sales - Get a glimpse into the marketing strategy (Account Management and Marketing Funnels) to frame our prioritization roadmap in such a way that is in alignment with their business targets
* *Who will you need to coordinate with?*
    * Naturally, this project would require cross-functional support and collaboration across different areas:
        * I expect to be working closely with Aleksandar to productize the data visualizations generated through the analytics pipeline.
        * I also would need to collaborate closely with Mark and Raman to devise an MLOPs and deployment roadmap for the POC
        * I would also value the support of fellow Data Scientists such as Scott to exchange ideas and technical approaches, as well as Malaika's vision into the product roadmap
        * Finally, the client engagement team would be our closest ally and testers
* *How will you get feedback?*
    * Internal feedback (2 layers):
        * Core: Scrum board as central repository of technical feedback
        * Extended: I would also set up a digital board (i.e., Trello) that everyone at Avalanche can use to throw in ideas on how to improve product usability
    * External feedback:
        * I would work closely with the Engineering, Data Science, and Client Engagement teams to schedule Beta tests before deploying to production
        * In the mid to long-term, I would seek collaborate with the Engineering, Data Science, and Client Engagement teams to integrate tools into the front-end that can help us get real-time feedback from customers and map their satisfaction over time.


## **Timeline**

I envision breaking down the development of this POC analytics dashboard into three main bi-weekly sprints, as follows:

### Sprint 1
* **What:** Have POC deployed in python-based web interface using Docker for testing purposes
* **How:**
    * Define core visualizations with Aleksandar, Malaika, and Client Engagement team
    * Set up app project using Django and integrate existing code
    * Set up required AWS resources
    * Develop required analytics functions
* **Inputs:**
    * Expected visualizations and insights
* **Outputs:**
    * Analytics dashboard POC deployed on Docker

### Sprint 2
* **What:** Integrate POC with existing Avalanche IT infrastructure
* **How:**
    * Integrate tech stack used
    * Integrate with Avanlanche's CI/CD pipeline
    * Integrate feedback gathered along Sprint 1
* **Inputs:**
    * Standalone POC deployed in Docker
* **Outputs:**
    * POC running in orchestation with other microservices

### Sprint 3
* **What:** Optimize processes along the ML cycle
* **How:**
    * Fine-tune existing ML models
    * Establish de-noising methods within robust text preprocessing pipelines
    * Conduct experiments to measure model performances
    * Standardize CI/CD processes within the scope of model training, development, and deployment
* **Inputs:**
    * POC running in orchestation with other microservices
* **Outputs:**
    * Analytics Platform v1.0
    


