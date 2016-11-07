import pandas as pd

def main():
    d = pd.read_csv('../private-data/prepped_random_sample.csv')

    for _, row in d.iterrows():
        print 'ok'

if __name__ == '__main__':
    main()
