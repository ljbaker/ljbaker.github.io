---
layout: posts
title: "Linear Algebra Review"
date: 2017-03-29
---

Linear Algebra Review
=====================

Linear algebra is the basis for many algorithms in statistics and
machine learning. I know from personal experience that most advanced
courses require an understanding of linear algebra, but few (if any)
actually cover it in depth. Here is a crash course in linear algebra
that highlights the basic operations necessary for multivariate analysis
while providing examples in R.

#### Matrix Addition

The addition of two matrices requires that the matrices have the same
dimensions, such that

*A*<sup>*n* × *m*</sup> + *B*<sup>*n* × *m*</sup> = *C*<sup>*n* × *m*</sup>

    A <- matrix(c(1,2,3,4),nrow=2)
    B <- t(A)
    A + B

    ##      [,1] [,2]
    ## [1,]    2    5
    ## [2,]    5    8

#### Scalar Addition

Adding a scalar to a matrix adds that scalar to each cell in the matrix.
The matrix retains the same shape.

*A*<sup>*n* × *m*</sup> + *b* = *C*<sup>*n* × *m*</sup>

    A <- matrix(c(1,2,3,4),nrow=2)
    b = 5
    A + b

    ##      [,1] [,2]
    ## [1,]    6    8
    ## [2,]    7    9

#### Scalar Multiplication

Multiplying a matrix by a scalar multiplies each cell in the matrix by
that scalar. Scalar multiplication works the same whether multiplying on
the left or the right of the matrix (just like normal algebra, but very
much not like matrix multiplication).

    A <- matrix(c(1,2,3,4),nrow=2)
    b = 10
    A*b

    ##      [,1] [,2]
    ## [1,]   10   30
    ## [2,]   20   40

    b*A

    ##      [,1] [,2]
    ## [1,]   10   30
    ## [2,]   20   40

#### Broadcasting

Broadcasting a vector to a matrix means that when we add a vector to a
matrix we implicitly repeat the vector along one dimension until it fits
the dimensions of the matrix, and then add that repeated vector to the
matrix.

NOTE: R (and many other languages) do not use implicit broadcasting.
Even though you may see a formula expressed like this...

*A*<sup>*n* × *m*</sup> + *b*<sup>*n* × 1</sup>

...if we put it into R it will return an error

    A <- matrix(c(1,2,3,4),nrow=2)
    v <- matrix(c(5,6))
    A + v #results in error

Instead, we have to explicitly coerce the vector into a matrix format.

    A <- matrix(c(1,2,3,4),nrow=2)
    v <- matrix(c(5,6))
    A + matrix(rep(v,2),nrow=2)

    ##      [,1] [,2]
    ## [1,]    6    8
    ## [2,]    8   10

Broadcasting seems to appear most often in the deep learning tradition
and often is not stated explicitly.

#### Hadamard Products (Element-wise Multiplication)

This is also called element-wise multiplication. Basically, multiply each
cell of a matrix by it's matched cell from an identically shaped matrix.
It is the default form of multiplication in R and many other languages,
with the notable exception of MATLAB (which is optimized for matrix
functions, as its name might suggest).

    A = matrix(c(1,2,3,4),nrow=2)
    B = matrix(c(1,2,3,4),nrow=2)
    A*B

    ##      [,1] [,2]
    ## [1,]    1    9
    ## [2,]    4   16

#### Vector Products

Now we're cooking. We sum the product of each cell of *a* by every cell
of *b*. Note that if *a* is a 1 × 3 row-vector than *b* must be a
column-vector of equal length (3 × 1) to get a scalar results (AKA a $1
1 $ matrix).

    a <- matrix(c(1,2,3),nrow=1)
    b <- matrix(c(1,2,3),nrow=3)
    a

    ##      [,1] [,2] [,3]
    ## [1,]    1    2    3

    b

    ##      [,1]
    ## [1,]    1
    ## [2,]    2
    ## [3,]    3

    a%*%b

    ##      [,1]
    ## [1,]   14

Also note that by these rules the reverse returns an *m* × *n* matrix.

    b%*%a

    ##      [,1] [,2] [,3]
    ## [1,]    1    2    3
    ## [2,]    2    4    6
    ## [3,]    3    6    9

