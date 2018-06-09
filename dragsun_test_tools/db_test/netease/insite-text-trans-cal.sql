  
select
t_aeli.id , t_aeli.source_content , t_aeli.trans_content
from article_edit_line_info t_aeli
left join article_edit_info t_aei on t_aeli.edit_id = t_aei.edit_id
left join sys_institution_info t_sii on t_sii.id = t_aei.ins_id
where
1=1
and t_aeli.gmt_create >= '${startTime}'
and t_aeli.gmt_create <= '${endTime}'
and t_sii.app_key = '${appKey}'
and t_aeli.source_content != '<p>'
and t_aeli.source_content != '</p>'
and t_aeli.source_content != ''
and ${idSqlClause}
order by t_aeli.id desc
limit  ${limitCount}  ;