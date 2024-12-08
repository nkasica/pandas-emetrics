# pandas-emetrics
`pandas-emetrics` is an in-progress python package built on top of [Pandas](https://pandas.pydata.org/docs/). My goal with this project is to make ethical considerations in relation to data, such as [k-anonymity](https://en.wikipedia.org/wiki/K-anonymity) and [l-diversity](https://personal.utdallas.edu/~muratk/courses/privacy08f_files/ldiversity.pdf), easily accessable to data scientists, analysts, researchers—basically anyone working with data.


### To-Do
- [ ] implement k_anonymize()
- [ ] further research into possible implementations of [t closeness](https://www.cs.purdue.edu/homes/ninghui/papers/t_closeness_icde07.pdf)
- [ ] further research into other ethical considerations that could be useful
- [ ] encrypt() function
- [ ] add unit tests for all functions
- [ ] add_noise() function

### References
- [K Anonymity](https://www.immuta.com/blog/k-anonymity-everything-you-need-to-know-2021-guide/)
- [L Diversity](https://personal.utdallas.edu/~muratk/courses/privacy08f_files/ldiversity.pdf)
- [Multivariate Mondrian Algorithm](https://pages.cs.wisc.edu/~lefevre/MultiDim.pdf)