I'll explain the rules of matrix alignment next

#### Matrix Products

Matrices must meet the aligned dimension. So, matrix
*A*<sup>*m* × *n*</sup> can be multiplied by matrix
*B*<sup>*n* × *p*</sup> but not matix *D*<sup>*p* × *n*</sup>. For
*A**B* = *C*, each cell of *C* is the sum of the product of each row of
*A* by each column of *B*. This is true of a matrix and a vector (e.g.,
*A*<sup>*m* × *n*</sup>*b*<sup>*n* × 1</sup> = *c*<sup>*m* × 1</sup>)...

    A <- matrix(c(1,2,3,4,5,6),nrow=3)
    b <- matrix(c(2,3),nrow=2)
    A

    ##      [,1] [,2]
    ## [1,]    1    4
    ## [2,]    2    5
    ## [3,]    3    6

    b

    ##      [,1]
    ## [1,]    2
    ## [2,]    3

    A%*%b

    ##      [,1]
    ## [1,]   14
    ## [2,]   19
    ## [3,]   24

...and a matrix times a matrix.

    A <- matrix(c(1,2,3,4,5,6),nrow=3)
    B <- matrix(c(1,2,3,4,5,6),nrow=2)
    A

    ##      [,1] [,2]
    ## [1,]    1    4
    ## [2,]    2    5
    ## [3,]    3    6

    B

    ##      [,1] [,2] [,3]
    ## [1,]    1    3    5
    ## [2,]    2    4    6

    A%*%B

    ##      [,1] [,2] [,3]
    ## [1,]    9   19   29
    ## [2,]   12   26   40
    ## [3,]   15   33   51

    A <- matrix(c(1,2,3,4),nrow=2)
    B <- matrix(c(1,2,3,4,5,6,7,8),nrow=2)
    A

    ##      [,1] [,2]
    ## [1,]    1    3
    ## [2,]    2    4

    B

    ##      [,1] [,2] [,3] [,4]
    ## [1,]    1    3    5    7
    ## [2,]    2    4    6    8

    A%*%B

    ##      [,1] [,2] [,3] [,4]
    ## [1,]    7   15   23   31
    ## [2,]   10   22   34   46

#### Identity Matrices

The properties of matrix algebra dictate that multiplying a square
matrix, *A*, by an identically shaped matrix of zeros with ones on the
diagonal, *I*, yields *A*. Many authors reserve *I* for the identity
matrix by convention, but please note that many **do not**.

    ID <- diag(3)
    A <- matrix(c(1,2,3,4,5,6,7,8,9),nrow=3)
    ID #identity

    ##      [,1] [,2] [,3]
    ## [1,]    1    0    0
    ## [2,]    0    1    0
    ## [3,]    0    0    1

    A

    ##      [,1] [,2] [,3]
    ## [1,]    1    4    7
    ## [2,]    2    5    8
    ## [3,]    3    6    9

    A%*%ID

    ##      [,1] [,2] [,3]
    ## [1,]    1    4    7
    ## [2,]    2    5    8
    ## [3,]    3    6    9

    ID%*%A

    ##      [,1] [,2] [,3]
    ## [1,]    1    4    7
    ## [2,]    2    5    8
    ## [3,]    3    6    9

    # NOTE: element-wise multiplication by identity matrix gives the diagonal
    A*ID

    ##      [,1] [,2] [,3]
    ## [1,]    1    0    0
    ## [2,]    0    5    0
    ## [3,]    0    0    9

    diag(A)

    ## [1] 1 5 9

#### Matrix Inversion

Just as we can solve for *x* in the algebraic equation *y* = *m**x* by
multiplying both sides by the inverse of *m* ($\\frac{1}{m}$) to get
$x = y\\frac{1}{m}$, we can solve for *x* in the linear algebraic
equation *y* = *A**x* by multiplying both sides by the inverse of *A*,
*A*<sup>−1</sup>. Please note that this is **not** the reciprocal of
*A*. Rather we're looking for the unique inverse that when multiplied by
the original will produce an identity matrix.

    A <- matrix(c(1,2,3,4),nrow=2)
    A

    ##      [,1] [,2]
    ## [1,]    1    3
    ## [2,]    2    4

    solve(A)

    ##      [,1] [,2]
    ## [1,]   -2  1.5
    ## [2,]    1 -0.5

