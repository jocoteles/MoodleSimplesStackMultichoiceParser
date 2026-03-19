# Buggy rules

In order to establish that the student has done something particular but wrong, it is useful for us to be able to apply wrong or buggy rules to expressions.  A typical example would be to expand out powers in the wrong way, e.g.

\[(x+y)^2=x^2+y^2.\]

# Powers obey linearity

`buggy_pow(ex)` Implements the buggy linearity rule for exponentiation, i.e.

\[(a+b)^n \rightarrow a^n+b^n.\]

This is  useful if we want to compare a student's answer to the result  of having done something wrong.

# Naive addition of fractions

`mediant(ex1,ex2)` calculates the mediant of two rational expressions.
The mediant of two fractions

\[ \text{mediant}\left(\frac{p_1}{q_1} , \frac{p_2}{q_2}\right)
:= \frac{p_1+p_2}{q_1+q_2}.\]

Note that both `denom` and `num` work on non-rational expressions, assuming the expression to be "over one" by implication.  Hence `mediant` will also assume the denominator is also one in such cases.

This is not always a buggy rule. It is used, for example, in connection with Farey sequences, but it is included here as in assessment this function is useful for checking a common mistake when adding fractions.

There is scope for further examples of such rules.

## See also

[Maxima reference topics](index.md#reference)



# Complex Numbers in STACK

Complex numbers, especially the display of complex numbers, is a surprisingly subtle issue.   This is because there is some genuine ambiguity in whether \(a+\mathrm{i}\, b\) is a single object or the sum of two parts.  In mathematics we use this ambiguity to our advantage, but in online assessment we need to be more precise.  There are also issues of unary minus, e.g. _not_ displaying \(1 + (-2)\mathrm{i}\). Similarly we typically do _not_ display numbers like \(0+1\mathrm{i}\), unless of course we want to at which point we need the option to do so!

The general rules when displaying a complex number in Cartesian form "\(a+\mathrm{i}\, b\)" are

1. the real part should always appear to the left of the imaginary part;
2. \(i\) (or whatever symbol is being used for the imaginary unit) should appear on the right of its coefficient if and only if the coefficient is a numerical value. By numerical value, we mean something like \(2\sqrt{2}\pi\) but not things like \( a \pi \), even if \( a \) is a constant.

Some examples:

* `3+2*%i` should display as \(3+2\,\mathrm{i}\).
* `3-%i` should display as \(3-\mathrm{i}\).
* `-a+b*%i` should display as \(-a+\mathrm{i}\,b\).
* `-b*%i` should display as \(-\mathrm{i}\,b\) (not normally as \(0-\mathrm{i}\,b\)).

STACK provides two functions, one which simplifies and one which does not.

1. `display_complex(ex)` takes an expression `ex` and tries to display this as a complex number obeying the above rules.  In particular, this function makes use of Maxima's `realpart` and `imagpart` function to split up `ex` into real and imaginary parts.  To do this it must assume `simp:true`, and so the real and imaginary part will be simplified.  For example, `display_complex(1+2*%i/sqrt(2))` is displayed as \(1+\sqrt{2}\,\mathrm{i}\).  If you really want \(1+\frac{2}{\sqrt{2}}\,\mathrm{i}\) then you will need to use the non-simplifying alternative below.  This function respects normal conventions, e.g. when `realpart` returns zero this function will not print \(0+2\,\mathrm{i}\), it just prints \(2\,\mathrm{i}\), etc.
2. `disp_complex(a, b)` assumes `a` is the real part and `b` is the imaginary part (no checking is done).  This function (mostly) does not simplify its arguments.  So `disp_complex(0, 2)` will appear as \(0+2\,\mathrm{i}\); `disp_complex(2/4, 1)` will appear as \(\frac{2}{4}+1\,\mathrm{i}\); and `disp_complex(2, 2/sqrt(2))` will appear as \(2+\frac{2}{\sqrt{2}}\,\mathrm{i}\).  Use the atom `null` if you do not want to print a zero for the real part, or print one times the imaginary part.  `disp_complex(null, 2)` will appear as \(2\,\mathrm{i}\) and `disp_complex(null, null)` will appear as just \(\mathrm{i}\).  Think of `null` as a non-printable unit (additive or multiplicative).

There is one exception.  In order to pull out a unary minus to the front, `disp_complex(a, b)` will simplify `b` if `b` is not a number and it contains a unary minus.  So, for example `disp_complex(a, (-b^2)/b)` is displayed \(a-\mathrm{i}\,b\).  (We _might_ be able to fix this but this edge case requires disproportionate effort: ask the developers if this is essential).

You cannot use these functions to display complex numbers in this form \(\frac{\mathrm{i}}{2}\), both these function will always display as \(\frac{1}{2}\,\mathrm{i}\).

Display respects the multiplication sign used elsewhere within expressions, so that you may have \(\frac{2\cdot \pi}{3}\,\mathrm{i}\) rather than \(\frac{2\, \pi}{3}\,\mathrm{i}\).

Note that the function `display_complex(ex)` returns the inert form `disp_complex(a, b)`.  The expression `disp_complex(a, b)` is an "inert form", which is only used to fine-tune the display.  This function is not actually defined and so Maxima always returns it unevaluated.  To remove the inert form from an expression, which is needed to manipulate this further, use `remove_disp_complex`, e.g., with the following.

    p1:disp_complex(a, b);
    p2:ev(p1, disp_complex=remove_disp_complex);

(Because `null` has two different meanings within an expression it isn't sufficient to just define `disp_complex(ex1, ex2) := ex1+ex2*%i`.)

There are occasions when you will need to explicitly add brackets to the displayed form of a complex number, e.g. to emphasise it is a single entity.  To add brackets there is a further "inert form" `disp_parens` which does nothing but add parentheses when the expression is displayed with the `tex()` function.  For example,

    p1:disp_parens(display_complex(1+%i))*x^2+disp_parens(display_complex(1-%i));

will display as \(\left( 1+\mathrm{i} \right)\cdot x^2+\left( 1-\mathrm{i} \right)\).  To remove these inert forms evaluate

    p2:ev(p1, disp_complex=remove_disp_complex, disp_parens=lambda([ex],ex));

You must remove inert forms before expressions are evaluated by the potential response tree, for example in the feedback variables.  For example, `disp_complex(a, b)` is not algebraically equivalent to `a+b*%i`.

## Polar and Exponential form

A complex number written as \(r e^{i\theta}\) is in _exponential form_ or _polar form_.  The Maxima function `polarform` re-writes a complex number in this form, however with `simp:false` it does not simplify the expressions for the modulus \(r\) or argument \(\theta\) (in STACK). Attempting to re-simplify the expression only returns the number to Cartesian form!

As a minimal example, try the following.

    simp:false;
    p1:polarform(1+%i);
    p2:ev(polarform(1+%i), simp);
    p3:ev(p2, simp);

First we have `p1` is  \( \left(\left(1\right)^2 + \left(1\right)^2\right)^{{{1}\over{2}}}\,e^{i\,{\rm atan2}\left(1 , 1\right)} \). Of course, we really need some simplification of the \(r\) and the \(\theta\) values.

Notice the difference between `p2`: \(\sqrt{2}\,e^{{{i\,\pi}\over{4}}}\), and `p3`: \(\sqrt{2}\,\left({{i}\over{\sqrt{2}}}+{{1}\over{\sqrt{2}}}\right)\) (which of course is not even \(1+i\) either!).

The problem is that in this case `ev( ... , simp)` is not _idempotent_, (i.e. \( \text{simplify}(\text{simplify}(ex)) \neq \text{simplify}(ex) \) in all cases) and the PHP-maxima connection inevitably passes an expression to and from Maxima multiple times.  If `simp:true` then we get multiple simplifications, in this example back to `p3`.

Instead, use `polarform_simp` to rewrite the expression in polar form, and do some basic simplification of \(r\) and \(\theta\).

    simp:false;
    p1:polarform_simp(1+%i);

returns `p1` as \(\sqrt{2}\,e^{\frac{i\,\pi}{4}}\).

Here are some design choices.

1. Positive numbers are returned as real numbers, not as \(r e^{i \times 0}\).  E.g. `polarform_simp(3)` is \(3\).
2. If \(r=1\) then this is not displayed. E.g. `polarform_simp(1/sqrt(2)*(-1+%i))` is \(e^{\frac{3\,i\,\pi}{4}}\).

If question level simplification is on, then the value will probably get re-simplified to Cartesian form.

The predicate `complex_exponentialp(ex)` determines if \(ex\) is written in complex exponential form, \(r e^{i\theta} \).
Note this test is strict

1. we must have \(r\geq 0\);
2. we must have \(-\pi < \theta \leq \pi\).
3. we expect negative real numbers to be written as \(r e^{i\pi}\).

This predicate needs `simp:false`.  In particular do not test using the `ATAlgEquiv` test, which always simplifies its arguments.  Instead test with `ATCasEqual(complex_exponentialp(ans1),true)` to avoid automatic simplification of `ans1` back to Cartesian form _before_ applying the predicate!

An example question is given in the stack library under `Topics\Complex_cube_roots.xml`.




# Asking students to solve equations

It is quite common to ask students to solve an algebraic equation.  The student's answer may be a list (or set) of numbers.  We need to check that this list is

1. Correct: every element of the list satisfies the equation.
2. Complete: every solution of the equation is in the list.

The best way to do (1) is *not* to check algebraic equivalence with the list/set of correct answers!  Instead, substitute the student's answer into the equation and see if it works.

We proceed by example.  Imagine the teacher has asked the student to solve `p=0` in the equation defined in the following "question variables".

    p:2*x^2+11*x-5/4;
    ta:solve(p,x);
    /* Solve gives a list of equations, we want a set of numbers. */
    ta:setify(maplist(rhs,ta));

For solutions we are not interested in order, but we need multiplicity.  Therefore a "bag" is what we need logically.  However, Maxima only has sets and lists.

If the student enters a set or list, the AlgEquiv answer test can be used to compare sets and lists, but it does so element-wise.  We need to do something different.

In the feedback variables we create a new list called "listans" as follows, assuming the student's answer is assigned to `ans1`.

    /* Need a *LIST* from this point on, so we have a definite order. */
    sans:listify(ans1);
    /* Substitute into the equation. */
    listans:maplist(lambda([ex],ev(p,x=ex)), listify(ans1));

The values of `listans` are what we get when we substitute in each of the students' answers into the equation.   We could also simplify this, but it isn't strictly necessary.

    /* "Simplify" the result (not strictly necessary). */
    listans:maplist(fullratsimp, listans);

Now we have a list of numbers.  We need to compare this with something, but the student's list may have a different number of entries than of the teacher's solution!

    /* Generate something to compare this list with. */
    zl:makelist(0,length(listans));

In the potential response tree, compare `listans` with `zl` using the AlgEquiv answer test and the `quiet=yes` option to suppress all feedback.

Next, assume we want to work out which answers in the student's list are wrong.

    /* To decide which answers in a list are equivalent. */
    /* Pick out the wrong answers. */
    we:sublist(sans, lambda([ex], not(algebraic_equivalence(ev(p,x=ex),0))));

To use this, we could put the following in the `false` branch feedback of the first node.

    The following answers you entered do not satisfy the equation
    \[ {@we@}. \]

The above test only makes sure that everything typed in by the student satisfies the equation.  In particular, the empty set `{}` will pass this test!  So, we now need to separately check that the student has all the solutions to the equation. To establish this you can check that the length of the teacher's answer is greater than the length of the student's. This can be done with the following test (i.e. the "greater than" test).

    ATGT(length(ta), length(fullratsimp(sans)))

If this test is true, then the student has missed some solutions.

The point really here is that we are not seeking equivalence with a particular set of numbers, rather we are establishing correctness (all things identified by the student are solutions) and completeness (all the solutions are identified by the student) as separate mathematical properties.

## Randomly generated variables

In the above example, we may have created a randomly generated variable.  E.g.

    v:rand([x,y,z,t]);
    p:a*v^2+b*v+c;

In this case, to make the substitution you need to put in an extra evaluation.

    listans:maplist(lambda([ex],ev(p,ev(v=ex))), listify(ans1));

## Repeated roots!

If the teacher asks a student to enter the answer as a set, then by default STACK does not remove duplicates because validation, etc. 
is done with `simp:false`.  If you want the student to enter repeated roots you must set `Auto-simplify` to `no` in the PRT to avoid losing solutions from the student.  You can then check that each answer satisfies the equation and the student has the correct number of answers using

    length(ans1)

being equivalent to the correct number using `EqualComAss` to avoid simplification.  
Note, that if you "simplify" `ans1` you are likely to lose answers as sets automatically lose duplicates.

Alternatively, you may want to simplify the student's answer to make sure they have the right number of *different* solutions.  This is a separate test.

    length(fullratsimp(ans1))

Exact circumstances of the question will dictate what to do, and whether the teacher expects students to enter duplicate roots the right number of times.

## Displaying equations with the LaTeX `aligned` environment.

STACK supports the `\begin{aligned} ... \end{aligned}` environment, which can be used to line up equations on the equal sign.  This is an inert function which displays its arguments.

For example, in CASText try `{@aligned([x^2+2,stackeq(3)],[x^3,stackeq(4)])@}`

In question variables try 

    /* Either definition of eq1 below works. */
    eq1:x^2+2=3 nounand x^3=4;
    eq1:[x^2+2=3, x^3=4];
    eq2:apply(aligned, map(lambda([ex], [lhs(ex),stackeq(rhs(ex))]), args(eq1)));

and then display `{@eq2@}` as normal.

STACK also supports an inert function `lrparens` which allows fine control over the `\left` and `\right` brackets in LaTeX output.  E.g.

    eq2:lrparens(".", ex, "\\}");

will simply wrap the LaTeX output of `ex` with `\left.` and `right\}`.  The first and third arguments of lrparens must be strings, and they much correspond to legitimate bracket types in LaTeX.  Note, as normal the curly braces need to be protected. 



# Geometry related Maxima functions

STACK adds a number of geometry related functions to maxima to help teachers establish mathematical properties, particularly when using the [Geogebra input](../Specialist_tools/GeoGebra/index.md).

These functions are defined in `stack/maxima/geometry.mac`.

___Note that unless already defined in Maxima, function names should match function names in Geogebra___


### `Length`

`Length(v)` returns the Euclidean length of the vector (represented as a list) from the origin to the point.

### `Distance`

`Distance(A, B)` returns the Euclidean distance between points represented as lists.  Works in any dimension.

### `Angle`

`Angle(A, B, C)` returns the angle between three points \(A\), \(B\), \(C\).  The function returns radians.
Note angles are given between \(-\pi\) and \(\pi\) (not between \(0\) and \(2\pi\)).



# The Greek Alphabet

Greek letters are transliterated using their English names.  I.e.

    [alpha,beta,gamma,delta,epsilon,zeta,eta,theta,iota,kappa,lambda,mu,nu,xi,omicron,pi,rho,sigma,tau,upsilon,phi,chi,psi,omega]
    
Upper case Greek letters have an upper-case English first letter.  I.e.

    [Alpha,Beta,Gamma,Delta,Epsilon,Zeta,Eta,Theta,Iota,Kappa,Lambda,Mu,Nu,Xi,Omicron,Pi,Rho,Sigma,Tau,Upsilon,Phi,Chi,Psi,Omega]
    
Many of the Greek letters already have a meaning in Maxima.

* `beta`:  The beta function is defined as \(\gamma(a) \gamma(b)/\gamma(a+b)\).
* `gamma`:  The gamma function.
* `delta`: This is the Dirac Delta function (only defined in Laplace).
* `zeta`: This is the Riemann zeta function.
* `lambda`: Defines and returns a lambda expression, i.e. an unnamed function.
* `psi`: The derivative of 'log (gamma (<x>))' of order '<n>+1', which has a strange syntax `psi[n](x)`.  It is also defined in the tensor package.

Note that by default, `psi` requires arguments and any attempt to use this variable name without arguments will result in an error.  For this reason we delete this function in STACK, and `psi` becomes an unnamed variable.


The following are given a specific value by STACK.

* `pi` is defined to be the numeric constant which is the ratio of the diameter to the circumference of a circle.  In Maxima this is normally `%pi`, but STACK also defines the letter `pi` to have this value.
* In Maxima the numeric constant which represents the so-called golden mean, \((1 + \sqrt{5})/2\) is `%phi`.

## "Undefine" Maxima defaults

It is currently not possible to "undefine" function names and return them to variables.





# Maxima and computer algebra use in STACK

STACK uses the computer algebra system (CAS) [Maxima](Maxima_background.md).  This section of the documentation deals with Maxima-specific functions, including core Maxima and functions defined by STACK.

## Maxima in STACK {#reference}

* [Predicate functions](Predicate_functions.md), which are useful to test expressions.
* [Numbers](Numbers.md), including floating point and complex numbers.
* [Simplification](Simplification.md) can be switched on and off in Maxima.
* [Inequalities](Inequalities.md).
* [Matrices and vectors](Matrix.md).
* [Statistics](Statistics.md).
* [Randomly generated objects](Random.md).
* [Maxima plot2d](Maxima_plot.md).
* [Buggy rules](Buggy_rules.md) implements rules which are not always valid!

## Working offline

We recommend you download and use the graphical desktop interface WxMaxima for working offline, on your desktop.

* Setting up a [STACK-Maxima sandbox](STACK-Maxima_sandbox.md) for testing code on the desktop.



# Inequalities

The non-strict inequalities \(\geq\) and \(\leq\) are created as infix operators with the respective syntax

    >=,  <=

Maxima allows single inequalities, such as \(x-1>y\), and also support for inequalities connected by logical operators, e.g. \( x>1 \text{ and } x<=5\).

You can test if two inequalities are the same using the algebraic equivalence test, see the comments on this below.  

Chained inequalities, for example \(1\leq x \leq2\text{,}\) are not permitted.  They must be joined by logical connectives, e.g. "\(x>1\) and \(x<7\)". 
As `and` and `or` are converted to `nounand` and `nounor` in student answers, you may need to use these forms in the teacher's answer as well.
For more information, see [Propositional Logic](../Topics/Propositional_Logic.md).

From version 3.6, support for inequalities in Maxima (particularly single variable real inequalities) was substantially improved.

# Functions to support inequalities

* `ineqprepare(ex)`

This function ensures an inequality is written in the form `ex>0` or `ex>=0` where `ex` is always simplified.  This is designed for use with the algebraic equivalence answer test in mind.

* `ineqorder(ex)`

This function takes an expression, applies `ineqprepare()`, and then orders the parts.  For example,

     ineqorder(x>1 and x<5);

returns

      5-x > 0 and x-1 > 0

It also removes duplicate inequalities.  Operating at this syntactic level will enable a relatively strict form of equivalence to be established, simply manipulating the form of the inequalities.  It will respect commutativity and associativity and `and` and `or`, and will also apply `not` to chains of inequalities.

If the algebraic equivalence test detects inequalities, or systems of inequalities, then this function is automatically applied.

* `make_less_ineq(ex)`

Reverses the order of any inequalities so that we have `A<B` or `A<=B`.  It does no other transformations.  This is useful because when testing equality up to commutativity and associativity we don't perform this transformation.  We need to put all inequalities a particular way around.  See the EqualComAss test examples for usage.

## See also

[Maxima reference topics](index.md#reference)





# Matrices and vectors in STACK

This page documents the use of matrices in STACK.  There is a topics page for setting [linear algebra](../Topics/Linear_algebra/index.md) STACK questions.

## Matrices ##

The operator `.` represents noncommutative multiplication and scalar product. The star `A*B` gives element-wise multiplication.

Maxima functions `addrow` and `addcol` appends rows/columns onto the matrix.

Maxima functions perform row operations

    rowswap(m,i,j)
    rowadd(m,i,j,k)

Where ` m[i]: m[i] + k * m[j]`.

    rowmul(m,i,k)

Where `m[i]: k * m[i]`.

STACK provides a function to compute reduced row echelon form

    rref(m)

## Assigning individual elements ##

To assign values to individual elements, use the simple syntax such as the following.

    m:matrix([1,1],[1,2])
    m[1,2]:3

Note also Maxima's `setelmx` function:

    setelmx (<x>, <i>, <j>, <M>)

Assigns `<x>` to the `(<i>, <j>)`'th element of the matrix `<M>`, and returns the altered matrix. `<M> [<i>, <j>]: <x>` has the same effect, but returns `<x>` instead of `<M>`.


### Showing working {#Showing-working}

It is quite common to want to show part of a matrix calculation "un-evaluated".  For example, the following is typical.

\[ \left[\begin{array}{cc} 1 & 2 \\ 4 & 5 \\ \end{array}\right] + \left[\begin{array}{cc} 1 & -1 \\ 1 & 2 \\ \end{array}\right] = \left[\begin{array}{cc} 1+1 & 2-1 \\ 4+1 & 5+2 \\  \end{array}\right] = \left[\begin{array}{cc} 2 & 1 \\ 5 & 7 \\ \end{array}\right] .\]

This is achieved, by having a question in which simplification is off, and we define the question variables as follows.

    A:matrix([1,2],[4,5]);
    B:matrix([1,-1],[1,2]);
    C:zip_with_matrix(A,B);
    D:ev(C,simp);

Notice the use of `zip_with_matrix` which is not a core Maxima function, but is defined by STACK.
The above equation is then generated by the CASText

    \[ {@A@}+{@B@}={@C@}={@D@}.\]

A similar procedure is needed for showing working when multiplying matrices.   Here we need to loop over the matrices, for square matrices we use the following.

    A:ev(rand(matrix([5,5],[5,5]))+matrix([2,2],[2,2]),simp);
    B:ev(rand(matrix([5,5],[5,5]))+matrix([2,2],[2,2]),simp);
    BT:transpose(B);
    C:zeromatrix (first(matrix_size(A)), second(matrix_size(A)));
    S:for a:1 thru first(matrix_size(A)) do for b:1 thru second(matrix_size(A)) do C[ev(a,simp),ev(b,simp)]:apply("+",zip_with("*",A[ev(a,simp)],BT[ev(b,simp)]));
    D:ev(C,simp);

Notice we need to simplify the arguments before we take indices of expressions, and the use of `zip_with`.  This is one problem with `simp:false`.

For non-square matrices we can use this.

    A:ev(rand(matrix([5,5,5],[5,5,5]))+matrix([2,2,2],[2,2,2]),simp);
    B:transpose(ev(rand(matrix([5,5,5],[5,5,5]))+matrix([2,2,2],[2,2,2]),simp));
    TA:ev(A.B,simp);
    BT:transpose(B);
    C:zeromatrix (first(matrix_size(A)), second(matrix_size(B)));
    S:for a:1 thru first(matrix_size(A)) do for b:1 thru second(matrix_size(B)) do C[ev(a,simp),ev(b,simp)]:apply("+",zip_with("*",A[ev(a,simp)],BT[ev(b,simp)]));
    D:ev(C,simp);

Now it makes no sense to include the point wise multiplication of elements as a possible wrong answer.

There must be a more elegant way to do this!

## Display of matrices ## {#matrixparens}

You can set the type of parentheses used to surround matrices in a number of ways.  Firstly, the admin user should set the site default in the qtype_stack options page.

For an individual question, the teacher can set the variable

    lmxchar:"(";

in any of the usual places, e.g. in the question variables.

To set the display of an individual matrix, `m` say, in castext you can use

    {@(lmxchar:"|", m)@}

Since `lmxchar` is a global setting in Maxima, you will have to set it back when you next display a matrix.  Not ideal, but there we are.

Note, STACK only displays matrices with matching parentheses.  If you want something like
\[ f(x) = \left\{ \begin{array}{cc} 1, & x<0 \\ 0, & x\geq 0 \end{array}\right.\]
then you will have to display the matrix without parentheses and sort out the mismatching parentheses in the CASText at the level of display.

For example, if we have the question variable `f:matrix([4*x+4, x<1],[-x^2-4*x-8, x>=1];` and the castext `\[ f(x) := \left\{ {@(lmxchar:"", f)@} \right. \]` 

STACK generates \[ f(x) := \left\{ {\begin{array}{cc} 4\cdot x+4 & x < 1 \\ -x^2-4\cdot x-8 & x\geq 1 \end{array}} \right. \]

LaTeX automatically sizes the parentheses and puts in `\right.` to represent a matching, but invisible closing parentesis.

You can control the alignment of the columns of the matrix using the function `stack_matrix_col(m)`. This function takes the matrix, and returns the string of characters "c", "l", or "r" to decide how to format the column in the LaTeX representation of the array.  By default, this is centered with "c". We need a _function_ to count the number of columns.  This is the default function.

    stack_matrix_col(ex) := simplode(maplist(lambda([ex], "c"), first(args(ex))))$

To change to right aligned columns, switch `"c"` to `"r"`.  This function takes the whole matrix and therefore potentially gives you full control.

For this function to take effect in the whole question, including validation of students' input, place the redefinition before `%_stack_preamble_end;` in the question variables.




# Introduction to Maxima for STACK users

A computer algebra system (CAS) is software that allows the manipulation of mathematical expressions in symbolic form. Most commonly, this is to allow the user to perform some computation.  For the purposes of assessment our calculation _establishes some relevant properties_ of the students' answers. These properties include

  * using a [predicate function](Predicate_functions.md) to find if a single expression has a property.  For example, are any of the numbers floating points?
  * comparing two expressions using an answer test to compare two expressions.  For example, is the student's expression equivalent to the teacher's?

Maxima is also used for [randomly generating](Random.md) structured mathematical objects which become parts of a question and [plotting graphs](Maxima_plot.md) of functions.

To write more than very simple STACK questions you will need to use some Maxima commands. This documentation does not provide a detailed tutorial on Maxima. A very good introduction is given in [Minimal Maxima](http://maxima.sourceforge.net/docs/tutorial/en/minimal-maxima.pdf), which this document assumes you have read.

STACK modifies Maxima in a number of ways.

## Types of object {#Types_of_object}

Everything in Maxima is either an _atom_ or an _expression_. Atoms are either an integer number, float, string or a name.  You can use the predicate `atom()` to decide if its argument is an atom.  Expressions have an _operator_ and a list of _arguments_. Note that the underscore symbol is _not_ an operator.  Thus `a_1` is an atom in maxima. Display of subscripts and fine tuning the display is explained in the [atoms, subscripts and fine tuning the LaTeX display](Subscripts.md) page.

Maxima is a very weakly typed language.  However, in STACK we need the following "types" of expression:

  1. equations, i.e. an expression in which the top operation is an equality sign;
  2. inequalities, for example \( x<1\text{, or }x\leq 1\);
  3. sets, for example, \(\{1,2,3\}\);
  4. lists, for example, \([1,2,3]\).   In Maxima ordered lists are entered using square brackets, for example as `p:[1,1,2,x^2]`.
    An element is accessed using the syntax `p[1]`.
  5. [matrices](Matrix.md).  The basic syntax for a matrix is `p:matrix([1,2],[3,4])`.  Each row is a list. Elements are accessed as `p[1,2]`, etc.
  6. logical expression.  This is a tree of other expressions connected by the logical `and` and `or`.  This is useful for expressing solutions to equations, such as `x=1 or x=2`.  Note, the support for these expressions is unique to STACK.
  7. expressions.

Expressions come last, since they are just counted as being _not_ the others! STACK defines [predicate functions](Predicate_functions.md) to test for each of these types.

## Numbers {#Numbers}

Numbers are important in assessment, and there is more specific and detailed documentation on how numbers are treated: [Numbers in STACK](Numbers.md).

## Alias ##

STACK defines the following function alias names

    simplify(ex) := ev(fullratsimp(ex), simp);
    int := integrate

The absolute value function in Maxima is entered as `abs()`.  STACK also permits you to enter using `|` symbols, i.e.`|x|`.  This is an alias for `abs`.  Note that `abs(x)` will be displayed by STACK as \(|x|\).

STACK also redefined a small number of functions

* The plot command `plot2d` is not used in STACK questions.  Use `plot` instead, which is documented on the [Maxima plot page](Maxima_plot.md).  This ensures your image files are available on the server.
* The random number command `random` is not used in STACK questions.  Use the command [`rand`](Random.md) instead.  This ensures pseudorandom numbers are generated and a student gets the same version each time they login.

## Parts of Maxima expressions {#Parts_of_Maxima_expressions}

### `op(x)` - the top operator

It is often very useful to take apart a Maxima expression. To help with this Maxima has a number of commands, including `op(ex)`, `args(ex)` and `part(ex,n)`. Maxima has specific documentation on this.

In particular,  `op(ex)` returns the main operator of the expression `ex`.  This command has some problems for STACK.

 1. calling `op(ex)` on an atom (see Maxima's documentation on the predicate `atom(ex)`) such as numbers or variable names, cause  `op(ex)` to throw an error.
 2. `op(ex)` sometimes returns a string, sometimes not.
 3. the unary minus causes problems.  E.g. in `-1/(1+x)`
    the operation is not "/", as you might expect, but it is "-" instead!

To overcome these problems STACK has a command

    safe_op(ex)

This always returns a string.  For an atom this is empty, i.e. `""`.  It also sorts out some unary minus problems.

We also have a function `get_safe_ops(ex)` which returns a set of "`safe_op`s" in the expression.  Atoms are ignored.

### `get_ops(ex)` - all operators

This function returns a set of all operators in an expression.  Useful if you want to find if multiplication is used anywhere in an expression.

## Maxima commands defined by STACK {#Maxima_commands_defined_by_STACK}

It is very useful when authoring questions to be able to test out Maxima code in the same environment which STACK uses Maxima. That is to say, with the settings and STACK specific functions loaded. To do this see [STACK-Maxima sandbox](STACK-Maxima_sandbox.md).

STACK creates a range of additional functions and restricts those available, many of which are described within this documentation.  See also [Predicate functions](Predicate_functions.md).

| Command                         | Description
| ------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
| `factorlist(ex)`                | Returns a list of factors of `ex` with or without multiplicities.  Note, the product of these factors may not be the original expression, and may differ by a factor of \(\pm 1\) due to unary minus extraction and ordering of variables.  For this reason, if you want to decide if `f1` is a factor of `ex` then it's better to check `remainder(ex,f1)` is zero, than membership of the factor list.  E.g. both `remainder(a^2-b^2,b-a)` and `remainder(a^2-b^2,a-b)` are zero, but `factorlist(a^2-b^2)` gives `[b-a,b+a]` which does not contain `a-b` as a factor.
By default, the list does not contain multiplicities. If the list should contain multiplicities, use factorlist(ex, true).
| `zip_with(f,a,b)`               | This function applies the binary function \(f\) to two lists \(a\) and \(b\) returning a list.
| `zip_with_matrix(f,A,B)`       | This function applies the binary function \(f\) to two matrices \(A\) and \(B\) returning a matrix.  An example is given in adding matrices to [show working](Matrix.md#Showing_working).| `coeff_list(ex,v)`              | This function takes an expression `ex` and returns a list of coefficients of `v`.
| `coeff_list_nz(ex,v)`           | This function takes an expression `ex` and returns a list of nonzero coefficients of `v`.
| `divthru(ex)`                   | Takes an algebraic fraction, e.g. \((x^4-1)/(x+2)\) and divides through by the denominator, to leave a polynomial and a proper fraction. Useful in feedback, or steps of a calculation.
| `stack_strip_percent(ex,var)`   | Removes any variable beginning with the `%` character from `ex` and replace them with variables from `var`.  Useful for use with solve, ode2 etc.  [Solve and ode2](../Topics/Differential_equations/Assessing_Responses.md#Solve_and_ode2).
| `exdowncase(ex)`                | Takes the expression `ex` and substitutes all variables for their lower case version (cf `sdowncase(ex)` in Maxima).  This is very useful if you don't care if a student uses the wrong case, just apply this function to their answer before using an [answer test](../Authoring/Answer_Tests/index.md).  Note, of course, that `exdowncase(X)-x=0.`
| `stack_reset_vars`              | Resets constants, e.g. \(i\), as abstract symbols, see [Numbers](Numbers.md).
| `safe_op(ex)`                   | Returns the operation of the expression as a string.  Atoms return an empty string (rather than throwing an error as does `op`).
| `comp_square(ex,v)`             | Returns a quadratic `ex` in the variable `v` in completed square form.
| `degree(ex,v)`                  | Returns the degree of the expanded form of `ex` in the variable `v`. See also Maxima's `hipow` command.
| `unary_minus_sort(ex)`          | Tidies up the way unary minus is represented within expressions when `simp:false`.  See also [simplification](Simplification.md).

## Assignment ## {#assignment}

In Maxima the assignment of a value to a variable is _very unusual_.

Input                  | Result
---------------------- | --------------------------------------
`a:1`                  | Assignment of the value \(1\) to \(a\).
`a=1`                  | An equation, yet to be solved.
`f(x):=x^2`            | Definition of a function.

In STACK simple assignments are of the more conventional form `key : value`, for example,

    n : rand(3)+2;
    p : (x-1)^n;

Of course, these assignments can make use of Maxima's functions to manipulate expressions.

    p : expand( (x-3)*(x-4) );

Another common task is that of _substitution_. This can be performed with Maxima's `subst` command. This is quite useful, for example if we define \(p\)  as follows, in the then we can use this in response processing to determine if the student's answer is odd.

    p : ans1 + subst(-x,x,ans1);

All sorts of properties can be checked for in this way. For example, interpolates. Another example is a stationary point of \(f(x)\) at \(x=a\), which can be checked for using

    p : subst(a,x,diff(ans1,x));

Here we have assumed `a` is some point given to the student, `ans1` is the answer and that \(p\) will be used in the response processing tree.

You can use Maxima's looping structures within Question variables. For example

    n : 1;
    for a:-3 thru 26 step 7 do n:n+a;

The result will be \(n=56\). It is also possible to define functions within the question variables for use within a question.

    f(x) := x^2;
    n : f(4);

## Logarithms ##

STACK loads the contributed Maxima package `log10`.  This defines logarithms to base \(10\) automatically. STACK also creates two aliases

1. `ln` is an alias for \(\log\), which are natural logarithms
2. `lg` is an alias for \(\log_{10}\), which are logarithms to base \(10\).
    It is not possible to redefine the command `log` to be to the base \(10\).

## Sets, lists, sequences, n-tuples {#sets-lists-sequences-n-tuples}

It is very useful to be able to display expressions such as comma separated lists, and n-tuples
\[ 1,2,3,4,\cdots \]
\[ (1,2,3,4) \]
Maxima has in-built functions for lists, which are displayed with square brackets \([1,2,3,4]\), and sets with curly braces \( \{1,2,3,4\} \).
Maxima has no default functions for n-tuples or for sequences.

STACK provides an inert function `sequence`.  All this does is display its arguments without brackets. For example `sequence(1,2,3,4)` is displayed \(1,2,3,4\). STACK provides convenience functions.

* `sequenceify`, creates a sequence from the arguments of the expression.  This turns lists, sets etc. into a sequence.
* `sequencep` is a predicate to decide if the expression is a sequence.
* The atom `dotdotdot` is displayed using the tex `\ldots` which looks like \(\ldots\).  This atom cannot be entered by students.

STACK provides an inert function `ntuple`.  All this does is display its arguments with round brackets. For example `ntuple(1,2,3,4)` is displayed \((1,2,3,4)\).

* `ntupleify` creates an n-tuple from the arguments of the expression.  This turns lists, sets etc. into an n-tuple.
* `ntuplep` is a predicate to decide if the expression is an ntuples.

In strict Maxima syntax `(a,b,c)` is equivalent to `block(a,b,c)`.  If students type in `(a,b,c)` using a STACK input it is filtered to `ntuple(a,b,c)`. Teachers must use the `ntuple` function explicitly to construct question variables, teacher's answers, test cases and so on. The `ntuple` is useful for students to type in coordinates.

If you want to use these functions, then you can create question variables as follows

    L1:[a,b,c,d];
    D1:apply(ntuple, L1);
    L2:args(D1);
    D2:sequenceify(L2);

Then `L1` is a list and is displayed with square brackets as normal. `D1` has operator `ntuple` and so is displayed with round brackets. `L2` has operator `list` and is displayed with square brackets.  Lastly, D2 is an `sequence` and is displayed without brackets.

You can, of course, apply these functions directly.

    T1:ntuple(a,b,c);
    S1:sequence(a,b,c,dotdotdot);

If you want to use `sequence` or `ntuple` in a PRT comparison, you probably want to turn them back into lists. E.g. `ntuple(1,2,3)` is not algebraically equivalent to `[1,2,3]`.  To do this use the `args` function.   We may, in the future, give more active meaning to the data types of `sequence` and `ntuple`.

Currently, students can enter expressions with "implied ntuples" E.g

* Student input of `(1,2,3)` is interpreted as `ntuple(1,2,3)`.
* Student input of `{(1,2,3),(4,5,6)}` is interpreted as `{ntuple(1,2,3),ntuple(4,5,6)}`.
* Since no operations are defined on ntuples, students cannot currently enter things like `(1,2,3)+s*(1,0,0)`.  There is nothing to stop a teacher defining the expression tree `ntuple(1,2,3)+s*ntuple(1,0,0)`, but the operations `+` and `*` are not defined for ntuples and so nothing will happen!  If you want a student to enter the equation of a line/plane they should probably use the matrix syntax for vectors.  (This may change in the future).

Matrices have options to control the display of the braces.  Matrices are displayed without commas.

If you are interacting with javascript do not use `sequenceify`.  If you are interacting with javascript, such ss [JSXGraph](../Specialist_tools/JSXGraph/index.md), then you may want to output a list of _values_ without all the LaTeX and without Maxima's normal bracket symbols. You can use

    stack_disp_comma_separate([a,b,sin(pi)]);

This function turns a list into a string representation of its arguments, without braces.
Internally, it applies `string` to the list of values (not TeX!).  However, you might still get things like `%pi` in the output.

You can use this with mathematical input: `{@stack_disp_comma_separate([a,b,sin(pi)])@}` and you will get the result `a, b, sin(%pi/7)` (without the string quotes) because when a Maxima variable is a string we strip off the outside quotes and don't typeset this in maths mode.


## Functions ##

It is sometimes useful for the teacher to define *functions* as part of a STACK question.  This can be done in the normal way in Maxima using the notation.

     f(x):=x^2;

Using Maxima's `define()` command is forbidden. An alternative is to define `f` as an "unnamed function" using the `lambda` command.

     f:lambda([x],x^2);

Here we are giving a name to an "unnamed function" which seems perverse.  Unnamed functions are extremely useful in many situations.

For example, a piecewise function can be defined by either of these two commands

     f(x):=if (x<0) then 6*x-2 else -2*exp(-3*x);
     f:lambda([x],if (x<0) then 6*x-2 else -2*exp(-3*x));

You can then plot this using

    {@plot(f(x),[x,-1,1])@}

# Maxima "gotcha"s! #

  * Maxima does not have a `degree` command for polynomials.  We define one via the `hipow` command.
  * Matrix multiplication is the dot, e.g. `A.B`. The star `A*B` gives element-wise multiplication.
  * The atoms `a1` and `a_1` are not considered to be algebraically equivalent.

## Further information and links  ##

* [Minimal Maxima](http://maxima.sourceforge.net/docs/tutorial/en/minimal-maxima.pdf)
* [Maxima on SourceForge](http://maxima.sourceforge.net)

## See also

[Maxima reference topics](index.md#reference)



# Embedding Maxima-generated plots via `plot()`, a wrapper for Maimxa's `plot2d()`

In STACK, the `plot` command has been defined to be a wrapper for Maxima's `plot2d` command.  The wrapper makes sure that an image file is given an appropriate name, file location, and that Maxima returns a URL to the user giving the image.  Not all of the features of `plot2d` are available through `plot`.

For example,

1. Try the following in a castext field. `{@plot(x^2,[x,-1,1])@}`.
2. You can add a second variable to control the range of the y-axes. `plot(x^2,[x,-1,1],[y,0,2])`.
3. To plot many functions in a single image, we need to define a list of expressions. `plot([x^2,sin(x)],[x,-1,1])`.
4. A list of functions can be created with Maxima's `makelist` command `(p(k):=x^k,pl:makelist(p(k),k,1,5),plot(pl,[x,-1,1]))`.

Notes.

* Currently STACK (PHP) calls Maxima, this in turn has `gnuplot` create a basic SVG image on the server and return a URL.
* By default plots are surrounded by the `<div class="stack_plot">`.  This puts whitespace around a plot, and places the plot in the centre of the screen.  To suppress this `div` use the option `[plottags,false]`.
* The default in Maxima is to include a legend consisting of a `string` representation of the plot.  In STACK this is turned off by default.  To switch it back on, use the command `[legend, true]`.  Any other value of the option `legend` will respect the original command.

## Maxima `plot2d()` options supported by `plot()` in STACK

The following `plot` options are currently supported by STACK.   If you would like to expand the range of options available please contact the developers.

    [xlabel, ylabel, label, legend, color, style, point_type, nticks, logx, logy, axes, box, plot_realpart, yx_ratio, xtics, ytics, ztic, grid2d, adapt_depth],

## Options only available in `plot()`

### Size of images

To change the size of the image use the Maxima variable `size`, e.g. `plot(x^2,[x,-1,1],[size,250,250])`.

### Image margin

To change the size of the margin around the image use the variable `margin`, e.g. `plot(x^2,[x,-1,1],[margin,5])`.

The value of this parameter is used to set gnuplot's margin parameters to the same value `X`.  There is no way to set these individually.

    set lmargin X
    set rmargin X
    set tmargin X
    set bmargin X

The margin also contains any axes numbers, labels etc. outside the plot area.   A value of `[margin, 0]` will therefore crop some of the labels.

### Alternate text for an image (alt tag) {#alttext}

The default alternate text for an image (img alt tag) generated by a plot command such as

    plot(x^2,[x,-2,2]);

is "STACK auto-generated plot of x^2 with parameters [[x,-2,2]]".  If your question asks students to "give an algebraic expression which describes this curve" then you will need to set alternative text which does not include the answer.

To set a specific alt tag, pass an equation `[alt,"..."]` as an argument to the plot function.

    plot(x^2,[x,-2,2],[alt,"Hello world"]);

If you would like an expression as part of this then try

    p:sin(x);
    plot(p,[x,-2,2],[alt,sconcat("Here is ",string(p))]);

### Language strings

Note, you cannot put language strings directly into the alt-text.  E.g. the following will not be translated.

    {@plot(x^2,[x,-2,2],[alt,"[[lang code='en,other']]A quadratic curve[[/lang]][[lang code='no']]En kvadratisk kurve[[/lang]]"])@}

You can define a castext element in the question variables which does get translated, e.g.

    altlbls: castext("[[lang code='en,other']]A quadratic curve[[/lang]][[lang code='no']]En kvadratisk kurve[[/lang]]");

and then use this in the castext:

    {@plot(x^2,[x,-2,2],[alt,altlbls])@}

This technique can be put into other language dependent plot variables.  E.g.

    xlabeltrans: castext("[[lang code='en,other']]Independent variable[[/lang]][[lang code='no']]Uavhengig variabel[[/lang]]");
    ylabeltrans: castext("[[lang code='en,other']]Dependent variable[[/lang]][[lang code='no']]Avhengig variabel[[/lang]]");

Then in the castext `{@plot(x*sin(1/x),[x,-1,2],[xlabel,xlabeltrans],[ylabel,ylabeltrans])@}`

# Example plots

## Traditional axes

A traditional plot with the axes in the middle can be generated by the following.

    {@plot([x^2/(1+x^2),2*x/(1+x^2)^2], [x, -2, 2], [y,-2.1,2.1], [box, false], [yx_ratio, 1], [axes, solid], [xtics, -2, 0.5, 2],[ytics, -2, 0.5, 2])@}

## Labels

The `ylabel` command rotates its argument through 90 degrees.  If you want a horizontal label on the \(y\)-axis you will need to use the `label` command instead.

    {@plot([x^2/(1+x^2),2*x/(1+x^2)^2], [x, -2, 2], [y,-2.1,2.1], [label,["y",-2.5,0.25]])@}

## Grid

The grid is controlled by the maxima command `grid2d`.  Compare the following.

    {@plot([x^2/(1+x^2),2*x/(1+x^2)^2], [x, -2, 2], [y,-2.1,2.1], grid2d)@}
    {@plot([x^2/(1+x^2),2*x/(1+x^2)^2], [x, -2, 2], [y,-2.1,2.1])@}

## Piecewise functions

A piecewise function can be defined with `if` statements.

    x0:2;
    f0:x^3;
    f1:sin(x);
    x0:2
    pg1:if x<x0 then f0 else f1;

With castext

    {@plot(pg1,[x,(x0-5),(x0+5)],[y,-10,10])@}

Notice that Maxima draws the discontinuity as a vertical line.

For a discontinuous function, use the `unit_step` and `kron_delta` functions, e.g.

    f0:x^3;
    f1:sin(x);
    x0:2;
    pg2(x) := f0*unit_step(x0-x) + f1*unit_step(x-x0) + und*kron_delta(x,x0);

Now use:

    {@plot(pg2(x), [x,(x0-5),(x0+5)], [y,-10,10], [legend,false])@}

A further example of a step function:

    step_fn(x,x0) := unit_step(x-x0-1/2) - unit_step(x-x0+1/2) + und*kron_delta(x,x0+1/2)+ und*kron_delta(x,x0-1/2);
    p1:sum(step_fn(x,2*k),k,-3,3);

which can be used with `{@plot(p1,[x,-5,5])@}`.

For a discontinuous function, with end points, add in discrete plots.

    C:-5;
    f0:x^3;
    f1:sin(x);
    x0:2;
    pg2(x) := f0*unit_step(x0-x) + f1*unit_step(x-x0) + und*kron_delta(x,x0);

    ps:[style, lines, points, points];
    pt:[point_type, circle,bullet,circle];
    pc:[color, blue,blue,red];

Now use:

    {@plot([pg2(x), [discrete,[[x0,C]]], [discrete,[[x0,limit(pg2(x),x,x0,'minus)],[x0,limit(pg2(x),x,x0,'plus)]]]], [x,(x0-5),(x0+5)], [y,-10,10], ps, pt, pc, [legend,false])@}

## Interaction with question blocks

It is possible to create multiple plots using the question blocks features.  E.g.

    [[foreach n="[1,2,3,4,5,6,7,8]"]]
        {@plot(x^n,[x,-1,1],[size,250,250],[plottags,false])@}
    [[/ foreach]]

To illustrate how the `margin` option can be used compare the above with

    [[foreach n="[1,2,3,4,5,6,7,8]"]]
        {@plot(x^n,[x,-1,1],[size,250,250],[plottags,false],[margin,1.8])@}
    [[/ foreach]]

## Bode plots

Maxima has a very basic package for bode diagrams, try `load(bode)` in a Maxima session.  This is not a supported package, so instead you can create Bode diagrams directly with code such as the following.

    /* Define two functions to do the plotting */
    bose_gain(f,r):=block([p,w], p:plot(20*log(abs( apply(f,[%i*w]) ))/log(10), [w, r[2],r[3]], [logx]), return(p) );
    bose_phase(f,r):=block([p,w], p:plot(  carg(  apply(f,[%i*w]))*180/%pi, [w, r[2],r[3]], [logx]), return(p) );
    /* Define a transfer function */
    H(s):=100*(1+s)/((s+10)*(s+100));

    /* Produce the graphs */
    gain: bose_gain(H,[w,1/1000,1000]);
    phase:bose_phase(H,[w,1/1000,1000]);


## A catalogue of plots

The following CASText gives representative examples of the plot2d features supported by STACK's plot command.  Cut and paste it into the CASchat script.  Beware that these are likely to cause a timeout on the CAS if you try them all at once.

    <h3>Basic plot</h3>
    {@plot(x^2,[x,-2,2])@}
    The following plot tests the option to explicitly test the alt-text.
    {@plot(x^3,[x,-3,3], [alt,"What is this function?"])@}
    <h3>Multiple graphs, clips the \(y\) values</h3>
    {@plot([x^3,exp(x)],[x,-2,2],[y,-4,4])@}
    <h3>Implicit plot</h3>
    {@plot(2^2*x*y*(x^2-y^2)-x^2-y^2=0, [x,-4,4], [y,-4,4])@}
    <h3>With and without a grid</h3>
    {@plot([x^2/(1+x^2),2*x/(1+x^2)^2], [x, -2, 2], [y,-2.1,2.1], grid2d)@}
    {@plot([x^2/(1+x^2),2*x/(1+x^2)^2], [x, -2, 2], [y,-2.1,2.1])@}
    <h3>Discrete plots</h3>
    Basic discrete plot.
    {@plot([discrete,[[0,0],[1,1],[0,2]]])@}
    Points: by default the points are too large!
    {@plot([discrete,[[0,0], [1,1], [1.5,(1.5)^2]]],[x,-2,2],[style, [points]],[point_type, bullet])@}
    {@plot([discrete,[[0,0], [1,1], [1.5,(1.5)^2]]],[x,-2,2],[style, [points, 1]],[point_type, bullet])@}
    Notice the size of the points is controlled by the second argument in the list `[points, 1]`.  This is documented in Maxima under "Plot option: style".  A more complicated example is below.
    {@plot([[discrete,[[0,0], [1,1], [1.5,(1.5)^2]]],[discrete,[[0,0.1], [0.75,1], [1.25,1.5]]]],[style, [points, 1, red, 1 ], [points, 1.5, blue, 1]])@}
    Combination of discrete plots with normal plots.
    {@plot([x^2, [discrete,[ [0,0], [1,1], [0,2]]]],[x,-2,2])@}
    {@plot([x^2, [discrete,[ [0,0], [1,1], [1.5,(1.5)^2]]]],[x,-2,2],[style, lines, [points, 1]],[point_type, bullet])@}
    {@plot([[discrete,[[30,7]]], -0.4*x+19],[x,0,60],[y,0,20],[style, points, lines], [color, red, blue],[point_type, asterisk])@}
    {@plot([[discrete,[[10, 0.6], [20, 0.9], [30, 1.1], [40, 1.3], [50, 1.4]]], 2*%pi*sqrt(l/980)], [l,0,50],[style, points, lines], [color, red, blue],[point_type, asterisk])@}
    Using different point styles.
    {@plot([[discrete, [[10, .6], [20, .9], [30, 1.1],[40, 1.3], [50, 1.4]]],[discrete, [[11, .5], [15, .9], [25, 1.2],[40, 1.3], [50, 1.4]]]],[style, points],[point_type,circle,square],[color,black,green])@}
    <h3>Parametric plots</h3>
    {@plot([parametric, cos(t), sin(3*t), [t,0,2*%pi]], [nticks, 500])@}
    <h3>Setting non-trivial options: labels on the axes and legend</h3>
    {@plot([x^2/(1+x^2),diff(x^2/(1+x^2),x)],[x,-1,2],[legend,true])@}
    {@plot(x*sin(1/x),[x,-1,2],[xlabel,"Independent variable"],[ylabel,"Dependent variable"],[legend,"This is a plot"])@}
    <h3>Log scale for y-axis, with red colour</h3>
    {@plot(exp(3*s),[s, -2, 2],[logy], [color,red])@}
    <h3>Turn off the box, grid and the axes</h3>
    Default options
    {@plot([parametric, (exp(cos(t))-2*cos(4*t)-sin(t/12)^5)*sin(t), (exp(cos(t))-2*cos(4*t)-sin(t/12)^5)*cos(t), [t, -8*%pi, 8*%pi]], [nticks, 100])@}
    <tt>[axes, false]</tt>
    {@plot([parametric, (exp(cos(t))-2*cos(4*t)-sin(t/12)^5)*sin(t), (exp(cos(t))-2*cos(4*t)-sin(t/12)^5)*cos(t), [t, -8*%pi, 8*%pi]], [nticks, 100], [axes,false])@}
    <tt>[box, false]</tt>
    {@plot([parametric, (exp(cos(t))-2*cos(4*t)-sin(t/12)^5)*sin(t), (exp(cos(t))-2*cos(4*t)-sin(t/12)^5)*cos(t), [t, -8*%pi, 8*%pi]], [nticks, 100], [box,false])@}
    <h3>Putting the axes in the middle</h3>
    {@plot([x^2/(1+x^2),2*x/(1+x^2)^2], [x, -2, 2], [y,-2.1,2.1], [box, false], [yx_ratio, 1], [axes, solid], [xtics, -2, 0.5, 2],[ytics, -2, 0.5, 2])@}
    <h3>Example with ticks, colour and alt-text</h3>
    {@plot([6*x,6^x,x^6,x^(1/6)], [x, -2.2, 2.2], [y, -5.2, 5.2], [box, false], [yx_ratio, 1], [axes, solid], [xtics, -5, 1, 5],[ytics, -5, 1, 5], cons(legend, ["f", "F", "g", "G"]), [alt, "Graph Of Multiple Functions"], [style, [linespoints, 1, 1.5]], [nticks, 5], [color, "#785EF0", "#DC267F", "#FE6100", "#648FFF"], [adapt_depth, 0]);@}




# Numbers in STACK

Separate pages document

1. [numerical answer tests](../Authoring/Answer_Tests/Numerical.md),
2. [complex numbers](Complex_numbers.md).
3. [numerical rounding](Numerical_rounding.md).

## Precise Constants ##

In Maxima the special constants are defined to be

    %i, %e, %pi

etc.   STACK also uses single letters, e.g.

    e: %e
    pi: %pi

Optionally, depending on the question settings, you have

    i: %i
    j: %i

Sometimes you need to use \(e\), or other constants, as an abstract symbol not a number.  The Maxima solution is to use the `kill()` command, but for security reasons users of STACK are not permitted to use this function. Instead use `stack_reset_vars(true)` in the question variables.  This resets all the special constants defined by STACK so the symbols can be redefined in an individual STACK question.  (On Maxima 5.42.1 (and possibly others) `stack_reset_vars(true)` also resets `ordergreat`, so if you need to use `stack_reset_vars(true)` it must be the first command in the question variables.  Since this has been fixed in Maxima 5.44.0, it was probably a bug in Maxima.)

If you want to change the display of the constant \(e\) you need to refer to the `%e%` value, e.g. `texput(%e, "\mathrm{e}");`.

## Modular arithmetic ##

The function `recursemod(ex, n)` recurses over an expression tree, and applies the function `mod(?, n)` to any numbers as identified by `numberp`.  This works on any expression, whereas `polymod` only applies to polynomials.

## Internal representation of numbers ##

Maxima has two data types to represent numbers: integers and floats.  Rational numbers are expressed as a division of two integers not with a dedicated data type, and surds with fractional powers or the `sqrt` function.
The option [Surd for Square Root](../Authoring/Question_options.md#surd) enables the question author to alter the way surds are displayed in STACK.

Similarly, complex numbers are not represented as a single object, but as a sum of real and imaginary parts, or via the exponential function.
The input and display of complex numbers is difficult, since differences exist between mathematics, physics and engineering about which symbols to use.
The option [sqrt(-1)](../Authoring/Question_options.md#sqrt_minus_one) is set in each question to sort out meaning and display.

## Floating point numbers ## {#Floats}

* To convert to a float use Maxima's `float(ex)` command.
* To convert a float to an exact representation use `rat(x)` to rationalise the decimal.

The variable \(e\) has been defined as `e:exp(1)`.  This now potentially conflicts with scientific notation `2e3` which means `2*10^3`.

If you expect students to use scientific notation for numbers, e.g. `3e4` (which means \(3\times 10^{4}\) ), then you may want to use the [option for strict syntax](../Authoring/Inputs/index.md#Strict_Syntax).

Please read the separate documentation on [numerical rounding](Numerical_rounding.md).

We also have mechanisms for keeping track of the number of significant figures. See the documentation on `dispsf(ex,n)` for detail.

## Maxima and floats with trailing zeros ##

For its internal representation, Maxima always truncates trailing zeros from a floating point number.  For example, the Maxima expression `0.01000` will be converted internally to `0.01`.  Actually this is a byproduct of the process of converting a decimal input to an internal binary float, and back again.  Similarly, when a number is a "float" data type, Maxima always prints at least one decimal digit to indicate the number is a float.  For example, the floating point representation of the number ten is \(10.0\).  This does _not_ indicate significant figures, rather it indicates data type.  In situations where the number of significant figures is crucial this is problematic.

Display of numbers in STACK is controlled with LaTeX, and the underlying LISP provides flexible ways to represent numbers.

Note, that apart from the units input, all other input types truncate the display of unnecessary trailing zeros in floating point numbers, loosing information about significant figures.  So, when the student's answer is a floating point number, trailing zeros will not be displayed.  If you want to specifically test for significant figures, use the [units input type](../Topics/Units.md), with the teacher's answer having no units.  The units input type should display the same number of significant figures as typed in by the student.

## Display of numbers with LaTeX ##

The display of numbers is controlled by Maxima's `texnumformat` command, which STACK modifies.

Stack provides two variables to control the display of integers and floats respectively.  The default values are

    stackintfmt:"~d";
    stackfltfmt:"~a";

These two variables control the output format of integers (identified by the predicate `integerp`) and floats (identified by the predicate `floatnump`) respectively.  These variables persist, so you need to define their values each time you expect them to change.

These variables must be assigned a string following Maxima's `printf` format.

These variables can be defined in the question variables, for global effect.  They can also be defined inside a Maxima block to control the display on the fly, and for individual expressions.  For example, consider the following CASText.

    The decimal number {@n:73@} is written in base \(2\) as {@(stackintfmt:"~2r",n)@}, in base \(7\) as {@(stackintfmt:"~7r",n)@}, in scientific notation as {@(stackintfmt:"~e",n)@} and in rhetoric as {@(stackintfmt:"~r",n)@}.

The result should be "The decimal number \(73\) is written in base \(2\) as \(1001001\), in base \(7\) as \(133\), in scientific notation as \(7.3E+1\) and in rhetoric as \(seventy-three\)."

To force all floating point numbers to scientific notation use

    stackfltfmt:"~e";

To force all floating point numbers to decimal floating point numbers use

    stackfltfmt:"~f";

You can also force all integers to be displayed as floating point decimals or in scientific notation using `stackintfmt` and the appropriate template.  This function calls the LISP `format` function, which is complex and more example are available [online](http://www.gigamonkeys.com/book/a-few-format-recipes.html) elsewhere.

| Template       | Input       |  TeX Output      |  Description/notes
| ----------- | ----------- | ---------------- | ----------------------------------------------------------------------------------------------
| `"~,4f"`       | `0.12349`   | \(0.1235\)       |  Output four decimal places: floating point.
|                | `0.12345`   | \(0.1234\)       |  Note the rounding.
|                | `0.12`      | \(0.1200\)       |
| `"~,5e"`       | `100.34`    | \(1.00340e+2\)   |  Output five decimal places: scientific notation.
| `"~:d"`        | `10000000`  | \(10,000,000\)   |  Separate decimal groups of three digits with commas.
| `"~,,\' ,:d"` | `10000000`  | \(10\ 000\ 000\)   |  Separate decimal groups of three digits with spaces.
| `~r`           | `9`         | \(\text{nine}\)  |  Rhetoric.
| `~:r`          | `9`         | \(\text{ninth}\) |  Ordinal rhetoric.
| `~7r`          | `9`         | \(12\)           |  Base 7.
| `~@r`          | `9`         | \(IX\)           |  Roman numerals.
| `~:@r`         | `9`         | \(VIIII\)        |  Old style Roman numerals.

There are many other options within the LISP format command. Please note with the rhetoric and Roman numerals that the numbers will be in LaTeX mathematics environments.

Note that the `@` symbol is currently not parsed correctly inside strings within CASText.  That is to say, you cannot currently type `{@(stackintfmt:"~@r",4)@}` into CASText.  This is a known bug.  To avoid this problem, define a variable in the question variables (e.g. `roman:"~@r";`) and use the variable name in the CASText (e.g. `{@(stackintfmt:roman,4)@}`).

Maxima has a separate system for controlling the number of decimal digits used in calculations and when printing the _value_ of computed results.  Trailing zeros will not be printed with the value.  This is controlled by Maxima's `fpprec` and `fpprintprec` variables.  The default for STACK is

    fpprec:20,          /* Work with 20 digits. */
    fpprintprec:12,     /* Print only 12 digits. */

## Changing the decimal separator, e.g. using a comma for separating decimals ##

STACK now supports a mechanism for changing the decimal separator and using a comma for separating decimals.  A question level option can be used to choose `,` or `.` as the decimal separator.  For finer control in other parts of the question, just set the variable

    stackfltsep:",";

The global variables `stackfltfmt` and `stackfltsep` should have independent effects.

If you use the option for a comma then items in sets, lists and as arguments to functions will no longer be separated by a comma.  To avoid conflicting notation, items will be separated by a semicolon (`;`).

If you separate decimal groups of digits with commas, e.g. if `stackfltfmt:"~:d"`, then these commas are replaced by spaces to avoid ambiguity.  The replacement of commas occurs in integers as well as floats to make sure commas in integers cause no confusion.

## STACK numerical functions and predicates ##

The following commands which are relevant to manipulation of numbers are defined by STACK.

| Command                         | Description
| ------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
| `significantfigures(x,n)`       | Truncate \(x\) to \(n\) significant figures (does perform rounding).
| `decimalplaces(x,n)`            | Truncate \(x\) to \(n\) decimal places  (does perform rounding). See below.
| `commonfaclist(l)`              | Returns the highest common factors of a list of numbers.
| `list_expression_numbers(ex)`   | Create a list with all parts for which `numberp(ex)=true`.
| `coeff_list(ex,v)`              | This function takes an expression \(ex\) and returns a list of coefficients of \(v\).
| `coeff_list_nz(ex,v)`           | This function takes an expression \(ex\) and returns a list of nonzero coefficients of \(v\).
| `numabsolutep(sa,ta,tol)`       | Is \(sa\) within \(tol\) of \(ta\)? I.e. \( |sa-ta|<tol \)
| `numrelativep(sa,ta,tol)`       | Is \(sa\) within \(tol\times ta\) of \(ta\)? I.e. \( |sa-ta|<tol\times ta \).
| `numrelativep(sa,ta,tol)`       | Is \(sa\) within \(tol\times ta\) of \(ta\)? I.e. \( |sa-ta|<tol\times ta \).
| `numexactp(sa,ta)`              | This function checks if one number equals another, but only when the floating point number is _exact_.   E.g. if `ta=1/4` then it has an exact decimal \(0.25\).  Here the float will be converted to a rational and compared.  However if `ta=1/3` then this decimal does not terminate, and so floats in `sa` will not be converted.

The following commands generate displayed forms of numbers.  These will not be manipulated further automatically, so you will need to use these at the last moment, e.g. only when generating the teacher's answer etc.

| Command                         | Description
| ------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
| `dispdp(x,n)`                   | Truncate \(x\) to \(n\) decimal places and display with trailing digits.  Note, this always prints as a float (or integer), and not in scientific notation.
| `dispsf(x,n)`                   | Truncate \(x\) to \(n\) significant figures and display with trailing digits.  Note, this always prints as a float, and not in scientific notation.
| `displaydp(x,n)`                | An inert internal function to record that \(x\) should be displayed to \(n\) decimal places with trailing digits.  This function does no rounding.
| `displaysci(x,n,expo)`          | An inert internal function to record that \(x\) should be displayed to \(n\) decimal places with trailing digits, in scientific notation.  E.g. \(x\times 10^{expo}\).
| `remove_numerical_inert(ex)`   | Removes the above inert forms from an expression `ex`.
| `scientific_notation(x,n)`      | Write \(x\) in the form \(m10^e\).   Only works reliably with `simp:false` (e.g. try 9000).  The optional second argument applies `displaysci(m,n)` to the mantissa to control the display of trailing zeros.

| Function                  | Predicate
| ------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
| `simp_numberp(ex)`          | Fixes `numberp(ex)` for `simp:false`.
| `simp_integerp(ex)`          | Fixes `integerp(ex)` for `simp:false`.
| `simp_floatnump(ex)`          | Fixes `floatnump(ex)` for `simp:false`.
| `real_numberp(ex)`          | Determines if \(ex\) is a real number.  This includes surds and symbolic numbers such as \(\pi\).
| `lowesttermsp(ex)`          | Is the rational expression in its lowest terms?
| `anyfloatex(ex)`            | Decides if any floats are in the expression.
| `scientific_notationp(ex)` | Determines if \(ex\) is written in the form \(a10^n\) where \(a\) is an integer or float, and \(n\) is an integer.

Please note that these predicate functions need to be used with `simp:false`.  Some answer tests, including the default algebraic equivalence (`ATAlgEquiv`) always simplify their arguments.  Instead use a non-simplifying answer test such as `EqualComAss`.

### Decimal places

The functions `decimalplaces(x,n)` and `dispdp(x,n)` perform rounding.  See the separate notes on [numerical rounding](Numerical_rounding.md) for details.  There are some edge cases.

* If `x` is not a real number (judged by `real_numberp`) then we return `ex` (without an error).
* `n` must be an integer, otherwise we throw an error.
* If `n` equals zero, then we round to the nearest integer with Maxima's `round` command.
* `n` negative is possible, in which case we round. e.g. `decimalplaces(314.15,-2)` gives `300`.
* `decimalplaces(x,n)` returns an integer if possible.  That is we don't return a float like `7.0` we return the integer `7` instead.
* `dispdp(x,n)` returns an inert form intended to display trailing zeros (if any).  In this case `x` must be a real number, otherwise we throw an error.



# Numerical rounding

Internally Maxima represents floats in binary, and so even simple calculations which would be exact in base ten (e.g. adding 0.16 to 0.12) might end up in a recurring decimal float which is not exactly equal to the result you would type in directly.

Try `452-4.52*10^2` in desktop Maxima, which is not zero, therefore `ATAlgEquiv(452,4.52*10^2)` fails. (Maxima 5.44.0, November 2022).  \(4.52\times 10^2\) ends up with recurring 9s when represented as a binary float, so it is not algebraically equivalent to the integer \(452\).

Rounding like this can also occur in calculations, for example

    p1:0.29;
    p2:0.18;
    p3:0.35;
    v0:1-(p1+p2+p3);
    v1:0.18;

Then Maxima returns `0.18` for `v0`, (as expected) but `v0-v1` equals \(5.551115123125783\times 10^{-17}\) and so `ATAlgEquiv(v0,v1)` will give false.  Please always use a [numerical test](../Authoring/Answer_Tests/Numerical.md) when testing floats.

As another example, try `100.4-80.0;` in a desktop Maxima session.

## Notes about numerical rounding ##

There are two ways to round numbers ending in a digit \(5\).

* Always round up, so that \(0.5\rightarrow 1\), \(1.5 \rightarrow 2\), \(2.5 \rightarrow 3\) etc.
* Another common system is to use ``Bankers' Rounding". Bankers Rounding is an algorithm for rounding quantities to integers, in which numbers which are equidistant from the two nearest integers are rounded to the nearest even integer. \(0.5\rightarrow 0\), \(1.5 \rightarrow 2\), \(2.5 \rightarrow 2\) etc.  The supposed advantage to bankers rounding is that in the limit it is unbiased, and so produces better results with some statistical processes that involve rounding.
* In experimental work, the number of significant figures requires sometimes depends on the first digits of the number.  For example, if the first digit is a \(1\) or \(2\) then we need to take an extra significant figure to ensure the relative error is suitably small.  The maxima string functions can be used to check the first digit of a number until we have bespoke internal functions to make this check.

Maxima's `round(ex)` command rounds multiples of 1/2 to the nearest even integer, i.e. Maxima implements Bankers' Rounding.  We do not currently have an option to always round up.

STACK has defined the function `significantfigures(x,n)` to conform to convention of rounding up.

## ATAlgEquiv and floating point numbers ##

We recommend you do _not_ use algebraic equivalence testing for floating point numbers.  Instead use one of the [numerical tests](../Authoring/Answer_Tests/Numerical.md).

Lists of numbers present issues with numerical rounding as well.  The `ATAlgEquiv` answer test does work with lists, matrices etc.  However, the numerical tests expect single floating point numbers and do not accept lists etc.

If you have lists of numbers one approach is the following in the feedback variables.

````
/* ta is the teacher's answer.
   ans1 is the student's answer.
   Create a matrix.
   */
S:matrix(LSG1-ans1);
/* Calculate the matrix norm. */
N:ev(S.transpose(S),simp);
/* Now test this is less that 1E-10 with the answer test ATGT(1E-10,N). */
````

Other options include finding `ev(max(map(abs, S), simp` to find the maximum error.



# Writing a permutation as a product of disjoint cycles

Let \[f= \left( \begin{array}{ccccccc} 1 & 2 & 3 & 4 & 5 & 6 & 7 \\ 3 & 1 & 5 & 7 & 2 & 6 & 4 \end{array}\right)\]

In pure mathematics we might ask students to write a permutation such as this as a product of disjoint cycles.

One way to do this is to expect students to write their answer as a list, including the one-cycles. e.g. the permutation \((1)(2 \: 3)\) is entered as `[[1],[2, 3]]`.

This list can be turned into a set of lists, so that the order of disjoint cycles is not important.  However, we need to write each cycle in a particular way.  For example, we would want `[2, 3, 4]` and `[3, 4, 2]` to be considered as equivalent.

One way to do this is to make sure the first element in the list is the minimum element in the list, by cycling through the list.  Essentially, we ensure each cycle is re-written in a definite form.  The following code does this for one cycle.  This function can be used in the question variables.

    /* Write a cycle with the smallest element at the front.  Gives a definite order. */
    perm_min_first(ex) := block(
        if length(ex)<2 then return(ex),
        if is(first(ex)<apply(min, rest(ex))) then return(ex),
        return(perm_min_first(append(rest(ex), [first(ex)])))
    );

Assume the student's answer `ans1` is entered as `[[1],[2, 3]]`.  In the feeback variables make sure each list in `ans1` has the smallest element first with the following code.

    sa1:maplist(perm_min_first, ans1);

Then compare `setify(sa1)` with the teacher's answer (which needs to be processed in a similar way) using algebraic equivalence (quiet).

This is a good example of where we do not have a specific data type and corresponding methods for equivalence, but the pre-processing of a student's answer will make sure we can establish the relevant equivalence. 



# Predicate functions

A predicate function takes an expression and returns Boolean values `true` or `false`.

The convention in [Maxima](Maxima_background.md) is to end predicate
functions with the letter "p". Many predicate functions exist
already within Maxima.  Some of the more useful to us are
listed below.   STACK defines an additional range of predicate
functions.  Some are described here, others are in the relevant specific sections of the documentation, such as [numbers](Numbers.md).

Since establishing mathematical properties are all about predicates they are particularly important for STACK.

You can use predicate functions directly in the [potential response tree](../Authoring/Potential_response_trees.md) by comparing the result with `true` using the
[answer test](../Authoring/Answer_Tests/index.md) AlgEquiv.

# Maxima type predicate functions #

The following are a core part of Maxima, but there are many others.  Notice, predicate functions end in the letter "p".

| Function                | Predicate
| ----------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
| `floatnump(ex)`         | Determines if \(ex\) is a float.  But use STACK's `float_floatnump(ex)` which works with `simp:false`.
| `numberp(ex)`           | Determines if \(ex\) is a number.  _NOTE_ `numberp` returns `false` if its argument is a symbol, even if the argument is a symbolic number such as \(\sqrt{2}\), \(\pi\) or \(i\), or declared to be even, odd, integer, rational, irrational, real, imaginary, or complex.   This function also does not work when `simp:false`, so see the dedicated page on [numbers](Numbers.md).
| `setp(ex)`              | Determines if \(ex\) is a set.
| `listp(ex)`             | Determines if \(ex\) is a list.
| `matrixp(ex)`           | Determines if \(ex\) is a matrix.
| `polynomialp(ex,[v])`   | Determines if \(ex\) is a polynomial in the list of variables v.

# STACK type predicate functions

The following type predicates are defined by STACK.

| Function                   | Predicate
| -------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
| `variablep(ex)`            | Determines if \(ex\) is a variable, that is an atom but not a real number, \(i\) or a string.
| `equationp(ex)`            | Determines if \(ex\) is an equation.
| `functionp(ex)`            | Determines if \(ex\) is a function definition, using the operator `:=`.
| `inequalityp(ex)`          | Determines if \(ex\) is an inequality.
| `expressionp(ex)`          | Determines if \(ex\) is _not_ a matrix, list, set, equation, function or inequality.
| `polynomialpsimp(ex)`      | Determines if \(ex\) is a polynomial in its own variables.
| `simp_numberp(ex)`         | Determines if \(ex\) is a number when `simp:false`.
| `simp_integerp(ex)`        | Determines if \(ex\) is an integer when `simp:false`.
| `simp_floatnump(ex)`        | Determines if \(ex\) is a float when `simp:false`.
| `real_numberp(ex)`         | Determines if \(ex\) is a real number (whether in float form or not).
| `rational_numberp(ex)`     | Determines if \(ex\) is written as a fraction.  For a true mathematical rational number use `rational_numberp(ex) or simp_integerp(ex)`
| `lowesttermsp(ex)`         | Determines if a fraction \(ex\) is in lowest terms.
| `complex_exponentialp(ex)` | Determines if \(ex\) is written in complex exponential form, \(r e^{i\theta} \).  Needs `simp:false`.
| `imag_numberp(ex)`         | Determines if \(ex\) is a purely imaginary number.

# STACK general predicates #

The following are defined by STACK.

| Function              | Predicate
| --------------------- | ------------------------------------------------------------------------------------------------
| `element_listp(ex,l)` | `true` if `ex` is an element of the _list_ \(l\).  (Sets have `elementp`, but lists don't)
| `all_listp(p,l)`      | `true` if all elements of \(l\) satisfy the predicate \(p\).
| `any_listp(p,l)`      | `true` if any elements of \(l\) satisfy the predicate \(p\).
| `sublist(l,p)`        | Return a list containing only those elements of the list \(l\) for which the predicate p is true

(The last of these is core Maxima and is not, strictly speaking, a predicate function)

# STACK other predicate functions #

| Function                  | Predicate
| ------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
| `expandp(ex)`             | true if \(ex\) equals its expanded form.
| `factorp(ex) `            | true if \(ex\) equals its factored form.  Note, if you would like to know if an expression is factored you need to use the [FacForm](../Authoring/Answer_Tests/index.md#Form) answer test.  Prime integers equal their factored form, composite integers do not.
| `continuousp(ex,v,xp) `   | true if \(ex\) is continuous with respect to \(v\) at \(xp\) (unreliable).
| `diffp(ex,v,xp,[n]) `     | true if \(ex\) is (optionally \(n\) times) differentiable with respect to \(v\) at \(xp\) (unreliable).

The last two functions rely on Maxima's `limit` command and hence are not robust.

# Establishing form #

A lot of what teachers do is try to establish if a student's answer "looks right" that is, in an appropriate form.

`linear_term_p(ex, p)` establishes that the expression `ex` is a simple product of one expression for which the predicate `p` is true and zero or more real numbers.

`linear_combination_p(ex, p)` establishes that the expression `ex` is a linear combination of terms for which `p` is true.

The teacher can then use this function to build more complex predicates such as the following

    fouriertermp(ex) := if ((safe_op(ex)="cos" or safe_op(ex)="sin") and linear_term_p(first(args(ex)), variablep)) then true else false$

This predicate function decides if we have a term of the form \(\sin(n\, v)\) or \(\cos(n\, v)\) where \(n\) is any product of real numbers (e.g. \(3\pi/2\)) and \(v\) is any variable.  A teacher might prefer to specify a particular variable.

    fouriertermp(ex) := if ((safe_op(ex)="cos" or safe_op(ex)="sin") and linear_term_p(first(args(ex)), lambda([ex2], ex2=t))) then true else false$

So, if you want to decide if the student's answer looks like \( \sum_{k=1}{n} a_k\cos(k\pi t) + a_k\cos(k\pi t) \) the combined predicate `linear_combination_p(ex, fouriertermp)` can be used.

Testing for form in this way is probably more reliable that the `substequiv` answer test which fails to match up expressions like \(A\sin(t)+B\cos(t)\) with \(A\sin(t)-B\cos(t)\).  As every, the minus sign is a problem.  However, the following predicate will work.

    simpletrigp(ex) := if (ex=cos(t) or ex=sin(t)) then true else false$

and the test `linear_combination_p(ex, simpletrigp)` will be able to do this.


# Related functions #

This is not, strictly speaking, a predicate function.  It is common to want to ensure that a student's expression is free of things like \(\sqrt{2}\), \(a^{1/2}\) or \(1+\sqrt[3]{2}\) in the denominator.  This include any complex numbers.

`rationalized(ex)` searches across the whole expression `ex` and looks in the denominators of any fractions.  If the denominators are free of such things the function returns `true` otherwise the function returns the list of offending expressions.  This design allows efficient feedback of the form ``the denominator in your expression should be free of the following: ...".

## See also

[Maxima reference topics](index.md#reference.md)



# Random objects

STACK can generate structured random objects.  STACK provides a [Maxima](Maxima_background.md) function `rand()` which can be used in the question and answer variables.

STACK creates pseudo-random numbers from a definite seed.
This ensures that when a particular student returns they see the same variant of the question.
(Note to site maintainers: if you upgrade your Maxima version mid-way through an academic cycle, then there is no gurantee that the random numbers will remain the same.  It is unlikely Maxima will change its random number generation between versions, but if it important to you please check first!)

For the purposes of learning and teaching, we do not need an algorithm which is statistically perfect. We are much more interested in simplicity, efficiency and reproducibility across platforms. Hence, we adopt pseudo-random numbers.

It is very important to test each random version a student is likely to see and not to leave this to chance.  To pre-generate and test random variants see the separate documentation on [deploying random variants](../STACK_question_admin/Deploying.md).

Users may also [systematically deploy](../STACK_question_admin/Deploying_systematically.md) all variants of a question in a simple manner.

## rand() {#rand}

STACK provides its own function `rand()`.

* `rand(n)` generates an integer between \(0\) and \(n-1\).
* `rand(n.0)` generates a floating point number between \(0\) and \(n\).  It is probably more useful to use something like a=float(rand(1000)/1000)
  to obtain an accurate number of decimal places.  An alternative is to use the [Maxima](Maxima_background.md) function `round()`
* `rand([a,b,...,z])` makes a random selection from a list.
* `rand({a,b,...,z})` makes a random selection from a set.
* `rand(matrix(..))` applies rand to each element of the matrix.

STACK provides the following functions for random generation of sets.

* `random_subset(u)` returns a random subset of `u`.
* `random_subset_n(u,n)` returns a random subset of `u` with `n` elements (if possible).
* `random_ne_subset(u)` returns a non-empty random subset of `u`.

There are also Maxima's random functions.  For example, to create a random list use `random_permutation`.

It is probably much better **not** to use conditional statements when creating random objects.
For example, if you would like to create a random small prime number, try

    p : rand([2,3,5,7,11,13,17,19]);

This might not appear to be the neatest mathematical solution, but it is probably the most reliable.

### rand_with_step(lower,upper,step) ###

Returns a random number from the set `{lower, lower+step, lower+2*step, ... , final}`. The examples below explain behaviour the best.
Examples:

* `rand_with_step(-5,5,1)` returns a random number from the set \(\{-5,-4,-3,-2,-1,0,1,2,3,4,5\}\).
* `rand_with_step(-5,5,2)` returns a random number from the set \(\{-5,-3,-1,1,3,5\}\).
* `rand_with_step(-5,3,3)` returns a random number from the set \(\{-5,-2,1\}\).

The function `rand_range(lower,upper,step)` does the same thing.

### rand_with_prohib(lower,upper,list) ###

Returns a random integer from the set [lower,upper] such that it cannot be any value in `list`.
This list can include values which are also random variables, for example, generated by `rand_with_step`.
Examples:

* `rand_with_prohib(-5,5,[0])` returns a random number from the set \(\{-5,-4,-3,-2,-1,1,2,3,4,5\}\).
* `rand_with_prohib(-5,5,[-1,0,1,sqrt(pi)])` returns a random number from the set \(\{-5,-4,-3,-2,2,3,4,5\}\).
* `rand_with_prohib(-5,3,[-5/2,a])` returns a random number from the set \(\{-5,-4,-3,-2,-1,0,1,2,3\}\backslash\{a\}\).

This can be used with matrices, to generate a matrix with non-zero entries for example.  The unnamed function in this example ignores its arguments.

    matrixmap(lambda([ex],rand_with_prohib(-5,5,[0])),zeromatrix(5,5));

To create a matrix of a random size you can use Maxima's `makelist` function, e.g.

    M1:apply(matrix, makelist(makelist(2^n/3^m, n,1,4), m,1,3));

### rand_selection(ex, n) ###

Returns a list containing a random selection of `n` different items from the list/set `ex`.  If `ex` contains duplicates, then the result may also contain duplicates.

### rand_selection_with_replacement(ex, n) ###

Returns a list containing a random selection of `n` items from the list/set `ex`.

## Generating random polynomials

Here is an example which generates a random polynomial, of degree 5, with coefficients between 0 and 6.

    apply("+",makelist(rand(7)*x^(k-1),k,6));

## Generating random expressions which needs to be "gathered and sorted"

It is relatively common to want to be able to generate random expressions which need to be "gathered and sorted".  For example in \(2y-y+3y+1\) we need to collect together the \(y\) terms.

    simp:false;
    p:apply("+",makelist(ev(rand_with_prohib(-5,5,[0])*y^rand(2),simp), ev(rand(6)+2,simp)));
    p:unary_minus_sort(p);

Now, the output from the first expression will be a random expression in constants and \(y\) variables.   The second line tidies up the unary minus.  For more details of this, see [simplification](Simplification.md).

    4*y+5*y+(-2*y)
    4*y+5*y-2*y

## Random objects with corresponding information

It is often necessary to generate a random object with a number of separate aspects to it.  For example, if you have scientific data and you need to include this in a question.

    t:rand(5)+3;
    idx:rand(3)+1;  /* Array indexes in Maxima start at 1, rand(n) returns 0,...,n-1.  */
    l1:["Mercury","Earth","Mars"];
    l2:[3.61,9.8,3.75];
    p:l1[idx];
    ta:t*l2[idx]/(4*%pi^2);

The question text can then be

    A pendulum is located on {@p@}. What length should the pendulum have in order to have a period of {@t@}s?

This indexing with the variable `idx` is quite robust.  Note that indexes in Maxima start at \(1\), whereas `rand(n)` could return zero.

Another option is to use `rand()` on a list of lists, allowing to group the information of an object in a slick way:

    t:rand(5)+3;
    [p, g] : rand([["Mercury",3.61], ["Earth",9.81], ["Mars",3.75]]);
    ta:t*g/(4*%pi^2);

Here, `rand()` will return one random list of the given lists, say `["Earth",9.81]`. The assignment `[p, g] : ["Earth",9.81]` then works as one would expect, namely just as `p : "Earth"; g : 9.81;` would.

## Random objects satisfying a condition

It is often necessary to create random objects which satisfy constraints.  For example, if you want to randomly generate a "small" prime number, just select one from a list.

    p:rand([2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]);

It is much better to (i) enumerate specific cases or (ii) reverse engineer the question to avoid conditional statements than randomly generate examples and "hope" one pops up eventually.  The reason is that the pseudo-random number generator will repeat the process from a seed _every time_ the question is generated!  If you put in loops, this could risk delays and time-outs etc.

The following is NOT RECOMMENDED, but enough people have insisted on doing it to document this approach.

If you must (and you risk an infinite loop of course....) you can use Maxima's `for` command.  A simple example is as follows.

    q:1;
    for k while not(is(primep(q))) do block(q:rand(98)+1);

## Structured random matrices

STACK has a contributed library for creating structured random matrices.  The code is online in the [contributed library](https://github.com/maths/moodle-qtype_stack/blob/master/stack/maxima/contrib/rand_matrix.mac)

To use this library you must load it into the question variables.

* To use the local copy on your server: `stack_include("rand_matrix.mac");`
* To use the latest code from github: `stack_include_contrib("rand_matrix.mac");`

See documentation on [inclusions](../Authoring/Inclusions.md) for more detail of these functions.

Then you can create random matrices, e.g. to generate a \(3\times 3\) invertible matrix use `{@rand_invertible(3)@}`.

## See also

[Maxima reference topics](index.md#reference)



# Real intervals and sets of real numbers

STACK has a simple system for representing and dealing with real intervals and sets of real numbers.

Simple real intervals may be represented by the inert functions `oo(a,b)`, `oc(a,b)`, `co(a,b)`, and `cc(a,b)`.  Here the character `o` stands for open end point, and `c` for a closed end point.  So `oc(-1,3)` is the interval \( \{ x\in\mathbb{R} | -1 < x \text{ and } x\leq 3.\} \), and is displayed as \( (-1,3] \) with mismatching brackets in the tradition of UK mathematics.

The Maxima function `union` requires its arguments to be sets, and intervals are not sets.  You must use the `%union` function (from the package `to_poly_solve`) to join simple intervals and combine them with discrete sets. E.g. `%union(oo(-2,-1),oo(1,2))`

Note that the `%union` function sorts its arguments (unless you have `simp:false`), and sort puts simple intervals of the form `oo(-inf,a)` out of order at the right hand end. So, some sorting functions return lists of intervals, not `%union` as you might expect, to preserve the order.

As arguments, the `%union` command can take both simple intervals and sets of discrete real numbers, e.g.

    %union(oo(-inf,0),{1},oo(2,3));

Similarly, STACK provides `%intersection` to represent an intersection of intervals (which the package `to_poly_solve` does not have).

Predicate functions

1. `intervalp(ex)` returns true if `ex` is a single simple interval.  Does not check `ex` is variable free, so `oo(a,b)` is a simple interval.   `{}`, `none`, `all` and singleton sets are not considered "intervals" by this predicate, use `realsetp` instead.  The primary purpose of this predicate is to detect intervals `oo`, `oc` etc within code.
2. `inintervalp(x, I)`  returns true if `x` is an element of `I` and false otherwise.  `x` must be a real number.  `I` must be a set of numbers or a simple interval of the form `oo(a,b)` etc.
3. `trivialintervalp(ex)` returns true if `ex` is a trivial interval such as \((a,a)\).
4. `unionp(ex)` is the operator a union?
5. `intersectionp(ex)` is the operator an intersection?
6. `realsetp(ex)` return true if `ex` represents a definite set of real numbers, e.g. a union of intervals.  All end points and set elements must be real numbers, so `oo(a,b)` is not a `realset`.  If you want to permit variables in sets and as endpoints use `realset_soft_p` instead.
7. `interval_disjointp(I1, I2)` establishes if two simple intervals are disjoint.
8. `interval_subsetp(S1, S2)` is the real set `S1` contained within the real set `S2`?
9. `interval_containsp(I1, S2)` is the simple interval `I1` an explicit sub-interval within the real set `S2`?  No proper subsets here, but this is useful for checking which intervals a student has.

Basic manipulation of intervals.

1. `interval_simple_union(I1, I2)` join two simple intervals.
2. `interval_sort(I)` takes a list of intervals and sorts them into ascending order by their left hand ends.  Returns a list.
3. `interval_connect(S)` Given a `%union` of intervals, checks whether any intervals are connected, and if so, joins them up and returns the ammended union.
4. `interval_tidy(S)`  Given a union of sets, returns the "canonical form" of this union.
5. `interval_intersect(S1, S2)` intersect two two simple intervals or two real sets, e.g. `%union` sets.
6. `interval_intersect_list(ex)` intersect a list of real sets.
7. `interval_complement(ex)` take a `%union` of intervals and return its complement.
8. `interval_set_complement(ex)` Take a set of real numbers, and return the `%union` of intervals not containing these numbers.
9. `interval_count_components(ex)` Take a set of real numbers, and return the number of separate connected components in the whole expression.  Simple intervals count as one, and sets count as number number of distinct points in the set.  Trivial intervals, such as the empty set, count for 0.  No simplification is done, so you might need to use `interval_tidy(ex)` first if you don't want to count just the representation.

## Natural domains, and real sets with a variable.

The function `natural_domain(ex)` returns the natural domain of a function represented by the expression `ex`, in the form of the inert function `realset`.  For example `natural_domain(1/x)` gives

    realset(x,%union(oo(0,inf),oo(−inf,0)));

The inert function `realset` allows a variable to be passed with a set of numbers.  This is mostly for displaying natural domains in a sensible way.  For example, where the complement of the intervals is a discrete set, the `realset` is displayed as \(x\not\in \cdots\) rather than \(x \in \cdots\) which is normally much easier to read and understand.

    realset(x,%union(oo(0,inf),oo(-inf,0)));

is displayed as \(x \not\in\{0\}\).

## Validation of students' answers

Students must simply type `union` (not `%union`) etc.

Validation of students' answer has a very loose sense of "type".  When we are checking the "type" of answer, if the teacher's answer is a "set" then the student's answer should also be a "set" (see `setp`).  If the teacher's answer is actually a set in the context where an interval should be considered valid, then the teacher's answer should be the inert function `%union`, e.g. `%union({1,2,3})`, to bump the type of the teacher's answer away from set and into `realset`.

Validation does some simple checks, so that mal-formed intervals such as `oo(1)` and `oo(4,3)` are rejected as invalid.

## Assessment of students' answers

The algebraic equivalence answer test will apply `interval_tidy` as needed and compare the results. Currently the feedback in this situation provided by this answer test is minimal.

If the student input is an interval, it is possible to access the upper and lower boundary through the `first` and `last` Maxima functions. For example, a PRT node checking whether the boundaries of an interval are correct (but not necessarily the interval type, like `co` or `oo`) can be done checking the algebraic equivalence of the student answer `[first(ans1), last(ans1)]` and the teacher answer `[first(ta1), last(ta1)]`.

Students will sometimes enter a closed interval as `[a, b]` or an open interval as `(a, b)`, appealing to common notation. In STACK the answer `[a,b]` is interpreted as a list however, and it can be convert into `cc(a,b)` using 

    ans1interval : if listp(ans1) then cc(first(ans1), last(ans1)) else ans1;

Similary, the answer `(a,b)` is interpreted as `ntuple(a,b)`, see [Sets, lists, sequences n-tuples](Maxima_background.md#sets-lists-sequences-n-tuples). There is no direct predicate function for n-tuples, but this answer can be converted into `oo(a,b)` using

    ans1interval : if is(safe_op(ans1) = "ntuple") then oo(first(ans1), last(ans1)) else ans1;



# Rules and patterns

Maxima has a system for defining rules and patterns.  For example, in desktop maxima

```
matchdeclare([a],true);
let(sin(a)^2, 1-cos(a)^2);
letsimp(sin(x)^4);
```

will give \(\sin(x)^4 \rightarrow \cos^4(x)-2\,\cos^2(x)+1\).

Support for `let` was added in v4.8.0 (November 2024), and only partial support is currently available.

In particular, Maxima's `let` function makes use of a special operator `->` which is unsupported in the Maxima-PHP connection.  To accommodate this, you must place `let` commands inside a block which returns it's last element.

For example, put the following the question variables will work (but the above example will not):

```
matchdeclare([a],true);
p1:(let(sin(a)^2, 1-cos(a)^2), letsimp(sin(x)^4));
```
and `{@p1@}` in some castext (e.g. the question) will give \(\cos^4(x)-2\,\cos^2(x)+1\).  Typically, Maxima will not perform this simplification.

### Matrix example

Imagine we want `I` to represent the identity matrix.

```
orderless(I);
matchdeclare([a],true);
/* Note use of a block to make sure the return value ("true" here) can be parsed back into PHP. */
(let(I*a, a),let(I^2, I),true);
p:letsimp(expand((A+I)^3));
```

Then castext such as `{@p@}` gives \({A^3+3\cdot A^2+3\cdot A+I}\).



# Simplification & ordering

## Algebraic equivalence

Is \((a^x)^y \equiv a^{x\,y}\)?  Well, it depends!  In particular you can easily derive the contradiction
\[ -1 = (-1)^1 = (-1)^{2\times \frac{1}{2}} \]
and using our rule \((a^x)^y \equiv a^{x\,y}\)
\[ = \left({(-1)^{2}}\right)^{\frac{1}{2}} = 1^{\frac{1}{2}} = 1.\]
To avoid problems like this we therefore have decided that

    ATAlgEquiv((a^x)^y, a^(x*y)) = [0, ""]

If you are teaching rules of indices to students for the first time this might come as a surprise!  If you would like STACK to implement this rule, then you need to also `assume(a>0)`.  This can be done in the feedback variables.  This is a design decision and not a bug (and is recorded in the system unit tests)!

Note the Maxima function `rootscontract` which converts products of roots into roots of products.

Note that Maxima resists the transformation \( (a^b)^c \rightarrow a^{bc} \), which is not always correct.  Instead, and when you know this will be correct, use `radcan` with `radexpand:all`.  For example, `ev(radcan((a^b)^c),radexpand:all,simp)`.

## Ordering terms

Maxima chooses an order in which to write terms in an expression. By default, this will use reverse lexicographical order for simple sums, so that we have \(b+a\) instead of \(a+b\).
In elementary mathematics this looks a little odd!  One way to overcome this is to use simplification below but another way is to alter the order in which expressions are transformed.

To alter the order in STACK you can use the Maxima commands `orderless` and `ordergreat`.  To have \(a+b\) you can use

    ordergreat(a,b);

See Maxima's documentation for more details.

1. Only one `orderless` or `ordergreat` command can be issued in any session.  The last one encountered will be used and the others ignored.
2. No warnings or errors are issued if more than one is encountered.
3. The `orderless` or `ordergreat` command is executed _first_ before any other commands.  Therefore the argument names are literal atoms and you _cannot_ use variable names.

As an example of the last point, consider the following in _desktop maxima_

   p:a+b;
   x:a;
   ordergreat(x);
   p:a+b;

The output of the last line, as expected will be \(a+b\).  However, if you put the above in the question variables then effectively you will have the following.

   ordergreat(x);
   /* Other stuff, including setting up error trapping for the execution of commands below. */
   p:a+b;
   x:a;
   p:a+b;

The output of the last line, as expected will be \(b+a\).  STACK moves `ordergreat` to be executed first, and at that point you have no assigned `x` to be the atom `a`.

This is a limitation, especially in questions where you want to have a randomly generated variable name.

## Fixing the order of some terms in sums and products

By default, maxima returns `a+b` as `b+a` because `b` is "greater" than `a`.

Sometimes we don't want to change the order in which Maxima displays expressions, but within part of an expression we do want to fix the order in the sum, even with `simp:true`.

One approach is to use the library in the rule-based simplifier and define

    fix_sum([ex]):=apply("nounadd",ex);

Here are some test cases (WIP)

````
{@a+b@}, </br> </br>
{@fix_sum(a,b)@}, </br>
{@fix_sum(a,b,c)@}, </br>
{@fix_sum(a,-b)@}, </br>
{@fix_sum(-a,b)@}, </br>
{@fix_sum(a,-b,c)@}, </br>
{@fix_sum(a,3)@}, </br>
{@fix_sum(a,-2,b)@}, </br>
{@fix_sum(a,3/2)@}, </br>
{@(simp:false,fix_sum(a,-3/2))@}, </br>
{@fix_sum(a,b,a+b)@}, </br>
{@fix_sum(a,b,fix_sum(a,b))@}</br>
{@fix_sum(a,b^fix_sum(a,b))@}</br>
</br>

{@(simp:false,verb_arith(fix_sum(a,-2,b)))@}, </br>
{@(simp:false,fix_sum(a,-3/2))@}, </br>
````

## Logarithms to an arbitrary base

By default, Maxima does not provide logarithms to an arbitrary base.  To overcome this, STACK provides a function `lg` for student entry.

* `lg(x)` is log of \(x\) to the base 10.
* `lg(x, a)` is log of \(x\) to the base \(a\).

STACK provides no simplification rules for these logarithms.  To simplify you must transform back to natural logarithms.

For example (with `simp:true` or `simp:false`)

    p:lg(27, 3)
    q:ev(p, lg=logbasesimp)

results in `p=lg(27, 3)`, and `q=3`.

The algebraic equivalence function `algebraic_equivalence`, and so anything upon which it depends, will automatically remove logarithms to other bases.
This includes the answer tests as needed.

## Selective simplification {#selective-simplification}

The level of simplification performed by Maxima can be controlled by changing Maxima's global variable `simp`, e.g.

    simp:true

When `simp` is set to `false`, no simplification is performed and Maxima is quite happy to deal with an expression such as \(1+4\) without actually performing the addition.
This is most useful for dealing with very elementary expressions, and for [showing working](../CAS/Matrix.md#Showing-working).

This variable can be set at the question level using the [options](../Authoring/Question_options.md) or for each [Potential response tree](../Authoring/Potential_response_trees.md).

When `simp` is set to `false`, you can evaluate an expression with simplification turned on by using `ev(..., simp)`, for example:

    simp:false;
    a:ev(1+1,simp);

will give \(a=2\).

### Within CASText (question text, general feedback, etc.)

Sometimes it is useful to control the level of simplification applied to expressions included within [CASText](../Authoring/CASText.md) using `{@...@}`.
In particular, to show steps in working, it is often necessary to turn simplification off.

To selectively control simplification within CASText (including the general feedback), you can use the following methods:

1. Set `simp:false` in the question options, or at the end of your question variables. That way all expressions in the CASText will be unsimplified, but you can use `{@ev(...,simp)@}` to simplify selectively.
2. Use evaluation flags to control the level of simplification for an individual CAS expression, for example:
```
{@3/9,simp=false@}
```
3. Use a [define block](../Authoring/Question_blocks/Static_blocks.md#define-block) to set the value of `simp`, e.g.
```
[[define simp="false"/]]
\({@3/9@} \neq {@1+1@}\)
[[define simp="true"/]]
\({@3/9@} \neq {@1+1@}\)
```
will produce \(\frac{3}{9}\neq1+1\) followed by \(\frac{1}{3}\neq2\).
4. Switch simplification
```
{@(simp:false,3/9)@}
```
This command sets the value of `simp` for this expression, and all others which follow, much like the define block above.

## Unary minus and simplification

There are still some problems with the unary minus, e.g. sometimes we get the display \(4+(-3x)\) when we would actually like to always display as \(4-3x\).
This is a problem with the unary minus function `-(x)` as compared to binary infix subtraction `a-b`.

To reproduce this problem type in the following into a Maxima session:

    simp:false;
    p:y^3-2*y^2-8*y;

This displays the polynomial as follows.

    y^3-2*y^2+(-8)*y

Notice the first subtraction is fine, but the second one is not.  To understand this, we can view the internal tree structure of the expression by typing in

    ?print(p);
    ((MPLUS) ((MEXPT) $Y 3) ((MMINUS) ((MTIMES) 2 ((MEXPT) $Y 2))) ((MTIMES) ((MMINUS) 8) $Y))

In the structure of this expression the first negative coefficient is `-(2*y^2)` BUT the second is `-(8)*y`.
This again is a crucial but subtle difference!
To address this issue we have a function

    unary_minus_sort(p);

which pulls "-" out the front in a specific situation: that of a product with a negative number at the front.
The result here is the anticipated `y^3-2*y^2-8*y`.

Note that STACK's display functions automatically apply `unary_minus_sort(...)` to any expression being displayed.

## Really insisting on printing the parentheses

Why does STACK (i.e. Maxima) not print out the parentheses?  For example, try the following.

    simp:false;
    p1:(a+b)+c;
    tex(p1);

The result is \(a+b+c\).  Where have the parentheses gone?  On the other hand `p2:a+(b+c)` is displayed as \(a+\left(b+c\right)\).  Why are these displayed differently?  Assuming `simp:false` and using Maxima's `?print` command we can see the internal structure.

* `?print(a+b+c)` gives `((MPLUS) $A $B $C)`.  This means we have the flattened (nary) sum of the three variables.  This will always not have brackets.
* `?print((a+b)+c)` gives `((MPLUS) ((MPLUS) $A $B) $C)`.  This is not yet flattened to an nary sum, but Maxima's tex routines suppress the parentheses, even with `simp:false`.  This is part of the problem.
* `?print(a+(b+c))` gives `((MPLUS) $A ((MPLUS) $B $C))`.  This is not yet flattened to an nary sum, and in this case it displayed as \(a+\left(b+c\right)\) by Maxima's TeX function.

Note, this display problem is not a bug.  Experts would interpret \(a+b+c\) as \((a+b)+c\) not as \(a+(b+c)\).  This is only a problem in teaching when we want to display (arguably not needed) parentheses.  To solve this display problem STACK has an inert `disp_parens` function.  All this function does is print round brackets (parentheses) around its argument.

For example, try the following.

    simp:false;
    p1:disp_parens(a+b)+c;
    tex(p1);

The result is \({\left( a+b \right)+c}\).

Parentheses can also be added to other expressions which, strictly speaking, do not need them. For example `int(disp_parens(x-2),x)` is displayed as \({\int {\left( x-2 \right)}{\;\mathrm{d}x}}\).

It may be necessary to remove the `disp_parens` from an expression.  STACK provides the function `remove_disp_parens(ex)` to remove this inert display function.  Actually, this function is remarkably simple.

    remove_disp_parens(ex) := ev(ex, disp_parens=lambda([ex2], ex2))$

The function `disp_parens` has no mathematical definition.  It just changes the TeX output.  The above function re-evaluates the expression, with this function equal to the identity function (`lambda([ex2], ex2))`).  Giving `disp_parens` this mathematical definition effectively removes it.

Note that the answer tests do not remove the `disp_parens` function from a teacher's expression.  Hence, `a+b+c` and ``disp_parens(a+b)+c` are not algebraically equivalent.  Teachers who use these display functions must remove them before answer tests are applied.  Students cannot use the `disp_parens` function.  Indeed, currently a student's input of `(a+b)+c` is displayed as Maxima does without the brackets (yes, this might be considered a bug).

## Selecting, and highlighting part of an expression

Like `disp_parens`, STACK provides a function `disp_select` which highlights part of an expression.  All this function does is colour the argument red and underline it.  For example `1+disp_select(x^2+2)` is displayed as \({1+\color{red}{\underline{x^2+2}}}\).  Note, the combination of colour and the underline is because it is considered poor practice to use colour alone to convey meaning.

STACK provides the function `remove_disp_select(ex)` to remove this inert display function.  The function `remove_disp(ex)` removes all inert display functions.

When creating feedback it is often useful to select, and highlight, part of an expression.  STACK provides a function `select(p1, ex)` to do this.  The select function traverses the expression tree for `ex` and when it encounters a sub-tree for which the predicate `p1` is true it adds `disp_select` to the sub-tree and stops traversing any further down that sub-tree.  While nested `disp_select` are possible (and will display multiple underlines: another reason for having underline) this particular function stops once `p1` is true.  You will need to build nested display by hand.

For example, to select all the integers in an expression you can use the predicate `integerp` and `select(integerp, 1+x+0.5*x^2)` gives \(\color{red}{\underline{1}}+x+0.5\cdot x^{\color{red}{\underline{2}}}\).

It is possible to use any of the existing predicate functions, or to define your own function in the question variables.

The function `select_apply(f1, ex)` traverses the expression and when it encounters the `disp_select` function it applied the function `f1` to that sub-tree of the expression.  This allows for selective simplification/modification of highlighted sub-trees.  For example,

    simp:false;
    p1:select(zeroMulp, (1-1)*x^2+0*x+1);
    p2:select_apply(simplify, p1);
    p3:select_apply(simplify, p1, false);

generates the following displayed expressions.

* `p1` displays as \({\left(1-1\right)\cdot x^2+\color{red}{\underline{0\cdot x}}+1}\).  We have selected all the parts for which the predicate `zeroMulp` is true.  This is the predicate which checks if the rule \(0 \times x \rightarrow 0 \) is applicable.  While the coefficient of \(x^2\) is equivalent to zero, it is unsimplified and the predicate `zeroMulp(1-1)` is false. This sub-tree is not selected by this predicate.
* `p2` displays as \({\left(1-1\right)\cdot x^2+0+1}\).  The displayed expression is subjected to the function `simplify`, and the displayed part replaced.  The rest of the expression is unchanged. By default the `disp_select` is removed and so the result is not coloured and underlined.
* `p3` displays as \({\left(1-1\right)\cdot x^2+\color{red}{\underline{0}}+1}\).  Notice the third, optional boolean, argument to `select_apply` in `p3`.  This argument will decide whether to continue to display the `disp_select` display or remove it (now the function has been applied).  The default is `true`, so here the red underline is not removed.

## If you really insist on a kludge....

In some situations you may find you really do need to work at the display level, construct a string and display this to the student in Maxima.
Please avoid doing this!

    a:sin(x^2);
    b:1+x^2;
    f:sconcat("\\frac{",stack_disp(a,""),"}{",stack_disp(b,""),"}");

Then you can put in `\({@f@}\)` into one of the CASText fields. Note, you need to add LaTeX maths delimiters, because when the CAS returns a string the command `{@f@}` will just display the contents of the string without maths delimiters.

## Tips for manipulating expressions

How do we do the following in Maxima?
\[ (1-x)^a \times (x-1) \rightarrow  -(1-x)^{a+1}.\]
Try

    q:(1-x)^a*(x-1);
    q:ratsubst(z,1-x,q);
    q:subst(z=1-x ,q);


How do we do the following in Maxima?
\[ (x-1)(k(x-1))^a \rightarrow  (x-1)^{a+1}k^a.\]

     factor(radcan((x-1)*(k*(x-1))^a))


Maxima's internal representation of an expression sometimes does not correspond with what you expect -- in that case, `dispform` may help to bring it into the form you expect. For example, the output of `solve` in the following code shows the \(b\) in the denominator as \(b^{-1}\) which gives unnatural-looking output when a value is substituted in -- this is fixed by using `dispform` and substituting into that variants instead.

    simp:true;
    eqn:b = 1/(6*a+3);
    ta1: expand(rhs(solve(eqn,a)[1]));
    dispta1:dispform(ta1);
    simp:false;
    subst(2,b,ta1);
    subst(2,b,dispta1);


## Creating sequences and series

One problem is that `makelist` needs simplification.  To create sequences/series, try something like the following

    an:(-1)^n*2^n/n!
    N:8
    S1:ev(makelist(k,k,1,N),simp)
    S2:maplist(lambda([ex],ev(an,n=ex)),S1)
    S3:ev(S2,simp)
    S4apply("+",S3)

Of course, to print out one line in the worked solution you can also `apply("+",S2)` as well.

To create the binomial coefficients

    simp:false;
    n:5;
    apply("+",map(lambda([ex],binomial(n,ex)*x^ex), ev(makelist(k,k,0,5),simp)));

## Surds

Imagine you would like the student to expand out \( (\sqrt{5}-2)(\sqrt{5}+4)=2\sqrt{5}-3 \).
There are two tests you probably want to apply to the student's answer.

1. Algebraic equivalence with the correct answer: use `ATAlgEquiv`.
2. That the expression is "expanded": use `ATExpanded`.

You probably then want to make sure a student has "gathered" like terms.  In particular you'd like to make sure a student has either
\[ 2\sqrt{5}-3 \text{ or } \sqrt{20}-3\]
but not \[ 5+4\sqrt{2}-2\sqrt{2}+6.\]
This causes a problem because `ATComAss` thinks that \[ 2\sqrt{5}-3 \neq \sqrt{20}-3.\]
So you can't use `ATComAss` here, and guarantee that all random variants will work by testing that we really have \(5+4\sqrt{2}\) for example.

What we really want is for the functions `sqrt` and `+` to appear precisely once in the student's answer, or that the answer is a sum of two things.

When surds appear in equations and sets we might need to force some kinds of simplification.  For example, when we try to establish that this set (the student's answer)
\[ {\left \{x=-\frac{\sqrt{19}}{2\cdot \sqrt{3}}-\frac{1}{2} , x=\frac{\sqrt{19}}{2\cdot \sqrt{3}}-\frac{1}{2} \right \}} \]
is equivalent to
\[ {\left \{x=\frac{-\sqrt{57}-3}{6} , x=\frac{\sqrt{57}-3}{6} \right \}} \]

If we were dealing with two *numbers*, then Maxima has no problem in establishing that 
\[ \frac{-\sqrt{57}-3}{6}-\frac{\sqrt{19}}{2\cdot \sqrt{3}}-\frac{1}{2} = 0\]
On the maxima command line try `p:(-3 + sqrt(9 + 48))/6+1/2 - sqrt(1/4 + 4/3);` then `radcan(p)`.  Within the AlgEquiv test `radcan` is applied automatically to _numbers_ within an expression, and this returns zero.

The problem with _sets_ is that we don't have the difference between two numbers.  We're trying to write all numbers in an unambiguous form, and then comepare the representation.  This (subtle) difference is the problem.  Instead of looking at equivalence with zero, we need to contol the form of surds explicitly.

### Control of surds ###

See also the Maxima documentation on `radexpand`.  For example

    radexpand:false$
    sqrt((2*x+10)/10);
    radexpand:true$
    sqrt((2*x+10)/10);

The first of these does not pull out a numerical denominator.  The second does.

Similarly, consider the output from these two examples.

    p1:(-3 + sqrt(9 + 48))/6;
    radcan(p1);
    trigrat(p1);
    radcan(trigrat(p1));

    p2:-1/2 + sqrt(1/4 + 4/3);
    radcan(p2);
    trigrat(p2);
    radcan(trigrat(p2));

Why don't we always apply `trigrat` to expressions?  Without knowing something about the expression, we might "expand" out the terms which causes a practical failure of the test due to timeout.  E.g. `expand((x+y)^(2^100))` is never going to execute.  Similarly, `trigrat` causes some (trig) expressions to expand, see below.


### Trig simplification ###

Maxima does have the ability to make assumptions, e.g. to assume that \(n\) is an integer and then simplify \(3\cos(n\pi/2)^2\) to \( \frac{3}{2}(1+(-1)^n)\).  Assume the student's answer is `ans1` then define the following feedback variables:

    declare(n,integer);
    sans1:ev(trigrat(ans1),simp);

The variable `sans1` can then be used in the PRT.  Just note that `trigrat` writes powers of trig functions in terms of multiple angles.  This can have an effect of "expanding" out an expression.  E.g. `trigrat(cos(n)^20)` is probably still fine, but `trigrat(cos(n)^2000)` is probably not!  For this reason `trigrat` is not part of the default routines to establish equivalence.  Trig simplification, especially when we make assumptions on variables like \(n\), needs to be done on a question by question basis.

## Boolean functions

See the page on [propositional logic](../Topics/Propositional_Logic.md).

## Further examples

Some further examples are given elsewhere:

* Matrix examples in [showing working](Matrix.md#Showing-working).
* An example of a question with `simp:false` is discussed in [authoring quick start 7](../AbInitio/Authoring_quick_start_7.md).
* Generating [random algebraic expressions](Random.md) which need to be "gathered and sorted".

Note also that [question tests](../STACK_question_admin/Testing.md#Simplification) do not simplify test inputs.



# STACK - Maxima Sandbox

It is very useful when authoring questions to be able to test out Maxima code on your local machine in the same environment in which STACK uses [Maxima](Maxima_background.md) on your server. That is to say, to run a desktop version of Maxima with the local settings and STACK specific functions loaded.  You can copy the Maxima code from the question testing page into the sandbox for offline testing and debugging of a question.  This is also used in [reporting](../Authoring/../STACK_question_admin/Reporting.md) and analysis of students' responses. To do this you will need to load the libraries of Maxima functions specific to STACK. You may also want to copy some of your local settings from the server to your local machine to ensure an identical setup, but this is not strictly necessary for most purposes.

The first step is to install wxMaxima on your local machine (http://maxima.sourceforge.net/).

### Getting the STACK libraries

You will need to download the STACK files onto your local machine.  Download all the STACK files from GitHub (git clone or as a .zip).  E.g. try `https://github.com/maths/moodle-qtype_stack/archive/master.zip`

The only files you need to run the sandbox are contained within the directory

    stack/maxima/

This directory also contains the wxMaxima file `sandbox.wmx` which is the "sandbox" interface file. Your goals are (i) to set Maxima's path so it can find all the files you have downloaded, and (ii) to load the file

    stack/maxima/stackmaxima.mac

Copy `sandbox.wmx` somewhere you can find it later and edit this file to reflect the location of the above file on your local machine.

On a Microsoft operating system, if you place the all the files (i.e. clone or unzip the download) into

    c:/tmp/stackroot

the `sandbox.wmx` should work without further adjustment.

Otherwise open `sandbox.wmx` with wxMaxima and follow the further instructions it contains to setup the path for Maxima.  __Note, the backslash character `\` is a control character so you will need to edit the path to replace the `\` with `/` in wxMaxima.__ Execute the sandbox file with wxMaxima when you have updated the settings with `cell > Evaluate all cells`.  If you see something like the following you have set this up correctly (version numbers will vary).

    [ STACK-Maxima started, library version 2022022300 ]

You can test this out by using, for example, the `rand()` function.

    rand(matrix([5,5],[5,5]));

to create a pseudo-random matrix.  If `rand` returns unevaluated, then you have not loaded the libraries correctly.

An alternative approach on a Microsoft operating system is to copy the contents of (a working) `sandbox.wmx` file into a

    %USERPROFILE%/Maxima/stacklocal.mac

Using `load("stacklocal")` in any worksheet will load the STACK environement.
On Linux you can copy the file `stacklocal.mac` to your home directory `~/.maxima/`.

### Using the answer tests

Please make sure you read the page on [answer tests](../Authoring/Answer_Tests/index.md) first.

Informally, the answer tests have the following syntax

    [Errors, Result, FeedBack, Note] = AnswerTest(StudentAnswer, TeacherAnswer, Opt)

actually the results returned in Maxima are

    [Valid, Result, FeedBack, Note] = AnswerTest(StudentAnswer, TeacherAnswer, Opt)

Errors are echoed to the console, and are trapped by another mechanism.  The valid field is used to render an attempt invalid, not wrong.

To call an answer test directly from Maxima, you need to use the correct function name.   For example, to call the algebraic equivalence (AlgEquiv) answer test you need to use

    ATAlgEquiv(x^2+2,x*(x+1));

The values returned are actually in the form

    [true,false,"",""]

Feedback is returned in the form of a language tag which is translated later. For example,

    (%i1) ATInt(x^2,x*(x+1),x);
    (%o1) [true,false,"ATInt_generic. ",
           "stack_trans('ATInt_generic' , !quot!\\[2\\,x+1\\]!quot!  , !quot!\\(x\\)!quot!  , !quot!\\[2\\,x\\]!quot! ); "]

If you just want to decide if two expressions are considered to be algebraically equivalent, then use

    algebraic_equivalence(ex1,ex2);

This is the function the answer test `ATAlgEquiv` uses without all the wrapper of a full answer test.

### Useful tips

STACK turns off the traditional two-dimensional display, which we can turn back on with the following command.

    display2d:true;

## Setting Maxima's Global Path (Microsoft)

Setting the path in Maxima is a problem on a Microsoft platform.  Maxima does not deal well with spaces in filenames, for example.  The simplest solution is to create a directory

    C:/maxima

and add this to Maxima's path.  Place all Maxima files in this directory, so they will then be seen by Maxima.
For Maxima 5.43.2, edit, or create, the file

    C:/Program Files/maxima-5.43.2/share/maxima/5.43.2/share/maxima-init.mac

ensure it contains the following lines, possibly modified to reflect the directory you have chosen

    file_search_maxima:append([sconcat("C:/maxima/###.{mac,mc}")],file_search_maxima)$
    file_search_lisp:append([sconcat("C:/maxima/###.{lisp}")],file_search_lisp)$

Other versions of Maxima are similar.

## Using preconfigured files on Linux and Windows

Here you will find some notes to support you to install and use  the  STACK Sandbox in Maxima including the plotting options. The good note is, that Gnuplot is delivered with Maxima on Windows. We can use it. For Linux you will find a file `moodle-qtype_stack_master/stack/maxima/stacklocallinux.mac` and for Window `moodle-qtype_stack_master/stack/maxima/stacklocalwin.mac`. Goal is to use the commands `load("stacklocalwin.mac")` or `load("stacklocallinux.mac")` in your Maxima worksheets.

### Preparation

The Maxima variable  `maxima_userdir` returns the user Maxima directory on your Linux or Windows machine. This is used to reduce the installation effort and no admin rights are needed.

Unzip the zip-file `moodle-qtype_stack-master.zip` in your `maxima_userdir`, so that the code resides in `maxima_userdir/moodle-qtype_stack_master/`.
Create the additional directories:
  1. `maxima_userdir/moodle-qtype_stack_master/tmp/`
  2. `maxima_userdir/plots/`
  2. `maxima_userdir/tmp/`


On Windows the directories are afterwords
  1. `%USERPROFILE%\maxima\moodle-qtype_stack_master\`
  1. `%USERPROFILE%\maxima\moodle-qtype_stack_master\tmp\`
  1. `%USERPROFILE%\maxima\plots\`
  1. `%USERPROFILE%\maxima\tmp\`

On Linux the directories are afterwords
  1. `~/.maxima/moodle-qtype_stack_master/`
  1. `~/.maxima/moodle-qtype_stack_master/tmp/`
  1. `~/.maxima/plots/`
  1. `~/.maxima/tmp/`

To use the STACK Sandbox in Maxima, just copy the file `stacklocalwin.mac` or `stacklocallinux.mac` into your `maxima_userdir`. Thus it is available for the `load` command. 

If git is available on your machine, you got to `maxima_userdir` in terminal an run the command `git pull https://github.com/maths/moodle-qtype_stack/` and move `moodle-qtype_stack` to `moodle-qtype_stack-master`.

### Troubleshouting

Sometimes one has to adjust the path to the directory where the svg are saved. Please try 
`IMAGE_DIR:sconcat(maxima_userdir,"/plots/")` if `IMAGE_DIR:sconcat(maxima_userdir,"/plots")` does not work. (And vice versa).


### Lets plot

To show the plots produced by STACK a small loop way is used. STACK stores the plot in an SVG file, which is written to a temporary directory. To show the plots an html file `maxima_userdir/plots/test.html` is used. To generate the file use  `add2HTML(string,fileappend)` is used.
The code looks like:
```
load("stacklocalwin.mac");
res:plot(cos(x),[x,0,6]);
add2HTML(res,false);
showHTML();
```
A file `testPlot.wxm` is in `stack/maxima/` included.

If you are not using Firefox on your Linux, you can adjust your browser in `stacklocallinux.mac`.

## Reflecting the settings on your server

The healthcheck page (Moodle admin access only) displays the contents of the Maxima configuration file which is written to the sever.  This contains Maxima commands to update the path (which you probably don't want to copy) and also the function `STACK_SETUP(ex)` which configures your particular version of STACK.  You may want to replace `STACK_SETUP(ex)` in the sandbox with `STACK_SETUP(ex)` from the Moodle server. For most users this should not be needed, and is most useful for advanced debugging where significant differences between versions matters.

It is more important to match the version of the STACK code you downloaded from github with the version you have on your server.  The STACK documentation page on your server gives the version number of the STACK code at the bottom of the documentation front page.  For example

    https://stack-demo.maths.ed.ac.uk/demo/question/type/stack/doc/doc.php/

shows the version of the STACK code the demo site is running. 

`{@stackmaximaversion@}` and `{@MAXIMA_VERSION@}` in a question text will return the STACK and Maxima version installed on your LMS. 



# Statistics support in STACK.


The following optional packages provide statistics support in Maxima:

    load("stats");
    load("distrib");
    load("descriptive");

Please see Maxima's documentation for information on the functions these packages contain.

These packages are included by default. The Debian package manager currently has a release of Maxima (as of Nov 2015) without these packages and attempting to load them renders STACK unusable. For this reason, they may have been disabled by your system administrator and your server may not support inclusion of these packages.

## Package: descriptive

Note that the "descriptive" package includes a number of functions to plotting graphs, such as boxplots and scatterplot.  These are not supported by STACK.

## STACK functions

STACK provides the `mode` function which returns the modal value in a list.



# Maxima strings in STACK questions

Strings are a basic data type in Maxima.  The predicate function `stringp(ex)` determines whether an expression is a string.  The function `string(ex)` takes a Maxima expression and returns a string representation.  We do not support Maxima's `parse_string` function.  There is no way to turn a string into a Maxima expression through STACK.  For example, if you use the string input you cannot later parse the student's answer into a Maxima expression.  Therefore, only use the string input if your answer is actually a string.

_The whole point of STACK is that teachers should seek to establish mathematical properties and the string match tests are provided for completeness (and because they are trivial to implement).  Experienced question authors almost never use the string match tests.  If you find yourself needing to use the string match tests for something mathematical please contact the developers._

There are 4 [string-related answer tests](../Authoring/Answer_Tests/String.md).

* String
* StringSloppy
* Levenshtein
* SRegExp

If your answer is a language string, then please consider using the [Damerau-Levenshtein distance](../Topics/Levenshtein_distance.md) rather than a string match.

## LaTeX within Maxima strings

You have to protect LaTeX backslashes in Maxima strings.  This is tedious, tricky and error prone!

For example, you have to define Maxima strings such as "\&#8203;\&#8203;( f(&#8203;n)=\&#8203;\&#8203;sin(n\&#8203;\&#8203;pi) \&#8203;\&#8203;)"

To help with this there is a tool to automatically add in these extra slashes as a one-off process.

The adminui tools have a chat page.  You can find the tool under the "STACK question dashboard" -> "Send general feedback to the CAS".  At the bottom of this page is an option "Protect slashes within Maxima string variables".

The "Protect slashes within Maxima string variables" option will add slashes _every time_ the option is selected, so this is effectively a one-off process.  However, you can write the strings in normal LaTeX and proof-read. Move these to maxima strings, before converting to Maxima strings.



## Atoms, subscripts and fine tuning the LaTeX display

Everything in Maxima is either an _atom_ or an _expression_. Atoms are either an integer number, float, string or a name.  You can use the predicate `atom()` to decide if its argument is an atom.  Expressions have an _operator_ and a list of _arguments_. 

You can change the TeX output for an atom with Maxima's `texput` command.  E.g. `texput(blob, "\\diamond")` will display the atom `blob` as \( \diamond \).  If you place `texput` commands in the question variables, this affects the display everywhere in the question including the inputs.  E.g. if a student types in `blob` then the validation feedback should say something like "your last answer was: \( \diamond \)".

Note that the underscore symbol is _not_ an operator.  Thus `a_1` is an atom in maxima. Hence, the atoms `a1` and `a_1` are not considered to be algebraically equivalent.   If you would like to consolidate subscripts in students' input see the documentation on the input option `consolidatesubscripts` in the [extra options](../Authoring/Inputs/index.md).  Also note that since the underscore is not an operator, an expression such as `(a_b)_c` is not valid Maxima syntax, but `a_b_c` is a valid name for an atom.

Display with subscripts is a subtle and potentially confusing issue because subscript notation in mathematics has many different uses.  For example,

1. Subscripts denote a function of the natural numbers, e.g. when defining terms in a sequence \(a_1, a_2, a_3\).  That is the subscript denotes function application.  \(a_n = a(n)\).
2. Subscripts denote differentiation, e.g. \( x_t \) is the derivative of \(x \) with respect to \(t\).
3. Subscripts denote coordinates in a vector, in \( \vec{v} = (v_1, v_2, \cdots, v_n)  \).

There are many other possible uses for subscripts, especially in other subjects e.g. in physics or [actuarial studies](../Reference/Actuarial.md).

Because Maxima considers subscripted expressions to be atoms, the default TeX output of an atom `V_alpha` from Maxima is \( {\it V\_alpha} \) (literally `{\it V\_alpha}`) and not \( V_{\alpha} \) as a user might expect.  For this reason STACK intercepts and redefines how atoms with the underscore are displayed.  In particular STACK (but not core Maxima) takes an atom `A_B`, applies the `tex()` command to `A` and `B` separately and concatenates the result using subscripts.  For example, if you define

    texput(A, "{\\mathcal A}");
    texput(B, "\\diamond");

then `A_B` is now displayed as \({{{\mathcal A}}_{\diamond}}\).

Below are some examples.

| Maxima code  | Maxima's `tex()` command                                  | STACK (if different)                                          | STACK plain atoms                         |
|--------------|-----------------------------------------------------------|---------------------------------------------------------------|-------------------------------------------|
| `A_B`        | `{\it A\_B}` \({\it A\_B}\)                               | `{{A}_{B}}` \( {{A}_{B}} \)                                   |                                           |
| `A[1]`       | `A_{1}` \( A_{1}\)                                        |                                                               |                                           |
| `A1`         | `A_{1}` \( A_{1} \)                                       |                                                               | `{\it A1}` \( {\it A1} \)                 |
| `A01`        | `A_{1}` \( A_{1} \)                                       |                                                               | `{\it A01}` \( {\it A01} \)               |
| `A_1`        | `A_{1}` \( A_{1} \)                                       |                                                               |                                           |
| `A_x1`       | `{\it A\_x}_{1}` \( {\it A\_x}_{1} \)                     | `{{A}_{x_{1}}}` \( {{A}_{x_1}} \)                             | `{{A}_{{\it x1}}}` \( {{A}_{{\it x1}}} \) |
| `A_BC`       | `{\it A\_BC}` \( {\it A\_BC} \)                           | `{{A}_{{\it BC}}}` \( {{A}_{{\it BC}}} \)                     |                                           |
| `A_alpha`    | `{\it A\_alpha}` \( {\it A\_alpha}\)                      | `{{A}_{\alpha}}` \( {{A}_{\alpha}} \)                         |                                           |
| `alpha_1`    | `\alpha_{1}` \( \alpha_{1} \)                             |                                                               |                                           |
| `A_B_C`      | `{\it A\_B\_C}` \( {\it A\_B\_C} \)                       | `{{{A}_{B}}_{C}}` \( {A_B}_C \)                               |                                           |
| `x_t(1)`     | `{\it x\_t}\left(1\right)` \( {\it x\_t}\left(1\right) \) | `{{\it x\_t}\left(1\right)}` \( {{\it x\_t}\left(1\right)} \) |                                           |
| `A[1,2]`     | `A_{1,2}` \( A_{1,2} \)                                   |                                                               |                                           |

Notes

1. The maxima atoms `A1` and `A_1` are different, and are _not_ algebraically equivalent.  If student input is using both forms, and this causes problems, look at the documentation on `consolidatesubscripts` in the [extra options](../Authoring/Inputs/index.md).
2. in the above examples all the different expressions `A1`, `A_1`, `A[1]` and the atom `A01`: generate the same tex code `A_{1}` \( A_{1}\), and so are indistinguishable at the display level.  If you would like to display `A1` without subscripts, STACK provides the flag `tex_plain_atoms`.  If you set `tex_plain_atoms:true` in your question (probably before the `%_stack_preamble_end` to make sure this option is available to inputs), then the TeX functions will not split up atoms `A1` and display this with subscripts.  See examples above.
3. The expression `x_t(1)` refers to the function `x_t` which is not an atom, and hence STACK's logic for displaying atoms with underscores does not apply (by design).  If you want to display a function name including a subscript you can explicitly use, e.g. `texput(x_t, "x_t");` to control the display, this is just not done automatically.
4. When we split up atoms for display we have two separate atoms.  E.g. `x_h` will be split into atoms `x` and `h` temporarily and the TeX display of `x` and `h` evaluated.  For this reason, student's input will validate the parts of the subscript sparately.  In particular, if `h` is a question variable and a student types in the atom `x_h` then since `h` is forbidden input the student's `x_h` will be invalid as well.  This might cause problems, but these can be avoided when the teacher uses appropriate variable names.

One situation where this design is not satisfactory is when you want to use both of the atoms `F` and `F_1` but with different display. For example `F` should display as \({\mathcal F}\) but `F_1` should display as \( F_1 \).  Such a situation is not hard to imagine, as it is often considered good style to have things like \( F_1 \in {\mathcal F}\).  The above design always splits up the atom `F_1` into `F` and `1`, so that the atom `F_1` will display as  \({\mathcal F}_1\).  (This is actually what you normally expect, especially with the Greek letter subscripts.)  To avoid this problem the logic which splits up atoms containing an underscore checks the texput properties list. If an entry has been made for a specific atom then STACK's display logic uses the entry, and does not split an atom over the underscore.  In the above example, use the following texput commands.

    texput(F, "{\\mathcal F}");
    texput(F_1, "{F_1}");

With this code `F` displays as \({\mathcal F}\), the atom `F_1` displays as \( F_1 \), and every subscript will display with calligraphic, e.g. `F_alpha` displays as \({\mathcal F}_{\alpha}\).  There is no way to code the reverse logic, i.e. define a special display only for the unique atom `F`.

Note that the [scientific units](../Topics/Units.md) code redefines and then assumes that symbols represent units.  E.g. `F` is assumed to represent Farad, and all units are typeset in Roman type, e.g. \( \mathrm{F} \) rather than the normal \( F \). This is typically the right thing to do, but it does restrict the number of letters which can be used for variable names in a particular question.  To overcome this problem you will have to redefine some atoms with texput.  For example,

    stack_unit_si_declare(true);
    texput(F_a, "F_a");

will display the atom `F_a` as \(F_a\), i.e. not in Roman.  If you `texput(F, "F")` the symbol `F` is no longer written in Roman, as you would expect from units.  This may be sensible if Farad could not possibly appear in context, but students might type a range of subscripted atoms involving `F`.

The use of texput is global to a question. There is no way to display a particular atom differently in different places (except perhaps in the feedback variables, which is currently untested: assume texput is global).

How would you generate the tex like \( A_{1,2} \)?  STACK's `sequence` command (see below) does output its arguments separated by a comma, so `sequence(1,2)` is displayed as \( {1,2} \), however the Maxima command `A_sequence(1,2)` refers to the function `A_sequence`, (since the underscore is not an operator).  Hence STACK's logic for splitting up _atoms_ containing the underscore does not apply.  (In any case, even if the display logic did split up function names we would still have the issue of binding power to sort out, i.e. do we have the atom with parts `A` and `sequence(1,2)` or the function named `A` and `sequence`?)  To create an output like \( A_{1,2} \) you have no option but to work at the level of display.  Teachers can create an inert function which displays using subscripts.

    texsub(a,b)

is typeset as \({a}_{b}\) i.e. `{a}_{b}` in LaTeX.  For example,

* `texsub(A, sequence(1,2))` will display as \({{A}_{1, 2}}\),
* with simplification off, `texsub(F,1-2)` will be displayed as \({F}_{1-2}\).

Note that the process of converting `theta_07` into the intermediate `texsub` form internally results in the `texsub(theta,7)` which removes the leading zero.  This is a known issue, for which a work around is to directly use `texput(theta_07, "{{\\theta}_{07}}")` or `texsub(theta,"07")`.  The second option does not produce optimal LaTeX, since it uses TeX `mbox`, e.g. `{{\theta}_{\text{07}}}`.



# Bespoke validators and feedback

The extra option `validator` to a particular [input](../Authoring/Inputs/index.md) allows additional bespoke validation, based on a function defined by the question author.  For example, you could require that the student's answer is a _list of exactly three equations_.

The extra option `feedback` to a particular [input](../Authoring/Inputs/index.md) allows additional bespoke feedback, based on a function defined by the question author.  This does not create an invalid input.

Please check [existing, supported, validation options](../Authoring/Inputs/index.md) before defining your own!

You cannot overwrite certain non-optional core validation, but all validation that is optional can naturally be turned off and a replacement given through this system. For example, you can use this system to give much more question-specific feedback.  Rather than forbid the variable `t` with the forbidden words system (non-specific error) you could define something very question specific.

    validate_contains_t(ex):= if member(t,listofvars(ex)) then "You can't use t here because the independent variable is x." else "".

For example, to check a list has at most three elements define the function named `validate_listlength` in the question variables, e.g.

    validate_listlength(ex) := block([l],
      if not(listp(ex)) then return(castext("Your answer must be a list")),
      l:length(ex),
      if l < 3 then return(castext("Your list only has {#l#} elements, which is too few.")),
      ""
    );

To use this feature put the following in the input extra options.

    validator:validate_listlength

Similarly, to just add a feedback message use the following in the input extra options.

    feedback:my_bespoke_feedback

Notes:

1. The validator/feedback must be a pure function of a single variable. There must be no reference to the input name within the validator function definition, indeed you cannot reference an input in the question variables.
2. If the validator function returns a non-empty string, then the student's answer will be considered invalid, and the string displayed to the student as a validation error message as part of the input validation.  Any string returned by the feedback function is displayed to the student, and validity is not changed.
3. If the validator function returns an empty string or `true` then the student's input is considered to be valid.  The use of an empty string here for valid is designed to encourage teachers to write meaningful error messages to students!
4. The function can reference other question variables, e.g. the teacher's answer.
5. The function is always executed with `simp:false` regardless of the question settings.
6. The function is called after the built-in validation checks, and only if the expression is already valid otherwise.  So, you cannot replace basic validation (by design).  This means you will/should have an expression which Maxima can evaluate if it gets as far as your validator function.  E.g. no missing `*` or mismatched brackets.
8. The student still cannot use any of the variable names defined in the question variables.
9. Validators only operate on a single input, and there is no mechanism to validate a combination of inputs at once.
10. The recommended style for naming validator functions is to begin the name with `validate_` or `feedback_`.

A single validator function can be re-used on multiple inputs within a single question. If you regularly copy validator functions from question to question please consider contributing this as a function to the core of STACK (see below for details). We expect to collect and support regularly used validators in future.

Validator functions basically test for a particular property.  Validator functions can be re-used to create an answer test. See the documentation on [`ATValidtor`](../Authoring/Answer_Tests/Other.md).

## Combining validators

If you wish to test for a number of separate properties then it is probably best to create separate functions for each property and combine them into a single validator.

For example, imagine you would like the following:

1. the answer must be a list;
2. the list has three elements;
3. each element is an equation.

E.g. `[x^2=1, y=1, x+z=1]` is a valid answer.  `[x^2+5, y=1]` is invalid (for two reasons).

Functions which establish these properties are:

    /* Define validator functions separately. */
    validate_islist(ex) := if listp(ex) then "" else "Your answer must be a list.";
    validate_allequations(ex) := if all_listp(equationp, ex) then "" else "All elements of your answer should be equations.";
    validate_checklen(ex) :=  if ev(is(length(ex)=3),simp) then "" else "Your list must have 3 elements.";
    /* Combine the validator functions. */
    validate_equationlist(ex) := stack_multi_validator(ex, [validate_islist, validate_allequations, validate_checklen]);

The last line creates a single validator function using the convenience function `stack_multi_validator` supported by STACK.

STACK supports two convenience functions

1. `stack_multi_validator` executes _all_ the validator functions and concatenates the result.
2. `stack_seq_validator` executes the validator functions in list order until one fails.  This means you can make assumptions in later validators about the _form_ of the expression.

If any validator throws an error then the student's answer is invalid.  E.g. using `any_listp` on a non-list will throw a Maxima error.

## Supported validators

The Maxima code is stored in the sourcecode in `stack/maxima/validator.mac`, e.g. on [github](https://github.com/maths/moodle-qtype_stack/blob/master/stack/maxima/validator.mac).

### Contributing validators to the core of STACK {#contributing}

When you regularly find yourself testing for particular properties, and copying code between questions, please consider contributing functions to the STACK core for longer term support.

You can [post your suggestion on the project's GitHub site](https://github.com/maths/moodle-qtype_stack/issues) or [submit code directly as a pull request](https://github.com/maths/moodle-qtype_stack/pulls).

## Improving validation feedback messages.

It is possible to include the student's answer, or part of the answer, in the validation feedback. This needs more work, of course.

The validator must return a string.  One way to include the studnet's answer in the message is to use `sconcat`, e.g. as follows

    sconcat("User-defined functions are not permitted in this input. In your answer ", stack_disp(op1, "i"), " appears to be used as a function. ")

Another option is to use the `castext` function.  Note, that the castext function has to be used only at the top level.  An example is given in the next section on language support.  You cannot currently return the result of multiple `castext` calls in a concatinated string.

An example of how to construct such a validator is `validate_nofunctions` in the contributed validators.

## Localisation and language support

To localise your validation messages use the castext `lang` block. For example

    ta:phi^2-1;
    validate_vars(ex) := block(
        if ev(subsetp(setify(listofvars(ex)),setify(listofvars(ta))), simp) then return(""),
        castext("[[lang code='fi']]Vastauksesi sisältää vääriä muuttujia.[[/lang]][[lang code='en']]Your answer contains the wrong variables.[[/lang]]")
    );

For the supported validator function, all language strings are drawn from the STACK language pack: STACK stores all language strings in the [plugin source code](https://github.com/maths/moodle-qtype_stack/blob/master/lang/en/qtype_stack.php), and these are then translated by volunteers using the online [AMOS system](https://lang.moodle.org/).

Individual language strings can then be referred to using STACK's `[[commonstring ... /]]` block.  For example, the language pack contains the string

    $string['Illegal_strings'] = 'Your answer contains "strings" these are not allowed here.';

An example of how to use this in Maxima code is below.

    validate_listoftwo(ex):=block(
        if not(listp(ex)) then return("Your answer must be a list."),
        if not(is(length(ex)=2)) then return("Your list must have two elements."),
        if stringp(second(ex)) then return(castext("[[commonstring key='Illegal_strings' /]]")),
        true
    );

In this example

1. `["Quadratic",x^2-1]` is valid.
2. `[x^2-1,"Quadratic"]` is invalid because the second argument here is a string. In this case the error message comes from the common language pack.

Many language examples have variables which need to be injected.  In this example, the variable `m0` needs to be injected.

    $string['ValidateVarsSpurious']   = 'These variables are not needed: {$a->m0}.';

To inject variables into a language string we define the value of `m0` in the `[[commonstring ... /]]` block.

    validate_spuriousvar(ex):=block([%_tmp,simp],
        simp:false,
        %_tmp: listofvars(ex),
        simp:true,
        %_tmp: setdifference(setify(%_tmp), {x,y,z}),
        if cardinality(%_tmp) = 0 then return(""),
        castext("[[commonstring key='ValidateVarsSpurious' m0='listify(%_tmp)'/]]")
    );

Note, when injecting a value `m0='X'` the `X` must be a Maxima expression, not a displayed string.

1. to inject the Maxima expression `X` with `{@...@}` injection (without wrapping like `\(...\)`) to a named placeholder `m0` use `m0='X'`.
1. to inject the Maxima expression `X` with `{#...#}` injection, to get raw values, to a named placeholder `m0` use `raw_m0='X'`.

For other prefix options see the [documentaiton for the commonstring block](../Authoring/Question_blocks/Static_blocks.md#commonstring-block).

## Further examples

To forbid the underscore character in a student's input.

    validate_underscore(ex) := if is(sposition("_", string(ex)) = false) then ""
               else "Underscore characters are not permitted in this input.";

# Sharing validators between questions

It is common to want to share validators between questions.  It would also be very helpful to contribute commonly used validator functions back to the STACK project.  To include a validator in more than one question you could post your validator function publicly.

1. Get the validator function working reliably in your question, locally.
2. Add the maxima function to this file, [`https://github.com/maths/moodle-qtype_stack/blob/master/stack/maxima/contrib/validators.mac`](https://github.com/maths/moodle-qtype_stack/blob/master/stack/maxima/contrib/validators.mac) or another file, preferably contributing to the STACK project.
3. Add documentation and comprehensive test cases (please!) to let other people know what the validator is intended to do, and to help ensure behaviour remains stable.
4. Include the [optional validators within the cas logic](../Authoring/Inclusions.md#inclusions-within-cas-logic) with either of the following

    stack_include("https://raw.githubusercontent.com/maths/moodle-qtype_stack/master/stack/maxima/contrib/validators.mac");
    stack_include_contrib("validators.mac");

Note the url `https://raw.githubusercontent.com/` is used to include the raw content of this file.

Including external content always poses a minor additional security risk.  In this case (1) the content is included and then subject to the same checks as if you had typed it yourself, and (2) the developers will take the same care in accepting contributions to the master branch as they do with the existing code base.

### Example: forbid underscores in an input

Create a new question.

1. Add the following to the question variables, which loads contributed validators.

    stack_include("https://raw.githubusercontent.com/maths/moodle-qtype_stack/master/stack/maxima/contrib/validators.mac");

  or add the following to the question variables

    stack_include_contrib("validators.mac");

2. Use the extra option `validator:validate_underscore` in the input.

### Example: forbid user-defined functions and array entries

As above, include the contributed validators.  Use the extra option `validator:validate_nofunctions` in the input.

# Validators and Maxima timeouts

Users have reported that in some circumstances, questions using bespoke validators run into seemingly unrelated Maxima timeouts. Examples of this behaviour are discussed in [Issue #1211](https://github.com/maths/moodle-qtype_stack/issues/1121) and on the [Zulip Community chat](https://stack-assessment.zulipchat.com/#narrow/channel/384532-question-troubleshooting/topic/Bespoke.20Validators.20and.20maxima.20timeouts).

It seems that this behaviour is related to calculus functions like `limit` and `integrate` in the question variables, independent of what the validator does. As a workaround, it often helps to forcefully evaluate such expressions using `ev(..., simp)`, e.g. try `c : ev(int(e^(s*x),x,0,1), simp);` instead of `c : int(e^(s*x),x,0,1);`.

Also, Maxima was originally designed as desktop software and it has an "interactive mode" somewhat hard-wired into the core code.  Try `integrate(x^n,x)` in a blank Maxima desktop session for an example.  The interactive mode has it's place, but if a validator uses one of the functions which has an interactive mode, and the student triggers this behaviour, then there will be a timeout.  We have looked at switching this off, but that's not completely possible.  This is another possible source of issues.
