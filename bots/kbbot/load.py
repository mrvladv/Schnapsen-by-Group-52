from .kb import KB, Boolean, Integer

# Initialise all variables that you need for you strategies and game knowledge.
# Add those variables here.. The following list is complete for the Play Jack strategy.
A0 = Boolean('a0')
A1 = Boolean('a1')
A2 = Boolean('a2')
A3 = Boolean('a3')
A4 = Boolean('a4')
A5 = Boolean('a5')
A6 = Boolean('a6')
A7 = Boolean('a7')
A8 = Boolean('a8')
A9 = Boolean('a9')
A10 = Boolean('a10')
A11 = Boolean('a11')
A12 = Boolean('a12')
A13 = Boolean('a13')
A14 = Boolean('a14')
A15 = Boolean('a15')
A16 = Boolean('a16')
A17 = Boolean('a17')
A18 = Boolean('a18')
A19 = Boolean('a19')
PA0 = Boolean('pa0')
PA1 = Boolean('pa1')
PA2 = Boolean('pa2')
PA3 = Boolean('pa3')
PA4 = Boolean('pa4')
PA5 = Boolean('pa5')
PA6 = Boolean('pa6')
PA7 = Boolean('pa7')
PA8 = Boolean('pa8')
PA9 = Boolean('pa9')
PA10 = Boolean('pa10')
PA11 = Boolean('pa11')
PA12 = Boolean('pa12')
PA13 = Boolean('pa13')
PA14 = Boolean('pa14')
PA15 = Boolean('pa15')
PA16 = Boolean('pa16')
PA17 = Boolean('pa17')
PA18 = Boolean('pa18')
PA19 = Boolean('pa19')

def general_information(kb):
    # GENERAL INFORMATION ABOUT THE CARDS
    # This adds information which cards are Jacks
    kb.add_clause(A0)
    kb.add_clause(A5)
    kb.add_clause(A10)
    kb.add_clause(A15)
    # Add here whatever is needed for your strategy.

def strategy_knowledge(kb):
    # DEFINITION OF THE STRATEGY
    # Add clauses (This list is sufficient for this strategy)
    # PJ is the strategy to play jacks first, so all we need to model is all x PJ(x) <-> J(x),
    # In other words that the PJ strategy should play a card when it is a jack
    kb.add_clause(~A0, PA0)
    kb.add_clause(~A5, PA5)
    kb.add_clause(~A10, PA10)
    kb.add_clause(~A15, PA15)
    kb.add_clause(~PA0, A0)
    kb.add_clause(~PA5, A5)
    kb.add_clause(~PA10, A10)
    kb.add_clause(~PA15, A15)
