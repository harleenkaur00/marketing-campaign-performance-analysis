import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
df = pd.read_csv(r"C:\Users\Dell\Desktop\eda project\nykaa_campaign_data.csv",encoding="ISO-8859-1")
print(df.info())
print(df.shape)
print(df.head())
print(df.describe())
print(df.isnull().sum())
print(df[df.duplicated])
print(df[df.duplicated(subset='Campaign_ID')])
print(df[df.duplicated(subset=['Campaign_ID','Date'])])



# which campaign type give the highest revenue
Campaignn_type=df.groupby("Campaign_Type")["Revenue"].sum()
highest_revenue = Campaignn_type.idxmax()
print(f" campaign type with highest revenue generation : {highest_revenue}")


#co-relation target_audiance and channel_used
#corelation = df["Target_Audience"].corr(df["Channel_Used"])
#print(f"corelation b/w audience and channel  is: {corelation}")


#filtering data
unique_channel_used = df['Channel_Used'].unique()
print(f"\nlist of  unique channel= {unique_channel_used}")

unique_target_audience = df['Target_Audience'].unique()
print(f"\nlist of  unique audience= {unique_target_audience}")


unique_campaign_used = df['Campaign_Type'].unique()
print(f"\nlist of  unique campaign= {unique_campaign_used}")









#first question best performing combination of campaign type,channel used and target audience based on roi(return on investment)

#splitting
df["Channel_Used"]= df["Channel_Used"].str.split(", ")
df =df.explode("Channel_Used")
roi_analysis = df.groupby(["Campaign_Type","Channel_Used","Target_Audience"])["ROI"].mean().reset_index()
#sort to get top performers
roi_analysis=roi_analysis.sort_values(by="ROI",ascending=False)
#top 10 best combos
top_10 = roi_analysis.head(10)
print(top_10)



#visualisation 

# Create a combined label for better readability
top_10["Combo"] = (
    top_10["Campaign_Type"] + " | " +
    top_10["Channel_Used"] + " | " +
    top_10["Target_Audience"]
)

plt.figure(figsize=(12,6))
plt.barh(top_10["Combo"], top_10["ROI"])
plt.xlabel("ROI")
plt.title("Top 10 Campaign Combinations by ROI")
plt.gca().invert_yaxis()
plt.show()











#where the biggest drop happens

#impression(saw)-->clicks--->leads(form filling)-->conversion(bought)
df=df.copy()#avoid modifaction on original datadset or working or copied dataset
#ctr=clicks through rate
df["CTR"]=df["Clicks"]/df["Impressions"]
df["Lead_Rate"]=df["Leads"]/df["Clicks"]
df["Conversion_Rate"] = df["Conversions"] / df["Leads"]


#avg funnel rate
funnel_avg=df[["CTR","Lead_Rate","Conversion_Rate"]].mean()
print(funnel_avg)


#visualization 
import matplotlib.pyplot as plt

stages = ["CTR", "Lead Rate", "Conversion Rate"]
values = funnel_avg.values

plt.figure(figsize=(8,5))
plt.bar(stages, values)
plt.title("Funnel Drop-off Analysis")
plt.ylabel("Average Rate")
plt.show()

df.groupby("Campaign_Type")[["CTR", "Lead_Rate", "Conversion_Rate"]].mean()






#highest revenue generatiion (by seen or by buying)

df["Revenue_per_Impression"] = df["Revenue"] / df["Impressions"]
df["Revenue_per_Conversion"] = df["Revenue"] / df["Conversions"]

segment_analysis = df.groupby("Customer_Segment")[[
    "Revenue_per_Impression",
    "Revenue_per_Conversion"
]].mean().reset_index()

segment_analysis = segment_analysis.sort_values(
    by="Revenue_per_Conversion", ascending=False
)

print(segment_analysis)


#visualization

plt.figure(figsize=(10,5))
plt.bar(segment_analysis["Customer_Segment"], segment_analysis["Revenue_per_Conversion"])
plt.title("Revenue per Conversion by Customer Segment")
plt.xticks(rotation=45)
plt.show()

