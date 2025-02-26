SELECT
    dr.estado,
    dr.cidade,
    dr.regiao,
    ROUND(AVG(fv.preco), 2) AS preco_medio
FROM fato_vendas fv
INNER JOIN dimensao_regiao dr ON fv.id_regiao = dr.id_regiao
GROUP BY dr.estado, dr.cidade, dr.regiao;

SELECT
    dc.num_quartos,
    dc.num_banheiros,
    dc.num_vagas,
    ROUND(AVG(fv.preco), 2) AS preco_medio
FROM fato_vendas fv
INNER JOIN dimensao_caracteristicas dc ON fv.id_caracteristicas = dc.id_caracteristicas
GROUP BY dc.num_quartos, dc.num_banheiros, dc.num_vagas
ORDER BY dc.num_quartos, dc.num_banheiros, dc.num_vagas;

SELECT
    dr.estado,
    dr.cidade,
    dr.regiao,
    COUNT(*) AS total_imoveis
FROM fato_vendas fv
INNER JOIN dimensao_regiao dr ON fv.id_regiao = dr.id_regiao
GROUP BY dr.estado, dr.cidade, dr.regiao
ORDER BY total_imoveis DESC;

SELECT
    di.tipo,
    COUNT(*) AS total_vendas,
    ROUND(AVG(fv.preco), 2) AS preco_medio
FROM fato_vendas fv
INNER JOIN dimensao_imovel di ON fv.id_imovel = di.id_imovel
GROUP BY di.tipo
ORDER BY di.tipo;

SELECT
    dc.num_quartos,
    COUNT(*) AS total_imoveis,
    ROUND(AVG(dc.tamanho)::numeric, 2) AS tamanho_medio
FROM fato_vendas fv
INNER JOIN dimensao_caracteristicas dc
    ON fv.id_caracteristicas = dc.id_caracteristicas
GROUP BY dc.num_quartos
ORDER BY dc.num_quartos;


SELECT
    dr.regiao,
    di.tipo,
    COUNT(*) AS num_anuncios,
    ROUND(AVG(fv.preco), 2) AS preco_medio
FROM fato_vendas fv
INNER JOIN dimensao_regiao dr ON fv.id_regiao = dr.id_regiao
INNER JOIN dimensao_imovel di ON fv.id_imovel = di.id_imovel
GROUP BY dr.regiao, di.tipo
ORDER BY dr.regiao, di.tipo;



