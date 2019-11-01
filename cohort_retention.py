def retention_cohort(
        df_,
        invoicedate='invoicedate',
        Quantity='Quantity',
        price='InvoiceAmount',
        CustomerId='DistributorId'
                    ):
    """
    :param df_: dataframe containing the transaction
                data with columns ['invoicedate', 'Quantity'
                'price', 'CustomerId']
    :param invoicedate:
    :param Quantity:
    :param price:
    :param CustomerId:
    :return: a dataframe with monthly retention percentage

    """
    df_[invoicedate] = pd.to_datetime(df_[invoicedate], errors='coerce')
    df_.dropna(inplace=True)
    df_['invoice_year_month'] = df_[invoicedate].map(lambda date: date.year * 100 + date.month)
    df_["revenue"] = df_[Quantity] * df_[price]
    df_cust_rev_monthly = df_.groupby([CustomerId, "invoice_year_month"])["revenue"].sum().reset_index()
    retent_df = pd.crosstab(df_cust_rev_monthly[CustomerId], df_cust_rev_monthly["invoice_year_month"]).reset_index()
    new_column_names = ['m_' + str(column) for column in retent_df.columns]
    retent_df.columns = new_column_names
    months = df_["invoice_year_month"].unique()
    months.sort()

    import numpy as np
    retent_array = []
    for i in range(0, len(months)):
        retent_data = {}
        selected_month = months[i]
        prev_months = months[:i]
        next_months = months[i + 1:]
        for prev_month in prev_months:
            retent_data[prev_month] = np.nan

        total_user_count = retent_df['m_' + str(selected_month)].sum()
        retent_data["total_user_count"] = total_user_count
        retent_data[selected_month] = 1

        query = "{} >0 ".format('m_' + str(selected_month))

        for next_month in next_months:
            query = query + " and {} > 0".format('m_' + str(next_month))
            retent_data[next_month] = np.round(retent_df.query(query)['m_' + str(next_month)].sum() / total_user_count,
                                               2)
        retent_array.append(retent_data)

    retent_cohort_df = pd.DataFrame(retent_array)
    retent_cohort_df.index = months[:]

    return retent_cohort_df
