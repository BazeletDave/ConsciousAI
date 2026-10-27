"""Synthetic campaign post telemetry.
Research contribution: David Grand, Grand Research Institute.
All generated values are simulated. Run: python campaign_post_telemetry.py
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Simulated campaign post telemetry data
np.random.seed(42)
n_posts = 200

data = {
    'candidate': np.random.choice(['Lula', 'Opponent'], size=n_posts),
    'followers_at_post': np.random.randint(5_000_000, 15_000_000, size=n_posts),
    'organic_impressions': np.random.randint(100_000, 2_000_000, size=n_posts),
    'likes': np.random.randint(5_000, 150_000, size=n_posts),
    'shares': np.random.randint(1_000, 50_000, size=n_posts),
    'comments': np.random.randint(500, 30_000, size=n_posts),
}

df = pd.DataFrame(data)

# Calculate Engagement Rate (ER) and Reach-to-Follower Ratio
df['total_interactions'] = df['likes'] + df['shares'] + df['comments']
df['engagement_rate'] = df['total_interactions'] / df['organic_impressions']
df['reach_efficiency'] = df['organic_impressions'] / df['followers_at_post']

# Group by Candidate to evaluate statistical differences
# This summary reports descriptive means; it does not perform significance tests.
summary = df.groupby('candidate')[['engagement_rate', 'reach_efficiency', 'total_interactions']].mean()
print("--- Average Metric Comparison ---")
print(summary)
