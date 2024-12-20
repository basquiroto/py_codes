WITH tb_cand AS (
SELECT SQ_CANDIDATO,
    NM_UE, 
    DS_CARGO, 
    SG_PARTIDO,
    DS_GENERO,
    DS_GRAU_INSTRUCAO,
    DS_ESTADO_CIVIL,
    DS_COR_RACA,
    DS_OCUPACAO
    FROM tb_candidaturas
),

tb_total_bens AS (
SELECT SQ_CANDIDATO,
    SUM(CAST(REPLACE(VR_BEM_CANDIDATO, ',', '.') AS DECIMAL(15,2))) AS total_bens
    FROM tb_bens 
    GROUP BY 1
),

tb_all_info_cand AS (
SELECT c.*, 
    COALESCE(tb.total_bens, 0) AS total_bens
    FROM tb_cand AS c
    LEFT JOIN tb_total_bens AS tb ON tb.SQ_CANDIDATO = c.SQ_CANDIDATO
),

tb_group_ue AS (
SELECT NM_UE,
       ROUND(AVG(CASE WHEN DS_GENERO = 'FEMININO' THEN 1 ELSE 0 END), 4) AS txGenFeminino,
       SUM(CASE WHEN DS_GENERO = 'FEMININO' THEN 1 ELSE 0 END) AS totalGenFeminino,
       ROUND(AVG(CASE WHEN DS_COR_RACA = 'PRETA' THEN 1 ELSE 0 END), 4) AS txCorRacaPreta,
       SUM(CASE WHEN DS_COR_RACA = 'PRETA' THEN 1 ELSE 0 END) AS totalCorRacaPreta,
       ROUND(AVG(CASE WHEN DS_COR_RACA IN ('PRETA', 'PARDA') THEN 1 ELSE 0 END), 4) AS txCorRacaPretaParda,
       SUM(CASE WHEN DS_COR_RACA IN ('PRETA', 'PARDA') THEN 1 ELSE 0 END) AS totalCorRacaPretaParda,
       ROUND(AVG(CASE WHEN DS_COR_RACA <> 'BRANCA' THEN 1 ELSE 0 END), 4) AS txCorRacaNaoBranca,
       SUM(CASE WHEN DS_COR_RACA <> 'BRANCA' THEN 1 ELSE 0 END) AS totalCorRacaNaoBranca,
       COUNT(*) AS totalCandidaturas
       FROM tb_all_info_cand
       GROUP BY 1
)

SELECT * FROM tb_group_ue;