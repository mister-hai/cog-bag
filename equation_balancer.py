#!/usr/bin/python3
import sys
import pyEQL
import chempy
import math, cmath
from variables_for_reality import pi,Vbe
from chempy import balance_stoichiometry, mass_fractions

# FORMULA RULES

Formula_entry_rules = '''

How to Enter Valid Chemical Formulas

Generally speaking, type the chemical formula of your solute the “normal” way and pyEQL should be able to inerpret it. Here are some examples:

    Sodium Chloride    - NaCl
    Sodium Sulfate     - Na(SO4)2
    Methanol           - CH4OH or CH5O
    Magnesium Ion      - Mg+2
    Chloride Ion       - Cl-

Formula Rules:

    *  Are composed of valid atomic symbols that start with capital letters
    
    *  Contain no non-alphanumeric characters other than ‘(‘, ‘)’, ‘+’, or ‘-‘
    
    *  If a ‘+’ or ‘-‘ is present, the formula must contain ONLY ‘+’ or ‘-‘ (e.g. ‘Na+-‘ is invalid) and the formula must end with either a series of charges (e.g. ‘Fe+++’) or a numeric charge (e.g. ‘Fe+3’)
    
    *  Formula must contain matching numbers of ‘(‘ and ‘)’
    
    *  Open parentheses must precede closed parentheses

'''

class EquationBalancer():
    def __init__(self):

    def balancer_help_message():
        return " Reactants and Products are Comma Seperated Values using"+\
        "symbolic names for elements e.g. \n "        +\
        " user input will be valid only in the form of:" +\
        "NH4ClO4,Al=>Al2O3,HCl,H2O,N2" + \
        " Note the lack of spaces"

    def validate_formula_input(equation_user_input : str):
        """
        :param formula_input: comma seperated values of element symbols
        :type formula_input: str     
    makes sure the formula supplied to the code is valid
    user input will be valid only in the form of:
    eq = "NH4ClO4,Al=>Al2O3,HCl,H2O,N2"
    note the lack of spaces
        """
        #user_input_reactants = "NH4ClO4,Al"
        #user_input_products  = "Al2O3,HCl,H2O,N2"
        #equation_user_input  = "NH4ClO4,Al=>Al2O3,HCl,H2O,N2"
        

        # if it doesn't work, lets see why!
        try:
            # validate equation formatting
            parsed_equation1 = equation_user_input.split("=>")[0]
            print(parsed_equation1)
            parsed_equation2 = equation_user_input.split("=>")[1]
            print(parsed_equation2)
            try:
                #validate reactants formatting
                user_input_reactants = str.split(parsed_equation1, sep =",")
            except Exception:
                redprint("reactants formatting")
                EquationBalancer.user_input_was_wrong("formula_reactants", user_input_reactants)                
            try:
                #validate products formatting
                user_input_products  = str.split(parsed_equation2, sep =",")
            except Exception:
                redprint("products formatting")
                EquationBalancer.user_input_was_wrong("formula_products", user_input_products)  
                #validate reactants contents
            for each in user_input_reactants:
                try:
                    chempy.Substance(each)
                except Exception:
                    redprint("reactants contents")
                    EquationBalancer.user_input_was_wrong("formula_reactants", each)  
                #validate products contents
            for each in user_input_products:
                try:
                    chempy.Substance(each)
                except Exception:
                    redprint("products contents")
                    EquationBalancer.user_input_was_wrong("formula_products", each)
        # if the inputs passed all the checks
            EquationBalancer.balance_simple_equation(user_input_reactants, user_input_products)
        except Exception:
            redprint("formula validation exception")
            EquationBalancer.user_input_was_wrong("formula_general", equation_user_input)


    def balance_simple_equation(reactants, products):
        #react = chempy.Substance.from_formula(reactants)
        #prod  = chempy.Substance.from_formula(products)
        balanced_reaction = chempy.balance_stoichiometry(reactants,products)
        #print(balanced_reaction)
        EquationBalancer.reply_to_query(balanced_reaction)



    def user_input_was_wrong(type_of_pebkac_failure : str, bad_string = ""):
        """
        You can put something funny here!
            This is something the creator of the bot needs to modify to suit
            Thier community.
        """
        formula_message    = "Stop being a doofus and feed me a good formula!"
        form_react_message = "the following input was invalid: " + bad_string 
        form_prod_message  = "the following input was invalid: " + bad_string
        if type_of_pebkac_failure == "formula":
            EquationBalancer.reply_to_query(formula_message)
        elif type_of_pebkac_failure == "formula_reactants":
            EquationBalancer.reply_to_query(form_react_message)
        elif type_of_pebkac_failure == "formula_products":
            EquationBalancer.reply_to_query(form_prod_message)
