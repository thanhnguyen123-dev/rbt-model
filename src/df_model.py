import pandas as pd
import csv


def get_df():
  # read from an excel file and drop irrelevant columns
  pd.set_option('display.max_rows', None)
  df = pd.read_excel('data/rbt_analysis.xlsx', '3-point and Majority')
  df = df.filter(regex='^(?!Unnamed)')
  dropped_cols = ['NONE', 'LOW', 'MODERATE', 'HIGH', '3-POINT SCALE']
  df.drop(dropped_cols, axis=1, inplace=True)


  df.to_csv('data/rbt.csv', index=False)
  with open('data/rbt.csv', 'r') as f:
      reader = csv.reader(f)
      rows_keep = [row for row in reader if row[0] != '']

  with open('data/rbt.csv', 'w', newline="") as wrt:
      writer = csv.writer(wrt)
      for row in rows_keep:
          writer.writerow(row)

  df = pd.read_csv('data/rbt.csv')
  return df


def get_question_type_df(df:pd.DataFrame, key:int) -> pd.DataFrame:
  df_row_indices = df.index[df.iloc[:, 0].str.contains('REMEMBER', na=False)].tolist()
  df_map = {}
  for i in range(len(df_row_indices)):
    start = df_row_indices[i]
    if (i < len(df_row_indices) - 1):
      end = df_row_indices[i+1]
    else:
      end = len(df)

    question_type_df = df.iloc[start:end].reset_index(drop=True)
    question_type_num = df.iloc[start, 1]
    
    row_name = question_type_df.iloc[:, 0].tolist()
    question_type_df.index = row_name

    del question_type_df['SKILL']

    df_map[question_type_num] = question_type_df
  
  return df_map[key]


  

