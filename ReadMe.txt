Running - 
Create a localhost. 
python -m SimpleHTTPServer
The localhost will use index.html as the home page. index.html creates an Iframe with source as index1.html which presently has the last run 1000 iterations data. (Also stored as Answer.html for backup)
If you want to test the code - you can just the run code and open local host on a browser. The graph will keep updating (as the recommender system write a new index1.html everytime it generates a new recommendation). 
The index.html refreshes itself every 2 seconds which is the same amount of sleep for each iteration. You can remove the time.sleep(2) from code, if you dont want to see the change in each recommendation.
The system requires the c3 Javascript library. Please keep in-place. 



The graph represents three sets of data.
The green line for distance. The values are multiplied by 10 so that one can see them significantly.
The orange line is the ratings. It is also multiplied by 10. And this line keeps changing with each refresh(well thats reequired)
The blue bar indicates the number of times I go to the restaurant till that particular iteration. This is NOT multiplied by 10.
The X-values are 0 to 14 indicating the restaurants A to O.

From the graph its easy to infer the correlation between distance, rating and the frequency.




The methodology is as follows: (You can find inline comments in code as well)
1. WE have ratings matrix (user-rating matrix)
2. We have co-ordinates of restaurants. ( I assume my home at (0,0)). Calculate the restaurant.
3. From the user -ratings I calculate a item-item similarity and create a similarity matrix.
4. The top similarities of each item - contribute and become the neighborhood of the corresponding item.
5. Based on the neighborhood I calculate values for the missing items for "you" only as we want the ratings only for me.
6. Now the distance is mapped to 5 values. 
	If distance > 4 units - assign 0
	If distance between 2 and 4 - assign 0.25
	If distance between 1 and 2 - assign 0.5
	If distance between 0.5 and 1 - assign 0.75
	If distance between 0 and 0.5 - assign 1
7. Add the rating and distance parameter. The eqn will be like 
	Rating + f(distance)
8. Now the restaurant with highest score will be recommended.
9. Get a random number between 1 and 5 (python's default implementation)
10. Assign the random number as the new rating for the resturant. But not directly. New rating will be ((prev_avg*freq)+rand)/(freq+1)
11. The new rating will be considered from next iteration onwards


Issue I find -
1. If the random number in every iteration somehow is on higher end for initial iterations - the recommended restaurant each time goes on repeating. which will lead to bias.
Solution - If i see a restaurant being recommended for 3rd time in row, then I choose the second best recommendation. (which is reality as well. You won't go to the same restaurant more than 2 times.

2. When I added the above solution - the first issue occurs again but this time if the same happens to the two restaurants. (Repeatition of recommendations)


Observation - Even when the issue occurs - still we see that it favours the higher rating and lesser distance. So still good as per the requirements.

The issue wouldn't occur in real life as we will have various parameters to choose a restaurant.