plt.figure(figsize=(10,5))
plt.bar(segment_analysis["Customer_Segment"], segment_analysis["Revenue_per_Impression"])
plt.title("Revenue per Conversion by Impression Segment")
plt.xticks(rotation=45)
plt.show()

'''#grouped visulaization

'''

x = np.arange(len(segment_analysis["Customer_Segment"]))
width = 0.35

plt.figure(figsize=(10,5))

plt.bar(x - width/2, segment_analysis["Revenue_per_Impression"], width, label="Rev/Impression")
plt.bar(x + width/2, segment_analysis["Revenue_per_Conversion"], width, label="Rev/Conversion")

plt.xticks(x, segment_analysis["Customer_Segment"], rotation=45)
plt.legend()
plt.title("Customer Segment Profitability Comparison")
plt.show()





#which channel give more roias well as engagement and conversion
#roi=return on investment 

df["Channel_Used"] = df["Channel_Used"].str.split(", ")
df_exploded = df.explode("Channel_Used")

channel_analysis = df_exploded.groupby("Channel_Used")[[
    "ROI", "Engagement_Score", "Conversions"
]].mean().reset_index()

channel_analysis = channel_analysis.sort_values(by="ROI", ascending=False)

print(channel_analysis)

#vsualisation

plt.figure(figsize=(8,6))

plt.scatter(
    channel_analysis["Engagement_Score"],
    channel_analysis["ROI"]
)

# Label points
for i, txt in enumerate(channel_analysis["Channel_Used"]):
    plt.annotate(txt, (
        channel_analysis["Engagement_Score"][i],
        channel_analysis["ROI"][i]
    ))

plt.xlabel("Engagement")
plt.ylabel("ROI")
plt.title("Channel Effectiveness: ROI vs Engagement")
plt.show()







#comapign duration effects on diff aspect

plt.figure(figsize=(8,6))

plt.scatter(df["Duration"], df["ROI"])

plt.xlabel("Campaign Duration")
plt.ylabel("ROI")
plt.title("Campaign Duration vs ROI")

plt.show()
# this graaph was unclear like not definingg on what aspect the nroi is relyed so to check this on diff aspect together we re using box plot


df_exploded.boxplot(column="ROI", by="Channel_Used", rot=45)
plt.title("ROI Distribution by Channel")
plt.suptitle("")
plt.show()




#lang based performance analysis
language_analysis = df.groupby("Language")[[
    "ROI", "Conversions", "Engagement_Score"
]].mean().reset_index()

language_analysis = language_analysis.sort_values(by="ROI", ascending=False)

print(language_analysis)

#visaualisation

x = np.arange(len(language_analysis["Language"]))
width = 0.3

plt.figure(figsize=(10,5))

plt.bar(x - width, language_analysis["ROI"], width, label="ROI")
plt.bar(x, language_analysis["Conversions"], width, label="Conversions")
plt.bar(x + width, language_analysis["Engagement_Score"], width, label="Engagement")

plt.xticks(x, language_analysis["Language"])
plt.legend()
plt.title("Language Performance Comparison")
plt.show()







#campaign having high impression but low conversion nd commmon factors they share

df = df.copy()

# Overall conversion rate
df["Conversion_Rate_Total"] = df["Conversions"] / df["Impressions"]

high_imp = df["Impressions"].quantile(0.75)
low_conv = df["Conversion_Rate_Total"].quantile(0.25)


bad_campaigns = df[
    (df["Impressions"] >= high_imp) &
    (df["Conversion_Rate_Total"] <= low_conv)
].copy()

print(bad_campaigns.head())


#visualisation
plt.figure(figsize=(10,6))

# All campaigns
plt.scatter(
    df["Impressions"],
    df["Conversions"],
    alpha=0.3,
    label="All Campaigns"
)

# Highlight bad campaigns
plt.scatter(
    bad_campaigns["Impressions"],
    bad_campaigns["Conversions"],
    label="High Imp, Low Conv",
    marker="x"
)

