---
layout: posts
title: "Linear Regression from Scratch (using Linear Algebra)"
date: 2017-04-08
---
A few weeks ago I posted a brief tutorial on linear algebra. It's hard
to appreciate how fundamental linear algebra is for statistics and
machine learning, especially since the most basic algorithms can be
generated using a single line of code in R. My goal here is to
demonstrate the relationship between linear algebra and the workhorse of
machine learning: linear regression.

Linear Regression
=================

And what a workhorse it is. Frankly, any psychology paper that
**doesn't** use linear regression at some point probably just uses
t-tests or chi-squares. It is freaking everywhere.

So what is it? Well, say we have some data on ice cream sales and local
weather.

    sales <- c(800, 1200, 1600, 2000, 1300, 1450, 900)
    temp <- c(65,   74,   85,   90,   77,   82,   68)
    plot(temp,sales)

![](https://ljbaker.github.io/images/regression-from-scratch_1.png)

Now, it doesn't take a statistical savant to see there exists some
relationship between temperature and ice cream sales. Moreover, that
relationship seems fairly linear: one value increases as the other
increases.

Linear regression is the fitting of a line to a plan of values. There
are two goals to be had here, depending on your theoretical slant. From
the viewpoint of a statistician, we can investigate the fit of the line
to the data to understand the strength of the relationship between two
or more variables. In the ice cream scenario, a statistician would be
interested in the effect of temperature on ice cream sales. From a
machine learning standpoint, we can use the line of best fit to predict
future sales depending on proposed future temperatures. Say the weather
calls for a 95 degree scorcher -- what can we estimate our sales to be?

Linear regression is trivially easy in R. I'll get that out of the way
now so we can talk about it.

    summary(lm(sales ~ temp))

    ##
    ## Call:
    ## lm(formula = sales ~ temp)
    ##
    ## Residuals:
    ##       1       2       3       4       5       6       7
    ##  31.250  26.381 -68.459 106.613  -8.576 -83.503  -3.706
    ##
    ## Coefficients:
    ##              Estimate Std. Error t value Pr(>|t|)    
    ## (Intercept) -2155.305    246.900  -8.729 0.000327 ***
    ## temp           44.985      3.176  14.164 3.16e-05 ***
    ## ---
    ## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
    ##
    ## Residual standard error: 70.41 on 5 degrees of freedom
    ## Multiple R-squared:  0.9757, Adjusted R-squared:  0.9708
    ## F-statistic: 200.6 on 1 and 5 DF,  p-value: 3.158e-05

This output tells us everything we want to know. We find a significant
effect of temperature on ice cream sales (as conducted by a t-test on the
coefficients of temperature to decide if the relationship may be due to
chance; *t*<sub>6</sub> = 14.164, *p* &lt; .001). Most people call it a
day with this output. We can also find the significance of the overall
model, fit with all the variables (including the intercept term;
*F*<sub>1, 5</sub> = 200.6, *p* &lt; .001). This is usually more
informative when comparing two models with multiple variables.
Furthermore, we have a multiple *R*<sup>2</sup> of .976, indicating that
the relationship between all factors in the model (temp and intercept)
and our predictor variable (sales) account for 97.57% of the variance.
Now, adding more factors to a model, even completely arbitrary factors,
are mathematically certain to explain more variance in a model. The
adjusted *R*<sup>2</sup> statistic this includes a penalty term to
account for the complexity of the model (i.e., number of factors
included). It is entirely possible to get a modest *R*<sup>2</sup> (say
~ .25) but an adjusted *R*<sup>2</sup> **below zero** if the model is
both complex and uninformative.

However, we can also delve deeper using R. For instance, we also find
the intercept and slope of the line that best fits between all points on
our plane.

    coef(lm(sales ~ temp))

    ## (Intercept)        temp
    ## -2155.30523    44.98547

These are exactly like you remember from middle school. The *intercept*
pinpoints the value of *y* when *x* is 0. In this case, our intercepts
states the expected sales at temperature = 0 are -$2155. We should
probably steer clear of selling ice cream in January then.

The coefficient of a variable indicates the *slope* of the line as *x*
increases. So the coefficient of temperature indicates that for each
degree increase in temperature, sales increase by $44.99.

We can plot a line according the slope and intercept to see the
prediction of our model

    plot(temp,sales)
    abline(coef(lm(sales~temp)))

![](https://ljbaker.github.io/images/regression-from-scratch_2.png)

This is nice and all, but we're putting a lot of faith in someone else's
code. Getting the results of a linear regression are not that difficult
with a little linear algebra -- let's take things apart and see how it
ticks.

From Scratch
------------

To start, how do we fit a line to these points in the first place? The
idea is to find the line with the least distance to each point. This is
calculated using the **residual sum of squares (RSS)**. The RSS is a
function of the coefficient weights, , on *x* and *y*, and is calculated
as

*R**S**S*(*β*)=*Σ*<sub>*i*</sub>(*y*<sub>*i*</sub> − *β**x*<sub>*i*</sub>)<sup>2</sup>

which in code, works like:

    rss <- function(beta,x,y){
      squares <- rep(0,length(x))
      for (i in 1:length(x)){
       squares[i] = (y[i] - beta*x[i])^2
      }
      return(sum(squares))
    }

Basically, we're looking for the that when multiplied by the *x* value
gets as closed to fitting a straight line as possible. Thus the goal is
to minimize the residual sum of squares. We can do this by arbitrarily
plugging-and-chugging through candidate betas...

    rss(0,temp,sales)

    ## [1] 13242500

    rss(44.9,temp,sales)

    ## [1] 32343171

    rss(60,temp,sales)

    ## [1] 77093300

...but this is obviously not a great idea. We can instead find
algorithmically by differentiating *R**S**S* with respect to and setting
it qual to 0. This results in:

$\\hat{\\beta} = (x^Tx)^{-1}x^Ty$

We can write this down in R as

    min.beta <- function(X,y){
      beta.hat <- solve(t(X)%*%X)%*%t(X)%*%y  
      return(beta.hat)
    }

But hold on a sec! This model does not include an intercept term, and
therefore assumes an intercept at the origin (0,0). We already know this
isn't the case. To calculate an intercept, *β*<sub>0</sub>, we have to
declare a vector to find the value of beta with *x* set to 1, or
basically the weight required to move a straight line to the the average
value of *y*. We simple add a vector of ones to our factor matrix, *X*.

    intercept <- rep(1,length(temp)) #vector of ones
    X <- cbind(intercept,temp) #matrix of factors (intercept & friends)
    y <- sales

We then plug into our minimum RSS function to get

    beta.hat <- min.beta(X,y)
    beta.hat #our weights for intercept and temp

    ##                  [,1]
    ## intercept -2155.30523
    ## temp         44.98547

$\\hat{y}$ is equivalent to the classic formula for plotting a line you
learned in middle school, *y* = *m**x* + *b*.

    y.hat = beta.hat[1] + beta.hat[2]*temp #intercept + slope*variable
    # which we can express in linear algebraic terms as
    y.hat <- X%*%beta.hat
    # and show they are equal
    X%*%beta.hat == beta.hat[1] + beta.hat[2]*temp

    ##      [,1]
    ## [1,] TRUE
    ## [2,] TRUE
    ## [3,] TRUE
    ## [4,] TRUE
    ## [5,] TRUE
    ## [6,] TRUE
    ## [7,] TRUE

Again, we can visualize this linear relationship.

    # ploting x and y
    plot(temp,sales)
    # the line of best fit (intercept and slope)
    abline(beta.hat)
    # the points predicted by the model for each value of temperature
    points(temp,y.hat,col="red")

![](https://ljbaker.github.io/images/regression-from-scratch_3.png)

We can calculate the error of the model as the difference between the
values of *y* and our predicted values, $\\hat{y}$, via the sum of
squared errors

$SSE = \\Sigma(y - \\hat{y})^2$

We then estimate the variance of the model using the unbiased estimator,
degrees of freed,*n* − *ν*, where are the number of model parameters. We
have two parameters, slope and intercept, so we have 7 − 2 degrees of
freedom.

$MSE = \\frac{\\Sigma(y - \\hat{y})^2}{n-2} = 4957.122$

This is known as the **mean squared error** and captures the amount of
variance between the predicted and observed values of *y*. However, the
mean squared error is unstandardized, meaning we have no way to gauge
whether nearly 5000 points of error is a good thing or a bad thing.
Fortunately, we can calculate *R*<sup>2</sup> just as simply. As
mentioned above, *R*<sup>2</sup> is a standardized metric of fit ranging
from 0-1 that can be interpreted as the proportion of variance explained
by our model. *R*<sup>2</sup> is calculated as

$R^2 = 1- \\frac{\\Sigma(y - \\hat{y})^2}{\\Sigma(y - \\bar{y})^2} = 97.57$

We can of course do all of this in a few lines of R.

    sse <- sum((y - y.hat)^2)
    sse

    ## [1] 24785.61

    mse = sse/(length(y)-2)
    mse

    ## [1] 4957.122

    r.squared <- 1- ((sum((y-y.hat)^2))/(sum((y-mean(y))^2)))
    r.squared

    ## [1] 0.9756834

Linear Regression "From A Box"
-----------------------------

R does all of these operations trivially easily, thankfully.

    # We first declare our model as y ~ x
    fit1 <- lm(sales ~ temp)

    # our betas
    coef(fit1)

    ## (Intercept)        temp
    ## -2155.30523    44.98547

    # double checking our calculation of beta
    round(beta.hat,2) == round(coef(fit1),2)

    ##           [,1]
    ## intercept TRUE
    ## temp      TRUE

    # double checking our our predicted values, y.hat
    round(y.hat,2) == round(fit1$fitted.values,2)

    ##      [,1]
    ## [1,] TRUE
    ## [2,] TRUE
    ## [3,] TRUE
    ## [4,] TRUE
    ## [5,] TRUE
    ## [6,] TRUE
    ## [7,] TRUE

    # plotting the data with the model
    plot(temp,sales)
    abline(coef(fit1)[1],coef(fit1)[2])
    points(temp,fit1$fitted.values,col="red")

![](https://ljbaker.github.io/images/regression-from-scratch_4.png)

Complete Demonstration
======================

Alright, let's play with some real data! I'm using a dataset available
by default with R: Motor Trend's road test evaluations from 1974. We
can flex our linear algebra muscles to see which factors most influence
fuel consumption. Importantly, this requires us to extend linear
regression to multiple factors.

    data(mtcars)
    attach(mtcars)
    dimnames(mtcars)

    ## [[1]]
    ##  [1] "Mazda RX4"           "Mazda RX4 Wag"       "Datsun 710"         
    ##  [4] "Hornet 4 Drive"      "Hornet Sportabout"   "Valiant"            
    ##  [7] "Duster 360"          "Merc 240D"           "Merc 230"           
    ## [10] "Merc 280"            "Merc 280C"           "Merc 450SE"         
    ## [13] "Merc 450SL"          "Merc 450SLC"         "Cadillac Fleetwood"
    ## [16] "Lincoln Continental" "Chrysler Imperial"   "Fiat 128"           
    ## [19] "Honda Civic"         "Toyota Corolla"      "Toyota Corona"      
    ## [22] "Dodge Challenger"    "AMC Javelin"         "Camaro Z28"         
    ## [25] "Pontiac Firebird"    "Fiat X1-9"           "Porsche 914-2"      
    ## [28] "Lotus Europa"        "Ford Pantera L"      "Ferrari Dino"       
    ## [31] "Maserati Bora"       "Volvo 142E"         
    ##
    ## [[2]]
    ##  [1] "mpg"  "cyl"  "disp" "hp"   "drat" "wt"   "qsec" "vs"   "am"   "gear"
    ## [11] "carb"

Checking out the help documentation for mtcars, we see that we have the
following data to work with:

1.  mpg Miles/(US) gallon
2.  cyl Number of cylinders
3.  disp Displacement (cu.in.)
4.  hp Gross horsepower
5.  drat Rear axle ratio
6.  wt Weight (1000 lbs)
7.  qsec 1/4 mile time
8.  vs V/S
9.  am Transmission (0 = automatic, 1 = manual)
10. gear Number of forward gears
11. carb Number of carburetors

For the sake of demonstration, let's predict a continuous variable from
other continuous variables. How about mpg by assorted factors?

    y <- matrix(mpg)
    intercept <- rep(1,length(mpg))
    X <- cbind(intercept,cyl,disp,hp,drat,wt,qsec)

    # remembering our function for calculating the smallest betas
    min.beta <- function(X,y){
      beta.hat <- solve(t(X)%*%X)%*%t(X)%*%y  
      return(beta.hat)
    }
    beta.hat <- min.beta(X,y)
    # we find our estimates of intercept and beta weights
    beta.hat

    ##                  [,1]
    ## intercept 26.30735899
    ## cyl       -0.81856023
    ## disp       0.01320490
    ## hp        -0.01792993
    ## drat       1.32040573
    ## wt        -4.19083238
    ## qsec       0.40146117

    # and then we find the predicted values of y given these factors
    y.hat <- X%*%beta.hat
    # which is the same as expressing
    y.hat =  beta.hat[1] + beta.hat[2]*cyl + beta.hat[3]*disp +
              beta.hat[4]*hp + beta.hat[5]*drat + beta.hat[6]*wt +
              beta.hat[7]*qsec
    y.hat == X%*%beta.hat

    ##       [,1]
    ##  [1,] TRUE
    ##  [2,] TRUE
    ##  [3,] TRUE
    ##  [4,] TRUE
    ##  [5,] TRUE
    ##  [6,] TRUE
    ##  [7,] TRUE
    ##  [8,] TRUE
    ##  [9,] TRUE
    ## [10,] TRUE
    ## [11,] TRUE
    ## [12,] TRUE
    ## [13,] TRUE
    ## [14,] TRUE
    ## [15,] TRUE
    ## [16,] TRUE
    ## [17,] TRUE
    ## [18,] TRUE
    ## [19,] TRUE
    ## [20,] TRUE
    ## [21,] TRUE
    ## [22,] TRUE
    ## [23,] TRUE
    ## [24,] TRUE
    ## [25,] TRUE
    ## [26,] TRUE
    ## [27,] TRUE
    ## [28,] TRUE
    ## [29,] TRUE
    ## [30,] TRUE
    ## [31,] TRUE
    ## [32,] TRUE

    # it's difficult to plot multivariate spaces
    # for now, it's simple enough to demonstrate that y.hat
    # approximates y
    plot(y.hat,y)

![](https://ljbaker.github.io/images/regression-from-scratch_5.png)

    # comparing to R's out of the box regression
    fit2 <- lm(mpg ~ cyl + disp + hp + drat + wt + qsec)

    # we got the same betas
    round(coef(fit2),2) == round(beta.hat,2)

    ##           [,1]
    ## intercept TRUE
    ## cyl       TRUE
    ## disp      TRUE
    ## hp        TRUE
    ## drat      TRUE
    ## wt        TRUE
    ## qsec      TRUE

    #and the same predictions of y
    round(fit2$fitted.values,2) == round(y.hat,2)

    ##    1    2    3    4    5    6    7    8    9   10   11   12   13   14   15
    ## TRUE TRUE TRUE TRUE TRUE TRUE TRUE TRUE TRUE TRUE TRUE TRUE TRUE TRUE TRUE
    ##   16   17   18   19   20   21   22   23   24   25   26   27   28   29   30
    ## TRUE TRUE TRUE TRUE TRUE TRUE TRUE TRUE TRUE TRUE TRUE TRUE TRUE TRUE TRUE
    ##   31   32
    ## TRUE TRUE
