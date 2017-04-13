---
layout: posts
title: "Repeated-Measures Regression"
date: 2017-03-25
---

Most tutorials on statistics and data science begin with a regression
example. This totally makes sense: regression is simple enough to
describe in non-mathematical language and involves interactions across
two dimensions, so it's easy to visualize. And while I find that most
researchers in psychology and computer science are intimately familiar
with general linear regression, the question I get most often is "how do
I account for repeated measurements from the same participant." I'll
tackle the basics of repeated-measures ANOVA in this tutorial and give a
few tips and tricks for easy analysis in R using R Markdown. I'm going
to assume the reader has some familiarity with linear regression, but
we'll go over some basics just to refresh.

Regression
----------

Say that we have two continuous measures -- numerical data that can
theoretically be measured in infinitely small units. These can be any
kind of real numbers, but regression is best suited for ratio numbers,
such as age in months, height in inches, time in milliseconds, or scores
on an IQ test. Let's go ahead and say that we have two relatively
intuitive scores, like age and height. It is relatively intuitive that
until late adolescence, age and height are highly related. The first
thing we can look at is the correlation between items.

    age <-    c(10,10,10,10,10,
                11,11,11,11,11,
                12,12,12,12,12,
                13,13,13,13,13,
                14,14,14,14,14)
    height <- c(54,58,56,51,52,
                56,58,62,53,52,
                60,60,63,53,53,
                62,60,65,55,54,
                64,61,68,56,54)
    cor(age,height)

    ## [1] 0.4880636

    cor.test(age,height)

    ##
    ##  Pearson's product-moment correlation
    ##
    ## data:  age and height
    ## t = 2.6818, df = 23, p-value = 0.01332
    ## alternative hypothesis: true correlation is not equal to 0
    ## 95 percent confidence interval:
    ##  0.1151367 0.7404076
    ## sample estimates:
    ##       cor
    ## 0.4880636

Furthermore, we can use linear regression to find the line that passes
as close to all the points in our dataset. This line serves two
purposes: first, like the correlation test, we can judge the likelihood
that one item affects another item. However in this case we can assume
direct causal relationships between items. Second, we can use this model
to predict future data.

For the sake of consistency, I'm using regression and not Analysis of
Variance (ANOVA). ANOVA is a special case of regression for categorical
data (e.g., conditions or groups). It behaves identically to regression
when using continuous data. *NOTE*: Many ANOVA functions in R or other
statistical software output the results of ANOVAs as
*F*<sub>*d**f*1, *d**f*2</sub> scores, whereas many regression functions
give output as *t*<sub>*d**f*</sub>. In those cases where *d**f*1 = 1,
*F*<sub>*d**f*1 = 1, *d**f*2</sub> = *t*<sub>*d**f*2</sub><sup>2</sup>.

You can *totally* do repeated measures ANOVAS using the aov package, but
things get a little complicated when trying to account for covariates.
I'll show you how to do both repeated-measures regression and
repeated-measures ANOVA, but we'll concentrate on regression for more
complicated models.

As always, we begin by visualizing the data.

    library(ggplot2)
    qplot(x = age, y = height, geom = "point") + geom_smooth(method='lm')

![](ljbaker.github.io/images/2017-03-25-rm-regression_1.png)

We then run a simple linear regression model predicting height from age.

    fit1 <- lm(height ~ age)
    summary(fit1)

    ##
    ## Call:
    ## lm(formula = height ~ age)
    ##
    ## Residuals:
    ##    Min     1Q Median     3Q    Max
    ##  -6.76  -4.02   0.24   2.82   7.24
    ##
    ## Coefficients:
    ##             Estimate Std. Error t value Pr(>|t|)    
    ## (Intercept)  38.6400     7.1189   5.428 1.62e-05 ***
    ## age           1.5800     0.5892   2.682   0.0133 *  
    ## ---
    ## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
    ##
    ## Residual standard error: 4.166 on 23 degrees of freedom
    ## Multiple R-squared:  0.2382, Adjusted R-squared:  0.2051
    ## F-statistic: 7.192 on 1 and 23 DF,  p-value: 0.01332

We see that age has a significant effect on height at *p* = .013. We
have an *R*<sup>2</sup> of .238, meaning this model accounts for about
24% of the variance seen in the data.

To run an ANOVA we simple run

    anova(fit1)

    ## Analysis of Variance Table
    ##
    ## Response: height
    ##           Df Sum Sq Mean Sq F value  Pr(>F)  
    ## age        1 124.82 124.820  7.1919 0.01332 *
    ## Residuals 23 399.18  17.356                  
    ## ---
    ## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1

