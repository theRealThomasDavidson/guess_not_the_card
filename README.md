     ::image:: https://github.com/theRealThomasDavidson/guess_not_the_card/workflows/test/badge.svg?branch=main
     :target: https://github.com/theRealThomasDavidson/guess_not_the_card/actions?workflow=test
     :alt: CI Status


# Guess Not The Card

This whole little project started as response to a 
[youtube video from Scam Nation (a majic and puzzle youtube channel)](https://www.youtube.com/watch?v=Pkp51MZUD3Q&t=1s).
In that video there was a puzzle/challenge to guess a card number(including jacks queens kings), afterward you would 
check the first card on top of a deck of cards without replacement. If the guessed card had the same number as the 
checked card then the game is lost, if the guessed card is different from the checked card then you get the chance to 
do it again. When you get to the end of the deck without having a match between guesses and checked cards you win. 

At the end of the video our host Brian Brushwood does a classic youtube call to action in "I wanna hear from all you
genius, all you mathematicians out there. I wanna know what the real probability is. Both for random numbers and 
for applying a strategy."

## Strategies

I felt that the responses in the comments section were pretty lack luster in answering this question. I only saw one 
person give any answer Ace Diamond [(their profile not the comment)](https://www.youtube.com/channel/UCSlcPhWYE-liv6IJLUen12w).
I would like to point out here that I think Ace did good work, but I wanted to add to what they did. 
Ace first of all explained a strategy that I later thought of as the best strategy but like Ace, I don't really have 
a good proof for this being the best strategy. Then Ace did a primitive monty carlo simulation where they giv you the 
full results but didn't do any statistical tests on it other than give a mean. 

In Ace's own words I will give the strategy I call "Memories": 

"So, my theory is that the best strategy is to always guess the card that has come up the most.  Once you get three of 
a kind turned up, you'll be guessing that one repeatedly, in which case you'll lose UNLESS another card value gets to 
three, and then surpasses the first one. Of course, then you can guess that value that has been turned up all four 
times through to the end, and win. ... I don't know if this is the best method, but it's the best idea I can think of.
"

One strategy that is mentioned in the video is to guess randomly. This I feel is pretty straightforward and no additonal 
explination is needed. 

The last strategy I proposed was "say what you see". It certainly is immersed in the environment described in the video. 
this strategy has the guesser remember only one card and do no additional steps, easy enough for a very drunk person to 
execute but should increase the players odds significantly over random guesses. 

## Simulations

So for simulations I made a monte carlo simulation that will psudorandomly generate a shuffled playing card deck, take 
a player strategy object and play the game by asking for guesses, report to a strategy player the card on top of the 
deck, and count wins and losses. 

To collect statistical information on these simulations I ran the simulations in batches of 10000 to get a chance of 
success for the strategy for that batch. I did this 4000 times to get a list of success rates that I could preform 
statistical tests on.
 
#### Danger math

-------

So, I assumed these batched success rates will follow the standard distribution (while I know this isn't the case I felt
 that it was mostly good enough I'm happy to revise). I used z scores to find the 95% confidence interval at z = 1.96.

------

#### Math finished for now the weak of heart can continue

From here we can estimate a range of values where we would expect the actual chance of winning given a specific strategy.

Results on Strategies:

#### Memories: 
    
 - run time: 2415.906s
 - 95% chance the solve answer is between 26.992642% and 27.020348%

#### Random_guess

 - run time: 1234.308s
 - 95% chance the solve answer is between 1.554700% and 1.562450%

#### Say_what_you_see 
 - run time: 891.587s
 - 95% chance the solve answer is between 4.187988% and 4.200332%

## Solves

Here we are doing the solves, these should give exact provable solutions to thw answers, these are calculated with 
python floating point numbers, so while these methods will give exact solutions the solution I have given does not do 
this whole thing with exact integer based fractions so it will be slightly off from where it should be, I also truncate 
the answer to 6 decimal places of a percent (8 decimal places of a proportion) and I this contributes to significantly 
more error than the floating point rounding errors.

#### Random_guess

In the video the solve was accurately described as being 12/13 raised to the nth power where n is the number of cards.
This can be explained by no matter what is drawn, the guesser will guess 12/13 times a different card and continue or a 
1/13 chance of losing there. No need to consider what cards are in the deck (the deck could be 52 of the same number and
 this still works.)
 
 solve chance on a new shuffled deck: 
 - 1.557294%
 - run time: 0.001s
 
 
#### Memories

The solve for memories is pretty difficult to get your head around, so be prepared to look over it several times before 
getting a full understanding. a few assumptions are made to turn this solver from a weeks project to a minutes project 
these might make it a bit more difficult to understand, but we are going over each of them here so everything is 
explicit. these assumptions are going to be ordered with the easiest ones understand first. (obviously this is 
subjective)

First, we don't care about which order cards were previously drawn in or what we guessed previously only if we have 
survived up until now. This one is pretty self-explanatory the reason it is used is because our game state is copied 
often during the solver and the memory and time it takes to do this are somewhat of a burdon. This also lets us 
consolidate game states that look similar but had different paths that led to them now we can simply add the chances 
that those two similar states(only differing in how they got there) together to get the chance that the state exists. 
This allows us to preform the calculations on far fewer states. 

Next, We don't care what number any card is. 

Okay, hear me out before you dismiss this. 

Seriously. Please. 

In an example of two players, alice and bob, alice sees that the first card is an ace and bob sees that his first card 
is a jack. The strategies for alice and  bob will still be the same if you only switch bob's answers of jack to ace and
vice versa and bob's deck will draw jacks instead of aces and vice versa. Because this transform between bob and alice 
will not change the odds that they win or what is left in the deck we are going to consider the further possibilities 
of them as a group.

This essentially mean that with a new deck the state can be described as 13 card numbers have 4 cards left in the deck.
Upon the first draw while there is a 4/52 chance that we draw a losing card but there is a 48/54 chance that the state 
becomes 12 card numbers have 4 cards left in the deck and 1 card number has 3 cards left in the deck.
We step through all the  different amounts that have at least one card number and do this. This as you can see consolidated the 
calculations we have to do going forward from 12 states to 1 and that is just on the first step.

So the method for this is we step through each possible state we describe the state like above and we also keep track of
the chance of that state happening from the initial state. Here we figure out all the states that can be created from 
this state and their chance of happening from this state. Then we assign that future state a chance of happing from the 
initial conditions as the chance that it's parent existed from the initial state multiplied by the chance that it happens
given the parent happened. If that future state already exists in the list of states we have we add the chance that we
just calculated to it's current chance. If the future state does not exist in our list of states we add to the list it 
with the chance that we calculated. We first deal with all states with 52 cards then 51 etc. This ordering ensures that 
no state is added to after it has already made child states. 

solve chance on a new shuffled deck: 
 - 27.019506%
 - run time:  0.008s
 #### Say what you see
 
 I thought there might be some simpler approach than the one I did above for this. I know i can describe this problem as
 "What is the chance of a deck not having duplicate cards multiplied by 1/13?" but I haven't been able to easily figure 
 this out.
 
 Feel free to discuss this in the issues section if you can do the math I can implement this but I've given it an hours
 thought and couldn't think of the answer off the top of my head. I might put more work into this one but idk just yet.
 I will probably implement this as above in the mean time but haven't gotten around to it.
 
