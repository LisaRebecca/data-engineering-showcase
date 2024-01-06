# Feasibility Assessment: Can the Data answer the Project's Main Question?

## Result
The research question can be answered by only using the present datasources generated in the data pipeline.

## Assessment

### Main Question
Which routes between German cities are the fastest by car (in comparison to travel by train) and should be electrified for a "quick win" (compared to new train tracks) in climate action?

### Information Contributed by Dataset 1 (Connections-Dataset)
Dataset 1 contains entries about connections between cities, and describes these trips between cities regarding travel time, travel mode, distance.

### Approach

Dataset 1 allows to compute the difference in travel times by car vs. by train on the same route (same destination and start). By sorting the deviations, we can find out which routes are the most disadvantageous and should be electrified first.

### Test of the Approach
The approach could be validated in the notebook "feasibility_assessment.ipynb".

### Additional Information
In addition to the main question, the datasets 1-3 can also answer the following questions:

- How well are german highways covered by ev chargers?
- Which districts are lagging behind in development?
- Which districts are exceptionally well-covered in ev-chargers?
- Which states are well-electrified and which lag behind?

This status-quo can be the basis for making recommendations about the most sensible locations to place new ev chargers. 