A square matrix multiplied by its inverse yields an identity matrix

    A%*%solve(A) #identity

    ##      [,1] [,2]
    ## [1,]    1    0
    ## [2,]    0    1

    solve(A)%*%A #identity

    ##      [,1] [,2]
    ## [1,]    1    0
    ## [2,]    0    1

Finding *A*<sup>−1</sup> is far more computationally complex, however,
and not all matrices have inverses.

    A <- matrix(c(1,2,3,4,5,6,7,8,9),nrow=3)
    A
    solve(A) #produces error

The above matrix has no inverse because it is **singular**, meaning that
multiplication by the matrix contracts space completely across at least
one dimension. More informally, this means that one or more columns or
rows are linearly dependent. In the above matrix, every row is the
previous row + 1, and every column is the preceding column + 3.

Singular matrices have a *determinant* of 0.

    # A is singular
    det(A)

    ## [1] -2

    A <- matrix(c(1,2,3,4),nrow=2)
    det(A)

    ## [1] -2

#### Determinants

The determinant is just the product of all eigenvalues of a matrix. It's
a handy way to calculate if any dimension of a matrix reduces to 0.

    A <- matrix(c(1,2,3,4,5,6,7,8,9),nrow=3)
    A

    ##      [,1] [,2] [,3]
    ## [1,]    1    4    7
    ## [2,]    2    5    8
    ## [3,]    3    6    9

    #the determinant of A
    det(A) #contracted completely

    ## [1] 0

    #the determinant of an identity matrix is always equal to 1
    ID <- diag(3)
    det(ID)

    ## [1] 1

#### Norms

Euclidean norms are the distance to the origin (0).

    A <- matrix(c(1,2,3,4),nrow=2)
    A

    ##      [,1] [,2]
    ## [1,]    1    3
    ## [2,]    2    4

    norm(A)

    ## [1] 7

    B <- matrix(c(1,1,1,1),nrow=2)
    norm(B)

    ## [1] 2

    C <- matrix(c(0,0,0,0),nrow=2)
    norm(C)

    ## [1] 0

    C <- matrix(c(1,0,0,1,0,0,1,0,0),nrow=3)
    C

    ##      [,1] [,2] [,3]
    ## [1,]    1    1    1
    ## [2,]    0    0    0
    ## [3,]    0    0    0

    norm(C)

    ## [1] 1

    D <- matrix(c(1,1,1,0,0,0,0,0,0),nrow=3)
    D

    ##      [,1] [,2] [,3]
    ## [1,]    1    0    0
    ## [2,]    1    0    0
    ## [3,]    1    0    0

    norm(D)

    ## [1] 3

The norm of an identity matrix is 1.

    E <- diag(3)
    E

    ##      [,1] [,2] [,3]
    ## [1,]    1    0    0
    ## [2,]    0    1    0
    ## [3,]    0    0    1

    norm(E) #norm of identity is 1

    ## [1] 1

The max norm is just the absolute value of the element with the largest
distance from 0.

#### Traces

The trace is simply the sum of the diagonals of a matrix.

    library("psych")
    A <- matrix(c(1,2,3,4,5,6,7,8,9),nrow=3)
    A

    ##      [,1] [,2] [,3]
    ## [1,]    1    4    7
    ## [2,]    2    5    8
    ## [3,]    3    6    9

    tr(A)

    ## [1] 15

Decomposition
=============

Eigendecomposition
------------------

The eigenvector, *λ*, of a matrix, *A*, is a non-zero vector that
preserves the directionality of the matrix when undergoing any form of
linear combination. The eigenvalue, *v*, is the scalar that multiplies
with the eigenvector to produce the original matrix, such that

*A**v* = *λ**v*

