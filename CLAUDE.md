Crie um dashboard streamlit de acordo com as orientações a seguir. 

Os dados deverão ser gerados e simulados.
Crie um ambiente virtual para instalar dependencias necessárias antes de começar.


# 📊 CHECKLIST DASHBOARD SHOWCASE - STREAMLIT

## 🔐 **SISTEMA DE LOGIN**
- [ ] Tela de login personalizada com branding
- [ ] Autenticação: usuário `gold` / senha `gold123`
- [ ] Design responsivo do login
- [ ] Validação de credenciais
- [ ] Redirecionamento pós-login
- [ ] Proteção de rotas/páginas

## 🎨 **SELETOR DE TEMAS (3 OPÇÕES)**

### **TEMA 1: Pastel Sofisticado & Clean**
- [ ] Paleta de cores pastel (azuis suaves, verdes menta, rosas claros)
- [ ] Design minimalista e limpo
- [ ] Tipografia elegante
- [ ] Espaçamento generoso
- [ ] Bordas suaves e sombras sutis
- [ ] Ícones minimalistas

### **TEMA 2: LEDs & Cores Vibrantes Elegantes**
- [ ] Cores neon/LED (ciano, magenta, amarelo elétrico)
- [ ] Efeitos de brilho e gradientes
- [ ] Tema dark com acentos vibrantes
- [ ] Animações sutis de LED
- [ ] Contraste alto mas elegante
- [ ] Ícones com efeitos luminosos

### **TEMA 3: Design Único & Inovador**
- [ ] Conceito visual diferenciado (ex: glassmorphism, neurofismo)
- [ ] Paleta de cores única
- [ ] Elementos visuais inovadores
- [ ] Layout não-convencional
- [ ] Interações criativas
- [ ] Personalidade visual forte

## 📈 **CONTEÚDO DO DASHBOARD (DADOS FAKE)**

### **Header/Cabeçalho**
- [ ] Logo da empresa "Gold" (com branding dourado)
- [ ] Título: "Gold - Dashboard Executivo" 
- [ ] Seletor de período/data
- [ ] Indicador de última atualização
- [ ] Menu de navegação entre temas

### **KPIs Principais (3-5 indicadores)**
- [ ] **Receita Total** (valor + % crescimento)
- [ ] **Vendas do Mês** (quantidade + meta)
- [ ] **Clientes Ativos** (número + variação)
- [ ] **Ticket Médio** (valor + tendência)
- [ ] **Taxa de Conversão** (% + comparativo)

### **Gráficos & Visualizações**
- [ ] **Gráfico de Linha**: Evolução de vendas Gold (últimos 12 meses)
- [ ] **Gráfico de Barras com Gradientes**: Top 5 produtos/serviços (usando Plotly com gradientes temáticos)
- [ ] **Gráfico Pizza**: Distribuição por região/categoria
- [ ] **Gráfico de Área**: Funil de vendas Gold
- [ ] **Heatmap**: Performance por período
- [ ] **Gauge/Velocímetro**: Meta vs realizado

### **Bibliotecas para Gradientes nos Gráficos**
- [ ] **Plotly**: Para gráficos de barras com gradientes dinâmicos
- [ ] **Configurações de cores**: Gradientes que combinam com cada tema
  - Tema 1 (Pastel): Gradientes suaves (azul claro → azul médio)
  - Tema 2 (LED): Gradientes vibrantes (ciano → magenta)
  - Tema 3 (Único): Gradientes personalizados conforme design
- [ ] **Plotly Express + Graph Objects**: Para controle total dos gradientes
- [ ] **Paletas customizadas**: Definir cores base para cada tema

### **Tabelas & Listagens**
- [ ] **Top Vendedores** (ranking com fotos fake)
- [ ] **Últimas Transações** (tabela interativa)
- [ ] **Produtos em Alta** (lista com indicadores)
- [ ] **Alertas/Notificações** (cards informativos)

### **Filtros & Interatividade**
- [ ] Filtro por período (dia/semana/mês/ano)
- [ ] Filtro por categoria/produto
- [ ] Filtro por região/vendedor
- [ ] Botões de refresh/atualização
- [ ] Export para Excel/PDF (simulado)

