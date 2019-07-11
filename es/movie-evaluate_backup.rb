!COMMENT!
Enter your description of the rulebase here.
!END_COMMENT!

TypeOfDescription=linguistic
InfMethod=Fuzzy_Approximation-logical
DefuzzMethod=ModifiedCenterOfGravity
UseFuzzyFilter=false

NumberOfAntecedentVariables=4
NumberOfSuccedentVariables=1
NumberOfRules=144

AntVariable1
 name=INP1
 settings=new
 context=<0,2.5,5>
 discretization=1000
 UserTerm
  name=low
  type=trapezoid
  parameters= 0 0 1.5 2
 End_UserTerm
 UserTerm
  name=med
  type=trapezoid
  parameters= 1.5 2 3.5 4
 End_UserTerm
 UserTerm
  name=high
  type=trapezoid
  parameters= 3.5 4 5 5
 End_UserTerm
End_AntVariable1

AntVariable2
 name=INP2
 settings=new
 context=<0,150,350>
 discretization=301
 UserTerm
  name=few
  type=trapezoid
  parameters= 0 0 5 25
 End_UserTerm
 UserTerm
  name=med
  type=trapezoid
  parameters= 5 25 50 100
 End_UserTerm
 UserTerm
  name=much
  type=trapezoid
  parameters= 50 100 225 250
 End_UserTerm
 UserTerm
  name=ve_much
  type=trapezoid
  parameters= 225 250 350 350
 End_UserTerm
End_AntVariable2

AntVariable3
 name=INP3
 settings=new
 context=<0,4,10>
 discretization=301
 UserTerm
  name=low
  type=trapezoid
  parameters= 0 0 2 3
 End_UserTerm
 UserTerm
  name=med
  type=trapezoid
  parameters= 2 3 6 7
 End_UserTerm
 UserTerm
  name=high
  type=trapezoid
  parameters= 6 7 10 10
 End_UserTerm
End_AntVariable3

AntVariable4
 name=INP4
 settings=new
 context=<0,0.00257605,1>
 discretization=1000
 UserTerm
  name=low
  type=trapezoid
  parameters= 0 0 0.001 0.005
 End_UserTerm
 UserTerm
  name=med
  type=trapezoid
  parameters= 0.001 0.005 0.01 0.05
 End_UserTerm
 UserTerm
  name=high
  type=trapezoid
  parameters= 0.01 0.05 0.15 0.2
 End_UserTerm
 UserTerm
  name=ve_high
  type=trapezoid
  parameters= 0.15 0.2 1 1
 End_UserTerm
End_AntVariable4

SucVariable1
 name=IMPORTANCE
 settings=new
 context=<0,0.4,1>
 discretization=301
 UserTerm
  name=ve_low_imp
  type=triang
  parameters= 0 0 0.25
 End_UserTerm
 UserTerm
  name=low_imp
  type=triang
  parameters= 0 0.25 0.5
 End_UserTerm
 UserTerm
  name=med_imp
  type=triang
  parameters= 0.25 0.5 0.75
 End_UserTerm
 UserTerm
  name=high_imp
  type=triang
  parameters= 0.5 0.75 1
 End_UserTerm
 UserTerm
  name=ve_high_imp
  type=triang
  parameters= 0.75 1 1
 End_UserTerm
End_SucVariable1

