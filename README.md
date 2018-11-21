# Readme

Generative classifier for data, maybe can be used as baseline during the RL. Intended to test
if two fields follow a similar distribution, if so, the likelihood of data Y P(Y|class=X) will be high.

## Output

Last 2 columns are negative log-likelihood for the respective classes (name and phone-number like data).
Calculations are basically Naive-Bayes, but looking at character level features instead of more common word level (like in spam filters)

```
Statistics for Names:
Mean Length:  6.11
Variance Length:  2.40
Statistics for Phone:
Mean Length:  11.01
Variance Length:  0.02
  0            Kata -9.78 -37.23
  1           Camel -11.73 -46.54
  2           Hazel -14.52 -46.54
  3           Honey -12.76 -46.54
  4           Neala -12.16 -46.54
  5          Laurie -13.81 -55.85
  6         Auberta -18.50 -65.16
  7         Devonna -17.83 -65.16
  8        Penelope -23.51 -74.47
  9       Corabella -21.55 -83.78
 10     298-226-268 -108.12 -21.08
 11     399-671-821 -108.12 -20.54
 12     445-387-130 -108.12 -21.26
 13     635-365-393 -108.12 -21.08
 14     808-012-082 -108.12 -20.62
 15     823-497-694 -108.12 -20.94
 16     850-081-338 -108.12 -21.01
 17     857-078-309 -108.12 -20.63
 18     911-249-189 -108.12 -20.54
 19     962-102-600 -108.12 -20.76
 ```
