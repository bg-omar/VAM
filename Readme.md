from ** text ** to \\textbf{ text } 

````regexp
find: \*\*(.*?)\*\*  
replace:  \\textbf{$1} 
```