local queries = require("queries");

for _, item in ipairs(arg) do
    article_name = item[1]
    article_id = item[2]
    local q = queries.vertex(article_id);
    set_vertex_metadata(q.query, "name", article_name);
end
