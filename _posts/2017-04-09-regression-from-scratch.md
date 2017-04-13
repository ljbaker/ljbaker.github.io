---
title: "Linear Regression using Linear Algebra"
author: "Lewis Baker"
date: "April 8, 2017"
output: html_document
---

A few weeks ago I posted a brief tutorial on linear algebra. It's hard to appreciate how fundamental linear algebra is for statistics and machine learning, especally since the most basic algorithms can be generated using a single line of code in R. My goal here is to demonstrate the relationship between linear algebra and the workhorse of machine learning: linear regression.

# Linear Regression

And what a workhorse it is. Frankly, any psychology paper that **doesn't** use linear regression at some point probably just uses t-tests or chi-squares. It is freaking everywhere.

So what is it? Well, say we have some data on ice cream sales and local weather. 

```{r}
sales <- c(800, 1200, 1600, 2000, 1300, 1450, 900)
temp <- c(65,   74,   85,   90,   77,   82,   68)
plot(temp,sales)
```

Now, it doesn't take a statistical savant to see there exists some relationship between temperature and ice cream sales. Moreover, that relationshp seems fairly linear: one value increases as the other increases. 

Linear regression is the fitting of a line to a plan of values. There are two goals to be had here, depending on your theoretical slant. From the viewpoint of a statistician, we can investigate the fit of the line to the data to understand the strength of the relationship between two or more variables. In the ice cream scenario, a statisticitan would be interested in the effect of temeprature on ice cream sales. From a machine learning standpoint, we can use the line of best fit to predict future sales depending on proposed future temperatures. Say the weather calls for a 95 degree scorcher -- what can we estimate our sales to be?

Linear regression is trivially easy in R. I'll get that out of the way now so we can talk about it.

```{r}
summary(lm(sales ~ temp))
```

This output tells us everything we want to know. We find a significant effect of temparture on ice cream sales (as conducted by a t-test on the coefficients of temparature to decide if the relationship may be due to chance; $t_6 = 14.164, p < .001$). Most people call it a day with this output. We can also find the significance of the overall model, fit with all the variables (including the intercept term; $F_{1,5} = 200.6, p < .001$). This is usually more informative when comparing two models with multiple varibles. Furthermore, we have a multiple $R^2$ of $.976$, indicating that the relationship between all factors in the model (temp and intercept) and our predictor variable (sales) account for 97.57% of the variance. Now, adding more factors to a model, even completely arbitrary factors, are mathematically certain to explain more variance in a model. The adjusted $R^2$ staistic this includes a penalty term to account for the complexity of the model (i.e., number of factors included). It is entirely possible to get a modest $R^2$ (say ~ .25) but an adjusted $R^2$ **below zero** if the model is both complex and uninformative. 

However, we can also delve deeper using R. For instance, we also find the intercept and slope of the line that best fits between all points on our plane. 

```{r}
coef(lm(sales ~ temp))
```

These are exactly like you remember from middle school. The *intercept* pinpoints the value of $y$ when $x$ is 0. In this case, our intercepts states the expected sales at temperature = 0 are -\$2155. We should probably steer clear of selling ice cream in January then. 

The coefficient of a variable indicates the *slope* of the line as $x$ increases. So the coefficient of temperature indicates that for each degree increase in temperature, sales increase by \$44.99. 

We can plot a line according the slope and intercept to see the prediction of our model

```{r}
plot(temp,sales)
abline(coef(lm(sales~temp)))
```

This is nice and all, but we're putting a lot of faith in someone else's code. Getting the results of a linear regression are not that difficult with a little linear algebra -- let's take things apart and see how it ticks.

## From Scratch

To start, how do we fit a line to these points in the first place? The idea is to find the line with the least distance to each point. This is calculated using the **residual sum of squares (RSS)**. The RSS is a function of the coefficient weights, \beta, on $x$ and $y$, and is calculated as

$$RSS(\beta) = \Sigma_i(y_i-\beta x_i)^2$$

which in code, works like:

```{r}
rss <- function(beta,x,y){
  squares <- rep(0,length(x))
  for (i in 1:length(x)){
   squares[i] = (y[i] - beta*x[i])^2
  }
  return(sum(squares))
}
```

Basically, we're looking for the \beta that when multiplied by the $x$ value gets as closed to fitting a straight line as possible. Thus the goal is to minimize the residual sum of squares. We can do this by arbitrarily plugging-and-chugging through candidate betas...

```{r}
rss(0,temp,sales)
rss(44.9,temp,sales)
rss(60,temp,sales)
```

...but this is obviously not a great idea. We can instead find \beta algorithmically by differentiating $RSS$ with respect to \beta and setting it qual to 0. This results in:

$\hat{\beta} = (x^Tx)^{-1}x^Ty$

We can write this down in R as

```{r}
min.beta <- function(X,y){
  beta.hat <- solve(t(X)%*%X)%*%t(X)%*%y  
  return(beta.hat)
}
```