# Threshold lines
plt.axvline(high_imp, linestyle="--")
plt.axhline(bad_campaigns["Conversions"].mean(), linestyle="--")

plt.xlabel("Impressions")
plt.ylabel("Conversions")
plt.title("Detection of Inefficient Campaigns")
plt.legend()
plt.show()





bad_campaigns["Channel_Used"] = bad_campaigns["Channel_Used"].str.split(", ")
bad_exp = bad_campaigns.explode("Channel_Used")

bad_exp["Channel_Used"].value_counts()
















#higher engagement = hig buying or ios it myth


x = df["Engagement_Score"]
y = df["Conversions"]

# Fit line
m, b = np.polyfit(x, y, 1)

plt.figure(figsize=(8,6))
plt.scatter(x, y, alpha=0.5)

plt.plot(x, m*x + b)  # trend line

plt.xlabel("Engagement")
plt.ylabel("Conversions")
plt.title("Engagement vs Conversions with Trend Line")

plt.show()


df["Engagement_Score"].corr(df["Conversions"])










#best combo of campaign and channel for different audiences

df = df.copy()

# Split multiple channels
df["Channel_Used"] = df["Channel_Used"].astype(str).str.split(", ")

# Expand rows
df_exp = df.explode("Channel_Used")
multi_analysis = df_exp.groupby(
    ["Target_Audience", "Campaign_Type", "Channel_Used"]
)[["ROI", "Conversions"]].mean().reset_index()

# Sort by ROI
multi_analysis = multi_analysis.sort_values(by="ROI", ascending=False)

print(multi_analysis.head())


top_per_audience = multi_analysis.groupby("Target_Audience").head(3)

print(top_per_audience)

#visualisation

import seaborn as sns


pivot = df_exp.pivot_table(
    values="ROI",
    index="Target_Audience",
    columns="Channel_Used",
    aggfunc="mean"
)

plt.figure(figsize=(10,6))
sns.heatmap(pivot, annot=True, fmt=".1f")

plt.title("ROI Heatmap (Audience vs Channel)")
plt.savefig("heatmap.png")
plt.close()


#finding worst combination as well


worst_per_audience = multi_analysis.groupby("Target_Audience").tail(3)

print(worst_per_audience)












#top performing campaign blueprint(what makes campaign succesful)





# Step 1: Copy data (safe practice)
df_q10 = df.copy()

# Step 2: Get Top 10% campaigns based on ROI
top_threshold = df_q10["ROI"].quantile(0.90)

top_campaigns = df_q10[df_q10["ROI"] >= top_threshold].copy()

print("Top 10% Campaigns Shape:", top_campaigns.shape)



print("\n Campaign Type Distribution:")
print(top_campaigns["Campaign_Type"].value_counts())

print("\n Target Audience Distribution:")
print(top_campaigns["Target_Audience"].value_counts())

print("\n Language Distribution:")
print(top_campaigns["Language"].value_counts())

print("\n Campaign Duration Stats:")
print(top_campaigns["Duration"].describe())


# Split multi-channel values
top_campaigns["Channel_Used"] = top_campaigns["Channel_Used"].str.split(", ")

# Explode into separate rows
top_exp = top_campaigns.explode("Channel_Used")

print("\n Channel Distribution:")
print(top_exp["Channel_Used"].value_counts())


# Campaign Type Plot
plt.figure(figsize=(6,4))
top_campaigns["Campaign_Type"].value_counts().plot(kind="bar")
plt.title("Top Campaign Types in High ROI Campaigns")
plt.xlabel("Campaign Type")
plt.ylabel("Count")
plt.show()

# Channel Plot
plt.figure(figsize=(6,4))
top_exp["Channel_Used"].value_counts().plot(kind="bar")
plt.title("Top Channels in High ROI Campaigns")
plt.xlabel("Channel")
plt.ylabel("Count")
plt.show()


top_campaigns = top_campaigns.sort_values(by="ROI", ascending=False)

top_campaigns.to_csv("top_campaigns.csv", index=False)
