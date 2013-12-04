# Countdown
##### Ruby v1.9.3
##### From [Best of Ruby Quiz](http://pragprog.com/book/fr_quiz/best-of-ruby-quiz)

According to Brian Candler in the Ruby Quiz book, Countdown is a British quiz show that asks contestants to solve an arithmetic problem.  We'll write a program to solve it.

#### Rules:

* Input is a list of six numbers, one from [25, 50, 75, 100] and five from (1..10) that the player may choose.
* A random target number in the range (100..999) is provided by a program.
* The contestant has 30 seconds to provide a series of arithmetic operations (+, -, *, /) on the six smaller numbers that result in the target, or at least as close as possible to the target.

#### Example:

* List of numbers 100, 5, 5, 2, 6, and 8.
* Target 522.

###### Solutions:

* (5 * 100) + ((5 + 6) * 2)
* (100 + 6) * 5 - 8
