class Util:

    @classmethod
    def active(cls, sale):
        i = 0
        if 'recurring' in sale:
            invoice = sale
        else:
            invoices = dict()
            sale = sale.invoices
            for invoice in sale:
                invoices[i] = invoice
                i += 1
            invoice = max(invoices.values())
        i = 0
        lineitems = dict()
        for lineitem_id in invoice.lineitems:
            lineitems[i] = lineitem_id['lineitem_id']
            i += 1
        return lineitems