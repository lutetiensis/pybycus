# pybycus

## Introduction

**pybycus** is a Python 3 package to parse the Ibycus format, used by the [PHI
& TLG CD-ROMs](http://stephanus.tlg.uci.edu/history.php).

Despite the notoriety they have acquired along the years, the documentation is
rather scarce and it takes many a days to get acquainted with their inner
format. We have not yet completely succeeded in that regard.

Other tools exist, and were of [great help](#acknowledgements) in our endeavor.
It is however difficult to understand the specifications of the format by
simply reading their code. Most of their developers actually had no access to
any documentation. The unexpected recent publication of some official
documents tremendously sped up our efforts.

The code was therefore written with two purposes in mind: not only implement a
tool that can be used to extract the information from the files; but also
document how they can be parsed. Python is in our view a great language as it
allows one to concentrate on the high-level approach—despite a consequent loss
of performance.

Our work is still new. We have only worked with Latin texts and not processed
beta codes yet. The output is not defined and will change. A lot remains to be
done, but we found the library mature enough to be published without blushing.

We hope it will be useful to the small community of modern scholars.

## API

### AUTHTAB.DIR

```python
import pybycus.authtab
authtab = pybycus.authtab.content("./AUTHTAB.DIR")
```

```
python3 -m pybycus.authtab ./AUTHTAB.DIR
```

### IDT

```python
import pybycus.idt
idt = pybycus.idt.content("./LAT0474.IDT")
```

```
python3 -m pybycus.idt ./LAT0474.IDT
```

### TXT

```python
import pybycus.txt
txt = pybycus.txt.content("./LAT0914.TXT")
```

```
python3 -m pybycus.txt ./LAT0914.TXT
```

## Acknowledgements

We would like to thank the following projects, which proved very helpful in
guiding our implementation and checking our results:

 - [tlgu](http://tlgu.carmen.gr/), by Dimitri Marinakis;
 - [libycus](http://libycus.sourceforge.net/), by Sean Redmond;
 - [Diogenes](https://github.com/pjheslin/diogenes/), by P. J. Heslin.

This project would never have been completed without all those who provided us
with documents and more especially, again, P. J. Heslin who released some of
the [PHI & TLG documentation](https://github.com/pjheslin/phi-tlg-docs/).

Last but not least, we express our gratitude to the [Packard Humanities
Institute](https://packhum.org/) and the [Thesaurus Linguae
Graecae](http://stephanus.tlg.uci.edu/) project. Their dream still lives on
half a century later, and we sincerely hope they would support our work.

## License

This code was written to be shared.

Please check the [LICENSE](LICENSE) file that comes with the code.
