local queries = require("queries");
local q = queries.vertices(arg);
return get_vertex_metadata(q.query, "name");
