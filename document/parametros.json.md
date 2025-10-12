# 📊 Parâmetros Técnicos - Arquivo JSON

## Localização do Arquivo

O arquivo `parametros.json` com todos os dados técnicos das variedades de cana-de-açúcar está localizado em:

**`src/parametros.json`**

## 📋 Estrutura dos Dados

O arquivo contém parâmetros técnicos para 15+ variedades de cana-de-açúcar, incluindo:

### Variedades Disponíveis
- **RB867515** - Alta produtividade, adaptada ao Centro-Sul
- **RB92579** - Resistente à seca, ideal para regiões áridas  
- **RB966928** - Alta concentração de sacarose
- **SP81-3250** - Variedade clássica, ampla adaptabilidade
- **CTC4** - Tecnologia CTC, alta produtividade
- **CTC9001** - Resistente a pragas e doenças
- **IAC91-1099** - Desenvolvida pelo IAC, boa brotação
- **IACSP95-5000** - Alta rusticidade
- **VAT90212** - Adaptada ao Nordeste
- **Co 997** - Variedade internacional
- **SP70-1143** - Clássica paulista
- **RB855453** - Boa para renovação
- **RB855536** - Resistente ao mosaico
- **RB72454** - Tradicional do setor
- **SP83-2847** - Boa produtividade industrial

### Parâmetros Técnicos por Variedade

Cada entrada contém:

```json
{
  "Variedade": "Nome da variedade",
  "Epoca": "Chuva/Seca",
  "Processo": "Manual/Mecanizado", 
  "e_rec_m": "Espaçamento recomendado (metros)",
  "g_final_rec": "Gemas por metro linear",
  "s_rec": "Taxa de sobrevivência",
  "g_to_rec": "Gemas por tonelada (milhares)",
  "l_to_rec": "Comprimento médio (metros)",
  "rho_rec": "Densidade aparente",
  "d_rec_kg_m": "Densidade kg/metro linear"
}
```

### Épocas de Plantio
- **Chuva**: Outubro a Março (melhor brotação)
- **Seca**: Abril a Setembro (menor disponibilidade hídrica)

### Processos de Plantio  
- **Manual**: Plantio convencional com mão de obra
- **Mecanizado**: Plantio com máquinas plantadoras

## 🔍 Como Consultar

### Para Desenvolvedores
```python
import json

# Carregar parâmetros
with open('src/parametros.json', 'r') as f:
    parametros = json.load(f)

# Filtrar por variedade
rb867515 = [p for p in parametros if p['Variedade'] == 'RB867515']
```

### Para Usuários
Os parâmetros são consultados automaticamente pelo programa principal durante os cálculos. Não é necessário manipular o arquivo diretamente.

## 📚 Fontes dos Dados

Os parâmetros foram compilados a partir de:

- **RIDESA** - Rede Interuniversitária para Desenvolvimento do Setor Sucroenergético
- **CTC** - Centro de Tecnologia Canavieira  
- **IAC** - Instituto Agronômico de Campinas
- **Embrapa** - Empresa Brasileira de Pesquisa Agropecuária

Para mais informações sobre as fontes, consulte: [`other/fontes_info.md`](other/fontes_info.md)

## ⚠️ Importante

- **Não edite** o arquivo diretamente sem conhecimento técnico
- Os valores são baseados em pesquisas científicas validadas
- Alterações podem impactar a precisão dos cálculos
- Para atualizações, consulte as fontes oficiais mencionadas

---

*Parâmetros atualizados em: 12/10/2025*
*Fonte: Compilação de dados oficiais do setor sucroenergético*