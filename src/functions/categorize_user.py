
# Categorize users based on these conditions
def categorize_user(df, page_value_threshold, duration_threshold):
    '''Categorize users based on page values, product-related duration, and purchase status
   
     Now to explain the categories 
    1. High Page Values, High Product_Related Duration, Made Purchase (HEMP)
        - Description: These are the most engaged and valuable users who spent significant time on product_related_activities and made purchase
         - Insights: Optimize their ex[perience further and analyze what drives their purchase decisions to replicate for other groups
    2. High Page Values, High Product-Related Duration, Made No Purchase (HENP)
        - Description: Engaged users who didnt convert despite showing strong purchase intent
        - Insights: Investigate potential barriers to conversion, such as pricing, user experience issues or product availability
    3. Zero Page values, High Product-Related Duration, Made Purchase (MEMP)
        - Description - Users who didn't contribute directly to page value but still converted. their long engagement suggests intent
        - Insights: Understand how they navigated and converted without contributing to page value metrics
    4. Zero Page Values, High Product-Related Duration, Made No Purchase (BENP)
        - Description: Users who spent time but didn't engage in activities that contribute to page value or conversion
        - Insights: Focus on re-engagement strategoies to convert these users (e.g retargeting campaigns)
    5. Zero Page Values, Zero Product-Related Duration, Made No Purchase (ZENP)
        - Description: COmpletely disengaged users who neither interacted nor converted
        - Evaluate why they landed on the site (irrelvant traffic sources) and refine targeting and investigate why they left the site without contributing no page value
    6. Zero Page Values, Zero Product-Related Duration, Made Purchase (ZEMP)
        - Description: Users who converted without spending significant time or contributing page value
        - Insights: Explore if these are repeat customers, direct navigators, or influenced by external factors like promotions

    
    Parameters:
        df (pd.DataFrame): The input DataFrame containing user data.
        page_value_threshold (float): Threshold for high/zero page values.
        duration_threshold (float): Threshold for high/zero product-related duration.
        
    Usage:   
    categorize_user(df, page_value_threshold=0, duration_threshold=0)

    Returns: 
        pd.Series: A series of categories corresponding to each user'''

    def assign_category(row):

        if row['page_values'] == 0 and row['product_related_duration'] > duration_threshold:
            return 'HEMP' if row['purchase'] == 1 else 'HENP'
        elif row['page_values'] == 0 and row['product_related_duration'] > duration_threshold:
            return 'MEMP' if row['purchase'] == 1 else 'BENP'
        elif row['page_values'] == 0 and row['product_related_duration'] == 0:
            return 'ZEMP' if row['purchase'] == 1 else 'ZENP'
        else:
            return 'Other'
    return df.apply(assign_category, axis=1)
    
    