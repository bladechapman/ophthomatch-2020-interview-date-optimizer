### Ophthalmology Residency Match 2020-2021 Interview Date Optimizer

Uses min cost flows to optimize interview date selection based on personal school ranking, interview date availability, and restrictions on max number of interviews allowed.

```
python3 -m pip install -r requirements.txt
./optimize.py
```

References
- [Google OR-Tools](https://developers.google.com/optimization/flow/mincostflow)
- [Jeff Erickson’s Notes on Minimum Cost Flows](http://jeffe.cs.illinois.edu/teaching/algorithms/notes/G-mincostflow.pdf)