Where we see the exact same results (remembering that
*F*<sub>1, 23</sub> = (*t*<sub>23</sub>)<sup>2</sup>) We can also
calculate the effect size, *η*<sup>2</sup>, as a ratio of the effect
explained by the variance measured. In this case, we divide the sum of
squares of age by the sum of squares total:

$\\frac{SS\_{age}}{SS\_{age}+SS\_{error}} = \\frac{124.8}{124.8+399.2} = .238$

We can interpret this as saying that 23.8% of our effect was determined
by age, and the remaining was accounted for by unknown variance.

This is all pretty noisy. All things considered, there are a lot of
differences between age groups that are still unaccounted for. Age
probably does explain a lot here, but what about individual differences
between children?

Repeated Measures Regression
----------------------------

Regression assumes independence between data points (i.e., that measures
were randomly sampled from the same distribution and to the best of our
knowledge are not related in any other way). We would then assume that
any variance not explained by our model is "noise" -- although let it be
said that one man's noise is another man's avenue for exploration.

But what if our data isn't independent? What if our scores were actually
taken from five children over the coarse of five years? Accounting for
the variation within a single individual can account for a great deal of
the overall variation in the population. Think of it this way: there are
as many different reasons why child A might be taller than child B, it
just happens that we know their ages and that age is a strong predictor
of height. But it could be that child A eats more spinach or that child
B comes from a relatively short family. However, if we measure child A
**twice** at two different time points, we know that everything about
that child's personal history at time 1 is true of the child at time 2,
accounting for a huge amount of unknown and potentially confounding
factors. We can infer that something different between time 1 and time 2
accounts for the differences in measurement.

Repeated-measures analysis is an absolute asset for studying human
behavior, as it radically reduces the number of measurements we need to
take to understand the impact of a stimulus. It's not a perfect fix --
as we'll address below -- but it's loads better than assuming
independence when we know some unknown factors may be influencing our
result.

Let's begin by adding a third measure of child identity. *NOTE*: Even
though we're giving subjects numerical values, it is important that we
tell R they are factors (categorical variables where numerical values
are nominal only). R assumes strings are categorical factors by default.
We'll then bind these factors into a single dataframe for easy analysis.

    subject <- factor(
               c(1,2,3,4,5,
                 1,2,3,4,5,
                 1,2,3,4,5,
                 1,2,3,4,5,
                 1,2,3,4,5))

    hdata <- data.frame(subject,age,height)
    head(hdata)

    ##   subject age height
    ## 1       1  10     54
    ## 2       2  10     58
    ## 3       3  10     56
    ## 4       4  10     51
    ## 5       5  10     52
    ## 6       1  11     56

We can now use our knowledge of subject identity to account for variance
within measures. Here, we'll use a *random-effects regression* also
known as a *hierarchical linear model* or *multilevel model* to account
for the effects of age nested within each individual subject.

    library(nlme)
    fit2 <- lme(height ~ age,
                random = ~1 | subject/age,
                data = hdata, method = "ML")
    summary(fit2)

    ## Linear mixed-effects model fit by maximum likelihood
    ##  Data: hdata
    ##        AIC      BIC    logLik
    ##   120.1845 126.2789 -55.09225
    ##
    ## Random effects:
    ##  Formula: ~1 | subject
    ##         (Intercept)
    ## StdDev:     3.67535
    ##
    ##  Formula: ~1 | age %in% subject
    ##         (Intercept)  Residual
    ## StdDev:     1.36603 0.7700397
    ##
    ## Fixed effects: height ~ age
    ##             Value Std.Error DF   t-value p-value
    ## (Intercept) 38.64  3.277380 19 11.789907       0
    ## age          1.58  0.231207 19  6.833713       0
    ##  Correlation:
    ##     (Intr)
    ## age -0.847
    ##
    ## Standardized Within-Group Residuals:
    ##        Min         Q1        Med         Q3        Max
    ## -1.0826688 -0.2819975  0.1198333  0.2681222  0.6960322
    ##
    ## Number of Observations: 25
    ## Number of Groups:
    ##          subject age %in% subject
    ##                5               25

The important line for most people will be the fixed-effects line, where
we see a significant effect of age.

Importantly, we can also do this using a more familiar ANOVA approach.
We can either print our output in ANOVA-friendly format...

    anova(fit2)

    ##             numDF denDF   F-value p-value
    ## (Intercept)     1    19 1090.1211  <.0001
    ## age             1    19   46.6996  <.0001

