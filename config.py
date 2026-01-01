CONFIG = {
    "MoneyGramFacture": {
        "date": "business_date", "montant": "net_total_total_stl", "pays": None,
        "id": "settlement_id", "devise": "settlement_currency", 
        "commission": "net_total_commission_amt_stl"
    },
    "MoneyGramTr": {
        "date": "tran_date", "montant": "base_amt", "pays": "orig_cntry",
        "id": "transaction_id", "devise": "settlement_currency", 
        "commission": "cmsn_stlmt_amt"
    },
    "RIA": {
        "date": "date", "montant": "montant_a_payer", "pays": "pays_denvoi",
        "id": "numero_de_transfert", "devise": "devise_de_paiement", 
        "commission": "montant_de_la_commission"
    },
    "SmallWorld": {
        "date": "date", "montant": "montant_destination", "pays": "pays_souce",
        "id": "ref", "devise": "devise_dest", 
        "commission": "commission_agent"
    },
    "Western": {
        "date": "paydate", "montant": "recprincipalloc", "pays": "reccountry",
        "id": "mtcn", "devise": "loccurrencycode", 
        "commission": "subagentcommchargesloc"
    }
}