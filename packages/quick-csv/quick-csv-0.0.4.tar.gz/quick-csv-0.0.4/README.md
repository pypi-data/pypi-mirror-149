## Quick CSV

Read and write small or large CSV/TXT files in a simple manner

### Installation
```pip
pip install quick-csv
```

### Examples for small files
Example 1: read and write csv or txt files
```python
from quickcsv.file import *
# read a csv file
list_model=read_csv('data/test.csv')
for idx,model in enumerate(list_model):
    print(model)
    list_model[idx]['id']=idx
# save a csv file
write_csv('data/test1.csv',list_model)

# write a text file
write_text('data/text1.txt',"Hello World!")
# read a text file
print(read_text('data/text1.txt'))
```
Example 2: create dataframe from a list of models
```python
from quickcsv.file import *
# read a csv file
list_model=read_csv('data/test.csv')
# create a dataframe from list_model
df=create_df(list_model)
# print
print(df)
```

### Examples for large files
Example 1: read large csv file
```python
from quickcsv.largefile import *
if __name__=="__main__":
    csv_path=r"umls_atui_rels.csv" # a large file (>500 MB)
    total_count=0

    def process_partition(part_df,i):
        print(f"Part {i}")

    def process_row(row,i):
        global total_count
        print(i)
        total_count+=1

    list_results=read_large_csv(csv_file=csv_path,row_func=process_row,partition_func=process_partition)

    print("Return: ")
    print(list_results)

    print("Total Record Num: ",total_count)

```

Example 2: query from a large csv file
```python
from quickcsv.largefile import *

if __name__=="__main__":
    csv_path=r"umls_sui_nodes.csv" # a large file (>500 MB)
    total_count=0
    # process each partition in the large file
    def process_partition(part_df,i):
        print(f"Part {i}")
        print()
    # process each row in a partition while reading
    def process_row(row,i):
        global total_count
        print(row)
        total_count+=1
    # field is a field in the csv file, and value is the value you need to find within the csv file
    list_results=read_large_csv(csv_file=csv_path, field="SUI",value="S0000004", append_row=True, row_func=process_row,partition_func=process_partition)

    print("Return: ")
    print(list_results)

    print("Total Record Num: ",total_count)
```

Example 3: read top N records from the large csv file
```python
from quickcsv.largefile import *

if __name__=="__main__":
    csv_path=r"umls_atui_rels.csv"
    total_count=0
    # return top 10 rows in the csv file
    list_results=read_large_csv(csv_file=csv_path,head_num=10)

    print("Return: ")
    print(list_results)

    print("Total Record Num: ",total_count)
```

### License

The `quick-csv` project is provided by [Donghua Chen](https://github.com/dhchenx). 

