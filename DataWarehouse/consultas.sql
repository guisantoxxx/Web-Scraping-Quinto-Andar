-- 1. Preço médio dos imóveis por região e cidade (com 2 casas decimais)
SELECT 
    dr.estado,
    dr.cidade,
    dr.regiao,
    ROUND(AVG(fv.preco), 2) AS preco_medio
FROM fato_vendas fv
INNER JOIN dimensao_regiao dr ON fv.id_regiao = dr.id_regiao
GROUP BY dr.estado, dr.cidade, dr.regiao;


-- 2. Variação do preço conforme número de quartos, banheiros e vagas
SELECT 
    dc.num_quartos,
    dc.num_banheiros,
    dc.num_vagas,
    ROUND(AVG(fv.preco), 2) AS preco_medio
FROM fato_vendas fv
INNER JOIN dimensao_caracteristicas dc ON fv.id_caracteristicas = dc.id_caracteristicas
GROUP BY dc.num_quartos, dc.num_banheiros, dc.num_vagas
ORDER BY dc.num_quartos, dc.num_banheiros, dc.num_vagas;

-- 3. Regiões com maior oferta de imóveis
SELECT 
    dr.estado,
    dr.cidade,
    dr.regiao,
    COUNT(*) AS total_imoveis
FROM fato_vendas fv
INNER JOIN dimensao_regiao dr ON fv.id_regiao = dr.id_regiao
GROUP BY dr.estado, dr.cidade, dr.regiao
ORDER BY total_imoveis DESC;

--- Algumas consultas a mais, podemos escolher as melhores
-- 1. Evolução das vendas por ano e trimestre: número de vendas e preço médio
SELECT 
    dt.ano,
    dt.quarter,
    COUNT(*) AS total_vendas,
    ROUND(AVG(fv.preco), 2) AS preco_medio
FROM fato_vendas fv
INNER JOIN dimensao_tempo dt ON fv.id_tempo = dt.id_tempo
GROUP BY dt.ano, dt.quarter
ORDER BY dt.ano, dt.quarter;

-- 2. Preço médio dos imóveis por tipo de imóvel
SELECT 
    di.tipo,
    COUNT(*) AS total_vendas,
    ROUND(AVG(fv.preco), 2) AS preco_medio
FROM fato_vendas fv
INNER JOIN dimensao_imovel di ON fv.id_imovel = di.id_imovel
GROUP BY di.tipo
ORDER BY di.tipo;

-- 3. Tamanho médio dos imóveis por número de quartos
SELECT 
    dc.num_quartos,
    COUNT(*) AS total_imoveis,
    ROUND(AVG(dc.tamanho), 2) AS tamanho_medio
FROM fato_vendas fv
INNER JOIN dimensao_caracteristicas dc ON fv.id_caracteristicas = dc.id_caracteristicas
GROUP BY dc.num_quartos
ORDER BY dc.num_quartos;


-- 4. Contagem de vendas por item disponível
SELECT 
    di_item.item,
    COUNT(*) AS total_vendas
FROM fato_vendas fv
INNER JOIN dimensao_imovel di ON fv.id_imovel = di.id_imovel
CROSS JOIN LATERAL unnest(di.itens_disponiveis) AS item_id
INNER JOIN dimensao_item di_item ON item_id = di_item.id_item
GROUP BY di_item.item
ORDER BY total_vendas DESC;

-- 5. Preço médio dos imóveis por região e tipo de imóvel
SELECT 
    dr.regiao,
    di.tipo,
    COUNT(*) AS total_vendas,
    ROUND(AVG(fv.preco), 2) AS preco_medio
FROM fato_vendas fv
INNER JOIN dimensao_regiao dr ON fv.id_regiao = dr.id_regiao
INNER JOIN dimensao_imovel di ON fv.id_imovel = di.id_imovel
GROUP BY dr.regiao, di.tipo
ORDER BY dr.regiao, di.tipo;
