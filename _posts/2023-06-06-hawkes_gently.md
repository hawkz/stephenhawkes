---
layout:     post
title:      Dirk Gently Unraveling the Data Web
date:       2023-06-09 08:30:00
summary:    Exploring Ochre with the Hawkes Process
categories: [blog, sector]
---

## A Tapestry of Connections: Weaving Data and Detective Work
In the intricate tapestry of data analysis, we use Python as our trusty magnifying glass, enabling us to spot hidden patterns and connections. Just as Dirk Gently unravels mysteries, we can untangle the complexities of our charity work by leveraging this powerful tool within Ochre. Let's embark on a journey where data becomes our partner in mystery-solving!

[Dan](https://twitter.com/dansutch) from [CAST](https://www.wearecast.org.uk/) set me the challenge of figuring out how we could get more insight from the data collected in Ochre, a platform that records updates about the projects, initiatives, programmes and mission for CAST and Catalyst. Having noodled on it a bit, I'm delighted to have stumbled onto the work named after Dr. Alan G. Hawkes (no relation, or I guess some relation somehow?) You can see it here: [The Hawkes process](https://en.wikipedia.org/wiki/Hawkes_process) I'm going to try and break it down, with a mix of how this is useful and mathsy/pythony examples, hopefully I'll be as hard to follow as Dirk Gently himself...

![Dirk Gently's desk](/img/hawkes_gently1.png)

In Dirk's world, events are like clues that lead us to unravel the mysteries of how things are connected. Just as Dirk follows a trail of clues, the Hawkes process helps us follow a trail of events and understand their hidden relationships. Let's imagine that these events are like puzzle pieces, and the Hawkes process is our magical magnifying glass that helps us fit them together.

Picture a scene where people are gathered, birds are singing, and cars are honking in a bustling city. The Hawkes process allows us to investigate how these events influence each other. For example, Dirk might notice that when people start clapping, it often leads to more birds chirping happily. Similarly, when birds chirp, it can trigger more cars to honk along the streets. Dirk's sharp detective skills help him see these connections and patterns.

Using special tools, like Dirk's detective machine, we record when events occur and their types. We feed this data into the machine, and it works its magic, just like Dirk solving a perplexing case. The machine analyzes the data and reveals the likelihood of one event causing another event, like a chain reaction of clues.

With the help of the Hawkes process, Dirk Gently can uncover the hidden connections between events. It's like peering into a web of secrets and discovering how everything is intertwined. By understanding these connections, Dirk can make predictions about what might happen next or uncover the underlying mysteries of the world.


## How do we build Dirk's Detective Machine for CAST?
Imagine that we have collected data on various events within the CAST capacity building program, such as training sessions, design hops, and deliverables shared. To uncover insights and understand the interconnectedness of these events, we can use the Hawkes process. In Python, we can utilize libraries such as `tick` or `PyHawkes` to implement the Hawkes process. Here's an example to kickstart our detective work:

```python
import tick.hawkes as hk

# Suppose we have collected event timestamps and event types
events = [1, 3, 5, 7, 9, 12, 14, 18]  # List of event timestamps
event_types = ['A', 'B', 'A', 'C', 'B', 'C', 'A', 'B']  # List of corresponding event types

# Define the Hawkes process parameters
baseline = {'A': 0.5, 'B': 0.3, 'C': 0.2}  # Baseline intensities for each event type
adjacency = [[0.1, 0.2, 0.0], [0.0, 0.1, 0.3], [0.2, 0.0, 0.1]]  # Influence matrix

# Perform inference to estimate the parameters
estimator = hk.EmpiricalLasso().fit(events, event_types)
estimated_baseline = estimator.baseline
estimated_adjacency = estimator.adjacency

# Unveil the insights from the estimated parameters
print("Original Baseline Intensities:", baseline)
print("Estimated Baseline Intensities:", estimated_baseline)
print("Original Influence Matrix:", adjacency)
print("Estimated Influence Matrix:", estimated_adjacency)
```

In this code snippet, we import the `tick.hawkes` library to access the functionality of the Hawkes process. We assume that we have collected event timestamps in the form of a list called `events` and their corresponding event types in a list called `event_types`. The next step is to define the parameters of the Hawkes process. We set the `baseline` parameter as the baseline intensities for each event type, indicating the average occurrence rate of events. The `adjacency` parameter represents the influence matrix, which quantifies the impact of one event type on another.

To estimate the parameters, we use the `fit()` method of the `hk.EmpiricalLasso` estimator from `tick.hawkes`. This estimator performs inference on the given event data and provides estimates for the baseline intensities (`estimated_baseline`) and influence matrix (`estimated_adjacency`). These estimated parameters offer valuable insights into the interconnectedness of events within our educational program.

### This can lead to 4 types of insight:
**Magnitude Comparison, Original vs. Estimated Baseline Intensities:** Helps us understand the impact of the Hawkes process on baseline intensities and the potential influence on the overall dynamics of the system. Significant changes may indicate that the Hawkes process has uncovered hidden patterns or variations in the occurrence rates of event types. 

**Ranking Comparison of Original vs. Estimated Baseline Intensities:** Comparing the original and estimated baseline intensities can provide insights into the relative importance or prominence of different event types. If the rankings of event types based on their intensities change after applying the Hawkes process, it suggests that the process has identified event types that play a more influential role within the system.

**Ranking Comparison of Original vs. Estimated Influence Matrix:** By comparing the original and estimated influence matrices, we can identify changes in the relative strengths of connections between event types. If the ranking of influence values changes, it indicates that the Hawkes process has revealed different levels of influence among event types. This comparison helps us understand the impact of the Hawkes process on the relationships and dependencies between event types.

**Pattern Comparison: Original vs. Estimated Influence Matrix:** By examining the patterns and structure of the original and estimated influence matrices, we can identify the emergence of new connections, the strengthening or weakening of existing connections, or the discovery of previously unrecognized dependencies. Changes in the pattern of influence can provide insights into the dynamics and interactions within the system, helping us uncover underlying mechanisms or causality between event types.

## Connecting the Dots: Measuring Interactions and Outcome Likelihood
In our journey to measure group interactions and uncover the likelihood of specific outcomes, we continue to rely on the Hawkes process as our detective's toolkit. Using Ochre's data and the Hawkes process, we can unravel fascinating insights that shed light on the impact of group interactions.

Let's say we want to measure the interactions between different groups involved in our project, such as Group A, Group B, and Group C. By employing the Hawkes process, we can quantify the influence of these interactions and predict the likelihood of achieving positive outcomes. Here's an example Python code snippet to guide us:

```python
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Suppose we have a DataFrame with group interactions and outcome data
df = pd.DataFrame({'Group': ['A', 'B', 'C', 'A', 'B'],
                   'Interaction': ['Collaboration', 'Knowledge Sharing', 'Planning', 'Knowledge Sharing', 'Collaboration'],
                   'Outcome': ['Good', 'Good', 'Average', 'Good', 'Average']})

# Measure the likelihood of good outcomes based on interactions
interaction_likelihood = df[df['Outcome'] == 'Good'].groupby('Interaction')['Group'].count() / df.groupby('Interaction')['Group'].count()

# Visualize the network graph of group interactions
G = nx.from_pandas_edgelist(df, 'Group', 'Interaction', create_using=nx.DiGraph())
pos = nx.spring_layout(G, seed=42)

plt.figure(figsize=(8, 6))
nx.draw_networkx(G, pos=pos, with_labels=True, node_color='lightblue', node_size=500)
plt.title('Group Interactions Network')
plt.show()
```

In this code snippet, we use the pandas library to work with the data. We assume that the group interactions and corresponding outcome data are stored in a DataFrame called `df`. The DataFrame has columns named "Group" representing the group names, "Interaction" representing the type of interaction, and "Outcome" representing the corresponding outcome, such as "Good" or "Average".

We calculate the likelihood of achieving good outcomes based on the interactions between groups. Using pandas' grouping and counting functions, we filter the data to consider only the rows with good outcomes (`df[df['Outcome'] == 'Good']`). Then, we group the filtered data by interaction type and count the occurrences of each interaction (`df.groupby('Interaction')['Group'].count()`). Dividing the count of good outcomes by the total count of interactions for each interaction type gives us the likelihood of good outcomes for that interaction.

To visualize the network graph of group interactions, we utilize the networkx library. We create a directed graph using the `from_pandas_edgelist()` function, where each group is represented as a node, and each interaction is represented as a directed edge. We then use the `spring_layout()` function to compute the positions of the nodes, and finally, use matplotlib to draw the graph. This visual representation allows us to observe the connections and interactions between different groups, aiding our understanding of the project dynamics.

## Predicting the Future: Decoding Project Progress from Status Indicators
In our quest to predict the future trajectory of projects, we turn to the power of data analysis and the Hawkes process. By leveraging historical data and status indicators, we can build predictive models that help us anticipate the progression of our projects.

Let's dive into an example Python code snippet that showcases how we can train a predictive model using the scikit-learn library:

```python
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Assume we have a dataset with project data and status indicators
df = pd.read_csv('project_data.csv')

# Prepare the data for modeling
X = df.drop(columns=['Status'])
y = df['Status']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a random forest classifier to predict project status
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Make predictions on the test set
predictions = model.predict(X_test)

# Evaluate the model's accuracy
accuracy = accuracy_score(y_test, predictions)
```

In this code snippet, we start by loading the project data and status indicators into a DataFrame called `df`. The dataset contains features related to the project (excluding the status) in the `X` variable and the corresponding project status in the `y` variable.

We then split the data into training and testing sets using the `train_test_split()` function from scikit-learn. The data is divided into 80% for training (`X_train, y_train`) and 20% for testing (`X_test, y_test`).

Next, we initialize a random forest classifier model with 100 decision trees using the `RandomForestClassifier` class from scikit-learn. We fit the model on the training data using the `fit()` method, which trains the model to learn patterns and relationships between the features and the project status.

Once the model is trained, we make predictions on the test set using the `predict()` method. The model uses the learned patterns to predict the project status based on the features of the test data.

To evaluate the performance of the model, we calculate the accuracy score by comparing the predicted project statuses with the actual statuses in the test set. The accuracy score indicates the percentage of correct predictions made by the model.

By leveraging predictive models, we gain the ability to anticipate project progress based on status indicators. This empowers us to identify potential risks, take proactive measures, and make informed decisions to ensure the successful execution of our projects.

![Dirk Gently writing Python](/img/hawkes_gently2.png)

## Case solved (maybe, but lots more to do!)
[Grabs licorice pipe to sound intelligent]
As we untangle the interconnected web of data within Ochre using the Hawkes process, we transform into data detectives, uncovering hidden patterns and insights. Hopefully this post goes a little way to demystify the technical aspects and inspire you to explore the power of data analysis in your work. It's something I've been wrestling with for a while, and I'm pleased to have a light at the end of the tunnel.

Armed with the Hawkes process, Python, and Ochre's data recording capabilities, we can optimize our programs, enhance group interactions, and start to predict project outcomes. I'm really energised by this discovery, and I'm looking forward to baking data into the decision-making processes, and paving the way for using the interconnectedness of all things to unlocking remarkable insights. Happy unraveling, measuring, and predicting!