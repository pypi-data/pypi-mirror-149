Air Adverse Effect Index
------------------------

Calculate the relative toxicity effect(s) of different trace gas compounds with [GenRA](https://comptox.epa.gov/genra/)

install with
```bash
pip install aaei
```
Or
```bash
pip install aaei ".[Viz]"
```
to include visualization capabilities


Example code:
```bash
mkdir health_effects
cd health_effects
AEI CopyExamples
AEI Run viz piv=Batch_Report_Target.csv
```

This tool uses the output of [GenRA](https://comptox.epa.gov/genra/) toxicological Generalized Read-across Database/tool.  
One or more chemicals can be statistically analyzed, these statistics can be applied to measured or simulated chemical concentrations.

See [Github](https://github.com/Kwabratseur/AAEI) for more details.
