select count(distinct url) from tags;
select count(*) from url_meta;
select count(*) from url_meta where title = 'error';

select * from tags order by id desc;

select * from url_meta order by id desc;	

delete from url_meta where url = 'h' and id > 0;

select * from url_meta where title = 'error' order by id desc;

update url_meta set url_md5 = md5(url) where id > 5;

update url_meta set title = 'error' where title like 'ApiError%' and id > 0;

select url, count(*) from tags where tag = 'python' and url_md5 not in (select distinct url_md5 from url_meta) group by url order by count(*) desc;

select * from url_meta order by id desc;