## 💡 **ELEMENTOS "UAAAL" (IMPRESSIONADORES)**

### **Animações & Efeitos**
- [ ] Loading animado entre temas
- [ ] Transições suaves nos gráficos
- [ ] Hover effects nos elementos
- [ ] Counter animado nos KPIs
- [ ] Progress bars animadas
- [ ] Micro-interações

### **Elementos Visuais Únicos**
- [ ] Cards com glassmorphism/neumorphism
- [ ] Gradientes dinâmicos
- [ ] Sombras e profundidade
- [ ] Ícones personalizados/animados
- [ ] Badges e indicadores visuais
- [ ] Sparklines nos KPIs

### **Layout Responsivo**
- [ ] Grid system flexível
- [ ] Adaptação mobile/tablet
- [ ] Sidebar colapsável
- [ ] Componentes redimensionáveis
- [ ] Breakpoints otimizados

## 🔧 **FUNCIONALIDADES TÉCNICAS**

### **Performance & UX**
- [ ] Cache de dados para velocidade
- [ ] Loading states elegantes
- [ ] Error handling gracioso
- [ ] Navegação intuitiva
- [ ] Breadcrumbs
- [ ] Tooltips informativos

### **Dados Simulados**
- [ ] Dataset fake realístico (pandas)
- [ ] Dados temporais consistentes
- [ ] Variações e tendências lógicas
- [ ] Nomes e empresas fictícias
- [ ] Métricas correlacionadas

### **Componentes Customizados**
- [ ] Métricas cards personalizados
- [ ] Botões temáticos
- [ ] Indicadores de status
- [ ] Headers customizados
- [ ] Footer com branding

## 📱 **SEÇÕES DO DASHBOARD**

### **Seção 1: Overview Executivo**
- [ ] KPIs principais em destaque
- [ ] Gráfico de tendência geral
- [ ] Alertas importantes
- [ ] Resumo executivo

### **Seção 2: Vendas & Revenue**
- [ ] Análise de vendas detalhada
- [ ] Performance por produto
- [ ] Comparativos temporais
- [ ] Metas vs realizados

### **Seção 3: Clientes & Marketing**
- [ ] Análise de clientes
- [ ] Segmentação
- [ ] Funil de conversão
- [ ] ROI de campanhas

### **Seção 4: Operacional**
- [ ] Indicadores operacionais
- [ ] Produtividade equipe
- [ ] Eficiência processos
- [ ] Custos e margens

## 🚀 **DIFERENCIAL COMPETITIVO**

### **Elementos Premium**
- [ ] Design profissional nível enterprise
- [ ] 3 temas completamente diferentes
- [ ] Interatividade avançada
- [ ] Visualizações únicas
- [ ] UX exemplar

### **Call-to-Actions**
- [ ] Botão "Quero o Meu Dashboard"
- [ ] Form de contato integrado
- [ ] Links para WhatsApp
- [ ] Demonstração de recursos
- [ ] Depoimentos simulados

## ✅ **CHECKLIST DE QUALIDADE FINAL**

### **Antes do Deploy**
- [ ] Teste em diferentes resoluções
- [ ] Teste dos 3 temas funcionando
- [ ] Verificação de performance
- [ ] Validação do login
- [ ] Check responsividade mobile
- [ ] Teste de navegação completa
- [ ] Validação visual de todos elementos
- [ ] Verificação de dados consistentes

### **Detalhes Finais**
- [ ] Favicon personalizado
- [ ] Meta tags otimizadas
- [ ] Loading inicial impactante
- [ ] Mensagens de feedback
- [ ] Documentação básica
- [ ] Instruções de navegação

---

## 💰 **SIMULAÇÃO DO VALOR STARTER**
**Dashboard mostrado:** Representa exatamente o que o cliente recebe no plano de **R$ 1.500/mês**
- ✅ 1 página principal completa
- ✅ 5 KPIs estratégicos
- ✅ Design profissional
- ✅ Login personalizado
- ✅ Atualizações automáticas (simuladas)
- ✅ 3 opções de tema/design