So there exists some value, an eigenvalue, which has all the properties
necessary to deduce A from eigenvectors. This can **massively** reduce
the data necessary to manipulate matrices. Finding them is trivially
simple using R.

    A <- matrix(rnorm(9),nrow=3)
    A

    ##           [,1]       [,2]        [,3]
    ## [1,] 0.3651522 -0.6456052 -0.03154097
    ## [2,] 0.6852002  2.0856765  0.20652004
    ## [3,] 1.0601793 -0.1844562 -1.04379950

    V <- eigen(A)$vectors #the eigenvectors
    V

    ##            [,1]         [,2]       [,3]
    ## [1,]  0.4182353  0.007177875 -0.7444747
    ## [2,] -0.8812611  0.064369610  0.4534869
    ## [3,]  0.2201323 -0.997900311 -0.4900072

    lambda <- eigen(A)$values #the eigenvalues
    lambda

    ## [1]  1.7089021 -1.0395270  0.7376541

By solving for *A*, we see that any matrix is equal to the matrix
product of it's eigenvectors by eigenvalues by the inverse of the
eigenvectors, or

*A* = *V**d**i**a**g*(*λ*)*V*<sup>−1</sup>.

Which is occassionally referenced colloqually as the **VDV** identity.

    print("reproducting the matrix, A, by VDV")

    ## [1] "reproducting the matrix, A, by VDV"

    V%*%diag(lambda)%*%solve(V)

    ##           [,1]       [,2]        [,3]
    ## [1,] 0.3651522 -0.6456052 -0.03154097
    ## [2,] 0.6852002  2.0856765  0.20652004
    ## [3,] 1.0601793 -0.1844562 -1.04379950

    print("A = VDV")

    ## [1] "A = VDV"

    round(A,digits=3) == round(V%*%diag(lambda)%*%solve(V),digits=3)

    ##      [,1] [,2] [,3]
    ## [1,] TRUE TRUE TRUE
    ## [2,] TRUE TRUE TRUE
    ## [3,] TRUE TRUE TRUE

Singular Value Decomposition
----------------------------

Eigendecomposition **requires** a square matrix. A more general version
of decomposition that does not require square matrices is the *Singular
Value Decomposition*.

The singular values of a matrix, *A*, are equal to the square roots of
the eigenvalues of *A*′*A*, or

