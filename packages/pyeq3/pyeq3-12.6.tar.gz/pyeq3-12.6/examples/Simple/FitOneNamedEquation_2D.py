import pyeq3


# see IModel.fittingTargetDictionary
equation = pyeq3.Models_2D.BioScience.HyperbolicLogistic()  # SSQABS by default

data = equation.exampleData
pyeq3.dataConvertorService().ConvertAndSortColumnarASCII(data, equation, False)
equation.Solve()

print(equation)
pyeq3.Output.Print.DatumInformation(equation)
pyeq3.Output.Print.FitStatistics(equation)

print()
print('Java Source Code:')
print(pyeq3.outputSourceCodeService().GetOutputSourceCodeJAVA(equation))
