# rotten-stars
Scapes audience reviews from Rotten Tomatoes, so that you can check their math.

# Example

Find the URL of the movie you're interested in. For example, [The Last Jedi](https://www.rottentomatoes.com/m/star_wars_the_last_jedi)'s URL is: `https://www.rottentomatoes.com/m/star_wars_the_last_jedi`. Note the text past the last `/`. That's the "identified" that Rotten Tomatoes is using for their reviews.

```
 > rotten-stars.py star_wars_the_last_jedi
```

Should give output like

```
------------------------------------------------------------ Summary

n-reviews:         1018
n-pages:           51
review average:    1.258,  i.e.,  25.2, which is  16.9%, (scaled to range [0-100]%)
non-1star average: 1.909,  i.e.,  38.2, which is  22.7%, (scaled to range [0-100]%)
Histogram
   0.5 stars: 470
   1.0 stars: 217
   1.5 stars: 90
   2.0 stars: 73
   2.5 stars: 25
   3.0 stars: 12
   3.5 stars: 9
   4.0 stars: 16
   4.5 stars: 12
   5.0 stars: 60
```

# About Rotten Tomatoes Rating System

The audience gives ratings from 0.5 stars to 5 stars. These are then converted into a "percentage liked". I'm not sure what math Rotten Tomatoes is using, but it's obviously been goosed to boost the perceptions of movies. It looks like they remove 0.5 star reviews, and multiply the average to get a number between `[20..100]`. But there's a floor of 20%! Also note that people disproportionatly give 0.5-star and 5-star reviews. 

The scaled range takes the average, and reports it as a percentage, where 0.5-stars is 0% and 5-stars is 100%. This is a fairer way to report "percentage liked it".

