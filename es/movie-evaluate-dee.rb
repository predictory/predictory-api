!COMMENT!
Enter your description of the rulebase here.
!END_COMMENT!

TypeOfDescription=linguistic
InfMethod=Logical_Deduction
DefuzzMethod=SimpDefuzzLingExpression
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
 "vr sm" "few" "qr sm" "low" | "ml sm"
 "vr sm" "few" "qr sm" "med" | "ml sm"
 "vr sm" "few" "qr sm" "high" | "ml sm"
 "vr sm" "few" "qr sm" "ve_high" | "vr sm"
 "vr sm" "few" "ro me" "low" | "ml sm"
 "vr sm" "few" "ro me" "med" | "ml sm"
 "vr sm" "few" "ro me" "high" | "ml sm"
 "vr sm" "few" "ro me" "ve_high" | "ml sm"
 "vr sm" "few" "qr bi" "low" | "ml sm"
 "vr sm" "few" "qr bi" "med" | "ml sm"
 "vr sm" "few" "qr bi" "high" | "ml sm"
 "vr sm" "few" "qr bi" "ve_high" | "ml sm"
 "vr sm" "med" "qr sm" "low" | "ml sm"
 "vr sm" "med" "qr sm" "med" | "ml sm"
 "vr sm" "med" "qr sm" "high" | "ml sm"
 "vr sm" "med" "qr sm" "ve_high" | "ml sm"
 "vr sm" "med" "ro me" "low" | "ml sm"
 "vr sm" "med" "ro me" "med" | "ml sm"
 "vr sm" "med" "ro me" "high" | "ml sm"
 "vr sm" "med" "ro me" "ve_high" | "ml sm"
 "vr sm" "med" "qr bi" "low" | "ml sm"
 "vr sm" "med" "qr bi" "med" | "ml sm"
 "vr sm" "med" "qr bi" "high" | "ml sm"
 "vr sm" "med" "qr bi" "ve_high" | "ml sm"
 "vr sm" "much" "qr sm" "low" | "ml sm"
 "vr sm" "much" "qr sm" "med" | "ml sm"
 "vr sm" "much" "qr sm" "high" | "ml sm"
 "vr sm" "much" "qr sm" "ve_high" | "ml sm"
 "vr sm" "much" "ro me" "low" | "ml sm"
 "vr sm" "much" "ro me" "med" | "ml sm"
 "vr sm" "much" "ro me" "high" | "ml sm"
 "vr sm" "much" "ro me" "ve_high" | "ml sm"
 "vr sm" "much" "qr bi" "low" | "ml sm"
 "vr sm" "much" "qr bi" "med" | "ml sm"
 "vr sm" "much" "qr bi" "high" | "ml sm"
 "vr sm" "much" "qr bi" "ve_high" | "ml sm"
 "vr sm" "ve_much" "qr sm" "low" | "ml sm"
 "vr sm" "ve_much" "qr sm" "med" | "ml sm"
 "vr sm" "ve_much" "qr sm" "high" | "ml sm"
 "vr sm" "ve_much" "qr sm" "ve_high" | "ml sm"
 "vr sm" "ve_much" "ro me" "low" | "ml sm"
 "vr sm" "ve_much" "ro me" "med" | "ml sm"
 "vr sm" "ve_much" "ro me" "high" | "ml sm"
 "vr sm" "ve_much" "ro me" "ve_high" | "ml sm"
 "vr sm" "ve_much" "qr bi" "low" | "ml sm"
 "vr sm" "ve_much" "qr bi" "med" | "ml sm"
 "vr sm" "ve_much" "qr bi" "high" | "ml sm"
 "vr sm" "ve_much" "qr bi" "ve_high" | "ml sm"
 "me" "few" "qr sm" "low" | "vr sm"
 "me" "few" "qr sm" "med" | "vr sm"
 "me" "few" "qr sm" "high" | "vr sm"
 "me" "few" "qr sm" "ve_high" | "me"
 "me" "few" "ro me" "low" | "ml sm"
 "me" "few" "ro me" "med" | "ml sm"
 "me" "few" "ro me" "high" | "vr sm"
 "me" "few" "ro me" "ve_high" | "vr sm"
 "me" "few" "qr bi" "low" | "ml sm"
 "me" "few" "qr bi" "med" | "ml sm"
 "me" "few" "qr bi" "high" | "ml sm"
 "me" "few" "qr bi" "ve_high" | "vr sm"
 "me" "med" "qr sm" "low" | "vr sm"
 "me" "med" "qr sm" "med" | "me"
 "me" "med" "qr sm" "high" | "me"
 "me" "med" "qr sm" "ve_high" | "me"
 "me" "med" "ro me" "low" | "vr sm"
 "me" "med" "ro me" "med" | "vr sm"
 "me" "med" "ro me" "high" | "vr sm"
 "me" "med" "ro me" "ve_high" | "me"
 "me" "med" "qr bi" "low" | "vr sm"
 "me" "med" "qr bi" "med" | "vr sm"
 "me" "med" "qr bi" "high" | "vr sm"
 "me" "med" "qr bi" "ve_high" | "vr sm"
 "me" "much" "qr sm" "low" | "me"
 "me" "much" "qr sm" "med" | "me"
 "me" "much" "qr sm" "high" | "me"
 "me" "much" "qr sm" "ve_high" | "me"
 "me" "much" "ro me" "low" | "vr sm"
 "me" "much" "ro me" "med" | "vr sm"
 "me" "much" "ro me" "high" | "me"
 "me" "much" "ro me" "ve_high" | "me"
 "me" "much" "qr bi" "low" | "vr sm"
 "me" "much" "qr bi" "med" | "vr sm"
 "me" "much" "qr bi" "high" | "vr sm"
 "me" "much" "qr bi" "ve_high" | "me"
 "me" "ve_much" "qr sm" "low" | "me"
 "me" "ve_much" "qr sm" "med" | "me"
 "me" "ve_much" "qr sm" "high" | "me"
 "me" "ve_much" "qr sm" "ve_high" | "me"
 "me" "ve_much" "ro me" "low" | "vr sm"
 "me" "ve_much" "ro me" "med" | "me"
 "me" "ve_much" "ro me" "high" | "me"
 "me" "ve_much" "ro me" "ve_high" | "me"
 "me" "ve_much" "qr bi" "low" | "vr sm"
 "me" "ve_much" "qr bi" "med" | "vr sm"
 "me" "ve_much" "qr bi" "high" | "me"
 "me" "ve_much" "qr bi" "ve_high" | "me"
 "vr bi" "few" "qr sm" "low" | "vr sm"
 "vr bi" "few" "qr sm" "med" | "vr sm"
 "vr bi" "few" "qr sm" "high" | "me"
 "vr bi" "few" "qr sm" "ve_high" | "vr bi"
 "vr bi" "few" "ro me" "low" | "vr sm"
 "vr bi" "few" "ro me" "med" | "vr sm"
 "vr bi" "few" "ro me" "high" | "me"
 "vr bi" "few" "ro me" "ve_high" | "me"
 "vr bi" "few" "qr bi" "low" | "vr sm"
 "vr bi" "few" "qr bi" "med" | "vr sm"
 "vr bi" "few" "qr bi" "high" | "vr sm"
 "vr bi" "few" "qr bi" "ve_high" | "me"
 "vr bi" "med" "qr sm" "low" | "me"
 "vr bi" "med" "qr sm" "med" | "me"
 "vr bi" "med" "qr sm" "high" | "vr bi"
 "vr bi" "med" "qr sm" "ve_high" | "vr bi"
 "vr bi" "med" "ro me" "low" | "me"
 "vr bi" "med" "ro me" "med" | "me"
 "vr bi" "med" "ro me" "high" | "me"
 "vr bi" "med" "ro me" "ve_high" | "vr bi"
 "vr bi" "med" "qr bi" "low" | "me"
 "vr bi" "med" "qr bi" "med" | "me"
 "vr bi" "med" "qr bi" "high" | "me"
 "vr bi" "med" "qr bi" "ve_high" | "me"
 "vr bi" "much" "qr sm" "low" | "me"
 "vr bi" "much" "qr sm" "med" | "vr bi"
 "vr bi" "much" "qr sm" "high" | "vr bi"
 "vr bi" "much" "qr sm" "ve_high" | "ml bi"
 "vr bi" "much" "ro me" "low" | "me"
 "vr bi" "much" "ro me" "med" | "me"
 "vr bi" "much" "ro me" "high" | "vr bi"
 "vr bi" "much" "ro me" "ve_high" | "vr bi"
 "vr bi" "much" "qr bi" "low" | "me"
 "vr bi" "much" "qr bi" "med" | "me"
 "vr bi" "much" "qr bi" "high" | "me"
 "vr bi" "much" "qr bi" "ve_high" | "vr bi"
 "vr bi" "ve_much" "qr sm" "low" | "vr bi"
 "vr bi" "ve_much" "qr sm" "med" | "vr bi"
 "vr bi" "ve_much" "qr sm" "high" | "ml bi"
 "vr bi" "ve_much" "qr sm" "ve_high" | "ml bi"
 "vr bi" "ve_much" "ro me" "low" | "vr bi"
 "vr bi" "ve_much" "ro me" "med" | "vr bi"
 "vr bi" "ve_much" "ro me" "high" | "vr bi"
 "vr bi" "ve_much" "ro me" "ve_high" | "ml bi"
 "vr bi" "ve_much" "qr bi" "low" | "me"
 "vr bi" "ve_much" "qr bi" "med" | "vr bi"
 "vr bi" "ve_much" "qr bi" "high" | "vr bi"
 "vr bi" "ve_much" "qr bi" "ve_high" | "vr bi"
END_RULES