But hold on a sec! This model does not include an intercept term, and therefore assumes an intercept at the origin (0,0). We already know this isn't the case. To calculate an intercept, $\beta_0$, we have to declare a vector to find the value of beta with $x$ set to 1, or basically the weight required to move a straight line to the the average value of $y$. We simple add a vector of ones to our factor matrix, $X$.

```{r}
intercept <- rep(1,length(temp)) #vector of ones
X <- cbind(intercept,temp) #matrix of factors (intercept & friends)
y <- sales
```

We then plug into our minimum RSS function to get

```{r}
beta.hat <- min.beta(X,y)
beta.hat #our weights for intercept and temp
```

$\hat{y}$ is equivalent to the classic formula for plotting a line you learned in middle school, $y = mx + b$. 

```{r}
y.hat = beta.hat[1] + beta.hat[2]*temp #intercept + slope*variable
# which we can express in linear algebraic terms as
y.hat <- X%*%beta.hat
# and show they are equal
X%*%beta.hat == beta.hat[1] + beta.hat[2]*temp 
```

Again, we can visualize this linear relationship.

```{r}
# ploting x and y
plot(temp,sales)
# the line of best fit (intercept and slope)
abline(beta.hat)
# the points predicted by the model for each value of temperature
points(temp,y.hat,col="red")
```

We can calculate the error of the model as the difference between the values of $y$ and our predicted values, $\hat{y}$, via the sum of squared errors

$SSE = \Sigma(y - \hat{y})^2$

We then estimate the variance of the model using the unbiased estimator, degrees of freed,$n - \nu$, where \nu are  the number of model parameters. We have two parameters, slope and intercept, so we have $7-2$ degrees of freedom. 

$MSE = \frac{\Sigma(y - \hat{y})^2}{n-2} = 4957.122$

This is known as the **mean squared error** and captures the amount of variance between the predicted and observed values of $y$. However, the mean squared error is unstandardized, meaning we have no way to guage whether nearly 5000 points of error is a good thing or a bad thing. Fortunately, we can calculate $R^2$ just as simply. As mentioned above, $R^2$ is a standardized metric of fit ranging from 0-1 that can be interpreted as the proportion of variance explained by our model. $R^2$ is calculated as 

$R^2 = 1- \frac{\Sigma(y - \hat{y})^2}{\Sigma(y - \bar{y})^2} = 97.57$

We can of course do all of this in a few lines of R.

```{r}
sse <- sum((y - y.hat)^2) 
sse
mse = sse/(length(y)-2)
mse
r.squared <- 1- ((sum((y-y.hat)^2))/(sum((y-mean(y))^2)))
r.squared
```

## Linear Regresion "From A Box"
R does all of these operations trivially easily, thankfully. 

```{r}
# We first declare our model as y ~ x
fit1 <- lm(sales ~ temp)

# our betas
coef(fit1) 

# double checking our calculation of beta
round(beta.hat,2) == round(coef(fit1),2)

# double checking our our predicted values, y.hat
round(y.hat,2) == round(fit1$fitted.values,2)

# plotting the data with the model
plot(temp,sales)
abline(coef(fit1)[1],coef(fit1)[2])
points(temp,fit1$fitted.values,col="red")
```

# Complete Demonstration

Alright, let's play with some real data! I'm using a dataset available by default with R: Motor Trend's road test evlatulations from 1974. We can flex our linear algebra muscles to see which factors most influence fuel consumption. Importantly, this requires us to extend linear regression to multiple factors.

```{r}
data(mtcars)
attach(mtcars)
dimnames(mtcars)
```
Checking out the help documentation for mtcars, we see that we have the following data to work with:

1. mpg	Miles/(US) gallon
2. cyl	Number of cylinders
3. disp	Displacement (cu.in.)
4. hp	Gross horsepower
5. drat	Rear axle ratio
6. wt	Weight (1000 lbs)
7. qsec	1/4 mile time
8. vs	V/S
9. am	Transmission (0 = automatic, 1 = manual)
10. gear	Number of forward gears
11. carb	Number of carburetors

For the sake of demonstration, let's predict a continuous variable from other continuous variables. How about mpg by assorted factors?

```{r}
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

# and then we find the predicted values of y given these factors
y.hat <- X%*%beta.hat
# which is the same as expressing 
y.hat =  beta.hat[1] + beta.hat[2]*cyl + beta.hat[3]*disp + 
          beta.hat[4]*hp + beta.hat[5]*drat + beta.hat[6]*wt + 
          beta.hat[7]*qsec
y.hat == X%*%beta.hat

# it's difficult to plot multivariate spaces
# for now, it's simple enough to demonstrate that y.hat
# approximates y
plot(y.hat,y)

# comparing to R's out of the box regression
fit2 <- lm(mpg ~ cyl + disp + hp + drat + wt + qsec)

# we got the same betas
round(coef(fit2),2) == round(beta.hat,2)

#and the same predictions of y
round(fit2$fitted.values,2) == round(y.hat,2)
```
