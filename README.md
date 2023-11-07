## GFF-Fasta-Extractor

#### Step 1: Check for the Shebang Line. Default is:
&ensp; ``` !#/usr/bin/python3 ```  &emsp; &ensp; # or\
&ensp; ``` !#/usr/bin/env python3 ``` 

&ensp; This can be confirmed by typing on command-line \
&ensp; ``` whereis python3 ``` 

#### Step 2: Make script executable and add to a directory in your PATH :
&ensp; ``` chmod 777 gff-to-fasta-extractor.py ``` \
&ensp; ``` echo $PATH ``` \
&ensp; ``` sudo cp gff-to-fasta-extractor.py /usr/bin/ ``` &ensp; # Adding to PATH

#### Step 3: On Command-Line
&ensp; ``` gff-to-fasta-extractor.py --source <.gff> file --type <feature_type> --attribute <Tag> --value <Tag-Value> ```

##### where: 
&ensp; --source: An input <.gff> file. (General Feature Format). \
&ensp;&ensp;&ensp;&ensp; A sample Saccharomyces_cerevisiae_S288C.annotation.gff is provided in th repo. \
&ensp; --type: feature type. Any of the types present in the 3rd column of the file. \
&ensp;&ensp;&ensp;&ensp; (For example: gene, CDS, repeat_region, exon, etc.)\
&ensp; --attribute: One of the multiple tags present in the 9th column.\
&ensp;&ensp;&ensp;&ensp; (For example: ID, Name, Parent, Alias)\
&ensp; --value: The corresponding tag's value.\
&ensp;&ensp;&ensp;&ensp; (For example: YAL044W, YAR003W)