$SVD(A) = \\sqrt(eigen(A'A))$

Singular values are broken into three parts: the square left-singular
values, *U*; the square right-singular values, *V*; and the singular
values, *D*, which are identity but not necessarily square. Suppose
that *A* is an *m* × *n* matrix. Then *U* is defined to be an *m* × *m*
matrix, *D* to be an m× n matrix, and *V* to be an *n* × *n* matrix,
such that

*A* = *U**D**V*<sup>*T*</sup>

    A <- matrix(rnorm(8),nrow=2)
    A

    ##           [,1]       [,2]      [,3]       [,4]
    ## [1,] 0.5103131 -0.3947435 0.8217034 -0.8018150
    ## [2,] 0.3997771 -0.3505536 0.4503121 -0.2334917

    D <- svd(A)$d
    #the singular values, D, of A...
    D

    ## [1] 1.488948 0.239558

    #... are equal to the square roots of eigenvalues of t(A)%*%A
    round(D,digits=4) == round(sqrt(eigen(t(A)%*%A)$values[1:2]),digits=4)

    ## [1] TRUE TRUE

    #left-singular values, U
    U <- svd(A)$u
    V

    ##            [,1]         [,2]       [,3]
    ## [1,]  0.4182353  0.007177875 -0.7444747
    ## [2,] -0.8812611  0.064369610  0.4534869
    ## [3,]  0.2201323 -0.997900311 -0.4900072

    #are equal to the eigenvectors of At(A)
    round(U,digits=4) == round(eigen(A%*%t(A))$vectors,digits=4)

    ##      [,1]  [,2]
    ## [1,] TRUE FALSE
    ## [2,] TRUE FALSE

    #...in theory, although we get a weird sign error here

    # and the right singular values
    V <- svd(A)$v
    V

    ##            [,1]        [,2]
    ## [1,] -0.4289464  0.46352871
    ## [2,]  0.3449206 -0.51052294
    ## [3,] -0.6292812  0.03493196
    ## [4,]  0.5486710  0.72338595

    # ...are equal to the eigenvectors of t(A)%*%A
    # round(t(V),digits=4) == round(eigen(t(A)%*%A)$vectors,digits=4)
    #...at least according to the book. I have no idea what's up with this.

    #this is V
    round(t(V),digits=4)

    ##         [,1]    [,2]    [,3]   [,4]
    ## [1,] -0.4289  0.3449 -0.6293 0.5487
    ## [2,]  0.4635 -0.5105  0.0349 0.7234

    #these are the eigenvectors of A'A
    round(eigen(t(A)%*%A)$vectors,digits=4)

    ##         [,1]    [,2]   [,3]    [,4]
    ## [1,]  0.4289  0.4635 0.0000  0.7753
    ## [2,] -0.3449 -0.5105 0.6118  0.4960
    ## [3,]  0.6293  0.0349 0.6831 -0.3690
    ## [4,] -0.5487  0.7234 0.3988 -0.1289

Moore-Penrose Pseudoinverse
---------------------------

Matrix inversion is not defined for non-square matrices. The
Moore-Penrose pseudoinverse gives the best guess for non-square
matrices.

    library("MASS")
    A <- matrix(rnorm(9),nrow=3) #square
    A

    ##            [,1]       [,2]        [,3]
    ## [1,] -1.5682121 -0.9034502 -0.09298713
    ## [2,]  0.4360353 -0.8432089 -0.81786100
    ## [3,]  0.8026337  1.4640708 -0.32777166

    round(ginv(A),digits=4) == round(solve(A),digits=4) #same as inverse for square matrices

    ##      [,1] [,2] [,3]
    ## [1,] TRUE TRUE TRUE
    ## [2,] TRUE TRUE TRUE
    ## [3,] TRUE TRUE TRUE

"Tall" matrices may have no solution. In this case, the Moore-Penrose
gives us the solution with smallest error

    B <- matrix(rnorm(8),nrow=4) #tall
    B

    ##            [,1]       [,2]
    ## [1,]  1.8582411 -2.1085288
    ## [2,]  0.1711606  0.2095676
    ## [3,] -0.7829083  0.7949081
    ## [4,]  2.0924569 -1.2117992

    #B is unsolvable, as B must be square, but we can find the pseudoinverse
    ginv(B)

    ##            [,1]      [,2]       [,3]      [,4]
    ## [1,] -0.4139413 0.4147174 0.06959474 0.8376305
    ## [2,] -0.7621656 0.4748432 0.19496880 0.7109612

"Wide" matrices may have infinite solutions. In this case the
Moore-Penrose gives us solution with smallest norm of *x*.

    C <- matrix(rnorm(8),nrow=2) #wide
    C

    ##            [,1]      [,2]        [,3]       [,4]
    ## [1,]  0.9989625 -1.435458  0.08161865 -1.1791857
    ## [2,] -0.9133007 -2.078490 -2.11419100 -0.3959627

    #we cannot solve for C, but we can find the best guess
    ginv(C)

    ##            [,1]       [,2]
    ## [1,]  0.3141145 -0.1693483
    ## [2,] -0.2401863 -0.1544152
    ## [3,]  0.1526874 -0.2530856
    ## [4,] -0.2789823  0.0269910

    norm(ginv(C))

    ## [1] 0.9859704

The Pseudoinverse from SVD
--------------------------

The Pseudoinverse is derived as

*A*<sup>+</sup> = *V**D*<sup>+</sup>*U*<sup>*T*</sup>

Where *D*<sup>+</sup> is calculated as the reciprocal of each non-zero
element of the diagonal matrix, *D*, and then taking its transpose.

    A <- matrix(rnorm(8),nrow=4)
    #a random matrix, A
    A

    ##            [,1]       [,2]
    ## [1,]  0.2647589 -0.7955339
    ## [2,]  0.6087539  0.1091682
    ## [3,] -0.5996705 -0.2350387
    ## [4,]  0.1802574  1.0710241

    D = svd(A)$d
    U = svd(A)$u
    V = svd(A)$v
    #the pseudoinverse is equal to functions on the components of the SVD
    round(ginv(A),digits=4) == round(V%*%(diag(1/D))%*%t(U),digits=4)

    ##      [,1] [,2] [,3] [,4]
    ## [1,] TRUE TRUE TRUE TRUE
    ## [2,] TRUE TRUE TRUE TRUE

And that's pretty much all you need to know enough linear algebra to do
some damage in the world of multivariate inference. I'll post a
follow-up soon that demonstrates how to use these basics for Principal
Components Analysis.
