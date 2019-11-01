def new_exist_ratio(
                    df,
                    InvoiceDate='InvoiceDate',
                    Quantity='Quantity',
                    price='UnitPrice',
                    CustomerID='CustomerID'
                    ):
    """

    :param df: dataframe containing
                transaction details
                with columns
                ['InvoiceDate','Quantity'
                'price','CustomerID']
    :param InvoiceDate:
    :param Quantity:
    :param price:
    :param CustomerID:
    :return: a dataframe of monthly revenue
            from new and existing user_types

    """

    df['revenue']=df[Quantity]*df[price]
    df[InvoiceDate]=pd.to_datetime(df[InvoiceDate],errors='coerce')
    df.dropna(inplace=True)
    df['invoice_year_month']=df[InvoiceDate].map(lambda date:date.year*100 + date.month)
    df_new_cust=df.groupby(CustomerID)[InvoiceDate].min().reset_index()
    df_new_cust.rename(columns={InvoiceDate:"min_purchase_date"},inplace=True)
    df_new_cust["min_purchase_yearMonth"]=df_new_cust['min_purchase_date'].map(lambda date : date.year*100 + date.month)
    df_cust=pd.merge(df,df_new_cust,on=CustomerID)
    df_cust['user_type']="new"
    df_cust.loc[df_cust["invoice_year_month"]>df_cust['min_purchase_yearMonth'],'user_type']='existing'
    df_cust_type_revenue=df_cust.groupby(["invoice_year_month","user_type"])['revenue'].sum().reset_index()

    return df_cust_type_revenue