RULES
 "low" "few" "low" "low" | "ve_low_imp"
 "low" "few" "low" "med" | "ve_low_imp"
 "low" "few" "low" "high" | "ve_low_imp"
 "low" "few" "low" "ve_high" | "low_imp"
 "low" "few" "med" "low" | "ve_low_imp"
 "low" "few" "med" "med" | "ve_low_imp"
 "low" "few" "med" "high" | "ve_low_imp"
 "low" "few" "med" "ve_high" | "ve_low_imp"
 "low" "few" "high" "low" | "ve_low_imp"
 "low" "few" "high" "med" | "ve_low_imp"
 "low" "few" "high" "high" | "ve_low_imp"
 "low" "few" "high" "ve_high" | "ve_low_imp"
 "low" "med" "low" "low" | "ve_low_imp"
 "low" "med" "low" "med" | "ve_low_imp"
 "low" "med" "low" "high" | "ve_low_imp"
 "low" "med" "low" "ve_high" | "ve_low_imp"
 "low" "med" "med" "low" | "ve_low_imp"
 "low" "med" "med" "med" | "ve_low_imp"
 "low" "med" "med" "high" | "ve_low_imp"
 "low" "med" "med" "ve_high" | "ve_low_imp"
 "low" "med" "high" "low" | "ve_low_imp"
 "low" "med" "high" "med" | "ve_low_imp"
 "low" "med" "high" "high" | "ve_low_imp"
 "low" "med" "high" "ve_high" | "ve_low_imp"
 "low" "much" "low" "low" | "ve_low_imp"
 "low" "much" "low" "med" | "ve_low_imp"
 "low" "much" "low" "high" | "ve_low_imp"
 "low" "much" "low" "ve_high" | "ve_low_imp"
 "low" "much" "med" "low" | "ve_low_imp"
 "low" "much" "med" "med" | "ve_low_imp"
 "low" "much" "med" "high" | "ve_low_imp"
 "low" "much" "med" "ve_high" | "ve_low_imp"
 "low" "much" "high" "low" | "ve_low_imp"
 "low" "much" "high" "med" | "ve_low_imp"
 "low" "much" "high" "high" | "ve_low_imp"
 "low" "much" "high" "ve_high" | "ve_low_imp"
 "low" "ve_much" "low" "low" | "ve_low_imp"
 "low" "ve_much" "low" "med" | "ve_low_imp"
 "low" "ve_much" "low" "high" | "ve_low_imp"
 "low" "ve_much" "low" "ve_high" | "ve_low_imp"
 "low" "ve_much" "med" "low" | "ve_low_imp"
 "low" "ve_much" "med" "med" | "ve_low_imp"
 "low" "ve_much" "med" "high" | "ve_low_imp"
 "low" "ve_much" "med" "ve_high" | "ve_low_imp"
 "low" "ve_much" "high" "low" | "ve_low_imp"
 "low" "ve_much" "high" "med" | "ve_low_imp"
 "low" "ve_much" "high" "high" | "ve_low_imp"
 "low" "ve_much" "high" "ve_high" | "ve_low_imp"
 "med" "few" "low" "low" | "low_imp"
 "med" "few" "low" "med" | "low_imp"
 "med" "few" "low" "high" | "low_imp"
 "med" "few" "low" "ve_high" | "med_imp"
 "med" "few" "med" "low" | "ve_low_imp"
 "med" "few" "med" "med" | "ve_low_imp"
 "med" "few" "med" "high" | "low_imp"
 "med" "few" "med" "ve_high" | "low_imp"
 "med" "few" "high" "low" | "ve_low_imp"
 "med" "few" "high" "med" | "ve_low_imp"
 "med" "few" "high" "high" | "ve_low_imp"
 "med" "few" "high" "ve_high" | "low_imp"
 "med" "med" "low" "low" | "low_imp"
 "med" "med" "low" "med" | "med_imp"
 "med" "med" "low" "high" | "med_imp"
 "med" "med" "low" "ve_high" | "med_imp"
 "med" "med" "med" "low" | "low_imp"
 "med" "med" "med" "med" | "low_imp"
 "med" "med" "med" "high" | "low_imp"
 "med" "med" "med" "ve_high" | "med_imp"
 "med" "med" "high" "low" | "low_imp"
 "med" "med" "high" "med" | "low_imp"
 "med" "med" "high" "high" | "low_imp"
 "med" "med" "high" "ve_high" | "low_imp"
 "med" "much" "low" "low" | "med_imp"
 "med" "much" "low" "med" | "med_imp"
 "med" "much" "low" "high" | "med_imp"
 "med" "much" "low" "ve_high" | "med_imp"
 "med" "much" "med" "low" | "low_imp"
 "med" "much" "med" "med" | "low_imp"
 "med" "much" "med" "high" | "med_imp"
 "med" "much" "med" "ve_high" | "med_imp"
 "med" "much" "high" "low" | "low_imp"
 "med" "much" "high" "med" | "low_imp"
 "med" "much" "high" "high" | "low_imp"
 "med" "much" "high" "ve_high" | "med_imp"
 "med" "ve_much" "low" "low" | "med_imp"
 "med" "ve_much" "low" "med" | "med_imp"
 "med" "ve_much" "low" "high" | "med_imp"
 "med" "ve_much" "low" "ve_high" | "med_imp"
 "med" "ve_much" "med" "low" | "low_imp"
 "med" "ve_much" "med" "med" | "med_imp"
 "med" "ve_much" "med" "high" | "med_imp"
 "med" "ve_much" "med" "ve_high" | "med_imp"
 "med" "ve_much" "high" "low" | "low_imp"
 "med" "ve_much" "high" "med" | "low_imp"
 "med" "ve_much" "high" "high" | "med_imp"
 "med" "ve_much" "high" "ve_high" | "med_imp"
 "high" "few" "low" "low" | "low_imp"
 "high" "few" "low" "med" | "low_imp"
 "high" "few" "low" "high" | "med_imp"
 "high" "few" "low" "ve_high" | "high_imp"
 "high" "few" "med" "low" | "low_imp"
 "high" "few" "med" "med" | "low_imp"
 "high" "few" "med" "high" | "med_imp"
 "high" "few" "med" "ve_high" | "med_imp"
 "high" "few" "high" "low" | "low_imp"
 "high" "few" "high" "med" | "low_imp"
 "high" "few" "high" "high" | "low_imp"
 "high" "few" "high" "ve_high" | "med_imp"
 "high" "med" "low" "low" | "med_imp"
 "high" "med" "low" "med" | "med_imp"
 "high" "med" "low" "high" | "high_imp"
 "high" "med" "low" "ve_high" | "high_imp"
 "high" "med" "med" "low" | "med_imp"
 "high" "med" "med" "med" | "med_imp"
 "high" "med" "med" "high" | "med_imp"
 "high" "med" "med" "ve_high" | "high_imp"
 "high" "med" "high" "low" | "med_imp"
 "high" "med" "high" "med" | "med_imp"
 "high" "med" "high" "high" | "med_imp"
 "high" "med" "high" "ve_high" | "med_imp"
 "high" "much" "low" "low" | "med_imp"
 "high" "much" "low" "med" | "high_imp"
 "high" "much" "low" "high" | "high_imp"
 "high" "much" "low" "ve_high" | "ve_high_imp"
 "high" "much" "med" "low" | "med_imp"
 "high" "much" "med" "med" | "med_imp"
 "high" "much" "med" "high" | "high_imp"
 "high" "much" "med" "ve_high" | "high_imp"
 "high" "much" "high" "low" | "med_imp"
 "high" "much" "high" "med" | "med_imp"
 "high" "much" "high" "high" | "med_imp"
 "high" "much" "high" "ve_high" | "high_imp"
 "high" "ve_much" "low" "low" | "high_imp"
 "high" "ve_much" "low" "med" | "high_imp"
 "high" "ve_much" "low" "high" | "ve_high_imp"
 "high" "ve_much" "low" "ve_high" | "ve_high_imp"
 "high" "ve_much" "med" "low" | "high_imp"
 "high" "ve_much" "med" "med" | "high_imp"
 "high" "ve_much" "med" "high" | "high_imp"
 "high" "ve_much" "med" "ve_high" | "ve_high_imp"
 "high" "ve_much" "high" "low" | "med_imp"
 "high" "ve_much" "high" "med" | "high_imp"
 "high" "ve_much" "high" "high" | "high_imp"
 "high" "ve_much" "high" "ve_high" | "high_imp"
END_RULES
