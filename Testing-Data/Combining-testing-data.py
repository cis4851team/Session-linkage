import pandas as pd
import xlrd

# filenames
fingerprints_names = []
#["xlsx1.xlsx", "xlsx2.xlsx", "xlsx3.xlsx"]
for num in range(1,20):
    fingerprints_names.append("fingerprints" + str(num) + ".xlsx")

urls_names = []
for num in range(1,21):
    urls_names.append("urls" + str(num) + ".xlsx")

# read them in
fingerprints = [pd.ExcelFile(name) for name in fingerprints_names]
urls = [pd.ExcelFile(name) for name in urls_names]

# turn them into dataframes
fingerprint_frames = [x.parse(x.sheet_names[0], header=None,index_col=None) for x in fingerprints]
urls_frames = [x.parse(x.sheet_names[0], header=None,index_col=None) for x in urls]

# delete the first row for all frames except the first
fingerprint_frames[1:] = [df[1:] for df in fingerprint_frames[1:]]
urls_frames[1:] = [df[1:] for df in urls_frames[1:]]

# concatenate them..
fingerprints_combined = pd.concat(fingerprint_frames)
urls_combined = pd.concat(urls_frames)

#1-10 are normal browsing sessions
#11-20 are private browsing sessions
fingerprints_combined[4] = 'non-private'
fingerprints_combined.iloc[0, 4] = 'Mode'
fingerprints_combined.iloc[8:, 4] = 'private'

urls_combined[4] = 'non-private'
urls_combined.iloc[0, 4] = 'Mode'
urls_combined.iloc[41:, 4] = 'private'


# write it out
fingerprints_combined.to_excel("fingerprints_combined.xlsx", header=False, index=False)
urls_combined.to_excel("urls_combined.xlsx", header=False, index=False)