import pandas as pd
import seaborn as sns, matplotlib.pyplot as plt

insurance_csv = "insurance.csv"
nba_salary = "nba_2022-23_all_stats_with_salary.csv"
df = pd.read_csv(nba_salary)

#print(df.head())
#print(df.describe())
#age,sex,bmi,children,smoker,region,charges

def univariate(df):
    output_df = pd.DataFrame(columns=['type', 'count', 'missing', 'unique', 'mode', 'min', 'q1', 'median', 'q3', 'max', 'mean', 'std', 'skew', 'kurt'])
    for col in df:
        dtype = df[col].dtype
        count = df[col].count()
        missing = df[col].isna().sum()
        unique = df[col].nunique()
        mode = df[col].mode()[0]

        if pd.api.types.is_numeric_dtype(df[col]):
            min = df[col].min()
            q1 = df[col].quantile(.25)
            median = df[col].median()
            q3 = df[col].quantile(.75)
            max = df[col].max()
            mean = df[col].mean()
            std = df[col].std()
            skew = df[col].skew()
            kurt = df[col].kurt()
            
            output_df.loc[col] = [dtype, count, missing, unique, mode, min, q1, median, q3, max, mean, std, skew, kurt]
            sns.histplot(data=df, x=col)
        else:
            output_df.loc[col] = [dtype, count, missing, unique, mode, '-', '-', '-', '-', '-', '-', '-', '-', '-']
            sns.countplot(data=df, x=col)
        plt.show()
    return output_df
print(univariate(df))