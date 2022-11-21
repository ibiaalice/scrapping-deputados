import scrapy


class SpiderScrappy(scrapy.Spider):
    name = "links_deputados"

    def start_requests(self):
        with open("lista_deputadas.txt") as file:
            array_links = file.readlines()
        for link in array_links:
            yield scrapy.Request(url=link, callback=self.parse)

    def parse(self, response):
        name_dept = response.xpath('//h2[@id="nomedeputado"]/text()').get()
        gender = "M"
        assiduity = response.xpath('//dd[@class="list-table__definition-description"]/text()').getall()
        table_assiduity_plenario  = [self.clean_text(p) for p in assiduity]
        assiduity_plenario = table_assiduity_plenario[0]
        justify_fault = table_assiduity_plenario[1]
        fault = table_assiduity_plenario[2]
        comission = table_assiduity_plenario[3]
        justify_fault_commission = table_assiduity_plenario[4]
        fault_commission = table_assiduity_plenario[5]

        bithday_date = self.clean_text(response.xpath('//ul[@class="informacoes-deputado"]//li/text()').getall()[4])

        total_spent = response.xpath('//ul[@class="gastos-anuais-deputado-container"]//tbody//tr//td/text()').getall()
        total_spent = [self.clean_text(g) for g in total_spent]
        
        grouped_total_par = []

        index = len(total_spent) // 3

    
        for i in range(index):
            grouped_total_par.append(total_spent[i*3:(i+1)*3])

        total_spent_parl = grouped_total_par[0][1]

        index_parl = -1

        for index,g in enumerate(grouped_total_par[1:]):
            if g[0] == 'Total Gasto':
                total_gasto_gabinete = g[1]
                index_parl = index

        month = ['JAV','FEV','MAR','MAI','ABR','JUN','JUL','AGO','SET','OUT','NOV','DEZ']


        column_parlamentar = [  'gasto_jan_par', 
                                'gasto_fev_par',
                                'gasto_mar_par',
                                'gasto_abr_par' ,
                                'gasto_maio_par',
                                'gasto_junho_par',
                                'gasto_jul_par',
                                'gasto_agosto_par',
                                'gasto_set_par',
                                'gasto_out_par',
                                'gasto_nov_par',
                                'gasto_dez_par'
                             ]

        gb_columns = [
                            'gasto_jan_gab',
                            'gasto_fev_gab',
                            'gasto_mar_gab',
                            'gasto_abr_gab' ,
                            'gasto_maio_gab',
                            'gasto_junho_gab',
                            'gasto_jul_gab', 
                            'gasto_agosto_gab',
                            'gasto_set_gab',
                            'gasto_out_gab',
                            'gasto_nov_gab',
                            'gasto_dez_gab'
                    ]

        map_spent_parlamentar = {v1:v2 for v1,v2 in zip(month, column_parlamentar)}
        map_spent_gabinete = {v1:v2 for v1,v2 in zip(month, gb_columns)}

        total_spent_parlamentar_prim = {v[0]:v[1] for v in grouped_total_par[:index_parl]}
        total_spent_parlamentar_seg = {v[0]:v[1] for v in grouped_total_par[index_parl:]}
        
        spent_parlamentar = {}
        
        for key,value in map_spent_parlamentar.items():
            if key in total_spent_parlamentar_prim:
                spent_parlamentar[value] = total_spent_parlamentar_prim[key]
            else:
                spent_parlamentar[value] = '-'

        spent_gabinete = {}
        for key,value in map_spent_gabinete.items():
            if key in total_spent_parlamentar_seg:
                spent_gabinete[value] = total_spent_parlamentar_seg[key]
            else:
                spent_gabinete[value] = '-'

        salary = self.clean_text(response.xpath('//*[@id="recursos-section"]/ul/li[2]/div/a/text()').get())
        
        dic = {
            'nome':name_dept,
            'genero':gender,
            'presenca_plenario':assiduity_plenario,
            'ausencia_justificada_plenario':justify_fault,
            'ausencia_plenario':fault,
            'presenca_comissao':comission,
            'ausencia_justificada_comissao':justify_fault_commission,
            'ausencia_comissao':fault_commission,
            'data_nascimento':bithday_date,
            'total_gasto_parlamentar':total_spent_parl,
            'total_gasto_gabinete':total_gasto_gabinete,
            'salario_bruto':salary
        }

        dic.update(spent_parlamentar)

        dic.update(spent_gabinete)

        yield dic

    def clean_text(self,t):
        t = t.replace('R$','')
        t = t.strip()
        t = t.replace('\n','')
        return t
       