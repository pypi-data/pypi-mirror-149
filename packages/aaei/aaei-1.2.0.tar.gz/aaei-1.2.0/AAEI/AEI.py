
#### import the simple module from the paraview
from paraview.simple import *
from paraview.vtk.numpy_interface import dataset_adapter as dsa

paraview.simple._DisableFirstRenderCameraReset()

#smarttinylabfoam = FindSource('Smarttinylab.foam')
#By not selecting something, do we retain the user selection??
# create a new 'Python Calculator'


# find source
midy = FindSource('midy')

# find source
aEI_normcsv = FindSource('AEI_norm.csv')
Raw = servermanager.Fetch(aEI_normcsv)
Data = dsa.WrapDataObject(Raw).RowData
Keys = Data.keys()[1:] # Drop name column
NameKeys = ["C10H16","CO2","O3","Cprod"] # Change this when you want to solve for other and more chemicals!
NameKeys = input("Give comma separated chemicals to take into account:").split(",")
ExprKeys = []# Same for this, should have similar length!
for i in NameKeys:
    ExprKeys.append("")
c = 0
Calculators = []
VariableNames = []
Dependency = smarttinylabfoam
for i, x in enumerate(Keys):
    for j, y in enumerate(Data[x]):
        chem = Data["Name"].GetValue(j)
        if chem in NameKeys:
            if y > 0:
                Calculators.append(PythonCalculator(registrationName='{}_{}_{}'.format(c,chem,x), Input=Dependency))
                Calculators[-1].Expression = '({}/max({}))*{}'.format(chem,chem,y)
                VariableNames.append('{}_{}_norm'.format(chem, x))
                Calculators[-1].ArrayName = '{}_{}_norm'.format(chem, x)
                Dependency = Calculators[-1]
            c += 1

for i in VariableNames:
    Chem, Test, nan = i.split("_")
    for j, x in enumerate(NameKeys):
        if x == Chem:
            ExprKeys[j] += "{}+".format(i)

AEI_chemcalc = []
AEI_EXPR = ""
for i, x in enumerate(ExprKeys):
    AEI_chemcalc.append(PythonCalculator(registrationName='{}_AEI'.format(NameKeys[i]), Input=Dependency))
    AEI_chemcalc[-1].Expression = "({})/6".format(x[:-1])
    AEI_EXPR += '{}_AEI+'.format(NameKeys[i])
    AEI_chemcalc[-1].ArrayName = '{}_AEI'.format(NameKeys[i])
    Dependency = AEI_chemcalc[-1]

AEI = PythonCalculator(registrationName='AEI', Input=Dependency)
AEI.Expression = "({})/{}".format(AEI_EXPR[:-1],len(NameKeys))
AEI.ArrayName = 'AEI'
