<!-- README.md -->

# VAMknots

A MiK\TeX/LaTeX package to visualize VAM vortex knots and Reidemeister moves
with U(1), SU(2), SU(3) styling.

## Installation

1. Copy the three files (`vamknots.dtx`, `vamknots.ins`, `README.md`)
   into your local `texmf` directory, e.g.:

C:\Users<you>\AppData\Local\MiKTeX\2.9\tex\latex\vamknots\

arduino
Copy
Edit

2. Open a command prompt in that folder and run:

tex vimknots.ins

markdown
Copy
Edit

This will generate `vamknots.sty`.

3. In the MiK\TeX Console, click **Refresh file name database**.

4. Now you can use it in any document:

```latex
\usepackage{vamknots}
```