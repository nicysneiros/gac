from geraldo import Report, ReportBand, ObjectValue, ReportBand, landscape, SystemField, BAND_WIDTH, Label, FIELD_ACTION_COUNT, FIELD_ACTION_AVG, FIELD_ACTION_MIN, FIELD_ACTION_MAX, FIELD_ACTION_SUM, FIELD_ACTION_DISTINCT_COUNT, BAND_WIDTH

from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_CENTER, TA_RIGHT

class PedidosReport(Report):
    title = 'Relatorio Financeiro-Pedidos'
    print_if_empty = True
    page_size = A4


    class band_summary(ReportBand):
        height = 0.8*cm
        elements = [
            SystemField(expression=u'----------------------------------------------------------------------------------------------------------------------------------------------------------------', top=0.1*cm,
                    width=BAND_WIDTH),
                
            Label(text="Lucro", top=0.5*cm, style={'fontName': 'Helvetica-Bold'},left=0.5*cm),
            ObjectValue(attribute_name='valorCobrado', top=0.5*cm, left=4*cm,\
                action=FIELD_ACTION_SUM),
            Label(text="Gastos", top=1*cm, style={'fontName': 'Helvetica-Bold'}, left=0.5*cm),
            ObjectValue(attribute_name='valorGasto', top=1*cm, left=4*cm,\
                action=FIELD_ACTION_SUM),
        ]

    class band_detail(ReportBand):
        height = 0.5*cm
        elements=(
                ObjectValue(attribute_name='cliente.nome', left=0.5*cm),
                ObjectValue(attribute_name='dataEntrega', left=3*cm),
                ObjectValue(attribute_name='valorCobrado',left=7*cm),
                ObjectValue(attribute_name='valorGasto', left=11*cm),                    
                )

       
    class band_page_header(ReportBand):
        height = 1.3*cm
        elements = [
                SystemField(expression='%(report_title)s', top=0.1*cm, left=0, width=BAND_WIDTH,
                    style={'fontName': 'Helvetica-Bold', 'fontSize': 18, 'alignment': TA_CENTER}),
                Label(text="Cliente", top=0.8*cm, left=0.5*cm),
                Label(text=u"Data Entrega", top=0.8*cm, left=3*cm),
                Label(text=u"Valor Cobrado", top=0.8*cm, left=7*cm),
                Label(text=u"Valor Gasto", top=0.8*cm, left=11*cm),
                SystemField(expression=u'Pagina %(page_number)d de %(page_count)d', top=0.1*cm,
                    width=BAND_WIDTH, style={'alignment': TA_RIGHT}),
                ]
        borders = {'bottom': True}

    class band_page_footer(ReportBand):
        height = 0.5*cm
        elements = [
                Label(text='GAC', top=0.1*cm),
                SystemField(expression=u'Impresso em %(now:Y, b d)s as %(now:H:i)s', top=0.1*cm,
                    width=BAND_WIDTH, style={'alignment': TA_RIGHT}),
                ]

        borders = {'top': True}        

class ProdutosReport(Report):
    title = 'Relatorio Financeiro-Produtos'
    print_if_empty = True
    page_size = A4



    class band_summary(ReportBand):
        height = 0.8*cm
        elements = [
            SystemField(expression=u'----------------------------------------------------------------------------------------------------------------------------------------------------------------', top=0.1*cm,
                    width=BAND_WIDTH),                
            Label(text="Lucro", top=0.5*cm,style={'fontName': 'Helvetica-Bold'}, left=0.5*cm),
            ObjectValue(attribute_name='valorCobrado', top=0.5*cm, left=4*cm,\
                action=FIELD_ACTION_SUM),
            Label(text="Gastos", top=1*cm, style={'fontName': 'Helvetica-Bold'},left=0.5*cm),
            ObjectValue(attribute_name='valorGasto', top=1*cm, left=4*cm,\
                action=FIELD_ACTION_SUM),
        ]



    class band_detail(ReportBand):
        height = 0.5*cm
        elements=(                
                ObjectValue(attribute_name='cliente.nome', left=0.5*cm),
                ObjectValue(attribute_name='dataVenda', left=3*cm,
                    get_value=lambda instance: instance.dataVenda.strftime('%d/%m/%Y')),
                ObjectValue(attribute_name='valorCobrado',left=7*cm),
                ObjectValue(attribute_name='valorGasto', left=11*cm),                    
                )
    class band_page_header(ReportBand):
        height = 1.3*cm
        elements = [
                SystemField(expression='%(report_title)s', top=0.1*cm, left=0, width=BAND_WIDTH,
                    style={'fontName': 'Helvetica-Bold', 'fontSize': 18, 'alignment': TA_CENTER}),
                Label(text=u"Cliente", top=0.8*cm, left=0.5*cm),
                Label(text="Data da Venda", top=0.8*cm, left=3*cm),
                Label(text=u"Valor Cobrado", top=0.8*cm, left=7*cm),
                Label(text=u"Valor Gasto", top=0.8*cm, left=11*cm),
                SystemField(expression=u'Pagina %(page_number)d de %(page_count)d', top=0.1*cm,
                    width=BAND_WIDTH, style={'alignment': TA_RIGHT}),
                ]
        borders = {'bottom': True}

    class band_page_footer(ReportBand):
        height = 0.5*cm
        elements = [
                Label(text='GAC', top=0.1*cm),
                SystemField(expression=u'Impresso em %(now:Y, b d)s as %(now:H:i)s', top=0.1*cm,
                    width=BAND_WIDTH, style={'alignment': TA_RIGHT}),
                ]
        borders = {'top': True}                