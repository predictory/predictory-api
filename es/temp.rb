!COMMENT!
Enter your description of the rulebase here.
!END_COMMENT!

TypeOfDescription=linguistic
InfMethod=Fuzzy_Approximation-logical
DefuzzMethod=ModifiedCenterOfGravity
UseFuzzyFilter=false

NumberOfAntecedentVariables=3
NumberOfSuccedentVariables=1
NumberOfRules=48

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
End_AntVariable3

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
 "low" "few" "low" | "ve_low_imp"
 "low" "few" "med" | "ve_low_imp"
 "low" "few" "high" | "ve_low_imp"
 "low" "few" "ve_high" | "low_imp"
 "low" "med" "low" | "ve_low_imp"
 "low" "med" "med" | "ve_low_imp"
 "low" "med" "high" | "ve_low_imp"
 "low" "med" "ve_high" | "ve_low_imp"
 "low" "much" "low" | "ve_low_imp"
 "low" "much" "med" | "ve_low_imp"
 "low" "much" "high" | "ve_low_imp"
 "low" "much" "ve_high" | "ve_low_imp"
 "low" "ve_much" "low" | "ve_low_imp"
 "low" "ve_much" "med" | "ve_low_imp"
 "low" "ve_much" "high" | "ve_low_imp"
 "low" "ve_much" "ve_high" | "ve_low_imp"
 "med" "few" "low" | "low_imp"
 "med" "few" "med" | "low_imp"
 "med" "few" "high" | "low_imp"
 "med" "few" "ve_high" | "med_imp"
 "med" "med" "low" | "low_imp"
 "med" "med" "med" | "med_imp"
 "med" "med" "high" | "med_imp"
 "med" "med" "ve_high" | "med_imp"
 "med" "much" "low" | "med_imp"
 "med" "much" "med" | "med_imp"
 "med" "much" "high" | "med_imp"
 "med" "much" "ve_high" | "med_imp"
 "med" "ve_much" "low" | "med_imp"
 "med" "ve_much" "med" | "med_imp"
 "med" "ve_much" "high" | "med_imp"
 "med" "ve_much" "ve_high" | "med_imp"
 "high" "few" "low" | "low_imp"
 "high" "few" "med" | "low_imp"
 "high" "few" "high" | "med_imp"
 "high" "few" "ve_high" | "high_imp"
 "high" "med" "low" | "med_imp"
 "high" "med" "med" | "med_imp"
 "high" "med" "high" | "high_imp"
 "high" "med" "ve_high" | "high_imp"
 "high" "much" "low" | "med_imp"
 "high" "much" "med" | "high_imp"
 "high" "much" "high" | "high_imp"
 "high" "much" "ve_high" | "ve_high_imp"
 "high" "ve_much" "low" | "high_imp"
 "high" "ve_much" "med" | "high_imp"
 "high" "ve_much" "high" | "ve_high_imp"
 "high" "ve_much" "ve_high" | "ve_high_imp"
END_RULES
