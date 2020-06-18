import pandas
import pandas as pd
import datetime

def corr_width(x: int):
    if x <= 7:
        return 7
    elif x >=30:
        return 30
    return x

def auto_columns_width(file_name, data, sheet_name, writer, width=1.7):
    
    # writer
    #global writer
    if not writer:
        writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
    
    if len(sheet_name) > 30:
        sheet_name = sheet_name[0:31]
    
    # drop pandas RangeIndex
    if isinstance(data.index, pd.core.indexes.range.RangeIndex):
        data.to_excel(writer, sheet_name=sheet_name, index=False)
    elif isinstance(data.index, pandas.core.indexes.numeric.Int64Index):
        data.to_excel(writer, sheet_name=sheet_name, index=False)
    else:
        data.to_excel(writer, sheet_name=sheet_name)
    
    # select current worksheet
    worksheet = writer.sheets[sheet_name]
    
    # read columns
    cols = list(data.columns)
    cols_iter = list(data.columns)
    
    # datacolumns to str
    for i in range(len(cols)):
        if isinstance(cols[i], datetime.date):
            cols[i] = cols[i].strftime('%Y-%m-%d')
    
    # if index exists = set k=1
    k = 0
    if data.index.dtype == object:
        k = 1
    
    # setting index length
    try:
        maxlen = max(data.index.astype(str).map(len)) * width
    except:
        maxlen = 5
    worksheet.set_column(0, 0, maxlen)
    
    # setting columns length
    for i, col in enumerate(cols, k):
        
        if data[cols_iter[i-k]].dtype == int:
            col_len = corr_width(len(col)) * width
        else:
            # эта помойка выбирает что длиннее - название столбца или какое-то значение внутри него
            try:
                col_len = max(corr_width(max(data[(cols_iter[i-k])].fillna(0).astype(str).map(len))), len(col))
                col_len *= width
            except:
                col_len = 5
        
        print(i, col, col_len)
        worksheet.set_column(i, i, col_len)
        
    return writer