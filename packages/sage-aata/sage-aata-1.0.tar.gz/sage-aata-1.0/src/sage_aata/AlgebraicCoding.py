#!/usr/bin/env python

# import the random module to use in the Bernoulli class
import random

# define the Bernoulli class
class Bernoulli:
    # define the constructor, that requires a parameter p, which should
    # be between zero and one.
    def __init__(self, p):
        self.p = p

    # define the method that will display information about the
    # object when in a print statement
    def __repr__(self):
        return f"Bernoulli distribution with parameter {self.p}"

    # define the method that performs a random trial from the
    # Bernoulli distribution based on the parameter p
    def randomTrial(self):
        value = random.random()
        if value < self.p:
            return 1
        else:
            return 0

# define the SymmetricChannel class
class SymmetricChannel:

    # define the constructor, which takes in a bernoulli object
    def __init__(self, b):
        # if b is a Bernoulli assign it to the bernoulli instance in the class,
        # if not, set the bernoulli instance to None
        if type(b) is Bernoulli:
            self.bernoulli = b
        else:
            self.bernoulli = None

    # define the method that will provide information about the object when
    # in a print statement
    def __repr__(self):
        return f"A SymmetricChannel based on a Bernoulli distribution with parameter {self.bernoulli.p}"

    # define a method to test whether or not the SymmetricChannel has been set up correctly.
    # this just means whether or not the bernoulli object was accepted correctly.
    def test(self):
        if type(self.bernoulli) is None:
            return "Not set up correctly"
        if type(self.bernoulli) is Bernoulli:
            return "Set up correctly"

    # This method takes in a list, and tests to ensure that it contains only
    # ones and zeros, then sends it through the SymmetricChannel,
    # simulating errors based on the Bernoulli instance variable that this
    # class contains.
    def transmit(self, message):
        test = True
        for i in range(0,len(message)):
            if message[i]!=0 and message[i]!=1:
                test = False
        if test:
            transmitted = []
            # for each of the numbers in the message
            for i in range(0,len(message)):
                # take a random trial from the bernoulli distribution.
                value = self.bernoulli.randomTrial()
                # then based on that random trial, either leave the message alone,
                # or commit an error in that bit.
                if value==0:
                    if message[i] == 0:
                        transmitted.append(0)
                    else:
                        transmitted.append(1)
                else:
                    if message[i] == 0:
                        transmitted.append(1)
                    else:
                        transmitted.append(0)
        else:
            print("The message must conain only zeros and ones.")
        # return the new message.
        return transmitted