Two points: **p* values are not a measure of magnitude of significance*.
A *p* of .001 is not 10 times as significant as *p* of .01. These values
have a whole lot of baggage attached to them which I'll hopefully tackle
in a future post, but suffice it to say that what we should be looking
at is effect size. It's a little harder to identify effect size in
random-effects regression, but thankfully there's an R package to do it
for us. The MuMIn package has excellent documentation, so I'll let it
speak for itself, but below we calculate the *marginal* *R*<sup>2</sup>
(i.e., the variance explained by fixed factors) and *conditional*
*R*<sup>2</sup> (i.e., the variance explained by the entire model of
fixed and random factors)

    library(MuMIn)
    r.squaredGLMM(fit2)

    ##       R2m       R2c
    ## 0.2456928 0.9719879

We see that our full model accounts for a whopping 97.2% of the
variance!

Adding fixed-effects variables
-----------------------------

Alright, now let's further say we know one more thing about our
subjects: their sex. We know from everyday experience that men tend to
be taller than women on average. Let's see what happens when we add an
additional factor of sex to the model. The prediction of a continuous
value from a continuous and a categorical variable is called an analysis
of covariance or *ANCOVA*, but it is also known as a multilevel model
with fixed-effects. It will be your best friend.

    sex     <- c("M","F","M","F","F",
                 "M","F","M","F","F",
                 "M","F","M","F","F",
                 "M","F","M","F","F",
                 "M","F","M","F","F")


    hdata <- data.frame(subject,age,height,sex)
    head(hdata)

    ##   subject age height sex
    ## 1       1  10     54   M
    ## 2       2  10     58   F
    ## 3       3  10     56   M
    ## 4       4  10     51   F
    ## 5       5  10     52   F
    ## 6       1  11     56   M

    fit3 <- lme(height ~ age*sex,
                random = ~ 1 | subject/age,
                method = "ML",
                data=hdata)
    summary(fit3)

    ## Linear mixed-effects model fit by maximum likelihood
    ##  Data: hdata
    ##        AIC      BIC    logLik
    ##   90.26511 98.79724 -38.13256
    ##
    ## Random effects:
    ##  Formula: ~1 | subject
    ##         (Intercept)
    ## StdDev:    2.486597
    ##
    ##  Formula: ~1 | age %in% subject
    ##         (Intercept)  Residual
    ## StdDev:   0.6250456 0.4001891
    ##
    ## Fixed effects: height ~ age * sex
    ##                 Value Std.Error DF   t-value p-value
    ## (Intercept)  44.93333  2.375915 18 18.912010  0.0000
    ## age           0.86667  0.147846 18  5.861952  0.0000
    ## sexM        -15.73333  3.756652  3 -4.188126  0.0248
    ## age:sexM      1.78333  0.233765 18  7.628738  0.0000
    ##  Correlation:
    ##          (Intr) age    sexM  
    ## age      -0.747              
    ## sexM     -0.632  0.472       
    ## age:sexM  0.472 -0.632 -0.747
    ##
    ## Standardized Within-Group Residuals:
    ##         Min          Q1         Med          Q3         Max
    ## -1.06688137 -0.33575569 -0.02967504  0.29389125  1.36694620
    ##
    ## Number of Observations: 25
    ## Number of Groups:
    ##          subject age %in% subject
    ##                5               25

We again find our significant effect of age, but that some of this
variance is also accounted for by a significant decrease in the height
between females and males ("sexM" indicates that we're comparing M to
the baseline, which by default is the first factor alphabetically). We
also find a significant interaction.

Paired Comparisons (In Progress)
--------------------------------

We know there is an interaction, but the output alone will not tell us
the direction of the effect. Rather than run a series of t-tests, we
need to account for familywise error rate with a single algorithm.

FWER's deserve their own entry at some point, but basically when you
make a comparison against chance at the .05 level, you're actually
saying that the probability that a distribution is due to chance is
1/20. By logical extension, if you run 20 tests on a completely random
set of data, one of those 20 tests will be significant through sheer
dumb luck. Again, massive simplification, but FWER controls for the
"dumb luck" factor of making multiple comparisons.

First, let's visualize our mean differences.

    qplot(x = age, y = height, color = sex,geom = "point") + geom_smooth(method='lm')

![](ljbaker.github.io/images/2017-03-25-rm-regression_2.png)

This gives us a pretty clear idea of what our interaction looks like: a
significant increase in height by age that increases more for males than
females. With factors that have only two levels, we really don't need
multiple comparison testing. However, many data science projects have
dozens of levels, and we'd like to know how groups distinguish
themselves. Below is code for running multiple comparisons using the
Tukey method. It won't work for a factor with two levels, but it might
help you in the future.

    library(multcomp)

    posthoc <- glht(fit3, mcp(sex = "Tukey"))
    summary(posthoc)
