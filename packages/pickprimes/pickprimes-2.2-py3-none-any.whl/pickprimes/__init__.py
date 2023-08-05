#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 19 13:15:30 2021

@author: marci
"""

def pickprimes(n):
    for i in range(2,n+1):
        cont = True
        for j in range (2, int(i**0.5)+1):
            if i%j == 0:
                cont = False
                break
        if cont:
            print(i, 'es primo')

def is_prime(n):
    if n == 1:
        return False
    elif n <= 0:
        return False
    else:
        cont = True
        for i in range(2, int(n**0.5)+1):
            if n%i == 0:
                cont = False
                break
        return cont