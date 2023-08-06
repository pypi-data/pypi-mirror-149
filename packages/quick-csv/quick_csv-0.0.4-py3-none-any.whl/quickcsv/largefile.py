import time

from dask import dataframe as dd

def cols_from_large_csv(csv_file,encoding='utf-8',low_memeory=False,):
    dask_df = dd.read_csv(csv_file,  low_memory=low_memeory, encoding=encoding)
    cols = list(dask_df.columns.values)
    return cols

def query_large_csv(csv_file,field="",value="",encoding="utf-8",is_vague=False):
    return read_large_csv(csv_file=csv_file,field=field,value=value,encoding=encoding,append_row=True,is_vague=is_vague)

def read_large_csv(csv_file,field="",value="",encoding='utf-8',is_vague=False,string_fields=None,int_fields=None,float_fields=None,
                   append_row=False,
                   low_memory=False,head_num=-1,row_func=None,partition_func=None):
    #for t in self.dict_tables[self.cb_tables.currentText()]:
    #    better_dtypes[t] = "string"
    better_dtypes = {}
    list_fields=[string_fields,int_fields,float_fields]
    list_fields_type=["string","float","int"]
    for idx,fields in enumerate(list_fields):
        if fields!=None:
            for f in fields:
                better_dtypes[f]=list_fields_type[idx]

    dask_df = dd.read_csv(csv_file, dtype=better_dtypes, low_memory=low_memory,encoding=encoding)

    cols = list(dask_df.columns.values)
    print(cols)

    list_all_model = []

    if head_num == -1:
        start=time.time()
        if field!=None and field!="":
            print(f"field: {field}")
            print(f"value: {value}")
            if is_vague:
                result = dask_df.query(f"`{field}`.str.contains(\"{value}\")", local_dict={"label": field, "value": value},
                                       engine="python")
            else:
                result = dask_df.query(f"`{field}` == \"{value}\"", local_dict={"label": field, "value": value})
        else:
            result=dask_df

        count = 0
        # num_partitions = len(result.divisions)
        print("partitions:", result.partitions)
        for part in result.partitions:
            start1 = time.time()
            part_df = part.compute()
            list_model = []
            count += 1
            if partition_func!=None:
                partition_func(part_df,count)
            for index, row in part_df.iterrows():
                model = {}
                for k in cols:
                    v = row[k]
                    if str(type(v)) != "str":
                        v = str(v)
                    model[k] = v
                if append_row:
                    list_model.append(model)
                # process each row
                if row_func!=None:
                    row_func(model,index)
            list_all_model += list_model
        end = time.time()
        print("query time: ", (end - start), "secs")
        return list_all_model
    else:
        # 返回前10行
        append_row=True
        result = dask_df.head(n=head_num)
        list_all_model = []
        for index, row in result.iterrows():
            model = {}
            for k in cols:
                v = row[k]
                if str(type(v)) != "str":
                    v = str(v)
                model[k] = v
            list_all_model.append(model)
    return list_all_model