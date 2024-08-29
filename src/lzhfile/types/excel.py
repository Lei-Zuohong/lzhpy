# -*- coding: UTF-8 -*-
# Public package
import pandas
import xlwings
# Private package
# Internal package

################################################################################
# 处理 Excel 文件的软件包
################################################################################


def dataframe_load(filename, region=''):
    '读取文件内表格'
    app = xlwings.App(visible=True, add_book=False)
    try:
        xbook = app.books.open(filename)
        xsheet = xbook.sheets[0]
        if(region==''):
            df = xsheet.used_range.options(pandas.DataFrame).value
        else:
            df = xsheet.range(region).options(pandas.DataFrame).value
        xbook.close()
    except Exception as e:
        print('Error loading dataframe from Excel')
        print(e)
    app.kill()
    return df

def dataframe_dump(filename, df, region=''):
    '表格保存至文件'
    app = xlwings.App(visible=True, add_book=False)
    try:
        xbook = app.books.add()
        xsheet = xbook.sheets[0]
        if(region==''):
            xsheet.range('A1').value = df
        else:
            xsheet.range(region).value = df
        xbook.save(filename)
        xbook.close()
    except Exception as e:
        print('Error dumping dataframe from Excel')
        print(e)
    app.kill()
    return df
        
